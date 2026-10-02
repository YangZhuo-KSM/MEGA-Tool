"""Reproducible review suggestions, never implicit approval of unsampled text."""
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from .corpus import ROOT, index
from .reviews import fingerprint
from .annotations import unit_issues


def scope_digest(data, ids):
    alignments = index(data['alignments'])
    return hashlib.sha256(json.dumps([
        [aid, fingerprint(data, alignments[aid]),
         [i for uid in alignments[aid]['de_ids']+alignments[aid]['zh_ids'] for i in unit_issues(data, uid)]]
        for aid in sorted(ids)
    ], ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def build_plan(data, first_batch=5, seed='paris-review-v1'):
    scope = [a for a in data['alignments'] if a['review_batch'] >= first_batch]
    units = index(data['units']); strata = defaultdict(list)
    reasons = defaultdict(list)
    def select(a, reason):
        if reason not in reasons[a['id']]: reasons[a['id']].append(reason)
    def size(a):
        return sum(len(units[u]['text']) for u in a['de_ids']+a['zh_ids'])
    for a in scope:
        editions = tuple(sorted({units[u]['edition_id'] for u in a['de_ids']+a['zh_ids']}))
        strata[(a['section_id'], editions)].append(a)
    for key, group in sorted(strata.items()):
        # Split each topic/source stratum by median length. Sample both halves.
        ordered = sorted(group, key=lambda a:(size(a), a['id']))
        target = min(len(group), max(2, math.ceil(len(group)*.2)))
        rng = random.Random(seed+repr(key))
        halves = [ordered[:len(ordered)//2], ordered[len(ordered)//2:]]
        chosen = []
        for half in halves:
            if half: chosen.append(rng.choice(half))
        available = [a for a in ordered if a not in chosen]
        chosen += rng.sample(available, target-len(chosen))
        for a in chosen: select(a, '分层随机样本：专题/来源版本及相对长短段')
        risks = defaultdict(list)
        for a in group:
            selected = [units[u] for u in a['de_ids']+a['zh_ids']]
            issues = [i for u in selected for i in unit_issues(data, u['id'])]
            if any(i['status']=='open' for i in issues): select(a, '未解决疑点：定向核查')
            if issues: risks['照录/字形疑点'].append(a)
            if any(len(u['locations'])>1 for u in selected): risks['跨页接续'].append(a)
            if len(a['de_ids'])>1 or len(a['zh_ids'])>1: risks['多单元对应'].append(a)
        for category, candidates in sorted(risks.items()):
            # One representative per risk type in each stratum; overlap limits burden.
            candidate = sorted(candidates, key=lambda a:(a['id'] not in reasons, -size(a), a['id']))[0]
            select(candidate, '风险代表样本：'+category)
    ids = [a['id'] for a in scope]
    return dict(schema_version=1, policy='stratified-review-v1', seed=seed,
                first_batch=first_batch, release=data['release'], created_date='2026-10-02',
                scope_ids=ids, scope_digest=scope_digest(data, ids),
                recommended=[dict(alignment_id=a['id'], reasons=reasons[a['id']]) for a in scope if a['id'] in reasons],
                note='质量发现用的分层随机与风险定向混合抽样，不提供统计置信保证；未抽中记录不自动确认。')


def load_plan(data, path=None):
    path = Path(path) if path else ROOT/'data/sampling_plan.json'
    if not path.exists(): return None
    plan = json.loads(path.read_text(encoding='utf-8'))
    expected = {a['id'] for a in data['alignments'] if a['review_batch']>=plan['first_batch']}
    if (set(plan['scope_ids']) != expected or scope_digest(data, plan['scope_ids']) != plan['scope_digest']):
        raise ValueError('抽样清单对应的正文、来源、疑点或收录范围已改变，请重新生成清单。')
    return plan

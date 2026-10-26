"""Exact batch-49 repair: preview by default, explicit apply/resume with journal."""
import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paris.sampling import scope_digest
from paris.corpus import validate

EXPECTED = {
    'corpus.json': 'f1ef72b6b99ba1f4230944cf1ba46acba7d0272207f99a0437c4494fd6372372',
    'extraction.json': 'faebf2d3c8670fc7e96485a84e0b1e37a800609c25711eb59ad536949efcee7f',
    'coverage_plan.json': 'a4d81724f622565366426654dd4c0405e063bd02b1007bb845f7288853d63208',
    'sampling_plan.json': 'c3801da8b012e5608d5acfc6cd3271d5e249c2ea1c54c9c0e3d2a4f1c19d431b',
    'reviews.json': '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb',
}
ISSUE = dict(
    id='mill_de_184_literal_0', unit_id='mill_de_184', kind='glyph_doubt', status='open',
    current_reading='|(', reported_reading='按扫描保留字形候选，待研究者核查',
    evidence_pages=['de_megaiv2:440'], text_anchor=dict(start=0, end=2, quote='|('),
    note='已对照原页；保留异常字形、历史拼写或页内界符，不按译文或语义静默替换。',
    recorded_by='Codex', recorded_at='2026-10-23')


def propose(data, plan):
    """Create in-memory candidates only when the existing frozen scope is intact."""
    if scope_digest(data, plan['scope_ids']) != plan['scope_digest']:
        raise ValueError('Frozen scope differs; refusing to propose a migration')
    units = {u['id']: u for u in data['units']}
    unit = units.get(ISSUE['unit_id'])
    if not unit or not unit['text'].startswith('|(Bei jener Compensation'):
        raise ValueError('Expected the documented literal anchor')
    if unit['evidence_pages'] != ISSUE['evidence_pages']:
        raise ValueError('Expected the documented evidence page')
    if any(i['id'] == ISSUE['id'] or (i['unit_id'] == ISSUE['unit_id'] and
           i['text_anchor']['quote'] == '|(') for i in data['editorial_issues']):
        raise ValueError('Issue already registered; do not repeat repair')
    if 'mill_184' not in plan['scope_ids']:
        raise ValueError('Target alignment absent from frozen scope')
    if any(r['alignment_id'] == 'mill_184' for r in plan['recommended']):
        raise ValueError('Target recommendation changed; re-evaluate the proposal')
    candidate = copy.deepcopy(data)
    candidate['editorial_issues'].append(copy.deepcopy(ISSUE))
    updated = copy.deepcopy(plan)
    updated['scope_digest'] = scope_digest(candidate, updated['scope_ids'])
    updated['recommended'].append(dict(alignment_id='mill_184', reasons=['未解决疑点：定向核查']))
    assert candidate['editorial_issues'][:-1] == data['editorial_issues']
    assert {k:v for k,v in candidate.items() if k != 'editorial_issues'} == {
        k:v for k,v in data.items() if k != 'editorial_issues'}
    assert updated['recommended'][:-1] == plan['recommended']
    assert {k:v for k,v in updated.items() if k not in ('scope_digest', 'recommended')} == {
        k:v for k,v in plan.items() if k not in ('scope_digest', 'recommended')}
    return candidate, updated


def atomic_write(path, raw):
    temp = path.with_name(path.name + '.repair49.tmp')
    with temp.open('wb') as stream:
        stream.write(raw)
        stream.flush()
        import os
        os.fsync(stream.fileno())
    temp.replace(path)


def apply_repair(root, transaction, resume=False, checkpoint=None):
    """Resume only exact old/new byte states; never overwrite an unknown state."""
    root, transaction = Path(root), Path(transaction)
    journal = transaction / 'migration.json'
    if resume:
        report = json.loads(journal.read_bytes())
        if report['status'] == 'complete':
            raise ValueError('Repair already complete; do not repeat')
        raw = {n: (transaction/n).read_bytes() for n in EXPECTED}
    else:
        if transaction.exists():
            raise ValueError('Transaction exists; inspect before explicit resume')
        raw = {n: (root/'data'/n).read_bytes() for n in EXPECTED}
    hashes = {n: hashlib.sha256(v).hexdigest() for n,v in raw.items()}
    if hashes != EXPECTED:
        raise ValueError('Fixed five-file hashes differ')
    data, plan = json.loads(raw['corpus.json']), json.loads(raw['sampling_plan.json'])
    candidate, updated = propose(data, plan)
    if validate(candidate):
        raise ValueError(validate(candidate))
    inverse = copy.deepcopy(candidate)
    inverse['editorial_issues'].pop()
    if inverse != data or scope_digest(inverse, plan['scope_ids']) != plan['scope_digest']:
        raise ValueError('Inverse proof failed')
    outputs = {n: (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
               for n,obj in [('corpus.json',candidate),('sampling_plan.json',updated)]}
    def check_states():
        states = {}
        for n in EXPECTED:
            current = (root/'data'/n).read_bytes()
            if current == raw[n]:
                states[n] = 'old'
            elif n in outputs and current == outputs[n]:
                states[n] = 'new'
            else:
                raise ValueError(f'Unknown state: {n}; refusing write')
        return states
    states = check_states()
    if not resume:
        if any(s != 'old' for s in states.values()):
            raise ValueError('Apply requires original bytes')
        transaction.mkdir(parents=True)
        for n,v in raw.items():
            (transaction/n).write_bytes(v)
            if (transaction/n).read_bytes() != v:
                raise ValueError('Backup verification failed')
        report = dict(status='prepared', before_sha256=hashes,
            after_sha256={n: hashlib.sha256(outputs.get(n,v)).hexdigest() for n,v in raw.items()},
            added_issue=ISSUE, old_scope_digest=plan['scope_digest'],
            new_scope_digest=updated['scope_digest'],
            previous_scope_digest=plan.get('previous_scope_digest'),
            scope_ids_preserved=len(plan['scope_ids']), recommendations_preserved=len(plan['recommended']),
            recommendations_after=len(updated['recommended']), added_recommendation=updated['recommended'][-1],
            inverse_digest_proof=True, events=[])
    def record(stage):
        report['status'] = stage
        report['states'] = check_states()
        report['events'].append(dict(stage=stage, time=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat()))
        atomic_write(journal, (json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        if checkpoint:
            checkpoint(stage)
    record('prepared' if not resume else 'resuming')
    for n,v in outputs.items():
        if check_states()[n] == 'old':
            atomic_write(root/'data'/n, v)
        record(n + ':written')
    if any((root/'data'/n).read_bytes() != outputs.get(n,v) for n,v in raw.items()):
        raise ValueError('Final byte verification failed')
    record('complete')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--resume', action='store_true')
    parser.add_argument('--quota', default='unavailable', help='Latest observed usage; never estimated')
    args = parser.parse_args()
    if args.apply or args.resume:
        import subprocess
        def checkpoint(stage):
            subprocess.run([sys.executable, str(ROOT/'scripts/checkpoint_automation.py'),
                '--phase', '49单项修复事务阶段='+stage+'；批次验收待完成；当前窗口门槛豁免，自动化PAUSED',
                '--next', '检查事务报告并完成49保护审计及受影响测试；本对话不追加50',
                '--quota', args.quota], check=True)
        report = apply_repair(ROOT, ROOT/'local_backups/batch49-issue-repair-20261023', args.resume, checkpoint)
        print(json.dumps(report,ensure_ascii=False))
        return
    raw = {n: (ROOT/'data'/n).read_bytes() for n in EXPECTED}
    hashes = {n: hashlib.sha256(v).hexdigest() for n,v in raw.items()}
    if hashes != EXPECTED:
        raise ValueError('Data changed since failure snapshot; inspect before proposing')
    data, plan = json.loads(raw['corpus.json']), json.loads(raw['sampling_plan.json'])
    candidate, updated = propose(data, plan)
    # Inverse proof: removing only the proposed issue must restore the frozen digest.
    candidate['editorial_issues'].pop()
    assert scope_digest(candidate, plan['scope_ids']) == plan['scope_digest']
    assert all((ROOT/'data'/n).read_bytes() == v for n,v in raw.items())
    report = dict(
        checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        status='proposal_only; no research files written; awaiting frozen-scope decision',
        expected_data_sha256=hashes, proposed_issue=ISSUE,
        old_scope_digest=plan['scope_digest'], proposed_scope_digest=updated['scope_digest'],
        previous_scope_digest_preserved=plan.get('previous_scope_digest'),
        scope_ids_preserved=len(plan['scope_ids']), recommendations_preserved=len(plan['recommended']),
        proposed_recommendations=len(updated['recommended']),
        added_recommendation=updated['recommended'][-1], inverse_digest_proof=True,
        untouched='text, IDs, sequences, locations, reviews, extraction, coverage, PDFs, existing issues',
        next='Approve this explicit delta before implementing an apply path; then audit 49 and affected tests')
    target = ROOT/'tmp/batch49-issue-repair-proposal.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()

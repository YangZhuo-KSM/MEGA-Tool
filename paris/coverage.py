"""Research coverage computed from live records, never from static completion claims."""
import json
from .corpus import ROOT
from .reviews import review_state

WORKS={'manuscript1':'第一手稿','manuscript2':'第二手稿','manuscript3':'第三手稿','mill':'穆勒评注'}


def load_plan(data, path=None):
    plan=json.loads((path or ROOT/'data/coverage_plan.json').read_text(encoding='utf-8'))
    if plan.get('schema_version')!=1: raise ValueError('未知覆盖计划版本')
    sections={s['id'] for s in data['sections']}; seen=set(); assigned=set()
    for item in plan['items']:
        if item['id'] in seen or item['work'] not in WORKS: raise ValueError('覆盖项ID或手稿无效')
        seen.add(item['id'])
        for sid in item['section_ids']:
            if sid not in sections or sid in assigned: raise ValueError('覆盖项章节缺失或重复计入')
            assigned.add(sid)
        total=item.get('total_groups')
        if total is not None and (type(total) is not int or total<1): raise ValueError('全文分母必须为正整数或未知')
        if item.get('completion')=='complete' and not item.get('completion_evidence'):
            raise ValueError('完整收录声明需要证据')
    if assigned!=sections: raise ValueError('存在未纳入覆盖计划的收录章节')
    return plan


def coverage_rows(data,reviews,plan):
    rows=[]
    for item in plan['items']:
        groups=[a for a in data['alignments'] if a['section_id'] in item['section_ids']]
        ids={uid for a in groups for uid in a['de_ids']+a['zh_ids']}
        units=[u for u in data['units'] if u['id'] in ids]
        checked=sum(u.get('proofread_status')=='scan_checked_ai' for u in units)
        confirmed=sum(review_state(data,a,reviews)[0]=='manually_verified' for a in groups)
        total=item.get('total_groups')
        if total is not None and len(groups)>total: raise ValueError('已收录组数超过已建立的全文分母')
        rows.append(dict(id=item['id'],work=item['work'],title=item['title'],section_ids=item['section_ids'],
            groups=len(groups),units=len(units),scan_checked=checked,confirmed=confirmed,
            collected_ratio=len(groups)/total if total else None,
            checked_ratio=checked/len(units) if units else None,
            confirmed_ratio=confirmed/len(groups) if groups else None,
            state='未收录' if not groups else '已完整收录' if item.get('completion')=='complete' else '部分收录',
            de_start=item.get('de_start'),zh_start=item.get('zh_start')))
    return rows

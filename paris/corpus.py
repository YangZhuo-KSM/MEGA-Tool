"""Read and validate the transparent JSON corpus. No database is needed."""
import json
import os
from pathlib import Path

ROOT = Path(os.environ['MEGA_TOOL_ROOT']).resolve() if os.environ.get('MEGA_TOOL_ROOT') else Path(__file__).resolve().parents[1]


def validate(data):
    errors=[]
    tables={}
    for name in ['sources','editions','sections','units','alignments','comparisons']:
        items=data.get(name,[])
        ids=[x.get('id') for x in items]
        if None in ids or len(ids)!=len(set(ids)):
            errors.append(f'{name}: ID缺失或重复')
        tables[name]={x.get('id'):x for x in items}
    if data.get('schema_version')!=1:
        errors.append('不支持的schema_version')
    for s in tables['sources'].values():
        if type(s.get('pdf_page_count')) is not int or s['pdf_page_count']<1:
            errors.append(f'{s["id"]}: PDF总页数无效')
    for e in tables['editions'].values():
        if e.get('source_id') not in tables['sources']:
            errors.append(f'{e["id"]}: 来源缺失')
        for field in ['title','year','publisher','edition','language']:
            if not e.get(field):
                errors.append(f'{e["id"]}: {field}缺失')
    def check_location(loc, context, allow_unnumbered=False):
        source=tables['sources'].get(loc.get('source_id'))
        n=loc.get('pdf_page')
        if not source or type(n) is not int or not 1<=n<=source['pdf_page_count']:
            errors.append(f'{context}: PDF页序无效')
        if allow_unnumbered and loc.get('printed_page') is None and loc.get('page_kind') in ('unnumbered','blank','illustration'):
            if not loc.get('note'): errors.append(f'{context}: 未编号页需要说明')
        elif not isinstance(loc.get('printed_page'),str) or not loc['printed_page']:
            errors.append(f'{context}: 印刷页必须为非空字符串')
    page_keys={}
    for loc in data.get('page_map',[]):
        check_location(loc,'page_map',True)
        key=(loc.get('source_id'),loc.get('pdf_page'))
        if key in page_keys:
            errors.append(f'page_map: 重复PDF页 {key}')
        page_keys[key]=loc.get('printed_page')
    missing_keys=set()
    for missing in data.get('missing_pages',[]):
        key=(missing.get('source_id'),missing.get('printed_page'))
        if (key[0] not in tables['sources'] or not isinstance(key[1],str) or not key[1]
            or missing.get('pdf_page') is not None or missing.get('status')!='confirmed_missing'
            or not missing.get('evidence') or not missing.get('note') or key in missing_keys):
            errors.append('missing_pages: 缺页记录需有效来源、印刷页、证据及说明，不得填PDF页序')
        if any(p['source_id']==key[0] and p.get('printed_page')==key[1] for p in data.get('page_map',[])):
            errors.append('missing_pages: 同一印刷页同时标为存在和缺失')
        missing_keys.add(key)
    sequences=set()
    for u in tables['units'].values():
        eid=u.get('edition_id')
        e=tables['editions'].get(eid)
        if not e or e.get('language')!=u.get('language'):
            errors.append(f'{u["id"]}: 版本或语言不匹配')
        if u.get('section_id') not in tables['sections'] or not u.get('text','').strip():
            errors.append(f'{u["id"]}: 章节或正文缺失')
        seq=(eid,u.get('section_id'),u.get('sequence'))
        if type(u.get('sequence')) is not int or seq in sequences:
            errors.append(f'{u["id"]}: 顺序缺失或重复')
        sequences.add(seq)
        # Empty locations are allowed for explicitly unlocated imports.
        for loc in u.get('locations',[]):
            check_location(loc,u['id'])
            if e and loc['source_id']!=e['source_id']:
                errors.append(f'{u["id"]}: 定位来源与版本不符')
            if page_keys.get((loc['source_id'],loc['pdf_page']))!=loc['printed_page']:
                errors.append(f'{u["id"]}: 定位与页码表不符')
    for a in tables['alignments'].values():
        if not a.get('de_ids') or a.get('section_id') not in tables['sections']:
            errors.append(f'{a["id"]}: 缺少德文或章节')
        if a.get('status') not in ['uncertain','automatically_aligned','manually_verified']:
            errors.append(f'{a["id"]}: 未知核验状态')
        if a.get('status')=='manually_verified' and not (a.get('verified_by') and a.get('verified_at')):
            errors.append(f'{a["id"]}: 人工核验缺少核验人/时间')
        for field,lang in [('de_ids','de'),('zh_ids','zh')]:
            ids=a.get(field,[])
            if len(ids)!=len(set(ids)):
                errors.append(f'{a["id"]}: 重复关联文本')
            for uid in ids:
                u=tables['units'].get(uid)
                if not u or u['language']!=lang or u['section_id']!=a['section_id']:
                    errors.append(f'{a["id"]}: 错误引用 {uid}')
    for c in tables['comparisons'].values():
        left=[tables['units'].get(i) for i in c.get('left_ids',[])]
        right=[tables['units'].get(i) for i in c.get('right_ids',[])]
        if not left or not right or any(x is None for x in left+right):
            errors.append(f'{c["id"]}: 比较引用缺失')
        elif len({x['language'] for x in left+right})!=1:
            errors.append(f'{c["id"]}: 比较需要同语种')
    for issue in data.get('editorial_issues',[]):
        u=tables['units'].get(issue.get('unit_id'))
        if not u:
            errors.append('editorial_issues: 文本单元引用无效')
            continue
        anchor=issue.get('text_anchor')
        if anchor:
            start,end=anchor.get('start'),anchor.get('end')
            if (type(start) is not int or type(end) is not int or not 0<=start<end<=len(u['text'])
                or u['text'][start:end]!=anchor.get('quote')):
                errors.append(f'{issue["id"]}: 转录标注位置已失效')
    return errors


def load_corpus(path=None):
    path=Path(path) if path else ROOT/'data'/'corpus.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    problems=validate(data)
    if problems:
        raise ValueError('\n'.join(problems))
    return data


def index(items):
    return {item['id']:item for item in items}


def aligned_units(data, alignment):
    units=index(data['units'])
    return ([units[x] for x in alignment['de_ids']], [units[x] for x in alignment['zh_ids']])


def context_units(data, unit):
    siblings=sorted((u for u in data['units'] if u['edition_id']==unit['edition_id'] and u['section_id']==unit['section_id']),key=lambda u:u['sequence'])
    pos=next(i for i,u in enumerate(siblings) if u['id']==unit['id'])
    return (siblings[pos-1] if pos else None, siblings[pos+1] if pos+1<len(siblings) else None)

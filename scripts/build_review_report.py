"""Generate a read-only review visualization from a stable research snapshot."""
import argparse
import base64
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paris.corpus import index, validate
from paris.reviews import review_state
from paris.sampling import load_plan


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def clip(text, limit):
    return text if len(text)<=limit else text[:limit]+'…'


def image_evidence():
    path=ROOT/'tmp/source_review/de_megaiv2/0440.png'
    if not path.is_file():
        return None
    from PIL import Image
    with Image.open(path) as im:
        w,h=im.size
        crop=im.crop((int(w*.18),int(h*.34),int(w*.82),int(h*.43)))
        out=BytesIO()
        crop.convert('RGB').save(out,format='JPEG',quality=85,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(out.getvalue()).decode('ascii')


def pages(locations):
    return '；'.join(f"印刷{p.get('printed_page') or '未编号'} / PDF{p['pdf_page']}" for p in locations)


def build(output):
    raw={n:(ROOT/'data'/n).read_bytes() for n in ('corpus.json','sampling_plan.json','reviews.json','coverage_plan.json','extraction.json')}
    data=json.loads(raw['corpus.json'])
    if validate(data):
        raise ValueError(validate(data))
    plan=load_plan(data)
    if not plan or plan!=json.loads(raw['sampling_plan.json']):
        raise RuntimeError('Sampling unavailable or changed during read')
    reviews=json.loads(raw['reviews.json'])
    last_batch=max(a['review_batch'] for a in data['alignments'])
    audit_paths=list((ROOT/'tmp').glob(f'*-batch{last_batch}-audit.json'))
    if not audit_paths:
        raise ValueError('The latest batch has no successful protection audit')
    current_audit=json.loads(max(audit_paths,key=lambda p:p.stat().st_mtime).read_text(encoding='utf-8'))
    if current_audit.get('data_sha256')!={n:sha(v) for n,v in raw.items()}:
        raise ValueError('Research snapshot differs from the latest successful audit')
    baseline=json.loads((ROOT/'local_backups/automation-20261023-111725-batch49-diagnosis/data/sampling_plan.json').read_text(encoding='utf-8'))
    if plan['recommended'][:len(baseline['recommended'])]!=baseline['recommended']:
        raise ValueError('The original recommendations or their reasons changed')
    old_ids={r['alignment_id'] for r in baseline['recommended']}
    reasons={r['alignment_id']:r['reasons'] for r in plan['recommended']}
    units,sections=index(data['units']),index(data['sections'])
    by_unit=defaultdict(list)
    for issue in data['editorial_issues']:
        if issue['status'] in ('open','retained_as_source'):
            by_unit[issue['unit_id']].append(issue)
    page_map={(p['source_id'],p['pdf_page']):p for p in data['page_map']}
    notes,note_ids=[],{}
    def intern(text):
        if text not in note_ids:
            note_ids[text]=len(notes);notes.append(text)
        return note_ids[text]
    groups,states=[],Counter()
    for a in data['alignments']:
        state=review_state(data,a,reviews)[0];states[state]+=1
        de,zh=[units[i] for i in a['de_ids']],[units[i] for i in a['zh_ids']]
        issues=[]
        for unit in de+zh:
            for issue in by_unit[unit['id']]:
                anchor=issue.get('text_anchor')
                if anchor:
                    s,e=anchor['start'],anchor['end']
                    if unit['text'][s:e]!=anchor['quote']:
                        raise ValueError('Anchor mismatch: '+issue['id'])
                    quote=anchor['quote'];context=unit['text'][max(0,s-40):e+55]
                else:
                    quote=issue.get('current_reading',issue['id'])
                    context='单元级疑点：现转录 '+quote+'；报告读法 '+issue.get('reported_reading','待核')
                refs=[]
                for ref in issue['evidence_pages']:
                    source,page=ref.rsplit(':',1)
                    p=page_map.get((source,int(page)))
                    refs.append(source+' · '+pages([p]) if p else ref)
                issues.append(dict(quote=quote,status=issue['status'],
                    context=context,note=intern(issue['note']),pages='；'.join(refs)))
        aid=a['id']
        if aid not in reasons and not issues:
            continue
        groups.append(dict(id=aid,label=a['label'],section=a['section_id'],sequence=min(u['sequence'] for u in de+zh),
            de=clip('\n'.join(u['text'] for u in de),240),zh=clip('\n'.join(u['text'] for u in zh),150),
            de_pages=pages([p for u in de for p in u['locations']]),zh_pages=pages([p for u in zh for p in u['locations']]),
            confirmed=state=='manually_verified',reasons=[intern(r) for r in reasons.get(aid,[])],
            is_new=aid in reasons and aid not in old_ids,issues=issues))
    groups.sort(key=lambda g:(list(sections).index(g['section']),g['sequence'],g['id']))
    path=ROOT/'docs/reports/completion-findings.json'
    findings=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    section_rows=[]
    for sid,section in sections.items():
        spans=[]
        for lang in ('de','zh'):
            selected=sorted((u for u in data['units'] if u['section_id']==sid and u['language']==lang and u.get('role','primary')=='primary'),key=lambda u:u['sequence'])
            locs=[p for u in selected for p in u['locations']]
            spans.append(str(locs[0].get('printed_page'))+'—'+str(locs[-1].get('printed_page')) if locs else '未收录')
        section_rows.append(dict(id=sid,title=section['title'],count=sum(a['section_id']==sid for a in data['alignments']),
            pages=' / '.join(spans),status=findings.get('sections',{}).get(sid,'范围结论待最终边界审计')))
    batches=[]
    for batch in sorted({a['review_batch'] for a in data['alignments'] if a['review_batch']>=49}):
        paths=list((ROOT/'tmp').glob(f'*-batch{batch}-audit.json'))
        audit=json.loads(max(paths,key=lambda p:p.stat().st_mtime).read_text(encoding='utf-8')) if paths else None
        batches.append(dict(batch=batch,added=sum(a['review_batch']==batch for a in data['alignments']),
            status='通过' if audit and audit.get('batch')==batch else '尚无成功审计报告'))
    payload=dict(generated_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),release=data['release'],
        corpus_sha256=sha(raw['corpus.json']),scope_digest=plan['scope_digest'],
        counts=dict(groups=len(data['alignments']),confirmed=states['manually_verified'],recommended=len(plan['recommended']),
            open=sum(i['status']=='open' for i in data['editorial_issues'])),
        repair=dict(applied=any(i['id']=='mill_de_184_literal_0' for i in data['editorial_issues']),recommended='mill_184' in reasons,
            details='仅补符号定位提醒和定向核查建议。原445条建议及理由逐条保护；符号原文保持照录，学术读法留待核查。'),
        completion=findings.get('summary','最终正文衔接仍在核定，暂不显示全文完成比例。'),
        groups=groups,notes=notes,sections=section_rows,batches=batches,evidence_image=image_evidence())
    if any((ROOT/'data'/n).read_bytes()!=value for n,value in raw.items()):
        raise RuntimeError('Research files changed during snapshot generation')
    template=(ROOT/'docs/reports/review-report.template.html').read_text(encoding='utf-8')
    encoded=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    fragment=template.replace('__MEGA_REVIEW_DATA__',encoded)
    if len(fragment.encode('utf-8'))>=1_000_000:
        raise ValueError('Fragment exceeds 1MB; shorten excerpts')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(fragment,encoding='utf-8')
    (ROOT/'docs/reports/review-report.data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=dict(generated_at=payload['generated_at'],release=data['release'],input_sha256={n:sha(v) for n,v in raw.items()},
        fragment=str(output),fragment_bytes=output.stat().st_size,groups_displayed=len(groups),
        issue_count=sum(len(g['issues']) for g in groups),prior_recommendations_preserved=len(baseline['recommended']),research_files_written=False)
    (ROOT/'docs/reports/report-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    build(parser.parse_args().output.resolve())

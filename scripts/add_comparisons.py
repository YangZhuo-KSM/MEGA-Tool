"""Add reviewed comparison samples; skip existing IDs to protect later edits."""
import copy
import json
from datetime import datetime,timezone,timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT/'data'/'corpus.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    extraction_path=path.with_name('extraction.json')
    evidence=json.loads(extraction_path.read_text(encoding='utf-8'))
    units={u['id']:u for u in data['units']}
    now=datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
    # The two Chinese readings were compared visually page by page; the selected
    # paragraphs have the same wording, with differing editorial note numbers.
    locations=[[61],[61],[61],[61],[61,62],[62],[62],[62,63],[63],[63],[63],[63]]
    first=copy.deepcopy(next(e for e in data['editions'] if e['id']=='de_megai2'))
    first.update(id='de_megai2_first',short_title='MEGA² I.2 · 第一种呈现',presentation='Erste Wiedergabe')
    if not any(e['id']==first['id'] for e in data['editions']):
        data['editions'].append(first)
    candidates=[]
    for n,pages in enumerate(locations,1):
        base=units[f'alienation_zh_{n:03}']
        u=copy.deepcopy(base)
        text=u['text']
        for old,new in [('⁷⁶','³³'),('⁷⁷','³⁴'),('⁷⁸','³⁵'),('⁷⁹','³⁶'),('⁸⁰','³⁷')]:
            text=text.replace(old,new)
        u.update(id=f'alienation_zh_single_{n:03}',edition_id='zh_single',role='comparison',text=text,
            locations=[dict(source_id='zh_single',printed_page=str(p-10),pdf_page=p) for p in pages],
            evidence_pages=[f'zh_single:{p}' for p in pages],proofread_at=now)
        candidates.append((base,u,'edition','两个中文出版版本的相同位置；样本正文相同，部分编者注号不同。文字差异包含注号，请结合原页判断。对应位置由AI整理，待研究者复核。'))
    # Only select these two cleanly readable passages from the first presentation.
    # Other candidate pages contain suspect glyphs and are deliberately not used
    # to assert substantive textual variants.
    for n,p in [(7,241),(11,242)]:
        base=units[f'alienation_de_{n:03}']
        u=copy.deepcopy(base)
        u.update(id=f'alienation_de_first_{n:03}',edition_id=first['id'],role='comparison',
            locations=[dict(source_id='de_megai2',printed_page=str(p-5),pdf_page=p)],
            evidence_pages=[f'de_megai2:{p}'],proofread_at=now)
        candidates.append((base,u,'presentation','同一MEGA卷的两种呈现，版本相同、编排和页码不同。本组可读正文经扫描核对相同；不据此推断所有段落相同。对应位置待研究者复核。'))
    for base,u,kind,note in candidates:
        if u['id'] in units:
            continue
        data['units'].append(u)
        for loc in u['locations']:
            sid,p=loc['source_id'],loc['pdf_page']
            evidence[f'{sid}:{p}']=(ROOT/'tmp'/'source_review'/sid/f'{p:04}.txt').read_text(encoding='utf-8')
            if not any(x['source_id']==sid and x['pdf_page']==p for x in data['page_map']):
                data['page_map'].append(dict(**loc,status='scan_checked_ai',checked_by='Codex',checked_at=now))
        data['corrections'].append(dict(unit_id=u['id'],method='scan_review_ai',reviewed_by='Codex',reviewed_at=now,extracted_reading=None,corrected_text=u['text'],evidence_pages=u['evidence_pages'],note='与已转录正文逐段比对扫描页；复用经图像核对相同的文字，中文保留本版本注号。'))
        data['comparisons'].append(dict(id=f'compare_{u["id"]}',label=f'{"中文版本" if kind=="edition" else "MEGA呈现"} · {u["label"]}',left_ids=[base['id']],right_ids=[u['id']],kind=kind,status='uncertain',note=note))
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    extraction_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(data["comparisons"])} comparisons, {len(data["units"])} units')


if __name__=='__main__':
    main()

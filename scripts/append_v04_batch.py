"""Append the scan-checked fifth review batch, refusing to change any prior record.

Source images checked: MEGA I/2 pp.376,383; collected Chinese pp.281,289.
Run once; repeated execution verifies the same append without overwriting edits.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus,validate
from paris.reviews import fingerprint

ROWS=[
('private_relation','工人作为活的资本',
'[...] |XL| Zinsen seines Capitals bildet. An dem Arbeiter existirt es also s[ub]jektiv, daß das Capital der sich ganz abhanden gekommene Mensch ist, wie es am Capital objektiv existirt, daß die Arbeit der sich abhanden gekommene Mensch ist. Der Arbeiter hat aber das Unglück ein lebendiges und daher bedürftiges Capital zu sein, das jeden Augenblick, wo es nicht arbeitet, seine Zinsen und damit seine Existenz verliert.',
'[……][XL]构成他的资本的利息。因此，资本是完全失去自身的人这种情况在工人身上主观地存在着，正像劳动是失去自身的人这种情况在资本身上客观地存在着一样。但是，工人不幸而成为一种活的、因而是贫困的资本，这种资本只要一瞬间不劳动便失去自己的利息，从而也失去自己的生存条件。'),
('private_relation','资本与工人的相互生产',
'Als Capital steigt Werth des Arbeiters nach Nachfrage und Zufuhr und auch physisch wird und wird gewußt sein Dasein, sein Leben als eine Zufuhr von Waare, wie jeder andern Waare. Der Arbeiter producirt das Capital, das Capital producirt ihn, er also sich selbst, und der Mensch als Arbeiter, als Waare ist das Product der ganzen Bewegung.',
'作为资本，工人的价值按照需求和供给而增长，而且，从肉体上来说，他的存在、他的生命，也同其他任何商品一样，过去和现在都被看成是商品的供给。工人生产资本，资本生产工人，因而工人生产自身，而且人作为工人、作为商品就是这整个运动的产物。'),
('private_relation','资本与工人的异己关系',
'Dem Menschen der nichts mehr ist als Arbeiter und als Arbeiter sind seine menschlichen Eigenschaften nur da, insofern sie für das ihm fremde Capital da sind. Weil sich aber beide fremd sind, daher in einem gleichgültigen, äusserlichen und zufälligen Verhältnisse stehn, so muß diese Fremdheit auch als wirklich erscheinen.',
'人只不过是工人，对作为工人的人，他的人的特性只有在这些特性对异己的资本来说是存在的时候才存在。但是，因为资本和工人彼此是异己的，从而处于漠不关心的、外部的和偶然的相互关系中，所以这种异己性也必定现实地表现出来。'),
('private_work','私有财产的主体本质',
'|I| ad. pag. XXXVI. Das subjektive Wesen des Privateigenthums, das Privateigenthum als für sich seiende Thätigkeit, als Subjekt, als Person, ist die Arbeit.',
'[I]补入第XXXVI页。私有财产的主体本质，作为自为地存在着的活动、作为主体、作为个人的私有财产，就是劳动。'),
('private_work','劳动原则与现代工业',
'Es versteht sich also, daß erst die Nationalökonomie, welche die Arbeit als ihr Princip erkannte, — Adam Smith — also nicht mehr das Privateigenthum nur mehr als einen Zustand ausser dem Menschen wußte, — daß diese Nationalökonomie sowohl als ein Produkt der wirklichen Energie und Bewegung des Privateigenthums (sie ist die für sich im Bewußtsein gewordne selbstständige Bewegung des Privateigenthums, die moderne Industrie als Selbst) zu betrachten ist, als ein-Produkt der modernen Industrie, wie sie andrerseits die Energie und Entwicklung dieser Industrie beschleunigt, verherrlicht, zu einer Macht des Bewußtseins gemacht hat.',
'因此，十分明显，只有把劳动视为自己的原则——亚当·斯密——，也就是说，不再认为私有财产仅仅是人之外的一种状态的国民经济学，只有这种国民经济学才应该被看成私有财产的现实能量和现实运动的产物（这种国民经济学是私有财产的在意识中自为地形成的独立运动，是现代工业本身），现代工业的产物；而另一方面，正是这种国民经济学促进并赞美了这种工业的能量和发展，使之变成意识的力量。'),
('private_work','货币主义和重商主义的本质观',
'Als Fetischdiener, als Katholiken erscheinen daher dieser aufgeklärten Nationalökonomie, die das subjektive Wesen des Reichthums — innerhalb des Privateigenthums — entdeckt hat, die Anhänger des Geld und Merkantilsystems, welche das Privateigenthum als ein nur gegenständliches Wesen für d[en] Menschen wissen.',
'因此，在这种揭示出——在私有制范围内——财富的主体本质的启蒙国民经济学⁹¹看来，那些认为私有财产对人来说仅仅是对象性的本质的货币主义体系和重商主义体系的拥护者，是拜物教徒、天主教徒。'),
]


def main():
    target=ROOT/'data/corpus.json'
    original=load_corpus(); data=copy.deepcopy(original)
    review_path=ROOT/'data/reviews.json'
    review_bytes=review_path.read_bytes() if review_path.exists() else None
    old_fingerprints={a['id']:fingerprint(original,a) for a in original['alignments']}
    if any(a['id']=='private_relation_001' for a in original['alignments']):
        raise SystemExit('Batch already present; refusing to overwrite researcher edits.')
    stamp='2026-10-02'  # Client Hong Kong date; no unobserved time of day.
    sections=[('private_relation','私有财产的关系','第二手稿','Das Verhältnis des Privateigentums'),
              ('private_work','私有财产和劳动','第三手稿','Privateigentum und Arbeit')]
    for sid,title,manuscript,alias in sections:
        data['sections'].append(dict(id=sid,title=title,work='1844年经济学哲学手稿',manuscript=manuscript,
            aliases=[alias],coverage='本节开头连续3个句群，非整节；句群边界为项目阅读划分'))
    locations={
        'private_relation': [('de_megai2','376',376),('zh_collected','281',306)],
        'private_work': [('de_megai2','383',383),('zh_collected','289',314)],
    }
    evidence=json.loads((ROOT/'data/extraction.json').read_text(encoding='utf-8'))
    counts={}
    for section,label,de,zh in ROWS:
        counts[section]=counts.get(section,0)+1; n=counts[section]
        for lang,text,loc in zip(['de','zh'],[de,zh],locations[section]):
            source,printed,pdf=loc; uid=f'{section}_{lang}_{n:03}'
            location=dict(source_id=source,printed_page=printed,pdf_page=pdf)
            raw=(ROOT/f'tmp/source_review/{source}/{pdf:04}.txt').read_text(encoding='utf-8')
            evidence[f'{source}:{pdf}']=raw
            unit=dict(id=uid,edition_id=source,language=lang,section_id=section,sequence=n,label=label,text=text,
                locations=[location],proofread_status='scan_checked_ai',proofread_by='Codex',proofread_at=stamp,
                evidence_pages=[f'{source}:{pdf}'],transcription_note='2026-10-02对照指定扫描页逐句录入；按句群划分，非原书自然段边界。保留历史拼写及中文注号，合并排版断行，不复现字重或斜体。核对时间仅记录香港日期；对应关系待研究者确认。')
            data['units'].append(unit)
            data['corrections'].append(dict(unit_id=uid,method='scan_review_ai',reviewed_by='Codex',reviewed_at=stamp,
                extracted_reading=None,corrected_text=text,evidence_pages=unit['evidence_pages'],
                note='原页完整OCR保存在extraction.json；本条为图像核对转录。未自动应用旧替换规则。'))
            if not any(p['source_id']==source and p['pdf_page']==pdf for p in data['page_map']):
                data['page_map'].append(dict(**location,status='scan_checked_ai',checked_by='Codex',checked_at=stamp))
        data['alignments'].append(dict(id=f'{section}_{n:03}',section_id=section,label=label,
            de_ids=[f'{section}_de_{n:03}'],zh_ids=[f'{section}_zh_{n:03}'],status='uncertain',proposed_by='Codex',
            verified_by=None,verified_at=None,review_batch=5,note='图像核对后的句群对应候选；第5批6组，待用户确认。'))
    # Existing rows, including the older coverage summary, remain byte-semantically intact.
    # Live coverage now comes from the independent coverage plan plus actual units/reviews.
    assert not validate(data),validate(data)
    assert all(fingerprint(data,a)==old_fingerprints[a['id']] for a in original['alignments'])
    for table in ('sources','editions','sections','units','alignments','page_map','comparisons','corrections','editorial_issues','coverage'):
        assert data.get(table,[])[:len(original.get(table,[]))]==original.get(table,[]),table
    backup=ROOT/'local_backups/v04-before-append'; backup.mkdir(parents=True,exist_ok=True)
    for name in ('corpus.json','extraction.json'):
        b=backup/name
        if b.exists(): raise FileExistsError(f'Backup already exists: {b}')
        b.write_bytes((ROOT/'data'/name).read_bytes())
    tmp=target.with_suffix('.v04.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); tmp.replace(target)
    (ROOT/'data/extraction.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert (review_path.read_bytes() if review_path.exists() else None)==review_bytes
    print('Appended 6 pending groups; all old records/fingerprints and reviews preserved.')
    print('Corpus SHA256:',hashlib.sha256(target.read_bytes()).hexdigest())


if __name__=='__main__': main()

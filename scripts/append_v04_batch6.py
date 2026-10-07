"""Append batch 6 once; retain every prior record and researcher review."""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paris.corpus import load_corpus, validate
from paris.reviews import fingerprint

# Transcribed from the local page images, including visible suspect spellings.
# Locations are per unit; no book-wide PDF offset is inferred.
ROWS = [
    ('private_relation', 4, '失去工作的工人',
     'Sobald es also dem Capital einfällt — nothwendiger oder willkührlicher Einfall — nicht mehr für den Arbeiter zu sein, ist er selbst nicht mehr für sich, er hat keine Arbeit, darum keinen Lohn und da er nicht als Mensch, sondern als Arbeiter Dasein hat, so kann er sich begraben lassen, verhungern etc.',
     '因此，资本一旦想到——不管是必然地还是任意地想到——不再对工人存在，工人自己对自己来说便不再存在：他没有工作，因而也没有工资，并且因为他不是作为人，而是作为工人存在，所以他就会被人埋葬，会饿死，等等。',
     [376], [306]),
    ('private_relation', 5, '工人与资本的存在条件',
     'Der Arbeiter ist nur als Arbeiter da, sobald er für sich als Capital da ist, und er ist nur als Capital da, sobald ein Capital für ihn da ist.',
     '工人只有当他对自己作为资本存在的时候，才作为工人存在；而他只有当某种资本对他存在的时候，才作为资本存在。',
     [376], [306]),
    ('private_relation', 6, '资本规定工人的生活',
     'Das Dasein des Capitals ist sein Dasein, sein Leben, wie es den Inhalt seines Lebens auf eine ihm gleichgültige Weise bestimmt.',
     '资本的存在是他的存在、他的生活，资本的存在以一种对他来说无所谓的方式规定他的生活的内容。',
     [376], [306, 307]),
    ('private_work', 4, '国民经济学的路德',
     'Engels hat daher mit Recht Adam Smith den nationalökonomischen Luther genannt.',
     '因此，恩格斯有理由把亚当·斯密称作国民经济学的路德①。',
     [383], [314]),
    ('private_work', 5, '财富本质的内在化',
     'Wie Luther als das Wesen der äusserüchen Welt d[er] Religion den Glauben erkannte und daher dem katholischen Heidenthum gegenüber trat, wie er die äussere Religiosität aufhob, indem er die Reügiosität zum innern Wesen d[es] Menschen machte, wie er den ausser dem Laien vorhandnen Pfaffen negüte, weü er den Pfaffen in das Herz des Laien versetzte, so wüd der ausser dem Menschen befindüche und von ihm unabhängige—also nur auf eine äusserliche Weise zu erhaltende und zu behauptende — Reichthum aufgehoben, d. h. diese seine äusserliche gedankenlose Gegenständlichkeit wüd aufgehoben, indem sich das Privateigenthum incorporirt im Menschen selbst und der Mensch selbst als sein Wesen erkannt — aber darum der Mensch selbst in der Bestimmung des Privateigenthums wie bei Luther der Religion gesezt wird.',
     '正像路德认为宗教、信仰是外部世界的本质，因而起来反对天主教异教一样，正像他把宗教笃诚变成人的内在本质，从而扬弃了外在的宗教笃诚一样，正像他把僧侣移入世俗人心中，因而否定了在世俗人之外存在的僧侣一样，由于私有财产体现在人本身中，人本身被认为是私有财产的本质，从而人本身被设定为私有财产的规定，就像在路德那里被设定为宗教的规定一样，因此在人之外存在的并且不依赖于人的——也就是只应以外在方式来保存和维护的——财富被扬弃了，换言之，财富的这种外在的、无思想的对象性就被扬弃了。①',
     [383, 384], [314, 315]),
    ('private_work', 6, '承认人与否定人',
     'Unter dem Schein einer Anerkennung d[es] Menschen, ist also die Nationalökonomie, deren Prinzip die Arbeit, vielmehr nur die conséquente Durchführung der Verläugnung des Menschen, indem er selbst nicht mehr in einer äusserüchen Spannung zu dem äusserüchen Wesen des Privateigenthums steht, sondern er selbst dieß gespannte Wesen des Privateigenthums geworden ist.',
     '由此可见，以劳动为原则的国民经济学表面上承认人，毋宁说，不过是彻底实现对人的否定而已，因为人本身已不再同私有财产的外在本质处于外部的紧张关系中，而是人本身成了私有财产的这种紧张的本质。',
     [384], [315]),
]
PRINTED = {('de_megai2', p): str(p) for p in [376, 383, 384]}
PRINTED.update({('zh_collected', 306): '281', ('zh_collected', 307): '282',
                ('zh_collected', 314): '289', ('zh_collected', 315): '290'})


def main(rows=ROWS, printed=PRINTED, batch=6, release='0.4.0-alpha2', doubts=None, reviewed_date='2026-10-02',
         new_sections=None, coverage_updates=None, issue_overrides=None, extra_page_maps=None):
    original = load_corpus()
    if any(a['review_batch'] == batch for a in original['alignments']):
        raise SystemExit(f'Batch {batch} already present; refusing to overwrite edits.')
    data = copy.deepcopy(original)
    coverage_path = ROOT / 'data/coverage_plan.json'
    coverage = json.loads(coverage_path.read_text(encoding='utf-8'))
    existing_sections = {s['id'] for s in data['sections']}
    for section in new_sections or []:
        if section['id'] in existing_sections:
            raise ValueError('New section ID already exists: '+section['id'])
        data['sections'].append(copy.deepcopy(section))
        existing_sections.add(section['id'])
    for item_id, section_ids in (coverage_updates or {}).items():
        item = next(i for i in coverage['items'] if i['id'] == item_id)
        if item['section_ids']:
            raise ValueError('Refusing to replace an existing coverage assignment: '+item_id)
        item['section_ids'] = list(section_ids)
    assigned = [sid for i in coverage['items'] for sid in i['section_ids']]
    if len(assigned) != len(set(assigned)) or set(assigned) != existing_sections:
        raise ValueError('Coverage assignments must include every section exactly once')
    review_path = ROOT / 'data/reviews.json'
    review_bytes = review_path.read_bytes() if review_path.exists() else None
    evidence_path = ROOT / 'data/extraction.json'
    evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
    stamp = reviewed_date
    for section, n, label, de, zh, de_pages, zh_pages in rows:
        for lang, text, source, pages in [('de', de, 'de_megai2', de_pages), ('zh', zh, 'zh_collected', zh_pages)]:
            uid = f'{section}_{lang}_{n:03}'
            locations = [dict(source_id=source, pdf_page=p, printed_page=printed[source, p]) for p in pages]
            refs = [f'{source}:{p}' for p in pages]
            unit = dict(id=uid, edition_id=source, language=lang, section_id=section,
                        sequence=n, label=label, text=text, locations=locations,
                        proofread_status='scan_checked_ai', proofread_by='Codex', proofread_at=stamp,
                        evidence_pages=refs,
                        transcription_note=f'{stamp}逐句核对本地PDF可见页面；按句群划分，非原书自然段。合并排版断行，保留历史拼写、注号与可见疑字，不复现字重或斜体。脚注正文仍在原页；对应关系待用户确认。')
            data['units'].append(unit)
            data['corrections'].append(dict(unit_id=uid, method='scan_review_ai', reviewed_by='Codex',
                reviewed_at=stamp, extracted_reading=None, corrected_text=text, evidence_pages=refs,
                note='图像核对转录；页级原提取文本保存在extraction.json。未应用旧替换规则。'))
            for loc in locations:
                p = loc['pdf_page']
                evidence[f'{source}:{p}'] = (ROOT / f'tmp/source_review/{source}/{p:04}.txt').read_text(encoding='utf-8')
                if not any(x['source_id'] == source and x['pdf_page'] == p for x in data['page_map']):
                    data['page_map'].append(dict(**loc, status='scan_checked_ai', checked_by='Codex', checked_at=stamp))
            if lang == 'de':
                for word in (doubts.get(uid, []) if doubts is not None else ['äusserüchen', 'Reügiosität', 'negüte', 'weü', 'wüd', 'befindüche']):
                    start = text.find(word)
                    while start >= 0:
                        data['editorial_issues'].append(dict(
                            id=f'{uid}_literal_{start}', unit_id=uid, kind='semantic_doubt',
                            status='retained_as_source', current_reading=word, reported_reading=word,
                            evidence_pages=[f'{source}:{pages[-1] if word == "Agricultor" else pages[0]}'],
                            text_anchor=dict(start=start, end=start+len(word), quote=word),
                            note=f'本地PDF可见字形为“{word}”，词形及语义存疑，按底本照录，未用上下文改写。这里只说明当前PDF的显示，尚未判定纸本或手稿原貌；可回查原页。',
                            recorded_by='Codex', recorded_at=stamp))
                        if word == '||n|':
                            data['editorial_issues'][-1].update(kind='glyph_doubt',status='open',
                                reported_reading='页内标记字形待辨',
                                note='本地PDF384的页内标记暂记||n|；其中字形与罗马数字II的区分仍待核。中文页用[II]，不据译文静默替换。正文保留候选并明确待审。')
                        if word == 'Element II gebundne':
                            data['editorial_issues'][-1].update(kind='glyph_doubt',status='open',
                                reported_reading='Element后的页内标记待辨',
                                note='本地PDF385在Element与gebundne之间可见II形标记，暂按可见字形照录；标记性质及转写形式待核，不据语义删除或改写。')
                        if word == '/|lll|':
                            data['editorial_issues'][-1].update(kind='glyph_doubt',status='open',
                                reported_reading='页内罗马数字及界符待辨',
                                note='本地PDF386在Aller Reichthum前的标记暂记/|lll|；竖线、字母l及罗马数字III的转写仍待核，不据中文[III]替换。')
                        override = (issue_overrides or {}).get(uid, {}).get(word)
                        if override:
                            allowed = {'kind', 'status', 'note', 'reported_reading', 'evidence_pages'}
                            if not set(override) <= allowed:
                                raise ValueError('Issue override may only change editorial description and evidence')
                            data['editorial_issues'][-1].update(copy.deepcopy(override))
                        start = text.find(word, start+len(word))
        data['alignments'].append(dict(id=f'{section}_{n:03}', section_id=section, label=label,
            de_ids=[f'{section}_de_{n:03}'], zh_ids=[f'{section}_zh_{n:03}'], status='uncertain',
            proposed_by='Codex', verified_by=None, verified_at=None, review_batch=batch,
            note=f'第{batch}批句群对应候选；跨页来源分别保存，等待用户确认。'))
    for page in extra_page_maps or []:
        if any(p['source_id'] == page['source_id'] and p['pdf_page'] == page['pdf_page']
               for p in data['page_map']):
            raise ValueError('Refusing to replace an existing page mapping')
        data['page_map'].append(copy.deepcopy(page))
        source, number = page['source_id'], page['pdf_page']
        evidence[f'{source}:{number}'] = (ROOT / f'tmp/source_review/{source}/{number:04}.txt').read_text(encoding='utf-8')
    for section in data['sections']:
        if section['id'] in {r[0] for r in rows}:
            count = sum(a['section_id'] == section['id'] for a in data['alignments'])
            section['coverage'] = f'本节开头连续{count}个句群，非整节；句群边界为项目阅读划分'
    data['release'] = release
    assert not validate(data), validate(data)
    for table in ('sources', 'editions', 'units', 'alignments', 'page_map',
                  'comparisons', 'corrections', 'editorial_issues', 'coverage'):
        assert data.get(table, [])[:len(original.get(table, []))] == original.get(table, []), table
    assert all(fingerprint(data, a) == fingerprint(original, a) for a in original['alignments'])
    backup = ROOT / f'local_backups/v04-before-batch{batch}'
    backup.mkdir(parents=True, exist_ok=False)
    for name in ('corpus.json', 'extraction.json', 'coverage_plan.json', 'sampling_plan.json'):
        (backup / name).write_bytes((ROOT / 'data' / name).read_bytes())
    target = ROOT / 'data/corpus.json'
    temp = target.with_suffix('.batch6.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temp.replace(target)
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if coverage_updates:
        temp = coverage_path.with_suffix('.tmp')
        temp.write_text(json.dumps(coverage, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        temp.replace(coverage_path)
    assert (review_path.read_bytes() if review_path.exists() else None) == review_bytes
    print(f'Added {len(rows)} pending groups; prior text/fingerprints and review bytes unchanged.')
    print('Corpus SHA256:', hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()

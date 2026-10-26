"""Independent post-write protection audit for batch 48 and its front-fill order."""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from paris.corpus import index, load_corpus, validate
from paris.reading import reading_pages
from paris.reviews import fingerprint, load_reviews, review_state
from paris.sampling import load_plan
import append_v04_batch48 as recipe


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = load_corpus()
    assert data['release'] == '0.4.0-alpha44'
    assert not validate(data), validate(data)
    backup = ROOT / 'local_backups/v04-before-batch48'
    before = json.loads((backup / 'corpus.json').read_text(encoding='utf-8'))
    assert before['release'] == '0.4.0-alpha43'
    assert len(before['alignments']) == 1131
    for table in ('sources', 'editions', 'units', 'alignments', 'page_map',
                  'comparisons', 'corrections', 'editorial_issues', 'coverage'):
        assert data[table][:len(before[table])] == before[table], table
    current_sections = index(data['sections'])
    for section in before['sections']:
        current = current_sections[section['id']]
        assert {k: v for k, v in section.items() if k != 'coverage'} == {
            k: v for k, v in current.items() if k != 'coverage'}
        if section['id'] != 'mill':
            assert current == section
    assert all(fingerprint(data, a) == fingerprint(before, a) for a in before['alignments'])

    old_evidence = json.loads((backup / 'extraction.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT / 'data/extraction.json').read_text(encoding='utf-8'))
    assert all(evidence[key] == value for key, value in old_evidence.items())
    assert digest(ROOT / 'data/reviews.json') == (
        '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb')
    assert (ROOT / 'data/reviews.json').read_bytes() == (
        ROOT / 'local_backups/batch48-entry-20261023/data/reviews.json').read_bytes()
    assert (ROOT / 'data/coverage_plan.json').read_bytes() == (backup / 'coverage_plan.json').read_bytes()

    added = data['alignments'][len(before['alignments']):]
    assert [a['id'] for a in added] == [f'mill_{n:03}' for n in range(156, 180)]
    assert all(a['review_batch'] == 48 and a['status'] == 'uncertain'
               and a['verified_by'] is None and a['verified_at'] is None for a in added)
    units = index(data['units'])
    for section, number, label, de, zh, de_pages, zh_pages in recipe.ROWS:
        aid = f'{section}_{number:03}'
        for lang, text, pages in (('de', de, de_pages), ('zh', zh, zh_pages)):
            u = units[f'{section}_{lang}_{number:03}']
            source = 'de_megaiv2' if lang == 'de' else 'zh_single'
            assert u['edition_id'] == source
            assert u['text'] == text and u['label'] == label
            assert u['sequence'] == recipe.SEQUENCES[aid]
            assert u['proofread_status'] == 'scan_checked_ai'
            assert u['evidence_pages'] == [f'{source}:{p}' for p in pages]
            assert u['locations'] == [dict(source_id=source, pdf_page=p,
                                          printed_page=recipe.PRINTED[source, p]) for p in pages]
    assert len(data['units']) == len(before['units']) + 48
    for stream in (recipe.DE, recipe.ZH):
        for key, expected in stream[2].items():
            assert hashlib.sha256(evidence[key].encode('utf-8')).hexdigest() == expected
            source, page = key.split(':')
            assert evidence[key] == (ROOT / f'tmp/source_review/{source}/{int(page):04}.txt').read_text(encoding='utf-8')

    added_issues = data['editorial_issues'][len(before['editorial_issues']):]
    for uid, words in recipe.DOUBTS.items():
        for word in words:
            issues = [i for i in added_issues if i['unit_id'] == uid
                      and i['text_anchor']['quote'] == word]
            assert issues, (uid, word)
            for issue in issues:
                for key, value in recipe.OVERRIDES[uid][word].items():
                    assert issue[key] == value
    assert 'in den Fall No. 1 gehören.' in units['mill_de_164']['text']
    assert units['mill_zh_176']['text'].count('1/10') == 5
    assert units['mill_zh_177']['text'].count('1/10') == 3
    assert units['mill_de_177']['locations'] == [
        dict(source_id='de_megaiv2', pdf_page=437, printed_page='443'),
        dict(source_id='de_megaiv2', pdf_page=439, printed_page='444')]
    illustration = next(p for p in data['page_map'] if p['source_id'] == 'de_megaiv2' and p['pdf_page'] == 438)
    assert illustration == recipe.EXTRA_PAGE_MAPS[0]
    assert not any(loc['source_id'] == 'de_megaiv2' and loc['pdf_page'] == 438
                   for u in data['units'] for loc in u['locations'])
    assert evidence['de_megaiv2:438'] == (ROOT / 'tmp/source_review/de_megaiv2/0438.txt').read_text(encoding='utf-8')

    mill_order = [aid for page in reading_pages(data, 'mill') for aid in page['alignment_ids']]
    assert mill_order == ([f'mill_{n:03}' for n in range(110, 180)]
                          + [f'mill_{n:03}' for n in range(62, 110)]
                          + [f'mill_{n:03}' for n in range(1, 62)])
    for sid in current_sections:
        old_order = [aid for page in reading_pages(before, sid) for aid in page['alignment_ids']]
        old_ids = set(old_order)
        new_order = [aid for page in reading_pages(data, sid)
                     for aid in page['alignment_ids'] if aid in old_ids]
        assert new_order == old_order, sid

    old_plan = json.loads((backup / 'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert len(old_plan['recommended']) == 421
    assert plan['recommended'][:421] == old_plan['recommended']
    assert set(old_plan['scope_ids']) <= set(plan['scope_ids'])
    reviews = load_reviews()
    states = Counter(review_state(data, a, reviews)[0] for a in data['alignments'])
    assert states['manually_verified'] == 24 and states['stale'] == 0
    for source in data['sources']:
        assert digest(ROOT / 'Asset_by_user' / source['file_name']) == source['sha256']
    report = dict(
        checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        release=data['release'], batch=48, prior_groups_preserved=len(before['alignments']),
        added=len(added), recipe_units_checked=48, prior_records_fingerprints_evidence_reviews='unchanged',
        review_states=dict(states), added_issues=len(added_issues),
        counts={key: len(data[key]) for key in ('units', 'alignments', 'page_map', 'sections')},
        sampling=dict(scope=len(plan['scope_ids']), recommended=len(plan['recommended']), prior_recommendations_preserved=421),
        scan_pages=dict(de_megaiv2=[433, 434, 435, 436, 437, 438, 439], zh_single=[168, 169, 170, 171, 172, 173]),
        next_start=dict(id='mill_180', sequence=-29930, de_pdf=439, de_line=29,
                        de_printed='444', de_anchor='Im ersten Fall öffnet das Gouvernement',
                        zh_pdf=173, zh_line=16, zh_printed='163', zh_anchor='在第一种情况下'),
        data_sha256={name: digest(ROOT / 'data' / name) for name in
                     ('corpus.json', 'extraction.json', 'coverage_plan.json', 'sampling_plan.json', 'reviews.json')})
    output = ROOT / 'tmp/alpha44-batch48-audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Audit an appended recipe against its preserved pre-batch snapshot (no writes to data)."""
import argparse
import hashlib
import importlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paris.corpus import index, load_corpus, validate
from paris.reading import reading_pages
from paris.reviews import fingerprint, load_reviews, review_state
from paris.sampling import load_plan


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(batch):
    recipe = importlib.import_module(f'append_v04_batch{batch}')
    data = load_corpus()
    assert not validate(data)
    backup = ROOT / f'local_backups/v04-before-batch{batch}'
    before = json.loads((backup / 'corpus.json').read_text(encoding='utf-8'))
    for table in ('sources', 'editions', 'units', 'alignments', 'page_map',
                  'comparisons', 'corrections', 'editorial_issues', 'coverage'):
        assert data[table][:len(before[table])] == before[table], table
    for section in before['sections']:
        current = index(data['sections'])[section['id']]
        assert {k: v for k, v in section.items() if k != 'coverage'} == {
            k: v for k, v in current.items() if k != 'coverage'}
    assert all(fingerprint(data, a) == fingerprint(before, a) for a in before['alignments'])
    old_evidence = json.loads((backup / 'extraction.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT / 'data/extraction.json').read_text(encoding='utf-8'))
    assert all(evidence[k] == v for k, v in old_evidence.items())
    old_coverage = json.loads((backup / 'coverage_plan.json').read_text(encoding='utf-8'))
    coverage = json.loads((ROOT / 'data/coverage_plan.json').read_text(encoding='utf-8'))
    assert old_coverage['evidence'] == coverage['evidence']
    for item in old_coverage['items']:
        current = index(coverage['items'])[item['id']]
        if item['section_ids']:
            assert current == item
        else:
            assert {k: v for k, v in current.items() if k != 'section_ids'} == {
                k: v for k, v in item.items() if k != 'section_ids'}
    added = data['alignments'][len(before['alignments']):]
    expected_ids = [f'{r[0]}_{r[1]:03}' for r in recipe.ROWS]
    assert [a['id'] for a in added] == expected_ids
    assert all(a['review_batch'] == batch and a['status'] == 'uncertain'
               and a['verified_by'] is None for a in added)
    units = index(data['units'])
    for section, number, label, de, zh, de_pages, zh_pages in recipe.ROWS:
        for language, text, pages in (('de', de, de_pages), ('zh', zh, zh_pages)):
            unit = units[f'{section}_{language}_{number:03}']
            assert unit['text'] == text and unit['label'] == label
            assert unit['sequence'] == number
            assert [loc['pdf_page'] for loc in unit['locations']] == pages
            assert unit['proofread_status'] == 'scan_checked_ai'
            assert all(loc['printed_page'] == recipe.PRINTED[loc['source_id'], loc['pdf_page']]
                       for loc in unit['locations'])
    for section in {r[0] for r in recipe.ROWS}:
        order = [aid for page in reading_pages(data, section) for aid in page['alignment_ids']]
        assert order == [f'{section}_{n:03}' for n in range(1, len(order) + 1)]
    old_plan = json.loads((backup / 'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert plan['recommended'][:len(old_plan['recommended'])] == old_plan['recommended']
    assert set(old_plan['scope_ids']) <= set(plan['scope_ids'])
    states = Counter(review_state(data, a, load_reviews())[0] for a in data['alignments'])
    assert states['manually_verified'] == 24 and states['stale'] == 0
    assert digest(ROOT / 'data/reviews.json') == '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb'
    report = dict(
        checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        release=data['release'], batch=batch, prior_groups_preserved=len(before['alignments']),
        added=len(added), recipe_units_checked=2 * len(recipe.ROWS),
        first=expected_ids[0], last=expected_ids[-1], review_states=dict(states),
        prior_records_fingerprints_evidence_and_reviews='unchanged',
        sampling=dict(scope=len(plan['scope_ids']), recommended=len(plan['recommended']),
                      prior_recommendations_preserved=len(old_plan['recommended'])),
        counts={k: len(data[k]) for k in ('units', 'alignments', 'page_map', 'sections')},
        data_sha256={n: digest(ROOT / 'data' / n) for n in
                     ('corpus.json', 'extraction.json', 'coverage_plan.json', 'sampling_plan.json', 'reviews.json')})
    output = ROOT / f'tmp/{data["release"].split("-")[-1]}-batch{batch}-audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch', type=int)
    audit(parser.parse_args().batch)

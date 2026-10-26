"""Verify batch 26 and the completed front-fill adjacency to mill_001."""
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
import append_v04_batch26 as batch26


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = load_corpus()
    assert data['release'] == '0.4.0-alpha22'
    assert not validate(data)
    backup = ROOT / 'local_backups' / 'v04-before-batch26'
    before = json.loads((backup / 'corpus.json').read_text(encoding='utf-8'))
    for table in ('sources', 'editions', 'units', 'alignments', 'page_map',
                  'comparisons', 'corrections', 'editorial_issues', 'coverage'):
        assert data[table][:len(before[table])] == before[table], table
    assert len(before['alignments']) == 612
    assert all(fingerprint(data, a) == fingerprint(before, a) for a in before['alignments'])

    units = index(data['units'])
    added = [a for a in data['alignments'] if a['review_batch'] == 26]
    assert [a['id'] for a in added] == [f'mill_{n:03}' for n in range(86, 110)]
    assert all(a['status'] == 'uncertain' for a in added)
    for section, number, _, de, zh, de_pages, zh_pages in batch26.ROWS:
        for language, text_value, pages in (('de', de, de_pages), ('zh', zh, zh_pages)):
            unit = units[f'{section}_{language}_{number:03}']
            assert unit['text'] == text_value
            assert unit['sequence'] == batch26.SEQUENCES[f'{section}_{number:03}']
            assert [loc['pdf_page'] for loc in unit['locations']] == pages

    source_order = [aid for page in reading_pages(data, 'mill') for aid in page['alignment_ids']]
    assert source_order[:48] == [f'mill_{n:03}' for n in range(62, 110)]
    assert source_order[48] == 'mill_001'
    assert units['mill_de_109']['locations'][-1]['pdf_page'] == 455
    assert units['mill_zh_109']['locations'][-1]['pdf_page'] == 191

    old_plan = json.loads((backup / 'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert len(old_plan['recommended']) == 211
    assert plan['recommended'][:211] == old_plan['recommended']
    reviews = load_reviews()
    states = Counter(review_state(data, a, reviews)[0] for a in data['alignments'])
    assert states['manually_verified'] == 24 and states['stale'] == 0
    reviews_hash = digest(ROOT / 'data' / 'reviews.json')
    assert reviews_hash == '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb'

    report = {
        'checked_at': datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        'release': data['release'],
        'prior_groups_preserved': len(before['alignments']),
        'added_by_batch': {'26': len(added)},
        'recipe_units_checked': len(batch26.ROWS) * 2,
        'source_order': {'front_fill_first': source_order[0],
                         'front_fill_last': source_order[47],
                         'existing_first': source_order[48]},
        'prior_review_fingerprints': 'unchanged',
        'reviews_sha256': reviews_hash,
        'review_states': dict(states),
        'sampling': {'scope': len(plan['scope_ids']), 'recommended': len(plan['recommended']),
                     'prior_recommendations_preserved': len(old_plan['recommended'])},
        'data_sha256': {name: digest(ROOT / 'data' / name) for name in
                        ('corpus.json', 'extraction.json', 'coverage_plan.json',
                         'sampling_plan.json', 'reviews.json')},
        'scan_pages': {'de_megaiv2': [453, 454, 455],
                       'zh_single': [189, 190, 191]},
        'counts': {key: len(data[key]) for key in ('units', 'alignments', 'page_map', 'sections')},
    }
    output = ROOT / 'tmp' / 'alpha22-batch26-audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()

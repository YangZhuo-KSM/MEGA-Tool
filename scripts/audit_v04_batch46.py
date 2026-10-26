"""Protect batch 46, including two independent negative-sequence front fills."""
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
import append_v04_batch46 as batch46


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = load_corpus()
    assert data['release'] == '0.4.0-alpha42'
    assert not validate(data)
    backup = ROOT / 'local_backups' / 'v04-before-batch46'
    before = json.loads((backup / 'corpus.json').read_text(encoding='utf-8'))

    for table in ('sources', 'editions', 'units', 'alignments', 'page_map',
                  'comparisons', 'corrections', 'editorial_issues', 'coverage'):
        assert data[table][:len(before[table])] == before[table], table
    for section in before['sections']:
        current = index(data['sections'])[section['id']]
        assert {k: v for k, v in section.items() if k != 'coverage'} == {
            k: v for k, v in current.items() if k != 'coverage'}
    assert all(fingerprint(data, a) == fingerprint(before, a)
               for a in before['alignments'])

    old_evidence = json.loads((backup / 'extraction.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT / 'data/extraction.json').read_text(encoding='utf-8'))
    assert all(evidence[key] == value for key, value in old_evidence.items())
    assert digest(ROOT / 'data/reviews.json') == (
        '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb')

    added = data['alignments'][len(before['alignments']):]
    expected_ids = ['alienation_085', 'alienation_086'] + [
        f'mill_{number:03}' for number in range(110, 132)]
    assert [item['id'] for item in added] == expected_ids
    assert all(item['review_batch'] == 46 and item['status'] == 'uncertain'
               and item['verified_by'] is None for item in added)

    units = index(data['units'])
    for section, number, label, de, zh, de_pages, zh_pages in batch46.ROWS:
        alignment_id = f'{section}_{number:03}'
        for language, text, pages in (('de', de, de_pages), ('zh', zh, zh_pages)):
            unit = units[f'{section}_{language}_{number:03}']
            assert unit['text'] == text and unit['label'] == label
            assert unit['sequence'] == batch46.SEQUENCES[alignment_id]
            assert [location['pdf_page'] for location in unit['locations']] == pages
            assert unit['proofread_status'] == 'scan_checked_ai'
            assert all(location['printed_page'] == batch46.PRINTED[
                location['source_id'], location['pdf_page']]
                for location in unit['locations'])

    alienation_order = [alignment_id for page in reading_pages(data, 'alienation')
                         for alignment_id in page['alignment_ids']]
    mill_order = [alignment_id for page in reading_pages(data, 'mill')
                  for alignment_id in page['alignment_ids']]
    assert alienation_order == ['alienation_085', 'alienation_086'] + [
        f'alienation_{number:03}' for number in range(1, 85)]
    assert mill_order == [f'mill_{number:03}' for number in range(110, 132)] + [
        f'mill_{number:03}' for number in range(62, 110)] + [
        f'mill_{number:03}' for number in range(1, 62)]

    old_plan = json.loads((backup / 'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert plan['recommended'][:len(old_plan['recommended'])] == old_plan['recommended']
    assert set(old_plan['scope_ids']) <= set(plan['scope_ids'])
    states = Counter(review_state(data, item, load_reviews())[0]
                     for item in data['alignments'])
    assert states['manually_verified'] == 24 and states['stale'] == 0

    report = {
        'checked_at': datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        'release': data['release'],
        'batch': 46,
        'prior_groups_preserved': len(before['alignments']),
        'added': len(added),
        'recipe_units_checked': len(batch46.ROWS) * 2,
        'front_fill_order': {
            'alienation': {'first': alienation_order[0], 'existing_first': alienation_order[2]},
            'mill': {'first': mill_order[0], 'prior_front_fill_first': mill_order[22],
                     'original_first': mill_order[70]},
        },
        'prior_records_fingerprints_evidence_and_reviews': 'unchanged',
        'review_states': dict(states),
        'sampling': {'scope': len(plan['scope_ids']),
                     'recommended': len(plan['recommended']),
                     'prior_recommendations_preserved': len(old_plan['recommended'])},
        'counts': {key: len(data[key])
                   for key in ('units', 'alignments', 'page_map', 'sections')},
        'scan_pages': {
            'de_megai2': [363, 364], 'zh_collected': [291, 292],
            'de_megaiv2': [424, 425, 426, 427, 428, 429],
            'zh_single': [159, 160, 161, 162, 163, 164],
        },
        'data_sha256': {name: digest(ROOT / 'data' / name) for name in
                        ('corpus.json', 'extraction.json', 'coverage_plan.json',
                         'sampling_plan.json', 'reviews.json')},
    }
    output = ROOT / 'tmp' / 'alpha42-batch46-audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Protect incremental Mill front-fill batches, including negative reading order.

Read-only audit: never imports recipes as executable append commands.
"""
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
    backup = ROOT / f'local_backups/v04-before-batch{batch}'
    before = json.loads((backup / 'corpus.json').read_text(encoding='utf-8'))
    data = load_corpus()
    assert not validate(data), validate(data)
    assert not any(a['review_batch'] == batch for a in before['alignments'])
    assert data['release'] == f'0.4.0-alpha{batch-4}'
    assert before['release'] == f'0.4.0-alpha{batch-5}'
    for table in ('sources','editions','units','alignments','page_map','comparisons',
                  'corrections','editorial_issues','coverage'):
        assert data[table][:len(before[table])] == before[table], table
    sections = index(data['sections'])
    for section in before['sections']:
        current = sections[section['id']]
        assert {k:v for k,v in current.items() if k != 'coverage'} == {
            k:v for k,v in section.items() if k != 'coverage'}
        if section['id'] != 'mill':
            assert current == section
    assert all(fingerprint(data,a) == fingerprint(before,a) for a in before['alignments'])
    evidence = json.loads((ROOT/'data/extraction.json').read_text(encoding='utf-8'))
    old_evidence = json.loads((backup/'extraction.json').read_text(encoding='utf-8'))
    assert all(evidence[k] == v for k,v in old_evidence.items())
    assert digest(ROOT/'data/reviews.json') == '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb'
    assert (ROOT/'data/coverage_plan.json').read_bytes() == (backup/'coverage_plan.json').read_bytes()
    added = data['alignments'][len(before['alignments']):]
    ids = [f'{s}_{n:03}' for s,n,*_ in recipe.ROWS]
    assert [a['id'] for a in added] == ids
    assert all(a['review_batch'] == batch and a['status'] == 'uncertain'
               and a['verified_by'] is None and a['verified_at'] is None for a in added)
    units = index(data['units'])
    assert len(data['units']) == len(before['units']) + len(ids)*2
    for section,n,label,de,zh,dp,zp in recipe.ROWS:
        aid = f'{section}_{n:03}'
        for lang,text,pages in [('de',de,dp),('zh',zh,zp)]:
            u = units[f'{section}_{lang}_{n:03}']
            source = 'de_megaiv2' if lang == 'de' else 'zh_single'
            assert u['edition_id'] == source and u['text'] == text and u['label'] == label
            assert u['sequence'] == recipe.SEQUENCES[aid] < 0
            assert u['proofread_status'] == 'scan_checked_ai'
            assert u['evidence_pages'] == [f'{source}:{p}' for p in pages]
            assert u['locations'] == [dict(source_id=source,pdf_page=p,
                printed_page=recipe.PRINTED[source,p]) for p in pages]
    for st in (recipe.DE,recipe.ZH):
        for key,expected in st[2].items():
            assert hashlib.sha256(evidence[key].encode('utf-8')).hexdigest() == expected
            source,page = key.split(':')
            assert evidence[key] == (ROOT/f'tmp/source_review/{source}/{int(page):04}.txt').read_text(encoding='utf-8')
    issues = data['editorial_issues'][len(before['editorial_issues']):]
    for uid,words in recipe.DOUBTS.items():
        for word in words:
            found = [i for i in issues if i['unit_id']==uid and i['text_anchor']['quote']==word]
            assert found,(uid,word)
            for issue in found:
                assert all(issue[k]==v for k,v in recipe.OVERRIDES[uid][word].items())
    for sid in sections:
        old = [aid for p in reading_pages(before,sid) for aid in p['alignment_ids']]
        now = [aid for p in reading_pages(data,sid) for aid in p['alignment_ids']]
        assert [aid for aid in now if aid in set(old)] == old,sid
        if sid == 'mill':
            prior_front = [a['id'] for a in before['alignments'] if a['id'].startswith('mill_')
                           and -30000 <= index(before['units'])[a['de_ids'][0]]['sequence'] < -29000]
            assert now[:len(prior_front)+len(ids)] == prior_front+ids
            assert now[len(prior_front)+len(ids):] == [a for a in old if a not in set(prior_front)]
    old_plan = json.loads((backup/'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert plan['recommended'][:len(old_plan['recommended'])] == old_plan['recommended']
    assert set(old_plan['scope_ids']) <= set(plan['scope_ids'])
    assert set(plan['scope_ids'])-set(old_plan['scope_ids']) == set(ids)
    states = Counter(review_state(data,a,load_reviews())[0] for a in data['alignments'])
    assert states['manually_verified']==24 and states['stale']==0
    for source in data['sources']:
        assert digest(ROOT/'Asset_by_user'/source['file_name']) == source['sha256']
    if hasattr(recipe,'extra_assertions'):
        recipe.extra_assertions(data,evidence)
    report = dict(checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
        release=data['release'],batch=batch,prior_groups_preserved=len(before['alignments']),
        added=len(ids),recipe_units_checked=len(ids)*2,added_issues=len(issues),
        prior_records_fingerprints_evidence_reviews='unchanged',review_states=dict(states),
        counts={k:len(data[k]) for k in ('units','alignments','page_map','sections')},
        sampling=dict(scope=len(plan['scope_ids']),recommended=len(plan['recommended']),
            prior_recommendations_preserved=len(old_plan['recommended'])),
        scan_pages=recipe.SCAN_PAGES,next_start=recipe.NEXT_START,
        data_sha256={n:digest(ROOT/'data'/n) for n in
            ('corpus.json','extraction.json','coverage_plan.json','sampling_plan.json','reviews.json')})
    output = ROOT/f'tmp/alpha{batch-4}-batch{batch}-audit.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch',type=int)
    audit(parser.parse_args().batch)

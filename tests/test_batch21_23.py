"""Regression checks for the fixed three-batch expansion and mixed source route."""
import hashlib
import json
from pathlib import Path

from paris.corpus import index, load_corpus
from paris.locator import locate
from paris.reviews import fingerprint
from paris.sampling import load_plan

ROOT = Path(__file__).resolve().parents[1]


def test_three_fixed_batches_and_pending_status():
    data = load_corpus()
    for batch in (21, 22, 23):
        group = [a for a in data['alignments'] if a['review_batch'] == batch]
        assert len(group) == 24
        assert all(a['status'] == 'uncertain' and not a['verified_by'] for a in group)
    cohort = [a for a in data['alignments'] if a['review_batch'] <= 23]
    assert sum(a['section_id'] == 'money' for a in cohort) == 47
    assert sum(a['section_id'] == 'mill' for a in cohort) == 37


def test_mill_uses_its_own_sources_and_identifies_excerpts():
    data = load_corpus()
    units = index(data['units'])
    for n in range(13,38):
        for lang, source in [('de','de_megaiv2'),('zh','zh_single')]:
            u = units[f'mill_{lang}_{n:03}']
            assert u['edition_id'] == source
            assert all(l['source_id'] == source for l in u['locations'])
    assert '马克思评注' in units['mill_de_013']['label']
    assert all('穆勒摘录' in units[f'mill_de_{n:03}']['label'] for n in range(14,38))
    # Coverage prose evolves as front-fill batches are added; source routing remains invariant.
    for u in data['units']:
        if u['section_id'] == 'mill':
            expected = 'de_megaiv2' if u['language'] == 'de' else 'zh_single'
            assert u['edition_id'] == expected


def test_poems_cross_page_citations_and_whitespace_page_boundary():
    data = load_corpus()
    units = index(data['units'])
    for n in (9,10,11):
        assert units[f'money_de_{n:03}']['text'].count('\n') >= 8
        assert units[f'money_zh_{n:03}']['text'].count('\n') >= 8
    assert [p['pdf_page'] for p in units['money_de_010']['locations']] == [435]
    assert [p['printed_page'] for p in units['money_zh_010']['locations']] == ['360','361']
    assert [p['printed_page'] for p in units['money_zh_047']['locations']] == ['364','365']
    assert [p['printed_page'] for p in units['mill_de_029']['locations']] == ['467','468']
    assert [p['printed_page'] for p in units['mill_zh_035']['locations']] == ['186','187']
    hit = next(h for h in locate(data,'我的劳动是什么') if h['unit']['id'] == 'mill_zh_013')
    assert hit['reference']['locations'][0]['printed_page'] == '185'


def test_old_records_review_fingerprints_and_frozen_samples():
    data = load_corpus()
    backup = ROOT / 'local_backups/v04-before-batch21'
    old = json.loads((backup/'corpus.json').read_text(encoding='utf-8'))
    for table in ('sources','editions','units','alignments','page_map','comparisons',
                  'corrections','editorial_issues','coverage'):
        assert data[table][:len(old[table])] == old[table]
    assert all(fingerprint(data,a) == fingerprint(old,a) for a in old['alignments'])
    old_plan = json.loads((backup/'sampling_plan.json').read_text(encoding='utf-8'))
    plan = load_plan(data)
    assert plan['recommended'][:len(old_plan['recommended'])] == old_plan['recommended']
    cohort_ids = {a['id'] for a in data['alignments'] if 5 <= a['review_batch'] <= 23}
    assert len(cohort_ids) == 540
    assert set(plan['scope_ids']) & cohort_ids == cohort_ids
    assert sum(r['alignment_id'] in cohort_ids for r in plan['recommended']) == 197
    assert hashlib.sha256((ROOT/'data/reviews.json').read_bytes()).hexdigest() == (
        '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb')

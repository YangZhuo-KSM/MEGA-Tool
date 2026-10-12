"""Actual long-span locations and source-literal doubts in the 30-group cohort."""
from paris.corpus import load_corpus, index
from paris.locator import locate
from paris.reading import reading_pages
from paris.annotations import unit_issues, annotated_html
from paris.sampling import load_plan


def test_thirty_groups_remain_complete_in_reading_pages():
    data = load_corpus()
    cohort = [a for a in data['alignments'] if a['review_batch'] == 13]
    assert [a['id'] for a in cohort] == [f'communism_{i:03}' for i in range(31, 61)]
    assert all(a['status'] == 'uncertain' and not a['verified_by'] for a in cohort)
    pages = reading_pages(data, 'communism')
    ids = [aid for page in pages for aid in page['alignment_ids']]
    assert ids[:60] == [f'communism_{i:03}' for i in range(1, 61)]
    assert any(len(p['alignment_ids']) > 1 for p in pages)


def test_bilingual_long_queries_resolve_all_original_pages():
    data = load_corpus()
    for query, uid, expected in [
        ('Die Gesellschaft ist die vollendete Wesenseinheit', 'communism_de_031', [390, 391]),
        ('而且我本身的存在是社会的活动；因此', 'communism_zh_033', [326, 327]),
        ('die wahre anthropologische Natur ist', 'communism_de_060', [395, 396]),
        ('如果心理学还没有打开这本书', 'communism_zh_059', [331, 332]),
    ]:
        hit = next(h for h in locate(data, query) if h['unit']['id'] == uid)
        assert [p['pdf_page'] for p in hit['reference']['locations']] == expected
        assert hit['reference']['plain'] and hit['targets'][0]['page'] is not None
    hit = next(h for h in locate(data, '人的本质的对象化都是必要的')
               if h['unit']['id'] == 'communism_zh_056')
    assert '第305—306页' in hit['reference']['plain']


def test_literal_words_and_glyph_candidates_retain_exact_evidence():
    data = load_corpus(); units = index(data['units'])
    for uid, token, evidence, status in [
        ('communism_de_033', 'mü', 'de_megai2:391', 'retained_as_source'),
        ('communism_de_050', 'Wiesen', 'de_megai2:394', 'retained_as_source'),
        ('communism_de_050', '||VIIl|', 'de_megai2:394', 'open'),
        ('communism_de_060', 'verüeren', 'de_megai2:396', 'retained_as_source'),
    ]:
        issues = [i for i in unit_issues(data, uid) if i['current_reading'] == token]
        assert issues and all(i['status'] == status and i['evidence_pages'] == [evidence] for i in issues)
        for issue in issues:
            a = issue['text_anchor']
            assert units[uid]['text'][a['start']:a['end']] == token
        assert 'editorial-mark' in annotated_html(units[uid]['text'], [], issues)
    plan = load_plan(data)
    selected = {r['alignment_id'] for r in plan['recommended']}
    assert {'communism_032', 'communism_037', 'communism_041', 'communism_050'} <= selected

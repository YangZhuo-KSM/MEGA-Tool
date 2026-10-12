"""A real shared source page, new chapter navigation, and unrepaired source readings."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
from paris.corpus import load_corpus, index
from paris.coverage import load_plan, coverage_rows
from paris.pages import units_on_page
from paris.locator import locate
from paris.annotations import unit_issues
from paris.sampling import load_plan as sampling_plan


def test_thirty_six_pending_groups_and_shared_chapter_boundary():
    data = load_corpus(); units = index(data['units'])
    batch = [a for a in data['alignments'] if a['review_batch'] == 14]
    assert len(batch) == 36
    assert [a['id'] for a in batch] == ([f'communism_{n:03}' for n in range(61,79)]
                                        + [f'hegel_{n:03}' for n in range(1,19)])
    assert all(a['status'] == 'uncertain' and a['verified_by'] is None for a in batch)
    assert [p['pdf_page'] for p in units['communism_de_078']['locations']] == [398,399]
    assert units['communism_zh_078']['locations'][0]['printed_page'] == '311'
    shared = {u['id'] for u in units_on_page(data, 'de_megai2', 399)}
    assert {'communism_de_078', 'hegel_de_001'} <= shared
    row = next(r for r in coverage_rows(data, {}, load_plan(data)) if r['id']=='hegel')
    assert row['groups'] == 108 and row['collected_ratio'] is None


def test_new_long_cross_page_search_preserves_both_printed_pages():
    data = load_corpus()
    hit = next(h for h in locate(data, '在批判每日每时以群众的愚钝无知')
               if h['unit']['id'] == 'hegel_zh_006')
    assert [p['pdf_page'] for p in hit['reference']['locations']] == [338,339]
    assert '第313—314页' in hit['reference']['plain']
    assert hit['targets'][0]['alignment_id'] == 'hegel_006'
    hit = next(h for h in locate(data, 'was nun mit der Logik') if h['unit']['id']=='hegel_de_005')
    assert [p['pdf_page'] for p in hit['reference']['locations']] == [399,400]


def test_literally_retained_extra_word_and_unresolved_markers():
    data = load_corpus(); units = index(data['units'])
    assert 'Verhältniß das „des Menschen' in units['hegel_de_009']['text']
    assert 'sezt das Wirkliche' in units['hegel_de_012']['text']
    assert 'wesentliehe' in units['hegel_de_002']['text']
    for uid,token,page,status in [
        ('communism_de_065','Verwüküchung','de_megai2:397','retained_as_source'),
        ('hegel_de_002','wesentliehe','de_megai2:399','retained_as_source'),
        ('hegel_de_001','16)','de_megai2:399','open'),
        ('hegel_de_015','||XJIl|','de_megai2:401','open'),
    ]:
        issue = next(i for i in unit_issues(data,uid) if i['current_reading']==token)
        assert issue['evidence_pages']==[page] and issue['status']==status
        anchor=issue['text_anchor']
        assert units[uid]['text'][anchor['start']:anchor['end']]==token
    ids = {r['alignment_id'] for r in sampling_plan(data)['recommended']}
    assert {'communism_069','communism_073','communism_074',
            'hegel_001','hegel_005','hegel_007','hegel_015'} <= ids


def test_new_topic_opens_in_the_reader_without_confirming(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    at.sidebar.selectbox(key='section_id').select('hegel').run()
    assert not at.exception
    assert any('批判辩证法的说明位置' in x.value for x in at.markdown)
    assert any('第312页' in x.value for x in at.caption)
    assert at.metric[0].value == '240' and at.metric[1].value == '0'

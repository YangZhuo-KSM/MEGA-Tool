"""Real cross-page boundaries and source-literal marks of the sixth batch."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
from paris.corpus import load_corpus, index
from paris.annotations import unit_issues, annotated_html


def test_batch6_cross_page_words_and_pending_state():
    data = load_corpus(); units = index(data['units'])
    batch = [a for a in data['alignments'] if a['review_batch'] == 6]
    assert len(batch) == 6
    assert all(a['status'] == 'uncertain' and a['verified_by'] is None for a in batch)
    for uid, pages in [('private_relation_zh_006', [306, 307]),
                       ('private_work_de_005', [383, 384]),
                       ('private_work_zh_005', [314, 315])]:
        assert [p['pdf_page'] for p in units[uid]['locations']] == pages
        assert len(units[uid]['evidence_pages']) == len(pages)
    assert units['private_relation_zh_006']['text'].startswith('资本的存在')
    assert 'Privateigenthum incorporirt' in units['private_work_de_005']['text']


def test_repeated_source_doubts_each_have_visible_exact_anchor():
    data = load_corpus(); unit = index(data['units'])['private_work_de_005']
    issues = unit_issues(data, unit['id'])
    assert len(issues) == 7
    assert sum(i['current_reading'] == 'wüd' for i in issues) == 2
    html = annotated_html(unit['text'], [], issues)
    assert html.count('class="editorial-mark"') == 7
    for issue in issues:
        anchor = issue['text_anchor']
        assert unit['text'][anchor['start']:anchor['end']] == issue['current_reading']
        assert issue['status'] == 'retained_as_source'
    assert len(unit_issues(data, 'private_work_de_006')) == 2


def test_sixth_batch_review_is_available_without_confirming(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews', lambda: {})
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('审核与资料').run()
    app.selectbox[0].select(6).run()
    assert not app.exception
    assert len(app.get('form')) == 6
    assert any('语义存疑' in x.value for x in app.warning)

from pathlib import Path
from streamlit.testing.v1 import AppTest
import pytest

from paris.corpus import load_corpus
from paris.reading import page_for_alignment

APP=str(Path(__file__).resolve().parents[1]/'app.py')


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    at=AppTest.from_file(APP).run(timeout=30)
    assert not at.exception
    return at


def displayed_text(at):
    return '\n'.join(x.value for kind in ['caption','markdown','info','success','subheader'] for x in getattr(at,kind))


def test_navigation_and_continuous_reading_keep_group_sequence(app):
    assert '竞争与垄断' in displayed_text(app) and '货币制度' in displayed_text(app)
    app.button(key='reading_next').click().run()
    assert app.sidebar.selectbox(key='reading_page').value=='reading-alienation_004'
    app.button(key='reading_prev').click().run()
    assert app.sidebar.selectbox(key='reading_page').value=='reading-alienation_001'
    app.toggle(key='continuous_reading').set_value(True).run()
    assert len(app.subheader)==4
    assert '阅读页 4' in displayed_text(app)
    assert not app.exception


def test_search_to_originals_and_reader_hides_internal_index(app,monkeypatch):
    calls=[]
    def missing(source,page):
        calls.append((source['id'],page))
        raise FileNotFoundError('模拟预览：'+source['id'])
    monkeypatch.setattr('paris.pages.render_page',missing)
    app.sidebar.radio(key='workspace').set_value('页码索引').run()
    app.selectbox(key='locator_source').select('zh_collected').run()
    app.text_area(key='locator_query').input('对象化').run()
    assert '第267—268页' in displayed_text(app)
    assert '人民出版社2002年' in displayed_text(app)
    assert 'PDF 第' not in displayed_text(app) and '292' not in displayed_text(app)
    app.button(key='result_alienation_zh_006_292').click().run()
    assert calls[-1]==('zh_collected',292)
    app.button(key='result_alienation_zh_006_293').click().run()
    assert ('zh_collected',293) in calls
    app.button(key='locate_alienation_zh_006_alienation_006').click().run()
    assert app.sidebar.radio(key='workspace').value=='德中对读'
    assert app.sidebar.selectbox(key='reading_page').value==page_for_alignment(load_corpus(),'alienation_006')['id']
    assert any('<mark>对象化</mark>' in m.value for m in app.markdown)
    assert 'PDF 第' not in displayed_text(app) and '292' not in displayed_text(app)
    assert not app.exception


def test_comparison_bridge_shows_original_hit_with_own_source(app):
    app.sidebar.radio(key='workspace').set_value('页码索引').run()
    app.selectbox(key='locator_source').select('zh_single').run()
    app.text_area(key='locator_query').input('对象化').run()
    app.button(key='locate_alienation_zh_single_006_alienation_006').click().run()
    assert '检索命中的比较版本' in [e.label for e in app.expander]
    assert '2000年版' in displayed_text(app)
    assert '仍待研究者复核' in displayed_text(app)
    assert not app.exception


def test_reader_filter_keeps_neighbors_and_does_not_renumber(app):
    app.sidebar.text_input(key='reader_query').input('Vergegenständlichung').run()
    assert app.sidebar.selectbox(key='reading_page').value=='reading-alienation_004'
    data=load_corpus()
    neighbor=next(u for u in data['units'] if u['id']=='alienation_de_004')
    assert any(neighbor['text'] in m.value for m in app.markdown)
    assert '阅读页 2' in displayed_text(app)
    assert not app.exception


def test_advanced_is_only_opt_in_mapping_surface(app):
    app.sidebar.radio(key='workspace').set_value('页码索引').run()
    assert not app.text_input
    assert 'PDF 第' not in displayed_text(app)
    app.toggle(key='advanced_pages').set_value(True).run()
    app.selectbox(key='mapping_source').select('zh_collected').run()
    app.text_input(key='mapping_value').input('267').run()
    assert 'PDF 第 292 页' in displayed_text(app)
    app.toggle(key='advanced_pages').set_value(False).run()
    assert 'PDF 第' not in displayed_text(app)
    assert not app.exception

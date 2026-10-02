from pathlib import Path
import copy
import pytest
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolate_reviews(monkeypatch):
    # Tests must not depend on or modify the researcher's real review file.
    monkeypatch.setattr('paris.reviews.load_reviews',lambda: {})


def app():
    at=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
    assert not at.exception
    return at


def test_default_reader_and_section_switch():
    at=app()
    assert at.metric[0].value=='42'
    assert at.metric[1].value=='0'
    at.sidebar.selectbox[0].select('mill').run()
    assert not at.exception
    assert at.sidebar.selectbox[1].value=='reading-mill_001'
    assert any('需要与产品的权力' in x.value for x in at.markdown)
    assert not any('竞争与垄断' in x.value for x in at.markdown)


def test_search_and_empty_result():
    at=app()
    at.sidebar.text_input[0].input('Vergegenständlichung').run()
    assert not at.exception
    assert any('<mark>' in x.value for x in at.markdown)
    at.sidebar.text_input[0].input('zzznoresults').run()
    assert not at.exception
    assert any('没有命中' in x.value for x in at.info)


def test_other_workspaces():
    at=app()
    for mode in ['页码索引','版本比较','术语分布','覆盖清单','审核与资料']:
        at.sidebar.radio[0].set_value(mode).run(timeout=30)
        assert not at.exception,mode
    assert at.metric[1].value=='0'


def test_page_index_query():
    at=app()
    at.sidebar.radio[0].set_value('页码索引').run()
    at.toggle(key='advanced_pages').set_value(True).run()
    at.selectbox(key='mapping_source').select('zh_collected').run()
    at.text_input(key='mapping_value').input('267').run()
    assert not at.exception
    assert any('PDF 第 292 页' in x.value for x in at.success)


def test_many_to_many_ui_and_missing_translation(monkeypatch):
    from paris.corpus import load_corpus
    sample=copy.deepcopy(load_corpus())
    first=sample['alignments'][0]
    first['de_ids']+=sample['alignments'][1]['de_ids']
    first['zh_ids']+=sample['alignments'][1]['zh_ids']
    monkeypatch.setattr('paris.corpus.load_corpus',lambda: sample)
    at=app()
    assert any('2 个德文单元 / 2 个中文单元' in x.value for x in at.caption)
    first['zh_ids']=[]
    at.run()
    assert any('中文尚未收录' in x.value for x in at.info)


def test_missing_pdf_has_a_readable_message(monkeypatch):
    def missing(*args):
        raise FileNotFoundError('尚未配置本地PDF')
    monkeypatch.setattr('paris.pages.render_page',missing)
    at=app()
    next(b for b in at.button if b.key.startswith('read_')).click().run()
    assert not at.exception
    assert any('尚未配置本地PDF' in x.value for x in at.info)


def test_two_original_pages_remain_open_after_rerun(monkeypatch):
    # Simulate unavailable PDFs: persistence is independent of the renderer.
    monkeypatch.setattr('paris.pages.render_page',lambda *args: (_ for _ in ()).throw(FileNotFoundError('测试原页')))
    at=app()
    next(b for b in at.button if b.key.startswith('read_')).click().run()
    [b for b in at.button if b.key.startswith('read_')][1].click().run()
    assert len([x for x in at.info if x.value=='测试原页'])==2
    at.sidebar.checkbox[0].check().run()
    assert len([x for x in at.info if x.value=='测试原页'])==2
    next(b for b in at.button if b.key.startswith('read_')).click().run()
    assert len([x for x in at.info if x.value=='测试原页'])==1
    assert not at.exception


def test_verified_alignment_keeps_transcription_issue_visible(monkeypatch):
    from paris.corpus import load_corpus,index
    from paris.reviews import fingerprint
    data=load_corpus()
    alignment=index(data['alignments'])['mill_004']
    record=dict(status='manually_verified',reviewer='test',note='字形待查',fingerprint=fingerprint(data,alignment))
    monkeypatch.setattr('paris.reviews.load_reviews',lambda: {'mill_004':record})
    at=app()
    at.sidebar.selectbox[0].select('mill').run()
    at.sidebar.selectbox[1].select('reading-mill_004').run()
    assert at.metric[1].value=='1'
    assert any('转录疑点' in w.value for w in at.warning)
    assert any('字形待查' in c.value for c in at.caption)
    assert not at.exception


def test_semantic_literal_mark_and_filter():
    at=app()
    at.sidebar.selectbox[0].select('mill').run()
    at.sidebar.checkbox[2].check().run()
    at.sidebar.selectbox[1].select('reading-mill_010').run()
    assert any('语义存疑 · 按底本照录：trete' in w.value for w in at.warning)
    assert any('editorial-mark' in m.value and '>trete</span>' in m.value for m in at.markdown)
    at.sidebar.text_input[0].input('trete').run()
    assert any('<mark>trete</mark></span>' in m.value for m in at.markdown)
    at.sidebar.selectbox[0].select('alienation').run()
    assert any('没有命中' in i.value for i in at.info)
    assert not at.exception

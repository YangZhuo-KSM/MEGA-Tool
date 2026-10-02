import copy
from pathlib import Path

from paris.corpus import load_corpus,validate
from paris.pages import lookup_pages,missing_pages,alignments_on_page,page_label
from streamlit.testing.v1 import AppTest
APP=str(Path(__file__).resolve().parents[1]/'app.py')


def test_unnumbered_and_duplicate_printed_labels():
    d=load_corpus()
    d['page_map'] += [dict(source_id='de_megai2',printed_page=None,pdf_page=1,page_kind='illustration',note='合成测试夹具：无编号插图'),
                      dict(source_id='de_megai2',printed_page='364',pdf_page=2)]
    assert not validate(d)
    assert len(lookup_pages(d,'de_megai2','364'))==2
    assert page_label(lookup_pages(d,'de_megai2','001','pdf_page')[0])=='无印刷页码'
    assert lookup_pages(d,'de_megai2','None')==[]
    assert lookup_pages(d,'de_megai2','1.5','pdf_page')==[]


def test_missing_is_not_unindexed_and_never_has_a_pdf_page():
    d=load_corpus()
    d['missing_pages']=[dict(source_id='de_megai2',printed_page='999',pdf_page=None,status='confirmed_missing',
        evidence='合成夹具，不是实际底本缺页结论',note='仅验证软件行为')]
    assert not validate(d)
    assert missing_pages(d,'de_megai2','999')
    assert not missing_pages(d,'de_megai2','998')
    assert not lookup_pages(d,'de_megai2','999')
    d['missing_pages'][0]['printed_page']='364'
    assert any('同时标为存在和缺失' in e for e in validate(d))


def test_cross_page_links_both_sides():
    d=load_corpus()
    for sid,pages in [('de_megai2',[364,365]),('zh_collected',[292,293])]:
        for page in pages:
            assert 'alienation_006' in [a['id'] for a in alignments_on_page(d,sid,page)]


def test_page_to_reader_jump_clears_previous_filters(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda: {})
    at=AppTest.from_file(APP).run()
    at.sidebar.selectbox[0].select('mill').run()
    at.sidebar.text_input[0].input('trete').run()
    at.sidebar.checkbox[2].check().run()
    at.sidebar.radio[0].set_value('页码索引').run()
    at.toggle(key='advanced_pages').set_value(True).run()
    at.selectbox(key='mapping_source').select('zh_collected').run()
    at.text_input(key='mapping_value').input('267').run()
    next(b for b in at.button if b.label=='打开对读：劳动的对象化').click().run()
    assert not at.exception
    assert at.sidebar.radio[0].value=='德中对读'
    assert at.sidebar.selectbox[0].value=='alienation'
    assert at.sidebar.selectbox[1].value=='reading-alienation_004'
    assert at.session_state['reading_focus']['alignment_id']=='alienation_006'
    assert at.sidebar.text_input[0].value==''
    assert not at.sidebar.checkbox[2].value


def test_missing_page_ui_has_no_preview(monkeypatch):
    d=copy.deepcopy(load_corpus())
    d['missing_pages']=[dict(source_id='de_megai2',printed_page='999',pdf_page=None,status='confirmed_missing',evidence='synthetic',note='测试')]
    monkeypatch.setattr('paris.corpus.load_corpus',lambda:d)
    monkeypatch.setattr('paris.reviews.load_reviews',lambda: {})
    at=AppTest.from_file(APP).run()
    at.sidebar.radio[0].set_value('页码索引').run()
    at.toggle(key='advanced_pages').set_value(True).run()
    at.text_input(key='mapping_value').input('999').run()
    assert any('已确认缺页' in w.value for w in at.warning)
    assert not at.success
    assert not any(b.key.startswith('index_') for b in at.button)
    assert not at.exception

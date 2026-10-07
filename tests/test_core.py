import copy
import json

import pytest

from paris.corpus import load_corpus,validate,index,aligned_units,context_units
from paris.search import normalize,find_spans,highlighted_html
from paris.pages import lookup_pages,units_on_page,resolve_source
from paris.compare import compare_texts,diff_html
from paris.stats import term_distribution
from paris.reviews import save_review,load_reviews,review_state


@pytest.fixture
def data():
    return load_corpus()


def test_curated_data_integrity(data):
    assert not validate(data)
    assert len(data['alignments'])==84
    assert len([a for a in data['alignments'] if a['section_id']=='mill'])==12
    assert all(a['status']=='uncertain' and not a['verified_by'] for a in data['alignments'])
    assert {a['review_batch'] for a in data['alignments']}==set(range(1,13))


@pytest.mark.parametrize('text,query,expected',[
    ('Straße STRASSE','strasse',[(0,6),(7,14)]),
    ('Äußerung','a\u0308usserung',[(0,8)]),
    ('A\u0308ußerung','äusserung',[(0,9)]),
    ('Arbeit\n   und\tCapital','arbeit und',[(0,13)]),
    ('Wesen Wesenheit','Wesen',[(0,5),(6,11)]),
    ('ß','s',[(0,1)]),
    ('Arbeit',' ',[]),
    ('Arbeit','不存在',[]),
])
def test_search_original_positions(text,query,expected):
    assert find_spans(text,query)==expected


def test_literal_case_and_whole_word():
    assert find_spans('Arbeit arbeiter Arbeit','Arbeit',True,True)==[(0,6),(16,22)]
    assert find_spans('Arbeit','arbeit',True)==[]
    assert find_spans('a.b a?b','a.b')==[(0,3)]


def test_html_is_escaped():
    rendered=highlighted_html('<script>&Straße',[(9,15)])
    assert '<script>' not in rendered
    assert '&lt;script&gt;&amp;' in rendered
    assert '<mark>Straße</mark>' in rendered


@pytest.mark.parametrize('fault',['duplicate','orphan','page','language','verification','page_map'])
def test_invalid_corpus_is_rejected(data,fault):
    if fault=='duplicate': data['units'].append(copy.deepcopy(data['units'][0]))
    if fault=='orphan': data['alignments'][0]['de_ids']=['missing']
    if fault=='page': data['units'][0]['locations'][0]['pdf_page']=0
    if fault=='language': data['alignments'][0]['de_ids']=data['alignments'][0]['zh_ids'][:]
    if fault=='verification': data['alignments'][0]['status']='manually_verified'
    if fault=='page_map': data['units'][0]['locations'][0]['printed_page']='999'
    assert validate(data)


@pytest.mark.parametrize('de_count,zh_count',[(1,2),(2,1),(2,2),(1,0)])
def test_alignment_cardinality(data,de_count,zh_count):
    a=data['alignments'][0]
    a['de_ids']=[f'alienation_de_{i:03}' for i in range(1,de_count+1)]
    a['zh_ids']=[f'alienation_zh_{i:03}' for i in range(1,zh_count+1)]
    assert not validate(data)
    de,zh=aligned_units(data,a)
    assert (len(de),len(zh))==(de_count,zh_count)


def test_exact_page_mapping_and_cross_page(data):
    assert lookup_pages(data,'zh_collected','267')[0]['pdf_page']==292
    assert lookup_pages(data,'zh_collected','292','pdf_page')[0]['printed_page']=='267'
    assert lookup_pages(data,'zh_collected','999')==[]
    u=index(data['units'])['alienation_de_006']
    assert len(u['locations'])==2
    assert u in units_on_page(data,'de_megai2',364)
    assert u in units_on_page(data,'de_megai2',365)
    data['page_map'].append(dict(source_id='de_megai2',printed_page='XI*',pdf_page=8))
    assert lookup_pages(data,'de_megai2','XI*')[0]['pdf_page']==8


def test_context_is_same_edition_and_section(data):
    u=index(data['units'])['mill_de_001']
    before,after=context_units(data,u)
    assert before is None
    assert after['id']=='mill_de_002'


def test_pdf_unavailable_or_wrong_file(tmp_path,data):
    source=data['sources'][0]
    with pytest.raises(FileNotFoundError):
        resolve_source(source,tmp_path)
    (tmp_path/'Asset_by_user').mkdir()
    (tmp_path/'Asset_by_user'/source['file_name']).write_bytes(b'not the source')
    with pytest.raises(ValueError,match='文件不同'):
        resolve_source(source,tmp_path)


@pytest.mark.parametrize('left,right,lang',[('劳动是生命。','劳动是自由生命。','zh'),('freie Arbeit','entfremdete Arbeit','de'),('gleich','gleich','de'),('<script>','&','zh')])
def test_diff_reconstructs_inputs(left,right,lang):
    changes=compare_texts(left,right,lang)
    assert ''.join(c['left'] for c in changes)==left
    assert ''.join(c['right'] for c in changes)==right
    assert '<script>' not in diff_html(changes,'left')


def test_statistics_are_auditable(data):
    primary=[u for u in data['units'] if u['language']=='de' and u.get('role','primary')=='primary']
    counts,hits=term_distribution(primary,'Arbeit')
    assert sum(counts.values())==sum(h['count'] for h in hits)
    assert sum(counts.values())==sum(u['text'].casefold().count('arbeit') for u in primary)
    assert not any(h['unit'].get('role')=='comparison' for h in hits)


def test_review_is_persistent_and_invalidated_by_edits(tmp_path,data):
    path=tmp_path/'reviews.json'
    a=data['alignments'][0]
    assert review_state(data,a,{})[0]=='uncertain'
    with pytest.raises(ValueError): save_review(data,a,'','',path=path)
    save_review(data,a,'测试核验人','仅测试夹具',path=path)
    reviews=load_reviews(path)
    assert review_state(data,a,reviews)[0]=='manually_verified'
    index(data['units'])[a['de_ids'][0]]['text']+='修改'
    assert review_state(data,a,reviews)[0]=='stale'
    save_review(data,a,'测试核验人','修订待审',status='uncertain',path=path)
    assert load_reviews(path)[a['id']]['history'][0]['status']=='manually_verified'


def test_comparison_samples(data):
    assert len(data['comparisons'])>=10
    assert {c['kind'] for c in data['comparisons']}=={'edition','presentation'}


def test_legacy_review_requires_matching_baseline(data):
    from paris.reviews import fingerprint,upgrade_legacy_record
    baseline=copy.deepcopy(data)
    a=data['alignments'][0]
    old=dict(status='manually_verified',reviewer='test',note='retain',reviewed_at='2026-10-01',
             fingerprint=fingerprint(data,a,version=1),history=[])
    migrated=upgrade_legacy_record(data,a,old,baseline)
    assert review_state(data,a,{a['id']:migrated})[0]=='manually_verified'
    assert migrated['reviewed_at']==old['reviewed_at'] and migrated['note']=='retain'
    assert migrated['history'][-1]['fingerprint']==old['fingerprint']
    assert old['history']==[]
    for table,key in [('sources','sha256'),('editions','year'),('units','text')]:
        changed=copy.deepcopy(data)
        changed[table][0][key]=str(changed[table][0][key])+'changed'
        with pytest.raises(ValueError): upgrade_legacy_record(changed,a,old,baseline)


def test_editorial_mark_overlap_escape_and_stale_anchor(data):
    from paris.annotations import annotated_html
    text='<trete>'
    issue={'text_anchor':{'start':1,'end':6,'quote':'trete'},'note':'"<unsafe>'}
    result=annotated_html(text,[(2,5)],[issue])
    assert '<mark>ret</mark>' in result
    assert '&lt;' in result and '&quot;&lt;unsafe&gt;' in result
    assert '<unsafe>' not in result
    issue['text_anchor']['quote']='other'
    assert 'editorial-mark' not in annotated_html(text,[],[issue])
    i=next(i for i in data['editorial_issues'] if i['id']=='mill-011-trete')
    i['text_anchor']['start']+=1
    assert any('转录标注位置已失效' in error for error in validate(data))

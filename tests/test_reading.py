import copy
import pytest

from paris.corpus import load_corpus,index
from paris.reading import reading_pages,page_for_alignment,page_units,group_height
from paris.citations import reference,format_pages,mapped_locations,reading_page_sources
from paris.locator import locate,snippets
from paris.clipboard import copy_button_html


def test_pages_multiple_groups_source_order_and_no_mutation():
    data=load_corpus()
    original=copy.deepcopy(data)
    pages=reading_pages(data,'alienation')
    assert any(len(p['alignment_ids'])>1 for p in pages)
    assert [aid for p in pages for aid in p['alignment_ids']]==[a['id'] for a in data['alignments'] if a['section_id']=='alienation']
    assert data==original


@pytest.mark.parametrize('de,zh',[(1,2),(2,1),(2,2)])
def test_group_cardinality_and_oversized_group_never_split(de,zh):
    data=load_corpus()
    first=data['alignments'][0]
    first['de_ids']=[f'alienation_de_{i:03}' for i in range(1,de+1)]
    first['zh_ids']=[f'alienation_zh_{i:03}' for i in range(1,zh+1)]
    pages=reading_pages(data,'alienation',budget=1)
    page=pages[0]
    assert page['alignment_ids']==[first['id']]
    assert len(page_units(data,page,'de'))==de
    assert len(page_units(data,page,'zh'))==zh
    assert sum(first['id'] in p['alignment_ids'] for p in pages)==1


def test_pagination_uses_both_columns_length_and_paragraphs():
    data=load_corpus(); units=index(data['units']); group=data['alignments'][0]
    old=group_height(group,units)
    units[group['zh_ids'][0]]['text']='中'*3000
    assert group_height(group,units)>old
    assert reading_pages(data,'alienation')[0]['alignment_ids']==[group['id']]
    units[group['zh_ids'][0]]['text']='\n'.join('中' for _ in range(100))
    assert group_height(group,units)>old


def test_reading_page_aggregates_both_printed_page_ranges():
    data=load_corpus(); page=page_for_alignment(data,'alienation_006')
    assert reading_page_sources(data,page_units(data,page,'de'))==['MEGA² I/2 · S. 364–365']
    assert reading_page_sources(data,page_units(data,page,'zh'))==['《马克思恩格斯全集》第3卷 · 第267—268页']


@pytest.mark.parametrize('query,uid,printed,pdf',[
    ('Vergegenständlichung','alienation_de_006',['364','365'],[364,365]),
    ('对象化','alienation_zh_006',['267','268'],[292,293]),
    ('trete','mill_de_011',['466'],[458]),
])
def test_text_locator_exact_source_pages(query,uid,printed,pdf):
    hit=next(h for h in locate(load_corpus(),query) if h['unit']['id']==uid)
    assert [p['printed_page'] for p in hit['reference']['locations']]==printed
    assert [p['pdf_page'] for p in hit['reference']['locations']]==pdf
    assert hit['targets']


def test_long_text_and_multiple_candidates_with_context():
    data=load_corpus(); u=index(data['units'])['mill_de_002']
    hits=locate(data,'  '+u['text'][20:250].replace(' ','\n  ')+' ')
    assert u['id'] in [h['unit']['id'] for h in hits]
    assert len(locate(data,'Arbeit'))>3
    for h in locate(data,'Arbeit'):
        assert '<mark>' in ''.join(snippets(h['unit']['text'],h['spans']))
    assert locate(data,'not-in-this-corpus-123')==[]


def test_comparison_results_use_explicit_bridge_and_keep_their_own_citation():
    data=load_corpus()
    hit=next(h for h in locate(data,'对象化') if h['unit']['id']=='alienation_zh_single_006')
    assert hit['targets'][0]['via_comparison']
    assert hit['targets'][0]['alignment_id']=='alienation_006'
    assert '2000年版' in hit['reference']['plain']
    assert all(p['source_id']=='zh_single' for p in hit['reference']['locations'])


@pytest.mark.parametrize('source,page,expected',[
    ('de_megai2_first','236','Marx: *Marx－Engels－Gesamtausgabe (MEGA²)*, Ⅰ/2, Berlin: Dietz Verlag, 1982. S.236.'),
    ('de_megaiv2','447','Marx: *Marx－Engels－Gesamtausgabe (MEGA²)*, Ⅳ/2, Berlin: Dietz Verlag, 1982. S.447.'),
    ('zh_single','164','马克思：《1844年经济学哲学手稿》，北京：人民出版社2000年版，第164页。'),
    ('zh_collected','268','《马克思恩格斯全集》第3卷，北京：人民出版社2002年，第268页。'),
])
def test_fixed_citation_templates(source,page,expected):
    data=load_corpus(); edition=index(data['editions'])[source]
    loc=dict(source_id=edition['source_id'],printed_page=page,pdf_page=20,status='scan_checked_ai')
    data['page_map'].append(loc)  # synthetic citation fixture, no corpus write
    unit=dict(edition_id=source,locations=[loc])
    ref=reference(data,unit)
    assert ref['markdown']==expected
    assert 'PDF' not in ref['plain']
    if source=='de_megaiv2':
        assert '1981' in ref['notes'][0] and edition['year']==1981
    if source=='zh_single':
        assert '尚未独立核验' in ref['notes'][0]
        assert edition['metadata_status']=='user_provided; title_image_checked'


def test_ranges_nonconsecutive_special_and_repeated_labels():
    assert format_pages(['236','237','239','239','XI*'])=='236–237, 239, XI*'
    assert format_pages(['268','269','271'],'zh')=='268—269、271'
    assert format_pages(['09','10','XI','XII','12*','13*'])=='09, 10, XI, XII, 12*, 13*'
    data=load_corpus(); u=copy.deepcopy(index(data['units'])['alienation_zh_006'])
    duplicate=dict(source_id='zh_collected',printed_page='267',pdf_page=21)
    data['page_map'].append(duplicate); u['locations'].append(duplicate)
    assert [p['pdf_page'] for p in mapped_locations(data,u)]==[292,293,21]
    assert reference(data,u)['plain'].endswith('第267—268页。')
    assert '292' not in reference(data,u)['plain']


def test_unknown_or_partial_mapping_never_invents_citation():
    data=load_corpus(); u=copy.deepcopy(index(data['units'])['alienation_zh_006'])
    data['page_map']=[p for p in data['page_map'] if not (p['source_id']=='zh_collected' and p['pdf_page']==293)]
    assert reference(data,u)['markdown']==''
    assert '定位未完整' in reference(data,u)['short']
    u['locations']=[]
    assert reference(data,u)['markdown']==''


def test_same_page_number_uses_source_binding():
    data=load_corpus()
    refs=[]
    for eid in ['de_megai2','zh_collected']:
        loc=dict(source_id=eid,printed_page='236',pdf_page=22)
        data['page_map'].append(loc)
        refs.append(reference(data,dict(edition_id=eid,locations=[loc]))['plain'])
    assert 'Ⅰ/2' in refs[0] and '第3卷' in refs[1]


def test_clipboard_payload_cannot_inject_script():
    result=copy_button_html('</script><script>alert(1)</script>')
    assert '</script><script>' not in result
    assert 'writeText(payload.plain)' in result and '复制引用' in result

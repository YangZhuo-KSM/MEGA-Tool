"""New chapter registration and real cross-page research workflow."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
from paris.corpus import load_corpus,index
from paris.coverage import load_plan,coverage_rows
from paris.locator import locate
from paris.reading import reading_pages,page_for_alignment
from paris.sampling import load_plan as sampling_plan


def test_new_chapter_registration_cross_page_and_frozen_sampling():
    data=load_corpus(); units=index(data['units'])
    batch=[a for a in data['alignments'] if a['review_batch']==10]
    assert len(batch)==6 and all(a['section_id']=='communism' and a['status']=='uncertain' for a in batch)
    row=next(r for r in coverage_rows(data,{},load_plan(data)) if r['id']=='communism')
    assert row['groups']==30 and row['state']=='部分收录' and row['collected_ratio'] is None
    assert units['communism_zh_004']['locations']==[
        dict(source_id='zh_collected',pdf_page=319,printed_page='294'),
        dict(source_id='zh_collected',pdf_page=320,printed_page='295')]
    assert units['communism_zh_004']['text'].endswith('状况。①')
    assert '||' in units['communism_de_006']['text']
    assert units['communism_de_006']['text'].endswith(';')
    pages=reading_pages(data,'communism')
    assert [aid for p in pages for aid in p['alignment_ids']]==[
        a['id'] for a in data['alignments'] if a['section_id']=='communism']
    # Frozen alpha5 suggestions are a regression baseline, independent of local backups.
    old_ids=['private_relation_001','private_relation_005','private_relation_006',
             'private_work_006','private_work_008','private_work_009','private_work_010',
             'private_work_011','private_work_015','private_work_016','private_work_018',
             'private_work_019','private_work_020','private_work_023']
    assert [r['alignment_id'] for r in sampling_plan(data)['recommended'][:14]]==old_ids


def test_new_chapter_search_originals_and_reader(monkeypatch):
    data=load_corpus()
    hit=next(h for h in locate(data,'改善工人状况','zh_collected') if h['unit']['id']=='communism_zh_004')
    assert '294—295' in hit['reference']['plain']
    assert hit['targets'][0]['alignment_id']=='communism_004'
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    calls=[]
    def preview(source,page):
        calls.append((source['id'],page))
        raise FileNotFoundError('测试预览')
    monkeypatch.setattr('paris.pages.render_page',preview)
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('覆盖清单').run()
    app.button(key='coverage_communism').click().run()
    assert app.sidebar.selectbox(key='section_id').value=='communism'
    assert any('无产和有产' in x.value for x in app.markdown)
    app.sidebar.radio(key='workspace').set_value('页码索引').run()
    app.selectbox(key='locator_source').select('zh_collected').run()
    app.text_area(key='locator_query').input('改善工人状况').run()
    for page in [319,320]:
        app.button(key=f'result_communism_zh_004_{page}').click().run()
    assert set(calls)=={('zh_collected',319),('zh_collected',320)}
    app.button(key='locate_communism_zh_004_communism_004').click().run()
    assert app.sidebar.selectbox(key='reading_page').value==page_for_alignment(data,'communism_004')['id']
    assert any('<mark>改善工人状况</mark>' in x.value for x in app.markdown)
    assert not app.exception


def test_eleventh_batch_dual_cross_page_and_marker_evidence():
    data=load_corpus(); units=index(data['units'])
    batch=[a for a in data['alignments'] if a['review_batch']==11]
    assert len(batch)==6 and all(a['status']=='uncertain' for a in batch)
    de=units['communism_de_011']; zh=units['communism_zh_011']
    assert [p['pdf_page'] for p in de['locations']]==[387,388]
    assert [p['printed_page'] for p in zh['locations']]==['295','296']
    assert 'Nivellirung' in de['text'] and 'Ni-vellirung' not in de['text']
    assert '共产主义②' in zh['text'] and zh['text'].endswith('⁹⁷')
    issue=next(i for i in data['editorial_issues'] if i['unit_id']==de['id'])
    assert issue['status']=='open' and issue['evidence_pages']==['de_megai2:388']
    anchor=issue['text_anchor']; assert de['text'][anchor['start']:anchor['end']]==anchor['quote']=='||IV|'
    for query,source,uid,page_range in [('Vollendung dieses Neides','de_megai2',de['id'],'387–388'),
        ('粗陋的共产主义','zh_collected',zh['id'],'295—296')]:
        hit=next(h for h in locate(data,query,source) if h['unit']['id']==uid)
        assert page_range in hit['reference']['plain']
        assert hit['targets'][0]['alignment_id']=='communism_011'
    plan=sampling_plan(data)
    assert any(r['alignment_id']=='communism_011' and '未解决疑点：定向核查' in r['reasons'] for r in plan['recommended'])


def test_large_batch_and_real_inserted_pages_are_distinct():
    from paris.pages import lookup_pages, units_on_page, missing_pages
    data=load_corpus(); units=index(data['units'])
    batch=[a for a in data['alignments'] if a['review_batch']==12]
    assert len(batch)==18 and all(a['status']=='uncertain' for a in batch)
    assert [a['id'] for a in batch]==[f'communism_{n:03}' for n in range(13,31)]
    assert [p['pdf_page'] for p in units['communism_zh_029']['locations']]==[323,326]
    illustration=lookup_pages(data,'zh_collected',324,'pdf_page')[0]
    blank=lookup_pages(data,'zh_collected',325,'pdf_page')[0]
    assert illustration['page_kind']=='illustration' and illustration['printed_page'] is None
    assert blank['page_kind']=='blank' and blank['printed_page'] is None
    assert lookup_pages(data,'zh_collected','301')[0]['pdf_page']==326
    for label in ['299','300']:
        assert not lookup_pages(data,'zh_collected',label) and not missing_pages(data,'zh_collected',label)
    assert not units_on_page(data,'zh_collected',324) and not units_on_page(data,'zh_collected',325)
    pages=reading_pages(data,'communism')
    assert len(pages)<30 and len({aid for p in pages for aid in p['alignment_ids']})==30
    for uid,word in [('communism_de_016','menschlichenresen'),('communism_de_027','Wtkung'),
                     ('communism_de_029','geschichthche'),('communism_de_030','Existenzweisenachgesellschaftliche')]:
        issue=next(i for i in data['editorial_issues'] if i['unit_id']==uid and i['current_reading']==word)
        anchor=issue['text_anchor']
        assert units[uid]['text'][anchor['start']:anchor['end']]==word
        assert issue['status']=='retained_as_source'
    plan=sampling_plan(data)
    assert any(r['alignment_id']=='communism_029' and '跨插页正文：定向核查' in r['reasons'] for r in plan['recommended'])


def test_search_across_inserted_pages_opens_only_actual_text_pages(monkeypatch):
    data=load_corpus()
    hit=next(h for h in locate(data,'既是运动的结果，又是运动的出发点','zh_collected')
             if h['unit']['id']=='communism_zh_029')
    assert '第298、301页' in hit['reference']['plain']
    assert '298—301' not in hit['reference']['plain']
    calls=[]
    def preview(source,page):
        calls.append((source['id'],page))
        raise FileNotFoundError('测试预览')
    monkeypatch.setattr('paris.pages.render_page',preview)
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('页码索引').run()
    app.selectbox(key='locator_source').select('zh_collected').run()
    app.text_area(key='locator_query').input('既是运动的结果，又是运动的出发点').run()
    for page in [323,326]:
        app.button(key=f'result_communism_zh_029_{page}').click().run()
    assert set(calls)=={('zh_collected',323),('zh_collected',326)}
    assert not any('PDF第' in x.value for x in app.markdown)
    app.button(key='locate_communism_zh_029_communism_029').click().run()
    assert app.sidebar.selectbox(key='reading_page').value==page_for_alignment(data,'communism_029')['id']
    assert any('<mark>既是运动的结果，又是运动的出发点</mark>' in x.value for x in app.markdown)
    assert not app.exception


def test_large_batch_review_forms_and_sample_filter(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('审核与资料').run()
    app.selectbox[0].select(12).run()
    assert len(app.get('form'))==18 and not app.exception
    app.toggle(key='sampled_only').set_value(True).run()
    assert len(app.get('form'))==6 and not app.exception

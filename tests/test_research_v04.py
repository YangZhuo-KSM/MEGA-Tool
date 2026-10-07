import copy
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

from paris.corpus import load_corpus,index,validate
from paris.coverage import load_plan,coverage_rows
from paris.stats import research_distribution
from paris.reviews import fingerprint


def test_coverage_has_all_four_works_without_fabricated_full_denominator():
    data=load_corpus(); plan=load_plan(data); rows=coverage_rows(data,{},plan)
    assert {r['work'] for r in rows}=={'manuscript1','manuscript2','manuscript3','mill'}
    assert len(rows)==14 and sum(r['groups']>0 for r in rows)==5
    assert sum(r['groups'] for r in rows)==84
    assert sum(r['units'] for r in rows)==168
    assert all(r['collected_ratio'] is None for r in rows)
    assert next(r for r in rows if r['id']=='wages')['checked_ratio'] is None
    assert next(r for r in rows if r['id']=='private_work')['confirmed_ratio']==0


def test_coverage_uses_live_review_fingerprints_and_separate_proofreading():
    data=load_corpus(); a=data['alignments'][0]
    reviews={a['id']:dict(status='manually_verified',reviewer='fixture',fingerprint=fingerprint(data,a))}
    row=next(r for r in coverage_rows(data,reviews,load_plan(data)) if r['id']=='alienation')
    assert row['confirmed']==1 and row['checked_ratio']==1
    index(data['units'])[a['de_ids'][0]]['text']+='changed'
    assert next(r for r in coverage_rows(data,reviews,load_plan(data)) if r['id']=='alienation')['confirmed']==0


def test_invalid_coverage_plan_rejected(tmp_path):
    import json
    data=load_corpus(); plan=load_plan(data)
    plan['items'][0]['section_ids']=['alienation']
    path=tmp_path/'plan.json'; path.write_text(json.dumps(plan),encoding='utf-8')
    with pytest.raises(ValueError,match='重复'): load_plan(data,path)


def test_new_batch_is_pending_and_has_exact_reviewed_locations():
    data=load_corpus(); new=[a for a in data['alignments'] if a['review_batch']==5]
    assert len(new)==6 and all(a['status']=='uncertain' and a['verified_by'] is None for a in new)
    assert not validate(data)
    units=index(data['units'])
    for a in new:
        second=a['section_id']=='private_relation'
        de=units[a['de_ids'][0]]; zh=units[a['zh_ids'][0]]
        assert de['locations'][0]['printed_page']==('376' if second else '383')
        assert zh['locations'][0]==dict(source_id='zh_collected',printed_page='281' if second else '289',pdf_page=306 if second else 314)
        assert de['proofread_status']==zh['proofread_status']=='scan_checked_ai'
        assert '句群' in zh['transcription_note']


def test_scoped_multiterm_counts_reproduce_rows_and_do_not_count_comparison_copies():
    data=load_corpus()
    report=research_distribution(data,{},['Arbeit','Capital','Arbeit'],'de',section_ids=['private_relation'])
    assert report['scope']['queries']==['Arbeit','Capital'] and report['scope']['units']==6
    for summary in report['summary']:
        assert summary['count']==sum(h['count'] for h in report['hits'] if h['query']==summary['query'])
    assert all(h['section_id']=='private_relation' and h['edition_id']=='de_megai2' for h in report['hits'])
    assert all('S.376.' in h['citation'] for h in report['hits'])
    assert all(h['review_states']==['uncertain'] for h in report['hits'])


def test_chinese_statistics_whole_word_option_does_not_erase_substrings():
    data=load_corpus()
    report=research_distribution(data,{},['私有财产'],'zh',section_ids=['private_work'],whole_word=True)
    assert report['hits'] and report['scope']['units']==24
    assert all('第289' in h['citation'] or '第290' in h['citation'] or '第291页' in h['citation'] or '第292页' in h['citation'] or '第293页' in h['citation'] for h in report['hits'])
    assert all(len(h['spans'])==h['count'] for h in report['hits'])


def test_confirmed_filter_rejects_stale_and_comparison_proxies():
    data=load_corpus(); a=data['alignments'][0]
    reviews={a['id']:dict(status='manually_verified',reviewer='fixture',fingerprint=fingerprint(data,a))}
    report=research_distribution(data,reviews,['国民经济学'],'zh',primary_only=False,confirmed_only=True)
    assert report['scope']['units']==1
    assert all(h['unit_id']==a['zh_ids'][0] for h in report['hits'])
    reviews[a['id']]['fingerprint']='stale'
    assert research_distribution(data,reviews,['国民经济学'],'zh',confirmed_only=True)['scope']['units']==0


def test_empty_scope_and_unknown_term_export_are_explicit():
    d=load_corpus()
    r=research_distribution(d,{},['missing'],edition_ids=[])
    assert r['scope']['units']==0 and not r['hits']
    assert all(x['count']==0 for x in r['summary'])


def test_research_workspaces_and_new_sample_jump(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('覆盖清单').run()
    assert not app.exception
    assert any(m.value=='5/14' for m in app.metric)
    app.button(key='coverage_private_work').click().run()
    assert app.sidebar.selectbox(key='section_id').value=='private_work'
    assert any('主体本质' in m.value for m in app.markdown)
    app.sidebar.radio(key='workspace').set_value('术语分布').run()
    app.selectbox(key='stats_language').select('zh').run()
    app.multiselect(key='stats_sections').set_value(['private_work']).run()
    app.text_area(key='stats_queries_zh').input('私有财产\n劳动').run()
    assert not app.exception
    assert any('24 个文本单元，2 项独立查询' in c.value for c in app.caption)
    app.checkbox(key='stats_confirmed').check().run()
    assert any('当前范围无命中' in i.value for i in app.info)
    app.sidebar.radio(key='workspace').set_value('审核与资料').run()
    app.selectbox[0].select(5).run()
    assert len(app.get('form'))==6
    assert not app.exception

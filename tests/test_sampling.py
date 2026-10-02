import copy
import json
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
from paris.corpus import load_corpus, index
from paris.sampling import build_plan, load_plan
from paris.reviews import save_review, load_reviews, review_state


def test_sample_has_strata_and_risks_without_changing_confirmations(tmp_path):
    data=load_corpus(); before=copy.deepcopy(data); plan=build_plan(data)
    assert plan==build_plan(data) and data==before
    assert len(plan['scope_ids'])==18 and len(plan['recommended'])==8
    selected={r['alignment_id'] for r in plan['recommended']}
    assert {'private_relation_006','private_work_008','private_work_011'}<=selected
    assert len(selected)<len(plan['scope_ids'])
    a=index(data['alignments'])[next(iter(selected))]
    path=tmp_path/'reviews.json'
    save_review(data,a,'test','sample checked',path=path)
    reviews=load_reviews(path)
    assert sum(review_state(data,x,reviews)[0]=='manually_verified' for x in data['alignments'])==1
    assert plan==build_plan(data)


def test_changed_scope_text_or_annotation_invalidates_plan(tmp_path):
    data=load_corpus(); path=tmp_path/'plan.json'
    path.write_text(json.dumps(build_plan(data)),encoding='utf-8')
    assert load_plan(data,path)
    for kind in ['text','issue','scope']:
        modified=copy.deepcopy(data)
        if kind=='text': index(modified['units'])['private_work_de_008']['text']+='x'
        elif kind=='issue': modified['editorial_issues'][-1]['note']+='changed'
        else: modified['alignments'].pop()
        with pytest.raises(ValueError): load_plan(modified,path)


def test_seventh_batch_real_cross_page_and_glyph_pending():
    data=load_corpus(); units=index(data['units'])
    assert [p['pdf_page'] for p in units['private_work_zh_008']['locations']]==[315,316]
    batch=[a for a in data['alignments'] if a['review_batch']==7]
    assert len(batch)==6 and all(a['status']=='uncertain' for a in batch)
    issue=next(i for i in data['editorial_issues'] if i['unit_id']=='private_work_de_011')
    assert issue['status']=='open' and issue['kind']=='glyph_doubt'


def test_sampling_filter_preserves_individual_review_forms(monkeypatch):
    monkeypatch.setattr('paris.reviews.load_reviews',lambda:{})
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio(key='workspace').set_value('审核与资料').run()
    app.selectbox[0].select(7).run()
    assert len(app.get('form'))==6
    app.toggle(key='sampled_only').set_value(True).run()
    assert not app.exception and len(app.get('form'))==4
    assert any('8/18' in x.value for x in app.info)

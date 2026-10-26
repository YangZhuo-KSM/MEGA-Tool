"""Read-only real-appender simulation; the write boundary is intercepted."""
import copy
import hashlib
import json
import runpy
from pathlib import Path
from unittest.mock import patch
import append_v04_batch6 as appender
import append_v04_batch52 as recipe
from paris.corpus import load_corpus, validate
from paris.sampling import load_plan, extend_plan

ROOT=Path(__file__).resolve().parents[1]
FILES=['corpus.json','extraction.json','coverage_plan.json','sampling_plan.json','reviews.json']
def hashes():
    return {n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in FILES}
class BeforeWrite(Exception):
    pass
def main():
    before=load_corpus()
    saved=hashes()
    prior=json.loads((ROOT/'tmp/alpha47-batch51-audit.json').read_text(encoding='utf-8'))
    assert saved==prior['data_sha256']
    assert len(before['alignments'])==1227
    assert {a['review_batch'] for a in before['alignments']}==set(range(1,52))
    assert not (ROOT/'local_backups/v04-before-batch52').exists()
    plan=load_plan(before)
    proposed=[]
    def check(data):
        errors=validate(data)
        if data['release']=='0.4.0-alpha48':
            proposed.append(copy.deepcopy(data))
        return errors
    def stop(*args,**kwargs):
        raise BeforeWrite()
    with patch.object(appender,'validate',side_effect=check),patch.object(Path,'mkdir',side_effect=stop):
        try:
            runpy.run_path(str(ROOT/'scripts/append_v04_batch52.py'),run_name='__main__')
        except BeforeWrite:
            pass
        else:
            raise AssertionError('Appender did not reach guarded write boundary')
    assert len(proposed)==1
    data=proposed[0]
    assert len(data['alignments'])==1236
    ids=[a['id'] for a in data['alignments'][1227:]]
    assert ids==[f'mill_{n:03}' for n in range(252,261)]
    assert [recipe.SEQUENCES[aid] for aid in ids]==list(range(-29858,-29849))
    recipe.extra_assertions(data,{})
    issues=data['editorial_issues'][len(before['editorial_issues']):]
    assert len(issues)==3
    for uid,words in recipe.DOUBTS.items():
        for word in words:
            matches=[i for i in issues if i['unit_id']==uid and i['text_anchor']['quote']==word]
            assert matches,(uid,word)
            assert all(all(i[k]==v for k,v in recipe.OVERRIDES[uid][word].items()) for i in matches)
    proposed_plan=extend_plan(data,plan,'2026-10-24')
    assert proposed_plan['recommended'][:len(plan['recommended'])]==plan['recommended']
    assert hashes()==saved
    report=dict(groups=9,new_issues=len(issues),old_json_unchanged=True,old_sha256=saved,
        appender_protection_and_prewrite_gate=True,explicit_issue_generation=True,
        ids_sequences_anchors_checked=True,
        proposed_sampling=[len(proposed_plan['recommended']),len(proposed_plan['scope_ids'])],
        scan_pages=recipe.SCAN_PAGES,next_start=recipe.NEXT_START,
        plain_review='谋生劳动与异化的四项规定；5页图像核查（含影印插页及旧首组），新增9组，3项开放字形疑点。已接mill_062。',
        ordinary_spot_checks=['mill_253','mill_255','mill_258'],
        cross_page_checks=['mill_259'])
    (ROOT/'tmp/batch52-prewrite-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    main()

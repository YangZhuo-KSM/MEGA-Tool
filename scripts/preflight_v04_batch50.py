"""Read-only batch50 simulation: stop the real appender before backup/write."""
import copy
import hashlib
import json
import runpy
from pathlib import Path
from unittest.mock import patch
import append_v04_batch6 as appender
import append_v04_batch50 as recipe
from paris.corpus import load_corpus, validate
from paris.sampling import load_plan, extend_plan

ROOT = Path(__file__).resolve().parents[1]
FILES = ['corpus.json','extraction.json','coverage_plan.json','sampling_plan.json','reviews.json']

def hashes():
    return {name:hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest() for name in FILES}

class BeforeWrite(Exception):
    pass

def main():
    before = load_corpus()
    saved = hashes()
    previous_audit = json.loads((ROOT/'tmp/alpha45-batch49-audit.json').read_text(encoding='utf-8'))
    assert saved == previous_audit['data_sha256']
    assert len(before['alignments']) == 1179
    assert {a['review_batch'] for a in before['alignments']} == set(range(1,50))
    assert not (ROOT/'local_backups/v04-before-batch50').exists()
    plan = load_plan(before)
    proposed = []
    def check(data):
        errors = validate(data)
        if data['release'] == '0.4.0-alpha46':
            proposed.append(copy.deepcopy(data))
        return errors
    def stop(*args, **kwargs):
        raise BeforeWrite()
    with patch.object(appender, 'validate', side_effect=check), patch.object(Path, 'mkdir', side_effect=stop):
        try:
            runpy.run_path(str(ROOT/'scripts/append_v04_batch50.py'), run_name='__main__')
        except BeforeWrite:
            pass
        else:
            raise AssertionError('Appender did not reach guarded write boundary')
    assert len(proposed) == 1
    data = proposed[0]
    assert len(data['alignments']) == 1203
    ids = [a['id'] for a in data['alignments'][1179:]]
    assert ids == [f'mill_{n:03}' for n in range(204,228)]
    assert [recipe.SEQUENCES[aid] for aid in ids] == list(range(-29906,-29882))
    recipe.extra_assertions(data, {})
    issues = data['editorial_issues'][len(before['editorial_issues']):]
    for uid, words in recipe.DOUBTS.items():
        for word in words:
            matches = [i for i in issues if i['unit_id']==uid and i['text_anchor']['quote']==word]
            assert matches, (uid, word)
            assert all(all(i[k]==v for k,v in recipe.OVERRIDES[uid][word].items()) for i in matches)
    proposed_plan = extend_plan(data, plan, '2026-10-23')
    assert proposed_plan['recommended'][:len(plan['recommended'])] == plan['recommended']
    assert hashes() == saved
    report = dict(groups=24, new_issues=len(issues), old_json_unchanged=True,
                  old_sha256=saved, appender_protection_and_prewrite_gate=True,
                  explicit_issue_generation=True, ids_sequences_anchors_checked=True,
                  proposed_sampling=[len(proposed_plan['recommended']),len(proposed_plan['scope_ids'])],
                  scan_pages=recipe.SCAN_PAGES,next_start=recipe.NEXT_START,
                  plain_review='信用业、银行业及社会交换首句；已核7页图像。保留异常字形和页内界符；中文红色批注线不作正文。',
                  ordinary_spot_checks=['mill_204','mill_213','mill_224'])
    (ROOT/'tmp/batch50-prewrite-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__ == '__main__':
    main()

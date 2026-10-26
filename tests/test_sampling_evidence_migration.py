import copy
import pytest
from paris.corpus import load_corpus, index
from paris.sampling import build_plan, scope_digest
from scripts.repair_sampling_evidence_page import migrate, ISSUE_ID


def fixture_pair():
    current = load_corpus()
    current = dict(current, alignments=[a for a in current['alignments'] if a['id'] == 'profit_049'])
    before = copy.deepcopy(current)
    index(before['editorial_issues'])[ISSUE_ID]['evidence_pages'] = ['de_megai2:342']
    return current, build_plan(before)


def test_one_page_migration_keeps_recommendations_and_corpus():
    data, plan = fixture_pair()
    originals = copy.deepcopy((data, plan))
    fixed = migrate(data, plan)
    assert fixed['scope_digest'] == scope_digest(data, plan['scope_ids'])
    assert fixed['recommended'] == plan['recommended']
    assert {k: v for k, v in fixed.items() if k != 'scope_digest'} == {
        k: v for k, v in plan.items() if k != 'scope_digest'}
    assert (data, plan) == originals
    assert migrate(data, fixed) == fixed


@pytest.mark.parametrize('change', ['text', 'location', 'issue_note', 'wrong_page'])
def test_other_frozen_changes_are_rejected(change):
    data, plan = fixture_pair()
    if change == 'text':
        index(data['units'])['profit_de_049']['text'] += 'changed'
    elif change == 'location':
        index(data['units'])['profit_de_049']['locations'][0]['printed_page'] = 'wrong'
    elif change == 'issue_note':
        index(data['editorial_issues'])[ISSUE_ID]['note'] += 'changed'
    else:
        index(data['editorial_issues'])[ISSUE_ID]['evidence_pages'] = ['de_megai2:344']
    with pytest.raises(ValueError):
        migrate(data, plan)

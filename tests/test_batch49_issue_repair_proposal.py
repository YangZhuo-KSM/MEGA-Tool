import copy

import pytest

from paris.sampling import scope_digest
from scripts.preview_batch49_issue_repair import ISSUE, propose


def fixture():
    data = dict(units=[dict(id='mill_de_184', text='|(Bei jener Compensation',
        evidence_pages=['de_megaiv2:440'], edition_id='de', locations=[])],
        alignments=[dict(id='mill_184', de_ids=['mill_de_184'], zh_ids=[])],
        editions=[dict(id='de', source_id='de_source')],
        sources=[dict(id='de_source')], editorial_issues=[])
    plan = dict(scope_ids=['mill_184'], recommended=[], previous_scope_digest='unchanged')
    plan['scope_digest'] = scope_digest(data, plan['scope_ids'])
    return data, plan


def test_proposal_is_single_append_and_preserves_inputs():
    data, plan = fixture()
    before = copy.deepcopy((data, plan))
    candidate, updated = propose(data, plan)
    assert (data, plan) == before
    assert candidate['editorial_issues'] == [ISSUE]
    assert updated['recommended'] == [dict(alignment_id='mill_184', reasons=['未解决疑点：定向核查'])]
    assert updated['previous_scope_digest'] == 'unchanged'
    candidate['editorial_issues'].pop()
    assert scope_digest(candidate, plan['scope_ids']) == plan['scope_digest']


@pytest.mark.parametrize('change', ['text', 'location', 'issue', 'digest'])
def test_proposal_rejects_unrelated_frozen_changes(change):
    data, plan = fixture()
    if change == 'text':
        data['units'][0]['text'] += 'extra'
    elif change == 'location':
        data['units'][0]['locations'].append(dict(source_id='de', pdf_page=1, printed_page='1'))
    elif change == 'issue':
        data['editorial_issues'].append(copy.deepcopy(ISSUE))
    else:
        plan['scope_digest'] = 'changed'
    with pytest.raises(ValueError, match='Frozen scope'):
        propose(data, plan)


def test_proposal_rejects_already_registered_issue():
    data, plan = fixture()
    data['editorial_issues'].append(copy.deepcopy(ISSUE))
    plan['scope_digest'] = scope_digest(data, plan['scope_ids'])
    with pytest.raises(ValueError, match='already registered'):
        propose(data, plan)

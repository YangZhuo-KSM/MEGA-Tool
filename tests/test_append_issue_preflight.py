import pytest

from scripts.append_v04_batch6 import issue_spans, validate_requested_issues


@pytest.mark.parametrize(('text', 'quote', 'expected'), [
    ('|(Bei jener', '|(', [(0, 2)]),
    ('a|(Bei', '|(', [(1, 3)]),
    ('word words sword word', 'word', [(0, 4), (17, 21)]),
    ('|XXV.|So', '|XXV.|', [(0, 6)]),
    ('a ζ. B', 'ζ.', [(2, 4)]),
    ('foofoo foo', 'foo', [(7, 10)]),
])
def test_literal_issue_edges(text, quote, expected):
    assert list(issue_spans(text, quote)) == expected


def test_empty_quote_rejected():
    with pytest.raises(ValueError, match='empty'):
        list(issue_spans('text', ''))


@pytest.mark.parametrize('uid', ['mill_de_184', 'misspelled_unit'])
def test_prewrite_gate_rejects_missing_or_historical_issue(uid):
    data = {'editorial_issues': [
        {'unit_id': uid, 'text_anchor': {'quote': '|('}}]}
    with pytest.raises(ValueError, match='not generated'):
        validate_requested_issues(data, 1, {uid: ['|(']})


def test_prewrite_gate_accepts_new_issue():
    data = {'editorial_issues': [
        {'unit_id': 'mill_de_184', 'text_anchor': {'quote': '|('}}]}
    validate_requested_issues(data, 0, {'mill_de_184': ['|(']})

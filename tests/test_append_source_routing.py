import pytest

from scripts.append_v04_batch6 import sequence_for_row, sources_for_section


def test_source_route_preserves_historical_default():
    assert sources_for_section('money') == ('de_megai2', 'zh_collected')


def test_source_route_can_select_mill_editions():
    routes = {'mill': ('de_megaiv2', 'zh_single')}
    assert sources_for_section('mill', routes) == ('de_megaiv2', 'zh_single')
    assert sources_for_section('money', routes) == ('de_megai2', 'zh_collected')


@pytest.mark.parametrize('route', ['de_megaiv2', ('de_megaiv2',), ('de_megaiv2', 4)])
def test_source_route_rejects_malformed_pairs(route):
    with pytest.raises(ValueError, match='two source IDs'):
        sources_for_section('mill', {'mill': route})


def test_sequence_override_keeps_id_and_source_order_independent():
    assert sequence_for_row('mill', 62) == 62
    assert sequence_for_row('mill', 62, {'mill_062': -20000}) == -20000


@pytest.mark.parametrize('value', [None, 1.5, 'before', True])
def test_sequence_override_requires_plain_integer(value):
    with pytest.raises(ValueError, match='must be an integer'):
        sequence_for_row('mill', 62, {'mill_062': value})

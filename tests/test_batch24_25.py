"""Regression checks for batches 24-30 and source-order continuity."""
from paris.corpus import index, load_corpus
from paris.reading import reading_pages
from paris.sampling import load_plan


def test_batches_24_through_30_are_fixed_pending_cohorts():
    data = load_corpus()
    for batch in (24, 25, 26, 27, 28, 29, 30):
        group = [a for a in data['alignments'] if a['review_batch'] == batch]
        assert len(group) == 24
        assert all(a['status'] == 'uncertain' and not a['verified_by'] for a in group)
    # Freeze the established cohort; later front fills are audited independently.
    assert sum(a['section_id'] == 'mill' and a['review_batch'] <= 46
               for a in data['alignments']) == 131


def test_front_fill_preserves_ids_but_reads_before_existing_mill_units():
    data = load_corpus()
    units = index(data['units'])
    for offset, number in enumerate(range(62, 110)):
        expected = -20000 + offset
        assert units[f'mill_de_{number:03}']['sequence'] == expected
        assert units[f'mill_zh_{number:03}']['sequence'] == expected
    order = [aid for page in reading_pages(data, 'mill') for aid in page['alignment_ids']]
    prior_ids = {a['id'] for a in data['alignments'] if a['review_batch'] <= 46}
    order = [aid for aid in order if aid in prior_ids]
    assert order[:71] == ([f'mill_{n:03}' for n in range(110, 132)]
                          + [f'mill_{n:03}' for n in range(62, 110)] + ['mill_001'])


def test_batch30_sampling_extension_keeps_prior_recommendations():
    data = load_corpus()
    plan = load_plan(data)
    prior_ids = {a['id'] for a in data['alignments'] if 5 <= a['review_batch'] <= 30}
    assert len(prior_ids) == 708
    assert len([r for r in plan['recommended'] if r['alignment_id'] in prior_ids]) == 251
    assert set(plan['scope_ids']) == {a['id'] for a in data['alignments']
                                     if a['review_batch'] >= plan['first_batch']}


def test_private_relation_batches_27_28_complete_existing_source_order():
    data = load_corpus()
    order = [aid for page in reading_pages(data, 'private_relation')
             for aid in page['alignment_ids']]
    assert order == [f'private_relation_{number:03}' for number in range(1, 55)]

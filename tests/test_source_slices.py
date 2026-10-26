import scripts.source_slices as source_slices


def test_join_page_hyphens_keeps_position_vector_aligned(monkeypatch, tmp_path):
    root = tmp_path
    data = root / 'data'
    cache = root / 'tmp' / 'source_review' / 'de_test'
    data.mkdir(parents=True)
    cache.mkdir(parents=True)
    (data / 'extraction.json').write_text(
        '{"de_test:1":"Nicht-", "de_test:2":"dasein"}', encoding='utf-8')
    monkeypatch.setattr(source_slices, 'ROOT', root)
    text, positions, _ = source_slices.stream(
        'de_test', [(1, 1, 1), (2, 1, 1)], join_page_hyphens=True)
    assert text == 'Nichtdasein'
    assert len(text) == len(positions)
    assert positions == [1] * 5 + [2] * 6

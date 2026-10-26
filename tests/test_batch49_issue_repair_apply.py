"""Exercise real file writes and interrupted two-file recovery on isolated copies."""
import hashlib
import json
from pathlib import Path

import pytest
from scripts import preview_batch49_issue_repair as repair


@pytest.fixture
def isolated(tmp_path):
    original = repair.ROOT / 'local_backups/automation-20261023-111725-batch49-diagnosis/data'
    if not (original/'corpus.json').exists():
        pytest.skip('Local frozen failure snapshot required for exact-hash apply test')
    (tmp_path/'data').mkdir()
    for name, expected in repair.EXPECTED.items():
        raw = (original/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == expected
        (tmp_path/'data'/name).write_bytes(raw)
    return tmp_path, tmp_path/'transaction'


def test_apply_exact_delta_backups_and_repeat_refusal(isolated):
    root, tx = isolated
    report = repair.apply_repair(root, tx)
    assert report['status'] == 'complete'
    for n,h in repair.EXPECTED.items():
        assert hashlib.sha256((tx/n).read_bytes()).hexdigest() == h
    before = json.loads((tx/'corpus.json').read_bytes())
    after = json.loads((root/'data/corpus.json').read_bytes())
    assert after['editorial_issues'].pop() == repair.ISSUE
    assert after == before
    old_plan = json.loads((tx/'sampling_plan.json').read_bytes())
    new_plan = json.loads((root/'data/sampling_plan.json').read_bytes())
    assert new_plan['recommended'].pop()['alignment_id'] == 'mill_184'
    new_plan['scope_digest'] = old_plan['scope_digest']
    assert new_plan == old_plan
    with pytest.raises(ValueError, match='Transaction exists'):
        repair.apply_repair(root, tx)
    with pytest.raises(ValueError, match='already complete'):
        repair.apply_repair(root, tx, resume=True)


def interrupt_after_corpus(root, tx):
    def crash(stage):
        if stage == 'corpus.json:written':
            raise RuntimeError('simulated interruption')
    with pytest.raises(RuntimeError):
        repair.apply_repair(root, tx, checkpoint=crash)
    report = json.loads((tx/'migration.json').read_bytes())
    assert report['states']['corpus.json'] == 'new'
    assert report['states']['sampling_plan.json'] == 'old'


def test_resume_interrupted_dual_file_write(isolated):
    root, tx = isolated
    interrupt_after_corpus(root, tx)
    written = (root/'data/corpus.json').read_bytes()
    report = repair.apply_repair(root, tx, resume=True)
    assert report['status'] == 'complete'
    assert (root/'data/corpus.json').read_bytes() == written
    assert report['recommendations_after'] == 446


def test_resume_rejects_unknown_state_without_writing(isolated):
    root, tx = isolated
    interrupt_after_corpus(root, tx)
    (root/'data/reviews.json').write_bytes(b'unknown')
    before = {n:(root/'data'/n).read_bytes() for n in repair.EXPECTED}
    with pytest.raises(ValueError, match='Unknown state'):
        repair.apply_repair(root, tx, resume=True)
    assert {n:(root/'data'/n).read_bytes() for n in repair.EXPECTED} == before


def test_apply_rejects_changed_input_before_backup(isolated):
    root, tx = isolated
    (root/'data/reviews.json').write_bytes(b'changed')
    with pytest.raises(ValueError, match='five-file hashes'):
        repair.apply_repair(root, tx)
    assert not tx.exists()

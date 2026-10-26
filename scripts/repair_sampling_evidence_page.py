"""Audited one-field migration for the batch-38 evidence-page correction.

Dry-run by default. Never redraw recommendations or weaken normal sampling checks.
"""
import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from paris.sampling import scope_digest

ISSUE_ID = 'profit_de_049_literal_298'
BEFORE = ['de_megai2:342']
AFTER = ['de_megai2:343']


def migrate(data, previous):
    """Accept exactly the documented evidence-page delta within the frozen scope."""
    candidate = copy.deepcopy(data)
    matches = [i for i in candidate['editorial_issues'] if i['id'] == ISSUE_ID]
    if len(matches) != 1 or matches[0]['evidence_pages'] != AFTER:
        raise ValueError('Expected the unique documented issue on page 343')
    if 'profit_049' not in previous['scope_ids']:
        raise ValueError('Documented alignment is absent from frozen scope')
    current_digest = scope_digest(data, previous['scope_ids'])
    if current_digest == previous['scope_digest']:
        return copy.deepcopy(previous)
    matches[0]['evidence_pages'] = BEFORE
    if scope_digest(candidate, previous['scope_ids']) != previous['scope_digest']:
        raise ValueError('Frozen scope has changes beyond the allowed evidence page')
    updated = copy.deepcopy(previous)
    updated['scope_digest'] = current_digest
    assert {k: v for k, v in updated.items() if k != 'scope_digest'} == {
        k: v for k, v in previous.items() if k != 'scope_digest'}
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'data/sampling_plan.json'
    raw = path.read_bytes()
    corpus_raw = (ROOT / 'data/corpus.json').read_bytes()
    previous = json.loads(raw)
    updated = migrate(json.loads(corpus_raw), previous)
    if updated == previous:
        print('Already consistent; no writes.')
        return
    summary = dict(issue_id=ISSUE_ID, field='evidence_pages', before=BEFORE, after=AFTER,
                   scope=len(previous['scope_ids']), recommendations_preserved=len(previous['recommended']),
                   old_scope_digest=previous['scope_digest'], new_scope_digest=updated['scope_digest'],
                   corpus_sha256=hashlib.sha256(corpus_raw).hexdigest(),
                   old_plan_sha256=hashlib.sha256(raw).hexdigest(),
                   checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
                   authorization='2026-10-21 user: solve current issue, then append three batches',
                   status='dry_run')
    if args.apply:
        backup = ROOT / 'local_backups/sampling-evidence-migration-20261021'
        backup.mkdir(exist_ok=False)
        (backup / 'sampling_plan.before.json').write_bytes(raw)
        (backup / 'corpus.before.json').write_bytes(corpus_raw)
        report = backup / 'migration.json'
        summary['status'] = 'prepared'
        report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if path.read_bytes() != raw or (ROOT / 'data/corpus.json').read_bytes() != corpus_raw:
            raise RuntimeError('Concurrent data change; refusing migration')
        temp = path.with_suffix('.migration.tmp')
        temp.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temp.replace(path)
        assert json.loads(path.read_bytes()) == updated
        assert (ROOT / 'data/corpus.json').read_bytes() == corpus_raw
        summary.update(status='applied', new_plan_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('Report:', report)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()

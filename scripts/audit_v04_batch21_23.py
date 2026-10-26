"""Verify the completed three-batch delivery and save compact local evidence."""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import index, load_corpus, validate
from paris.reviews import fingerprint, load_reviews, review_state
from paris.sampling import load_plan
import append_v04_batch21 as b21
import append_v04_batch22 as b22
import append_v04_batch23 as b23


def main():
    data = load_corpus()
    assert not validate(data)
    before = json.loads((ROOT/'local_backups/v04-before-batch21/corpus.json').read_text(encoding='utf-8'))
    for table in ('sources','editions','units','alignments','page_map','comparisons',
                  'corrections','editorial_issues','coverage'):
        assert data[table][:len(before[table])] == before[table]
    assert all(fingerprint(data,a) == fingerprint(before,a) for a in before['alignments'])
    units = index(data['units'])
    rows = b21.ROWS + b22.ROWS + b23.ROWS
    for section,n,_,de,zh,dp,zp in rows:
        for lang,text,pages in [('de',de,dp),('zh',zh,zp)]:
            unit = units[f'{section}_{lang}_{n:03}']
            assert unit['text'] == text
            assert [p['pdf_page'] for p in unit['locations']] == pages
    plan = load_plan(data)
    old_plan = json.loads((ROOT/'local_backups/v04-before-batch21/sampling_plan.json').read_text(encoding='utf-8'))
    assert plan['recommended'][:len(old_plan['recommended'])] == old_plan['recommended']
    reviews = load_reviews()
    counts = Counter(review_state(data,a,reviews)[0] for a in data['alignments'])
    assert counts['manually_verified'] == 24 and counts['stale'] == 0
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(ROOT/'data/reviews.json') == '24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb'
    report = dict(checked_at=datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds'),
      release=data['release'], prior_groups_preserved=len(before['alignments']),
      added_by_batch={str(n):sum(a['review_batch']==n for a in data['alignments']) for n in (21,22,23)},
      recipe_units_checked=len(rows)*2, prior_review_fingerprints='unchanged',
      reviews=dict(counts), sampling=dict(recommended=len(plan['recommended']),scope=len(plan['scope_ids']),
        prior_recommendations_preserved=len(old_plan['recommended'])),
      data_sha256={name:digest(ROOT/'data'/name) for name in
                   ('corpus.json','extraction.json','coverage_plan.json','sampling_plan.json','reviews.json')},
      scan_pages_reviewed={'de_megai2':[434,435,436,437,438],
       'zh_collected':[384,385,386,387,388,389,390],
       'de_megaiv2':[458,459,460],'zh_single':[195,196,197]},
      ordinary_spot_checks=['money_024','money_047','mill_029'],
      counts={key:len(data[key]) for key in ('units','alignments','page_map','sections')})
    path = ROOT/'tmp/alpha19-batch-audit.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    main()

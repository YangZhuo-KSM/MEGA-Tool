"""Freeze the review sample list for the current expansion scope."""
import json
import argparse
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus
from paris.sampling import build_plan, extend_plan

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--date', required=True, help='Hong Kong review date YYYY-MM-DD')
    args=parser.parse_args()
    path=ROOT/'data/sampling_plan.json'
    data=load_corpus()
    plan=extend_plan(data,json.loads(path.read_text(encoding='utf-8')),args.date) if path.exists() else build_plan(data,created_date=args.date)
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Suggested {len(plan['recommended'])}/{len(plan['scope_ids'])} groups; no reviews changed.")

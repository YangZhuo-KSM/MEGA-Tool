"""Freeze the review sample list for the current expansion scope."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus
from paris.sampling import build_plan

if __name__ == '__main__':
    plan=build_plan(load_corpus())
    (ROOT/'data/sampling_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Suggested {len(plan['recommended'])}/{len(plan['scope_ids'])} groups; no reviews changed.")

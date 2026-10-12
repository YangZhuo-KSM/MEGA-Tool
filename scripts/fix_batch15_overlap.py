"""Remove one overlapping batch-15 doubt anchor once; text and reviews stay unchanged."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus.json"
REVIEWS = ROOT / "data/reviews.json"
BACKUP = ROOT / "local_backups/v04-before-batch15-overlap-fix.json"

data = json.loads(CORPUS.read_text(encoding="utf-8"))
reviews = REVIEWS.read_bytes()
unit = next(u for u in data["units"] if u["id"] == "hegel_de_052")
long_start = unit["text"].index("wtklichen")
duplicates = [i for i in data["editorial_issues"]
              if i["unit_id"] == "hegel_de_052"
              and i["current_reading"] == "wtkliche"
              and i["text_anchor"]["start"] == long_start]
if len(duplicates) != 1:
    raise SystemExit(f"Expected one overlapping issue, found {len(duplicates)}")
BACKUP.write_bytes(CORPUS.read_bytes())
data["editorial_issues"].remove(duplicates[0])
temp = CORPUS.with_suffix(".overlap.tmp")
temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temp.replace(CORPUS)
assert REVIEWS.read_bytes() == reviews
print("Removed one overlapping issue; text and reviews unchanged.")
print("Corpus SHA256:", hashlib.sha256(CORPUS.read_bytes()).hexdigest())

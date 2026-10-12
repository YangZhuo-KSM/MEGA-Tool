"""Add two omitted batch-15 marker annotations once; do not alter text or reviews."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus.json"
REVIEWS = ROOT / "data/reviews.json"
BACKUP = ROOT / "local_backups/v04-before-batch15-marker-fix.json"

data = json.loads(CORPUS.read_text(encoding="utf-8"))
if data.get("release") != "0.4.0-alpha11":
    raise SystemExit("Expected alpha11 corpus")
units = {u["id"]: u for u in data["units"]}
review_bytes = REVIEWS.read_bytes()
specs = [
    ("hegel_de_059", "||XXVI|", ["de_megai2:407"],
     "页内标记按底本保留；中文对应作XXVI。正文照录，等待研究者核查。"),
    ("hegel_de_060", "||", ["de_megai2:407", "de_megai2:408"],
     "跨页双竖线按底本位置保留，连接Gegenstände。正文照录，等待研究者核查。"),
]
if any(i["unit_id"] == uid and i["current_reading"] == token
       for uid, token, _, _ in specs for i in data["editorial_issues"]):
    raise SystemExit("Marker issue already present; refusing duplicate fix")
BACKUP.write_bytes(CORPUS.read_bytes())
for uid, token, pages, note in specs:
    text = units[uid]["text"]
    start = text.find(token)
    if start < 0:
        raise ValueError(f"Missing marker {token!r} in {uid}")
    data["editorial_issues"].append({
        "id": f"{uid}_literal_{start}",
        "unit_id": uid,
        "kind": "glyph_doubt",
        "status": "open",
        "current_reading": token,
        "reported_reading": note,
        "evidence_pages": pages,
        "text_anchor": {"start": start, "end": start + len(token), "quote": token},
        "note": note,
        "recorded_by": "Codex",
        "recorded_at": "2026-10-12",
    })
temp = CORPUS.with_suffix(".marker.tmp")
temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temp.replace(CORPUS)
assert REVIEWS.read_bytes() == review_bytes
print("Added 2 marker annotations; text and reviews unchanged.")
print("Corpus SHA256:", hashlib.sha256(CORPUS.read_bytes()).hexdigest())

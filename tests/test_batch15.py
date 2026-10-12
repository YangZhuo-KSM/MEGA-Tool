"""Batch 15: Hegel outline, long argument units, and exact source pages."""
import hashlib
import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

from paris.annotations import unit_issues
from paris.corpus import index, load_corpus
from paris.locator import locate
from paris.pages import units_on_page
from paris.sampling import load_plan as load_sampling_plan


ROOT = Path(__file__).resolve().parents[1]


def test_forty_two_pending_groups_and_append_only_boundary():
    data = load_corpus(); units = index(data["units"])
    batch = [a for a in data["alignments"] if a["review_batch"] == 15]
    assert [a["id"] for a in batch] == [f"hegel_{n:03}" for n in range(19, 61)]
    assert all(a["status"] == "uncertain" and a["verified_by"] is None for a in batch)
    assert units["hegel_de_019"]["locations"][0]["printed_page"] == "402"
    assert units["hegel_zh_060"]["locations"][0]["printed_page"] == "324"
    assert {u["id"] for u in units_on_page(data, "de_megai2", 402)} >= {
        "hegel_de_019", "hegel_de_024"
    }


def test_long_cross_page_units_return_every_printed_page():
    data = load_corpus()
    outline = next(h for h in locate(data, "审核法律的理性")
                   if h["unit"]["id"] == "hegel_zh_021")
    assert [p["printed_page"] for p in outline["reference"]["locations"]] == ["316", "317"]
    assert "第316—317页" in outline["reference"]["plain"]
    long_hit = next(h for h in locate(data, "现实的、肉体的、站在坚实的呈圆形的地球上")
                    if h["unit"]["id"] == "hegel_zh_060")
    assert long_hit["targets"][0]["alignment_id"] == "hegel_060"
    assert [p["pdf_page"] for p in long_hit["reference"]["locations"]] == [349]
    german = next(h for h in locate(data, "wükliche") if h["unit"]["id"] == "hegel_de_060")
    assert [p["printed_page"] for p in german["reference"]["locations"]] == ["407", "408"]


def test_visible_source_anomalies_are_retained_and_annotated():
    data = load_corpus(); units = index(data["units"])
    checks = [
        ("hegel_de_052", "wtklichen", "de_megai2:406"),
        ("hegel_de_055", "Bewußtsem", "de_megai2:406"),
        ("hegel_de_056", "gegenständüches", "de_megai2:407"),
        ("hegel_de_057", "natürÜches", "de_megai2:407"),
        ("hegel_de_059", "f ixüt", "de_megai2:407"),
        ("hegel_de_060", "wükliche", "de_megai2:407"),
    ]
    for uid, token, page in checks:
        issue = next(i for i in unit_issues(data, uid) if i["current_reading"] == token)
        anchor = issue["text_anchor"]
        assert units[uid]["text"][anchor["start"]:anchor["end"]] == token
        assert issue["status"] == "retained_as_source" and issue["evidence_pages"] == [page]
    assert [i["current_reading"] for i in unit_issues(data, "hegel_de_052")].count("wtkliche") == 1
    marker = next(i for i in unit_issues(data, "hegel_de_060")
                  if i["current_reading"] == "||")
    assert marker["kind"] == "glyph_doubt" and marker["status"] == "open"
    assert marker["evidence_pages"] == ["de_megai2:407", "de_megai2:408"]


def test_sampling_and_reader_include_batch_fifteen(monkeypatch):
    data = load_corpus()
    recommended = {r["alignment_id"] for r in load_sampling_plan(data)["recommended"]}
    assert len(recommended) == 76
    assert any(f"hegel_{n:03}" in recommended for n in range(19, 61))
    monkeypatch.setattr("paris.reviews.load_reviews", lambda: {})
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run(timeout=30)
    app.sidebar.selectbox(key="section_id").select("hegel").run()
    app.sidebar.text_input[0].input("wtklichen").run()
    assert not app.exception
    assert app.metric[0].value == "240" and app.metric[1].value == "0"
    assert any("语义存疑 · 按底本照录：wtklichen" in w.value for w in app.warning)


def test_prior_records_reviews_and_sampling_choices_are_unchanged():
    data = load_corpus()
    backup_root = ROOT / "local_backups/v04-before-batch15"
    old = json.loads((backup_root / "corpus.json").read_text(encoding="utf-8"))
    for table in ("sources", "editions", "units", "alignments", "page_map",
                  "comparisons", "corrections", "editorial_issues", "coverage"):
        assert data.get(table, [])[:len(old.get(table, []))] == old.get(table, [])
    old_plan = json.loads((backup_root / "sampling_plan.json").read_text(encoding="utf-8"))
    current_plan = load_sampling_plan(data)
    assert current_plan["recommended"][:len(old_plan["recommended"])] == old_plan["recommended"]
    assert hashlib.sha256((ROOT / "data/reviews.json").read_bytes()).hexdigest() == (
        "24cedf775f5254bf98932ac34f12fbc8bda68df2fa7fbc8bd9b10dc30749f1bb"
    )

"""Batch 16: natural being, objectivity, and speculative illusion."""
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


def test_forty_eight_pending_groups_and_append_only_boundary():
    data = load_corpus(); units = index(data["units"])
    batch = [a for a in data["alignments"] if a["review_batch"] == 16]
    assert [a["id"] for a in batch] == [f"hegel_{n:03}" for n in range(61, 109)]
    assert all(a["status"] == "uncertain" and a["verified_by"] is None for a in batch)
    assert units["hegel_de_061"]["locations"][0]["printed_page"] == "408"
    assert units["hegel_zh_108"]["locations"][-1]["printed_page"] == "329"
    assert {u["id"] for u in units_on_page(data, "de_megai2", 411)} >= {
        "hegel_de_101", "hegel_de_108"
    }


def test_cross_page_units_return_every_printed_page():
    data = load_corpus()
    objectivity = next(h for h in locate(data, "对于第三者来说是对象")
                       if h["unit"]["id"] == "hegel_zh_066")
    assert [p["printed_page"] for p in objectivity["reference"]["locations"]] == ["324", "325"]
    assert "第324—325页" in objectivity["reference"]["plain"]
    argument = next(h for h in locate(data, "真正的知识和真正的生活")
                    if h["unit"]["id"] == "hegel_zh_108")
    assert [p["pdf_page"] for p in argument["reference"]["locations"]] == [353, 354]
    german = next(h for h in locate(data, "kein Gegenständliches")
                  if h["unit"]["id"] == "hegel_de_072")
    assert [p["printed_page"] for p in german["reference"]["locations"]] == ["408", "409"]


def test_scan_readings_override_obvious_text_layer_errors_and_mark_page_symbols():
    data = load_corpus(); units = index(data["units"])
    clean = " ".join(units[f"hegel_de_{n:03}"]["text"] for n in range(61, 109))
    for visible in ("natürlich", "Wirklichkeit", "Sinnlichkeit", "alles", "seinen", "weil", "Schein", "weiß", "Religion"):
        assert visible in clean
    for ocr_error in ("natürÜch", "Wirküchkeit", "Sinnüchkeit", "aües", "semen", "weü", "Schern", "Reügion"):
        assert ocr_error not in clean
    checks = [
        ("hegel_de_064", "exis||tiren", ["de_megai2:408"]),
        ("hegel_de_073", "||XXVII|", ["de_megai2:409"]),
        ("hegel_de_095", "||XXVIII|", ["de_megai2:410"]),
        ("hegel_de_105", "I", ["de_megai2:411"]),
    ]
    for uid, token, pages in checks:
        issue = next(i for i in unit_issues(data, uid) if i["current_reading"] == token)
        anchor = issue["text_anchor"]
        assert units[uid]["text"][anchor["start"]:anchor["end"]] == token
        assert issue["kind"] == "glyph_doubt" and issue["status"] == "open"
        assert issue["evidence_pages"] == pages


def test_sampling_and_reader_include_batch_sixteen(monkeypatch):
    data = load_corpus()
    recommended = {r["alignment_id"] for r in load_sampling_plan(data)["recommended"]}
    assert len(recommended) == 76
    assert any(f"hegel_{n:03}" in recommended for n in range(61, 109))
    monkeypatch.setattr("paris.reviews.load_reviews", lambda: {})
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.sidebar.selectbox(key="section_id").select("hegel").run()
    app.sidebar.text_input[0].input("exis||tiren").run()
    assert not app.exception
    assert app.metric[0].value == "240" and app.metric[1].value == "0"
    assert any("exis||tiren" in w.value for w in app.warning)


def test_prior_records_reviews_and_sampling_choices_are_unchanged():
    data = load_corpus()
    backup_root = ROOT / "local_backups/v04-before-batch16"
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

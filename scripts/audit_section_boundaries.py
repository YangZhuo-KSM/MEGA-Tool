"""Build a read-only inventory for section boundary and coverage audits.

The report derives current first/last units, source pages, planned starts,
section transitions, notes and editorial-issue counts from the authoritative
JSON files.  It deliberately does not infer that a section is complete: scan
evidence and editorial matter still require page-by-page review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((ROOT / "data" / name).read_bytes()).hexdigest()


def primary(unit: dict) -> bool:
    return unit.get("role", "primary") == "primary"


def locations(unit: dict) -> list[dict]:
    return unit.get("locations") or []


def unit_summary(unit: dict | None) -> dict | None:
    if unit is None:
        return None
    locs = locations(unit)
    text = unit.get("text", "")
    return {
        "id": unit["id"],
        "sequence": unit["sequence"],
        "printed_pages": list(dict.fromkeys(x.get("printed_page") for x in locs)),
        "pdf_pages": list(dict.fromkeys(x.get("pdf_page") for x in locs)),
        "text_head": text[:160],
        "text_tail": text[-160:],
    }


def page_span(units: list[dict]) -> dict:
    locs = [loc for unit in units for loc in locations(unit)]
    return {
        "sources": list(dict.fromkeys(loc.get("source_id") for loc in locs)),
        "printed_pages": list(dict.fromkeys(loc.get("printed_page") for loc in locs)),
        "pdf_pages": sorted({loc.get("pdf_page") for loc in locs}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    corpus = load_json("corpus.json")
    coverage = load_json("coverage_plan.json")
    units = [unit for unit in corpus["units"] if primary(unit)]
    issues = corpus.get("editorial_issues", [])
    alignments = corpus["alignments"]

    unit_by_id = {unit["id"]: unit for unit in units}
    section_units: dict[str, dict[str, list[dict]]] = {}
    for unit in units:
        section_units.setdefault(unit["section_id"], {}).setdefault(unit["language"], []).append(unit)
    for language_map in section_units.values():
        for values in language_map.values():
            values.sort(key=lambda item: item["sequence"])

    issue_counts = Counter(unit_by_id.get(issue.get("unit_id"), {}).get("section_id") for issue in issues)
    notes_by_section: dict[str, list[dict]] = {}
    for alignment in alignments:
        note = alignment.get("note") or ""
        if note and note != "AI拟定对应，待研究者逐批确认。":
            notes_by_section.setdefault(alignment["section_id"], []).append(
                {"id": alignment["id"], "note": note}
            )

    section_reports = []
    for item in coverage["items"]:
        section_id = item["section_ids"][0]
        by_language = section_units.get(section_id, {})
        de = by_language.get("de", [])
        zh = by_language.get("zh", [])
        section_alignments = [a for a in alignments if a["section_id"] == section_id]
        section_reports.append(
            {
                "id": section_id,
                "title": item["title"],
                "planned_start": {"de_printed": item.get("de_start"), "zh_printed": item.get("zh_start")},
                "alignment_count": len(section_alignments),
                "sequence": {
                    "de": [de[0]["sequence"], de[-1]["sequence"]] if de else None,
                    "zh": [zh[0]["sequence"], zh[-1]["sequence"]] if zh else None,
                },
                "de": {
                    "first": unit_summary(de[0] if de else None),
                    "last": unit_summary(de[-1] if de else None),
                    "span": page_span(de),
                },
                "zh": {
                    "first": unit_summary(zh[0] if zh else None),
                    "last": unit_summary(zh[-1] if zh else None),
                    "span": page_span(zh),
                },
                "editorial_issue_count": issue_counts.get(section_id, 0),
                "alignment_notes": notes_by_section.get(section_id, []),
            }
        )

    transitions = []
    ordered = [item["id"] for item in coverage["items"] if item["id"] != "mill"]
    reports = {item["id"]: item for item in section_reports}
    for left_id, right_id in zip(ordered, ordered[1:]):
        left = reports[left_id]
        right = reports[right_id]
        transitions.append(
            {
                "from": left_id,
                "to": right_id,
                "de": {
                    "last": left["de"]["last"],
                    "first": right["de"]["first"],
                },
                "zh": {
                    "last": left["zh"]["last"],
                    "first": right["zh"]["first"],
                },
            }
        )

    report = {
        "report_type": "inventory_only",
        "warning": "Page spans and adjacency are candidates for scan review, not automated completeness findings.",
        "release": corpus["release"],
        "data_sha256": {
            name: sha256(name)
            for name in ("corpus.json", "extraction.json", "coverage_plan.json", "sampling_plan.json", "reviews.json")
        },
        "counts": {
            "sections": len(corpus["sections"]),
            "units": len(corpus["units"]),
            "primary_units": len(units),
            "alignments": len(alignments),
        },
        "sections": section_reports,
        "transitions": transitions,
    }

    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        path = args.output if args.output.is_absolute() else ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        print(path)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

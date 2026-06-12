import csv
import json
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "related_work_matrix.csv"
STATE = DOCS / "crossref_harvest_state.json"

QUERIES = [
    "shared autonomy",
    "control authority",
    "authority transfer robot",
    "teleoperation intent inference",
    "shared control robot manipulation",
    "assistive teleoperation robot",
    "robot arbitration human control",
    "authority allocation robot",
    "human-robot shared control",
    "collaborative control human robot",
    "physical human robot interaction autonomy",
    "robot assistance handover authority",
    "mixed-initiative control robot",
    "autonomous intervention robot assistance",
    "shared autonomy manipulation",
    "shared autonomy navigation",
    "robot intent recognition shared autonomy",
    "control arbitration human robot",
    "human-in-the-loop robot control authority",
    "adaptive shared control",
]


def clean(s):
    if s is None:
        return ""
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s


def pick_title(item):
    titles = item.get("title") or []
    return clean(titles[0]) if titles else ""


def pick_venue(item):
    for key in ("container-title", "short-container-title"):
        vals = item.get(key) or []
        if vals:
            return clean(vals[0])
    return ""


def year(item):
    for key in ("published-print", "published-online", "created", "issued"):
        parts = (((item.get(key) or {}).get("date-parts")) or [])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def fetch_query(q, rows=100, cursor="*"):
    url = "https://api.crossref.org/works"
    params = {
        "query": q,
        "rows": rows,
        "select": "DOI,title,author,container-title,short-container-title,published-print,published-online,created,issued,type,URL",
        "mailto": "codex@example.com",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def main():
    DOCS.mkdir(exist_ok=True)
    seen = OrderedDict()
    stats = []
    for q in QUERIES:
        fetched = 0
        try:
            payload = fetch_query(q, rows=100)
        except Exception as e:
            stats.append({"query": q, "error": str(e), "fetched": fetched})
            continue
        items = payload.get("message", {}).get("items", [])
        for item in items:
            doi = clean(item.get("DOI"))
            title = pick_title(item)
            if not title:
                continue
            key = doi.lower() if doi else title.lower()
            if key in seen:
                continue
            authors = item.get("author") or []
            author_str = "; ".join(
                clean(" ".join(filter(None, [a.get("given", ""), a.get("family", "")]))) for a in authors[:6] if a
            )
            seen[key] = {
                "paper_id": len(seen) + 1,
                "query_seed": q,
                "title": title,
                "year": year(item),
                "venue": pick_venue(item),
                "doi": doi,
                "url": clean(item.get("URL")),
                "authors": author_str,
                "problem_claimed": "",
                "mechanism": "",
                "hidden_assumptions": "",
                "fixed_variables": "",
                "ignored_failures": "",
                "less_novel": "",
                "open_questions": "",
                "relevance_score": "",
                "bucket": "",
                "notes": "",
                "source": "crossref",
            }
            fetched += 1
        stats.append({"query": q, "fetched": fetched})
        if len(seen) >= 1100:
            break

    fieldnames = list(next(iter(seen.values())).keys()) if seen else [
        "paper_id", "query_seed", "title", "year", "venue", "doi", "url", "authors",
        "problem_claimed", "mechanism", "hidden_assumptions", "fixed_variables",
        "ignored_failures", "less_novel", "open_questions", "relevance_score", "bucket",
        "notes", "source"
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in seen.values():
            writer.writerow(row)

    STATE.write_text(json.dumps({"queries": stats, "total": len(seen)}, indent=2), encoding="utf-8")
    print(f"wrote {len(seen)} rows to {OUT}")


if __name__ == "__main__":
    sys.exit(main())

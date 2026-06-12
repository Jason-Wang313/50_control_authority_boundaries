import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INP = DOCS / "related_work_matrix.csv"
OUT = DOCS / "literature_ranked.csv"

KEYWORDS = {
    "shared autonomy": 12,
    "shared control": 12,
    "control authority": 15,
    "authority": 7,
    "arbitration": 10,
    "mixed-initiative": 10,
    "teleoperation": 9,
    "assistive": 8,
    "handover": 8,
    "intent": 8,
    "human-robot": 6,
    "human robot": 6,
    "navigation": 5,
    "manipulation": 5,
    "assist": 4,
    "safety": 4,
    "adaptive": 5,
    "switch": 4,
    "override": 8,
    "allocation": 6,
}


def score(title, venue, query):
    text = f"{title} {venue} {query}".lower()
    s = 0
    for k, v in KEYWORDS.items():
        if k in text:
            s += v
    if re.search(r"\b(robotics|hri|human-robot interaction|icra|iros|rss|science robotics|tj|ijrr)\b", text):
        s += 5
    return s


def main():
    rows = []
    with INP.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["relevance_score"] = score(r["title"], r["venue"], r["query_seed"])
            rows.append(r)
    rows.sort(key=lambda r: (-int(r["relevance_score"]), r["year"], r["title"]))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"ranked {len(rows)} rows")


if __name__ == "__main__":
    main()

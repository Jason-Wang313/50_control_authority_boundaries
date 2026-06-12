import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INP = DOCS / "literature_ranked.csv"
TOP300 = DOCS / "serious_skim_300.csv"
TOP200 = DOCS / "deep_read_220.csv"
TOP100 = DOCS / "hostile_prior_100.csv"


def write_slice(rows, path, n):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows[:n])


def main():
    with INP.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    write_slice(rows, TOP300, 300)
    write_slice(rows, TOP200, 220)
    write_slice(rows, TOP100, 100)
    print("exported shortlists")


if __name__ == "__main__":
    main()

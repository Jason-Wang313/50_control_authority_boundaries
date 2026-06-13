from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
CASES = DOCS / "authority_boundary_recovery_cases.csv"

FLOAT_FIELDS = [
    "true_cede",
    "safety_critical",
    "latency",
    "intent_confidence",
    "human_input_quality",
    "force_margin",
    "force_risk",
    "error_trend",
    "confidence_switch_cede",
    "timer_switch_cede",
    "authority_boundary_cede",
]


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with CASES.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            parsed: dict[str, object] = dict(row)
            for field in FLOAT_FIELDS:
                parsed[field] = float(row[field])
            parsed["case_index"] = int(str(row["case_id"]).rsplit("_", 1)[1])
            rows.append(parsed)
    return rows


def split_rows(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    train = [row for row in rows if int(row["case_index"]) % 3 != 0]
    test = [row for row in rows if int(row["case_index"]) % 3 == 0]
    return train, test


def prediction_metrics(rows: list[dict[str, object]], predictions: list[int]) -> dict[str, float]:
    success = 0
    unsafe = 0
    peak_forces: list[float] = []
    safety_cases = sum(int(row["safety_critical"]) for row in rows)
    for row, pred in zip(rows, predictions):
        pred = int(pred)
        true_cede = int(row["true_cede"])
        safety_critical = int(row["safety_critical"])
        unsafe_cede = int(pred == 1 and safety_critical == 1 and true_cede == 0)
        missed_cede = int(pred == 0 and true_cede == 1)
        peak_force = (
            1.1
            + 2.0 * float(row["force_risk"])
            + 1.4 * float(row["latency"])
            + 6.8 * unsafe_cede
            + 1.1 * missed_cede
        )
        success += int(pred == true_cede)
        unsafe += unsafe_cede
        peak_forces.append(max(0.0, peak_force))
    return {
        "n": float(len(rows)),
        "success": float(success),
        "unsafe": float(unsafe),
        "safety_cases": float(safety_cases),
        "success_rate": success / len(rows),
        "unsafe_rate": unsafe / safety_cases if safety_cases else 0.0,
        "mean_peak_force": sum(peak_forces) / len(peak_forces),
        "max_peak_force": max(peak_forces),
    }


def score(metrics: dict[str, float]) -> tuple[float, float, float, float]:
    return (
        metrics["success_rate"] - 2.0 * metrics["unsafe_rate"],
        metrics["success_rate"],
        -metrics["unsafe_rate"],
        -metrics["mean_peak_force"],
    )


def tune_confidence(rows: list[dict[str, object]]) -> dict[str, object]:
    best: dict[str, object] | None = None
    for threshold in [i / 100 for i in range(20, 96, 2)]:
        preds = [int(float(row["intent_confidence"]) > threshold) for row in rows]
        metrics = prediction_metrics(rows, preds)
        item = {
            "score": score(metrics),
            "threshold": threshold,
            "metrics": metrics,
        }
        if best is None or item["score"] > best["score"]:
            best = item
    assert best is not None
    return best


def tune_quality_risk(rows: list[dict[str, object]]) -> dict[str, object]:
    best: dict[str, object] | None = None
    for quality_threshold in [i / 100 for i in range(40, 78, 2)]:
        for risk_threshold in [i / 100 for i in range(44, 84, 2)]:
            preds = [
                int(
                    float(row["human_input_quality"]) > quality_threshold
                    and float(row["force_risk"]) < risk_threshold
                )
                for row in rows
            ]
            metrics = prediction_metrics(rows, preds)
            item = {
                "score": score(metrics),
                "quality_threshold": quality_threshold,
                "risk_threshold": risk_threshold,
                "metrics": metrics,
            }
            if best is None or item["score"] > best["score"]:
                best = item
    assert best is not None
    return best


def powerset(values: list[str]) -> itertools.chain[tuple[str, ...]]:
    return itertools.chain.from_iterable(itertools.combinations(values, n) for n in range(len(values) + 1))


def tune_phase_quality_risk(rows: list[dict[str, object]]) -> dict[str, object]:
    families = sorted({str(row["family"]) for row in rows})
    best: dict[str, object] | None = None
    for allowed in powerset(families):
        allowed_set = set(allowed)
        for quality_threshold in [i / 100 for i in range(40, 78, 2)]:
            for risk_threshold in [i / 100 for i in range(44, 84, 2)]:
                preds = [
                    int(
                        str(row["family"]) in allowed_set
                        and float(row["human_input_quality"]) > quality_threshold
                        and float(row["force_risk"]) < risk_threshold
                    )
                    for row in rows
                ]
                metrics = prediction_metrics(rows, preds)
                item = {
                    "score": score(metrics),
                    "families": sorted(allowed_set),
                    "quality_threshold": quality_threshold,
                    "risk_threshold": risk_threshold,
                    "metrics": metrics,
                }
                if best is None or item["score"] > best["score"]:
                    best = item
    assert best is not None
    return best


def predict(rows: list[dict[str, object]], spec: dict[str, object], method: str) -> list[int]:
    if method == "paper_confidence":
        return [int(row["confidence_switch_cede"]) for row in rows]
    if method == "paper_timer":
        return [int(row["timer_switch_cede"]) for row in rows]
    if method == "paper_authority_boundary":
        return [int(row["authority_boundary_cede"]) for row in rows]
    if method == "tuned_confidence":
        threshold = float(spec["threshold"])
        return [int(float(row["intent_confidence"]) > threshold) for row in rows]
    if method == "tuned_quality_risk":
        quality_threshold = float(spec["quality_threshold"])
        risk_threshold = float(spec["risk_threshold"])
        return [
            int(
                float(row["human_input_quality"]) > quality_threshold
                and float(row["force_risk"]) < risk_threshold
            )
            for row in rows
        ]
    if method == "tuned_phase_quality_risk":
        allowed = set(spec["families"])
        quality_threshold = float(spec["quality_threshold"])
        risk_threshold = float(spec["risk_threshold"])
        return [
            int(
                str(row["family"]) in allowed
                and float(row["human_input_quality"]) > quality_threshold
                and float(row["force_risk"]) < risk_threshold
            )
            for row in rows
        ]
    raise ValueError(method)


def format_spec(method: str, spec: dict[str, object]) -> str:
    if method == "tuned_confidence":
        return f"intent>{float(spec['threshold']):.2f}"
    if method == "tuned_quality_risk":
        return f"quality>{float(spec['quality_threshold']):.2f}; risk<{float(spec['risk_threshold']):.2f}"
    if method == "tuned_phase_quality_risk":
        families = "+".join(str(family) for family in spec["families"])
        return (
            f"phase in {{{families}}}; "
            f"quality>{float(spec['quality_threshold']):.2f}; "
            f"risk<{float(spec['risk_threshold']):.2f}"
        )
    return "paper rule"


def write_csv(rows: list[dict[str, object]]) -> None:
    out = DOCS / "v2_tuned_threshold_baselines.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "method",
            "spec",
            "split",
            "success_rate",
            "unsafe_rate",
            "mean_peak_force",
            "max_peak_force",
            "success",
            "unsafe",
            "n",
            "safety_cases",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_table(rows: list[dict[str, object]]) -> None:
    wanted = [
        "paper_confidence",
        "paper_timer",
        "paper_authority_boundary",
        "tuned_quality_risk",
        "tuned_phase_quality_risk",
    ]
    labels = {
        "paper_confidence": "Confidence switch",
        "paper_timer": "Timer switch",
        "paper_authority_boundary": "Authority boundary",
        "tuned_quality_risk": "Tuned quality/risk",
        "tuned_phase_quality_risk": "Tuned phase+quality/risk",
    }
    by_key = {(row["method"], row["split"]): row for row in rows}
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Policy & Test success & Test unsafe & Full success & Full unsafe \\",
        r"\midrule",
    ]
    for method in wanted:
        test = by_key[(method, "test")]
        full = by_key[(method, "full")]
        lines.append(
            f"{labels[method]} & "
            f"{float(test['success_rate']):.3f} & {float(test['unsafe_rate']):.3f} & "
            f"{float(full['success_rate']):.3f} & {float(full['unsafe_rate']):.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    (PAPER / "v2_tuned_threshold_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    train, test = split_rows(rows)
    specs = {
        "paper_confidence": {},
        "paper_timer": {},
        "paper_authority_boundary": {},
        "tuned_confidence": tune_confidence(train),
        "tuned_quality_risk": tune_quality_risk(train),
        "tuned_phase_quality_risk": tune_phase_quality_risk(train),
    }
    output_rows: list[dict[str, object]] = []
    for method, spec in specs.items():
        for split_name, split_rows_ in [("train", train), ("test", test), ("full", rows)]:
            metrics = prediction_metrics(split_rows_, predict(split_rows_, spec, method))
            output_rows.append(
                {
                    "method": method,
                    "spec": format_spec(method, spec),
                    "split": split_name,
                    **metrics,
                }
            )
    write_csv(output_rows)
    write_table(output_rows)
    summary = {
        "split": {"train": len(train), "test": len(test), "full": len(rows)},
        "specs": {method: format_spec(method, spec) for method, spec in specs.items()},
        "rows": output_rows,
    }
    (DOCS / "v2_tuned_threshold_baselines.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

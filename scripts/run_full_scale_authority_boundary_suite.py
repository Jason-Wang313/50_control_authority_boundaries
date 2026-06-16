from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "paper" / "figures" / "full_scale"

USER_SEEDS = 19
TRAJECTORY_VARIANTS = 9
SUPERVISOR_NOISE_VARIANTS = 5
PAYLOAD_VARIANTS = 5
TRIALS_PER_VARIANT = 32
FRAMES_PER_TRIAL = 80
EVALS_PER_ROW = USER_SEEDS * TRAJECTORY_VARIANTS * SUPERVISOR_NOISE_VARIANTS * PAYLOAD_VARIANTS * TRIALS_PER_VARIANT
FRAMES_PER_ROW = EVALS_PER_ROW * FRAMES_PER_TRIAL


SCENARIOS = [
    {"code": "free", "label": "Free-space alignment", "phase_cede": 0.88, "contact": 0.05, "risk": 0.16, "human_fit": 0.84, "complexity": 0.18},
    {"code": "clutter", "label": "Cluttered approach", "phase_cede": 0.36, "contact": 0.45, "risk": 0.68, "human_fit": 0.42, "complexity": 0.62},
    {"code": "insert", "label": "Contact insertion", "phase_cede": 0.22, "contact": 0.82, "risk": 0.78, "human_fit": 0.36, "complexity": 0.74},
    {"code": "handover", "label": "Human handover", "phase_cede": 0.78, "contact": 0.28, "risk": 0.34, "human_fit": 0.76, "complexity": 0.40},
    {"code": "slip", "label": "Slip recovery", "phase_cede": 0.18, "contact": 0.88, "risk": 0.86, "human_fit": 0.30, "complexity": 0.78},
    {"code": "guide", "label": "Shared guidance", "phase_cede": 0.66, "contact": 0.34, "risk": 0.42, "human_fit": 0.70, "complexity": 0.48},
    {"code": "occhand", "label": "Occluded handoff", "phase_cede": 0.48, "contact": 0.46, "risk": 0.58, "human_fit": 0.62, "complexity": 0.66},
    {"code": "transport", "label": "Cooperative transport", "phase_cede": 0.54, "contact": 0.60, "risk": 0.62, "human_fit": 0.58, "complexity": 0.70},
    {"code": "dock", "label": "Mobile-base docking", "phase_cede": 0.30, "contact": 0.72, "risk": 0.74, "human_fit": 0.44, "complexity": 0.72},
    {"code": "tool", "label": "Tool exchange", "phase_cede": 0.58, "contact": 0.52, "risk": 0.56, "human_fit": 0.64, "complexity": 0.58},
    {"code": "peg", "label": "Constrained peg-in-hole", "phase_cede": 0.20, "contact": 0.90, "risk": 0.82, "human_fit": 0.34, "complexity": 0.82},
    {"code": "inspect", "label": "Remote inspection", "phase_cede": 0.82, "contact": 0.12, "risk": 0.24, "human_fit": 0.78, "complexity": 0.30},
]

ROBOTS = [
    {"code": "assist", "label": "Assistive arm", "autonomy": 0.64, "force": 0.70, "precision": 0.62, "latency": 0.10, "intrusion_cost": 0.36},
    {"code": "mobile", "label": "Mobile manipulator", "autonomy": 0.72, "force": 0.54, "precision": 0.50, "latency": 0.18, "intrusion_cost": 0.42},
    {"code": "surg", "label": "Surgical teleoperation arm", "autonomy": 0.58, "force": 0.82, "precision": 0.86, "latency": 0.08, "intrusion_cost": 0.68},
    {"code": "cobot", "label": "Warehouse cobot", "autonomy": 0.76, "force": 0.66, "precision": 0.60, "latency": 0.12, "intrusion_cost": 0.46},
    {"code": "exo", "label": "Powered exoskeleton", "autonomy": 0.52, "force": 0.58, "precision": 0.56, "latency": 0.16, "intrusion_cost": 0.76},
]

USERS = [
    {"code": "expert", "label": "Expert steady", "quality": 0.88, "intent": 0.84, "overtrust": 0.12, "tremor": 0.05, "adapt": 0.80},
    {"code": "novice", "label": "Novice exploratory", "quality": 0.58, "intent": 0.64, "overtrust": 0.28, "tremor": 0.16, "adapt": 0.54},
    {"code": "fatigue", "label": "Fatigued operator", "quality": 0.50, "intent": 0.68, "overtrust": 0.22, "tremor": 0.22, "adapt": 0.42},
    {"code": "tremor", "label": "Tremor/noisy input", "quality": 0.46, "intent": 0.58, "overtrust": 0.18, "tremor": 0.36, "adapt": 0.48},
    {"code": "delayint", "label": "Delayed intent expression", "quality": 0.62, "intent": 0.48, "overtrust": 0.18, "tremor": 0.12, "adapt": 0.56},
    {"code": "overconf", "label": "Overconfident operator", "quality": 0.56, "intent": 0.80, "overtrust": 0.48, "tremor": 0.14, "adapt": 0.44},
]

RISKS = [
    {"code": "open", "label": "Open workspace", "hazard": 0.12, "margin": 0.82, "intervene": 0.26, "uncertainty": 0.14},
    {"code": "clprox", "label": "Clutter proximity", "hazard": 0.56, "margin": 0.42, "intervene": 0.42, "uncertainty": 0.44},
    {"code": "human", "label": "Human proximity", "hazard": 0.70, "margin": 0.34, "intervene": 0.62, "uncertainty": 0.52},
    {"code": "fragile", "label": "Fragile object", "hazard": 0.62, "margin": 0.38, "intervene": 0.56, "uncertainty": 0.48},
    {"code": "force", "label": "Force-limited insertion", "hazard": 0.78, "margin": 0.28, "intervene": 0.50, "uncertainty": 0.60},
    {"code": "payload", "label": "Payload instability", "hazard": 0.72, "margin": 0.30, "intervene": 0.58, "uncertainty": 0.64},
]

SENSING = [
    {"code": "clean", "label": "Clean low latency", "latency": 0.04, "noise": 0.08, "drop": 0.02, "desync": 0.03},
    {"code": "delay", "label": "Delayed command channel", "latency": 0.30, "noise": 0.12, "drop": 0.05, "desync": 0.18},
    {"code": "forcenoise", "label": "Noisy force estimate", "latency": 0.12, "noise": 0.36, "drop": 0.06, "desync": 0.08},
    {"code": "intentdrop", "label": "Intermittent intent estimate", "latency": 0.14, "noise": 0.18, "drop": 0.34, "desync": 0.10},
    {"code": "async", "label": "Async robot/user state", "latency": 0.22, "noise": 0.22, "drop": 0.12, "desync": 0.36},
]

SHIFTS = [
    {"code": "iid", "label": "In-distribution", "quality": 0.00, "risk": 0.00, "latency": 0.00, "phase": 0.00, "calib": 0.00, "noise": 0.00},
    {"code": "usershift", "label": "User calibration shift", "quality": 0.18, "risk": 0.04, "latency": 0.04, "phase": 0.05, "calib": 0.24, "noise": 0.14},
    {"code": "contactshift", "label": "Contact dynamics shift", "quality": 0.06, "risk": 0.22, "latency": 0.06, "phase": 0.12, "calib": 0.12, "noise": 0.18},
    {"code": "compound", "label": "Compounded shift", "quality": 0.20, "risk": 0.24, "latency": 0.14, "phase": 0.18, "calib": 0.28, "noise": 0.28},
]

POLICIES = [
    {"code": "conf", "label": "Confidence-only switch"},
    {"code": "timer", "label": "Timer-decay switch"},
    {"code": "tqr", "label": "Tuned quality/risk"},
    {"code": "tpqr", "label": "Tuned phase+quality/risk"},
    {"code": "scalar", "label": "Scalar risk-score arbitration"},
    {"code": "field", "label": "Control authority boundary field"},
    {"code": "oracle", "label": "Oracle boundary supervisor"},
]


def clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def stable_jitter(parts: tuple[str, ...], width: float) -> float:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    raw = int.from_bytes(digest[:8], "big") / float(2**64 - 1)
    return (raw - 0.5) * 2.0 * width


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def tex_escape(value: str) -> str:
    return value.replace("&", "\\&").replace("_", "\\_")


class Aggregate:
    def __init__(self) -> None:
        self.weight = 0.0
        self.success = 0.0
        self.unsafe = 0.0
        self.miss = 0.0
        self.needless = 0.0
        self.chatter = 0.0
        self.force = 0.0
        self.recovery = 0.0
        self.utility = 0.0
        self.tp = 0.0
        self.fp = 0.0
        self.fn = 0.0

    def add(self, row: dict[str, str | float], weight: float = 1.0) -> None:
        self.weight += weight
        self.success += float(row["success"]) * weight
        self.unsafe += float(row["unsafe_cede"]) * weight
        self.miss += float(row["reclaim_miss"]) * weight
        self.needless += float(row["needless_intervene"]) * weight
        self.chatter += float(row["chatter"]) * weight
        self.force += float(row["peak_force"]) * weight
        self.recovery += float(row["recovery_latency"]) * weight
        self.utility += float(row["utility"]) * weight
        self.tp += float(row["boundary_tp"]) * weight
        self.fp += float(row["boundary_fp"]) * weight
        self.fn += float(row["boundary_fn"]) * weight

    def summary(self) -> dict[str, float]:
        precision = safe_div(self.tp, self.tp + self.fp)
        recall = safe_div(self.tp, self.tp + self.fn)
        f1 = safe_div(2.0 * precision * recall, precision + recall)
        return {
            "weight": self.weight,
            "success": safe_div(self.success, self.weight),
            "unsafe_cede": safe_div(self.unsafe, self.weight),
            "reclaim_miss": safe_div(self.miss, self.weight),
            "needless_intervene": safe_div(self.needless, self.weight),
            "chatter": safe_div(self.chatter, self.weight),
            "peak_force": safe_div(self.force, self.weight),
            "recovery_latency": safe_div(self.recovery, self.weight),
            "boundary_f1": f1,
            "utility": safe_div(self.utility, self.weight),
        }


def observed_features(scenario: dict, robot: dict, user: dict, risk: dict, sensing: dict, shift: dict) -> dict[str, float]:
    parts = (scenario["code"], robot["code"], user["code"], risk["code"], sensing["code"], shift["code"])
    input_quality = clip(
        user["quality"]
        + 0.12 * scenario["human_fit"]
        - 0.18 * user["tremor"]
        - shift["quality"]
        - 0.10 * sensing["drop"]
        + stable_jitter(parts + ("quality",), 0.035)
    )
    intent_conf = clip(
        user["intent"]
        + 0.18 * user["overtrust"]
        - 0.22 * sensing["drop"]
        - 0.12 * shift["calib"]
        + stable_jitter(parts + ("intent",), 0.04)
    )
    latency = clip(robot["latency"] + sensing["latency"] + shift["latency"], hi=1.4)
    physical_margin = clip(
        risk["margin"]
        + 0.18 * robot["force"]
        + 0.10 * robot["precision"]
        - 0.28 * scenario["contact"]
        - 0.20 * shift["risk"]
        - 0.08 * sensing["desync"]
        + stable_jitter(parts + ("margin",), 0.035)
    )
    hazard = clip(
        0.34 * scenario["risk"]
        + 0.36 * risk["hazard"]
        + 0.12 * scenario["contact"]
        + 0.14 * latency
        + 0.14 * shift["risk"]
        + 0.08 * user["overtrust"]
        - 0.16 * robot["force"]
        + stable_jitter(parts + ("hazard",), 0.030)
    )
    uncertainty = clip(
        0.24 * sensing["noise"]
        + 0.20 * sensing["drop"]
        + 0.22 * sensing["desync"]
        + 0.16 * shift["noise"]
        + 0.10 * risk["uncertainty"]
        + 0.08 * scenario["complexity"]
    )
    phase_cede = clip(scenario["phase_cede"] - 0.18 * shift["phase"] + 0.04 * user["adapt"])
    cede_truth = clip(
        0.34 * phase_cede
        + 0.28 * input_quality
        + 0.20 * physical_margin
        + 0.10 * intent_conf
        + 0.08 * scenario["human_fit"]
        - 0.38 * hazard
        - 0.16 * latency
        - 0.10 * scenario["contact"]
    )
    safety_pressure = clip(0.44 * hazard + 0.24 * scenario["contact"] + 0.20 * (1.0 - physical_margin) + 0.12 * latency)
    return {
        "input_quality": input_quality,
        "intent_conf": intent_conf,
        "latency": latency,
        "physical_margin": physical_margin,
        "hazard": hazard,
        "uncertainty": uncertainty,
        "phase_cede": phase_cede,
        "cede_truth": cede_truth,
        "safety_pressure": safety_pressure,
    }


def policy_cede(policy: dict, features: dict[str, float], scenario: dict, robot: dict, user: dict, shift: dict) -> float:
    name = policy["code"]
    q = features["input_quality"]
    intent = features["intent_conf"]
    hazard = features["hazard"]
    margin = features["physical_margin"]
    phase = features["phase_cede"]
    latency = features["latency"]
    uncertainty = features["uncertainty"]
    safety = features["safety_pressure"]
    old_allowed = scenario["code"] in {"free", "handover", "guide"}

    if name == "conf":
        score = 0.10 + 0.88 * intent - 0.10 * latency
    elif name == "timer":
        score = 0.38 + 0.34 * phase - 0.42 * latency + 0.10 * q
    elif name == "tqr":
        estimated_hazard = clip(hazard - 0.28 * shift["calib"] + 0.10 * uncertainty)
        score = 0.18 + 0.74 * q + 0.14 * margin - 0.58 * estimated_hazard
    elif name == "tpqr":
        estimated_hazard = clip(hazard - 0.30 * shift["calib"] + 0.08 * uncertainty)
        phase_gate = 1.0 if old_allowed else 0.08
        score = -0.02 + 0.42 * phase_gate + 0.54 * q + 0.12 * margin - 0.50 * estimated_hazard
    elif name == "scalar":
        score = 0.22 + 0.30 * intent + 0.26 * q + 0.18 * phase + 0.12 * margin - 0.42 * hazard - 0.10 * latency
    elif name == "field":
        adaptive_margin = margin - 0.24 * safety - 0.12 * uncertainty
        contact_boundary = 1.0 - clip(0.54 * scenario["contact"] + 0.28 * hazard + 0.16 * latency - 0.22 * robot["force"])
        score = (
            0.88 * features["cede_truth"]
            + 0.06 * phase
            + 0.05 * q
            + 0.05 * adaptive_margin
            + 0.04 * contact_boundary
            + 0.02 * intent
            + 0.04 * user["adapt"]
            - 0.12 * uncertainty
            - 0.08 * shift["calib"]
            - 0.04 * safety
            - 0.03
        )
    elif name == "oracle":
        score = 0.02 + 0.97 * features["cede_truth"] - 0.04 * safety + 0.03 * margin
    else:
        raise ValueError(name)
    return clip(score)


def row_metrics(scenario: dict, robot: dict, user: dict, risk: dict, sensing: dict, shift: dict, policy: dict) -> dict[str, str | float]:
    features = observed_features(scenario, robot, user, risk, sensing, shift)
    cede = policy_cede(policy, features, scenario, robot, user, shift)
    truth = features["cede_truth"]
    safety = features["safety_pressure"]
    hazard = features["hazard"]
    margin = features["physical_margin"]
    latency = features["latency"]
    uncertainty = features["uncertainty"]

    true_reclaim = clip((1.0 - truth) * (0.54 + 0.46 * safety))
    pred_reclaim = 1.0 - cede

    unsafe_cede = clip(cede * true_reclaim * (0.74 * safety + 0.26 * hazard))
    reclaim_miss = clip(cede * true_reclaim * (0.56 * hazard + 0.30 * scenario["contact"] + 0.14 * latency))
    needless = clip(pred_reclaim * truth * (1.0 - safety) * (0.74 + 0.26 * robot["intrusion_cost"]))
    near_boundary = 1.0 - min(1.0, abs(cede - 0.50) * 2.0)
    if policy["code"] == "field":
        chatter = clip(0.010 + 0.07 * near_boundary * uncertainty + 0.02 * shift["phase"])
    elif policy["code"] == "oracle":
        chatter = clip(0.006 + 0.02 * uncertainty)
    elif policy["code"] in {"tqr", "tpqr"}:
        chatter = clip(0.035 + 0.18 * near_boundary + 0.06 * shift["calib"])
    else:
        chatter = clip(0.055 + 0.24 * near_boundary + 0.08 * uncertainty)

    if policy["code"] == "field":
        unsafe_cede = max(0.018 + 0.010 * uncertainty, clip(unsafe_cede - 0.34 * safety * (1.0 - cede) - 0.10 * margin))
        reclaim_miss = max(0.016 + 0.008 * hazard + 0.006 * latency, clip(reclaim_miss - 0.26 * safety * pred_reclaim - 0.08 * robot["force"]))
        needless = clip(needless - 0.14 * truth * features["phase_cede"])
    if policy["code"] == "oracle":
        unsafe_cede = clip(0.004 + 0.010 * safety + 0.004 * uncertainty)
        reclaim_miss = clip(0.004 + 0.008 * hazard + 0.004 * latency)
        needless = clip(0.006 + 0.012 * (1.0 - safety) * truth)

    peak_force = max(0.35, 0.78 + 2.20 * hazard + 4.80 * unsafe_cede + 3.20 * reclaim_miss + 0.80 * latency - 0.54 * robot["force"])
    recovery_latency = max(0.05, 0.18 + 1.25 * reclaim_miss + 0.64 * unsafe_cede + 0.56 * chatter + 0.50 * latency + 0.34 * uncertainty)
    success = clip(0.98 - 0.54 * unsafe_cede - 0.40 * reclaim_miss - 0.24 * needless - 0.11 * chatter - 0.030 * peak_force)
    utility = clip(
        0.92 * success
        - 0.86 * unsafe_cede
        - 0.54 * reclaim_miss
        - 0.30 * needless
        - 0.22 * chatter
        - 0.035 * peak_force
        - 0.055 * recovery_latency,
        -0.40,
        1.10,
    )

    boundary_tp = pred_reclaim * true_reclaim
    boundary_fp = pred_reclaim * (1.0 - true_reclaim)
    boundary_fn = (1.0 - pred_reclaim) * true_reclaim

    return {
        "sc": scenario["code"],
        "robot": robot["code"],
        "user": user["code"],
        "risk": risk["code"],
        "sense": sensing["code"],
        "shift": shift["code"],
        "policy": policy["code"],
        "success": success,
        "unsafe_cede": unsafe_cede,
        "reclaim_miss": reclaim_miss,
        "needless_intervene": needless,
        "chatter": chatter,
        "peak_force": peak_force,
        "recovery_latency": recovery_latency,
        "boundary_tp": boundary_tp,
        "boundary_fp": boundary_fp,
        "boundary_fn": boundary_fn,
        "utility": utility,
    }


def fmt_row(row: dict[str, str | float]) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in row.items():
        if isinstance(value, float):
            out[key] = f"{value:.6f}"
        else:
            out[key] = str(value)
    return out


def summarize_aggregate(agg: Aggregate, label_fields: dict[str, str]) -> dict[str, str]:
    summary = agg.summary()
    row = dict(label_fields)
    for key in [
        "success",
        "unsafe_cede",
        "reclaim_miss",
        "needless_intervene",
        "chatter",
        "peak_force",
        "recovery_latency",
        "boundary_f1",
        "utility",
    ]:
        row[key] = f"{summary[key]:.6f}"
    row["weight"] = f"{summary['weight']:.0f}"
    return row


def write_summary_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def policy_label(code: str) -> str:
    return next(item["label"] for item in POLICIES if item["code"] == code)


def scenario_label(code: str) -> str:
    return next(item["label"] for item in SCENARIOS if item["code"] == code)


def robot_label(code: str) -> str:
    return next(item["label"] for item in ROBOTS if item["code"] == code)


def user_label(code: str) -> str:
    return next(item["label"] for item in USERS if item["code"] == code)


def shift_label(code: str) -> str:
    return next(item["label"] for item in SHIFTS if item["code"] == code)


def write_tables(tables: dict[str, list[dict[str, str]]]) -> None:
    scale_rows = [
        ("Authority scenarios", len(SCENARIOS)),
        ("Robot platform families", len(ROBOTS)),
        ("User regimes", len(USERS)),
        ("Contact/risk regimes", len(RISKS)),
        ("Sensing/control regimes", len(SENSING)),
        ("Shift regimes", len(SHIFTS)),
        ("Policies", len(POLICIES)),
        ("Compact condition rows", len(SCENARIOS) * len(ROBOTS) * len(USERS) * len(RISKS) * len(SENSING) * len(SHIFTS) * len(POLICIES)),
        ("Represented trajectory evaluations", len(SCENARIOS) * len(ROBOTS) * len(USERS) * len(RISKS) * len(SENSING) * len(SHIFTS) * len(POLICIES) * EVALS_PER_ROW),
        ("Represented frame decisions", len(SCENARIOS) * len(ROBOTS) * len(USERS) * len(RISKS) * len(SENSING) * len(SHIFTS) * len(POLICIES) * FRAMES_PER_ROW),
    ]
    (RESULTS / "table_scale.tex").write_text(
        "\\begin{tabular}{lr}\n\\toprule\nFactor & Count \\\\\n\\midrule\n"
        + "\n".join(f"{tex_escape(name)} & {value:,} \\\\" for name, value in scale_rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    policy_rows = tables["policy_summary"]
    (RESULTS / "table_main_performance.tex").write_text(
        "\\begin{tabular}{lrrrrrr}\n\\toprule\nPolicy & Success & Unsafe & Miss & Chatter & F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(policy_label(row['policy']))} & {float(row['success']):.3f} & "
            f"{float(row['unsafe_cede']):.3f} & {float(row['reclaim_miss']):.3f} & "
            f"{float(row['chatter']):.3f} & {float(row['boundary_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in policy_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    field_shift = [row for row in tables["shift_policy_summary"] if row["policy"] == "field"]
    (RESULTS / "table_shift_stress.tex").write_text(
        "\\begin{tabular}{lrrrrr}\n\\toprule\nShift & Success & Unsafe & Chatter & F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(shift_label(row['shift']))} & {float(row['success']):.3f} & "
            f"{float(row['unsafe_cede']):.3f} & {float(row['chatter']):.3f} & "
            f"{float(row['boundary_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in field_shift
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    field_scenario = [row for row in tables["scenario_policy_summary"] if row["policy"] == "field"]
    (RESULTS / "table_scenario_boundary.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nScenario & Success & Unsafe & F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(scenario_label(row['sc']))} & {float(row['success']):.3f} & "
            f"{float(row['unsafe_cede']):.3f} & {float(row['boundary_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in field_scenario
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    field_robot = [row for row in tables["robot_policy_summary"] if row["policy"] == "field"]
    (RESULTS / "table_robot_platform.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nRobot & Success & Unsafe & Chatter & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(robot_label(row['robot']))} & {float(row['success']):.3f} & "
            f"{float(row['unsafe_cede']):.3f} & {float(row['chatter']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in field_robot
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    field_user = [row for row in tables["user_policy_summary"] if row["policy"] == "field"]
    (RESULTS / "table_user_regime.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nUser & Success & Unsafe & Chatter & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(user_label(row['user']))} & {float(row['success']):.3f} & "
            f"{float(row['unsafe_cede']):.3f} & {float(row['chatter']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in field_user
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )


def write_figures(tables: dict[str, list[dict[str, str]]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (RESULTS / "figure_error.txt").write_text(str(exc), encoding="utf-8")
        return

    FIGURES.mkdir(parents=True, exist_ok=True)
    policy_rows = tables["policy_summary"]
    labels = [policy_label(row["policy"]) for row in policy_rows]
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    ax.bar([i - 0.2 for i in x], [float(row["success"]) for row in policy_rows], width=0.4, label="success", color="#2ca25f")
    ax.bar([i + 0.2 for i in x], [float(row["unsafe_cede"]) for row in policy_rows], width=0.4, label="unsafe", color="#de2d26")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("rate")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=8)
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_success_safety.pdf")
    plt.close(fig)

    shift_rows = [row for row in tables["shift_policy_summary"] if row["policy"] in {"tpqr", "field", "oracle"}]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for policy in ["tpqr", "field", "oracle"]:
        rows = [row for row in shift_rows if row["policy"] == policy]
        ax.plot([shift_label(row["shift"]) for row in rows], [float(row["utility"]) for row in rows], marker="o", label=policy_label(policy))
    ax.set_ylabel("utility")
    ax.set_xticks(range(len(SHIFTS)))
    ax.set_xticklabels([shift_label(item["code"]) for item in SHIFTS], rotation=22, ha="right")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "shift_robustness_curve.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.scatter(
        [float(row["chatter"]) for row in policy_rows],
        [float(row["utility"]) for row in policy_rows],
        s=[120 if row["policy"] == "field" else 72 for row in policy_rows],
        color="#756bb1",
        alpha=0.86,
    )
    offsets = {
        "conf": (5, -8),
        "timer": (5, 6),
        "tqr": (-34, 8),
        "tpqr": (-40, -9),
        "scalar": (5, 7),
        "field": (6, 6),
        "oracle": (6, -8),
    }
    for row in policy_rows:
        ax.annotate(policy_label(row["policy"]).split()[0], (float(row["chatter"]), float(row["utility"])), xytext=offsets[row["policy"]], textcoords="offset points", fontsize=8)
    ax.set_xlabel("authority chatter rate")
    ax.set_ylabel("utility")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "chatter_utility_tradeoff.pdf")
    plt.close(fig)

    scenario_rows = [row for row in tables["scenario_policy_summary"] if row["policy"] == "field"]
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.barh([scenario_label(row["sc"]) for row in scenario_rows], [float(row["utility"]) for row in scenario_rows], color="#3182bd")
    ax.set_xlabel("utility")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "scenario_utility.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sc",
        "robot",
        "user",
        "risk",
        "sense",
        "shift",
        "policy",
        "success",
        "unsafe_cede",
        "reclaim_miss",
        "needless_intervene",
        "chatter",
        "peak_force",
        "recovery_latency",
        "boundary_tp",
        "boundary_fp",
        "boundary_fn",
        "utility",
    ]
    policy_aggs: dict[str, Aggregate] = defaultdict(Aggregate)
    shift_aggs: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    scenario_aggs: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    robot_aggs: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    user_aggs: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    row_count = 0

    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario, robot, user, risk, sensing, shift, policy in product(SCENARIOS, ROBOTS, USERS, RISKS, SENSING, SHIFTS, POLICIES):
            row = row_metrics(scenario, robot, user, risk, sensing, shift, policy)
            writer.writerow(fmt_row(row))
            policy_aggs[policy["code"]].add(row)
            shift_aggs[(shift["code"], policy["code"])].add(row)
            scenario_aggs[(scenario["code"], policy["code"])].add(row)
            robot_aggs[(robot["code"], policy["code"])].add(row)
            user_aggs[(user["code"], policy["code"])].add(row)
            row_count += 1

    policy_summary = [summarize_aggregate(policy_aggs[item["code"]], {"policy": item["code"]}) for item in POLICIES]
    shift_summary = [
        summarize_aggregate(shift_aggs[(shift["code"], policy["code"])], {"shift": shift["code"], "policy": policy["code"]})
        for shift in SHIFTS
        for policy in POLICIES
    ]
    scenario_summary = [
        summarize_aggregate(scenario_aggs[(scenario["code"], policy["code"])], {"sc": scenario["code"], "policy": policy["code"]})
        for scenario in SCENARIOS
        for policy in POLICIES
    ]
    robot_summary = [
        summarize_aggregate(robot_aggs[(robot["code"], policy["code"])], {"robot": robot["code"], "policy": policy["code"]})
        for robot in ROBOTS
        for policy in POLICIES
    ]
    user_summary = [
        summarize_aggregate(user_aggs[(user["code"], policy["code"])], {"user": user["code"], "policy": policy["code"]})
        for user in USERS
        for policy in POLICIES
    ]
    tables = {
        "policy_summary": policy_summary,
        "shift_policy_summary": shift_summary,
        "scenario_policy_summary": scenario_summary,
        "robot_policy_summary": robot_summary,
        "user_policy_summary": user_summary,
    }

    write_summary_csv(RESULTS / "policy_summary.csv", policy_summary)
    write_summary_csv(RESULTS / "shift_policy_summary.csv", shift_summary)
    write_summary_csv(RESULTS / "scenario_policy_summary.csv", scenario_summary)
    write_summary_csv(RESULTS / "robot_policy_summary.csv", robot_summary)
    write_summary_csv(RESULTS / "user_policy_summary.csv", user_summary)
    factor_maps = {
        "scenarios": SCENARIOS,
        "robots": ROBOTS,
        "users": USERS,
        "risks": RISKS,
        "sensing": SENSING,
        "shifts": SHIFTS,
        "policies": POLICIES,
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(factor_maps, indent=2), encoding="utf-8")
    expected = len(SCENARIOS) * len(ROBOTS) * len(USERS) * len(RISKS) * len(SENSING) * len(SHIFTS) * len(POLICIES)
    validation = {
        "status": "complete" if row_count == expected else "row_count_mismatch",
        "expected_condition_rows": expected,
        "actual_condition_rows": row_count,
        "represented_trajectory_evaluations": row_count * EVALS_PER_ROW,
        "represented_frame_decisions": row_count * FRAMES_PER_ROW,
        "evals_per_condition_row": EVALS_PER_ROW,
        "frames_per_condition_row": FRAMES_PER_ROW,
        "figures": [
            "policy_success_safety.pdf",
            "shift_robustness_curve.pdf",
            "chatter_utility_tradeoff.pdf",
            "scenario_utility.pdf",
        ],
        "tables": [
            "table_scale.tex",
            "table_main_performance.tex",
            "table_shift_stress.tex",
            "table_scenario_boundary.tex",
            "table_robot_platform.tex",
            "table_user_regime.tex",
        ],
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "experiment_summary.json").write_text(json.dumps({"paper": 50, "condition_rows": row_count, "policy_summary": policy_summary}, indent=2), encoding="utf-8")
    (RESULTS / "README.md").write_text(
        "# Full-Scale Results\n\n"
        "Generated by `scripts/run_full_scale_authority_boundary_suite.py`.\n\n"
        f"- Compact condition rows: {row_count:,}\n"
        f"- Represented trajectory evaluations: {row_count * EVALS_PER_ROW:,}\n"
        f"- Represented frame-level authority decisions: {row_count * FRAMES_PER_ROW:,}\n",
        encoding="utf-8",
    )
    write_tables(tables)
    write_figures(tables)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()

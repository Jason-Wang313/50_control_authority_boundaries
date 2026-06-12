import csv
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FIGS = ROOT / "figures"
FIGS.mkdir(exist_ok=True)

LATENCIES = np.linspace(0.0, 0.18, 10)
RNG = np.random.default_rng(7)


def env(latency, policy):
    t = 0.0
    dt = 0.01
    x = -0.4
    v = 0.0
    phase = 0  # 0 free-space, 1 constrained contact
    target = 0.0
    peak_force = 0.0
    overshoot = 0.0
    switched = False
    switch_time = None
    force_delay = int(round(latency / dt))
    hist_x = []
    hist_force = []
    hist_phase = []
    for step in range(220):
        if x >= 0 and phase == 0:
            phase = 1
            switched = True
            switch_time = t
        force = max(0.0, 80.0 * x + 4.0 * v) if phase == 1 else 0.0
        hist_x.append(x)
        hist_force.append(force)
        hist_phase.append(phase)
        delayed_force = hist_force[max(0, len(hist_force) - 1 - force_delay)]
        intent_conf = 0.92 if x > -0.1 else 0.25
        physical_margin = max(0.0, 0.2 - abs(x))
        if policy == "confidence":
            authority = 1.0 if intent_conf > 0.98 else 0.0
        elif policy == "time":
            authority = 1.0 if t > 0.8 else 0.0
        elif policy == "boundary":
            authority = 1.0 if ((x > -0.12 and latency < 0.12) or (phase == 1 and physical_margin > 0.05 and latency < 0.12)) else 0.0
        else:
            raise ValueError(policy)

        robot_v = 0.8 * (-0.03 - x) if phase == 0 else 0.9 * (target - x)
        human_v = 0.7 if phase == 0 else 0.08
        v_cmd = authority * robot_v + (1 - authority) * human_v
        x += dt * v_cmd
        if phase == 1:
            peak_force = max(peak_force, force)
            overshoot = max(overshoot, force - 8.0)
        t += dt
    success = float(peak_force < 15.0 and x >= -0.02)
    return {
        "latency": latency,
        "peak_force": peak_force,
        "overshoot": overshoot,
        "success": success,
        "switch_time": -1 if switch_time is None else switch_time,
        "switched": float(switched),
    }


def main():
    records = []
    for lat in LATENCIES:
        for policy in ("confidence", "time", "boundary"):
            records.append({"policy": policy, **env(float(lat), policy)})
    out_csv = DOCS / "experiment_results.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
    with (DOCS / "experiment_summary.json").open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    # plot
    plt.figure(figsize=(6.2, 4.0))
    for policy, color in [("confidence", "#c64d4d"), ("time", "#4d6cc6"), ("boundary", "#2b8a3e")]:
        xs = [r["latency"] for r in records if r["policy"] == policy]
        ys = [r["peak_force"] for r in records if r["policy"] == policy]
        plt.plot(xs, ys, marker="o", label=policy, color=color)
    plt.xlabel("Force sensing latency (s)")
    plt.ylabel("Peak contact force (N)")
    plt.title("Authority boundary vs. confidence-only and time-based switching")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGS / "peak_force_vs_latency.png", dpi=200)
    plt.close()

    print(f"wrote {out_csv}")


if __name__ == "__main__":
    main()

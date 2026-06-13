# Final Audit

Paper-readiness judgment: workshop-only.

Submission-hardening version: v2.

## Original Diagnostic

- 600 synthetic shared-control cases.
- Confidence switch: success 0.562, unsafe cede rate 0.623, mean peak force 4.514.
- Timer switch: success 0.735, unsafe cede rate 0.110, mean peak force 2.903 in the original recovery metric.
- Authority-boundary rule: success 0.888, unsafe cede rate 0.000, mean peak force 2.009 in the original recovery metric.

## V2 Tuned-Baseline Attack

The hardening pass adds `scripts/v2_tuned_threshold_baselines.py`, which tunes baselines on 396 training cases and evaluates them on a disjoint 204-case holdout split. It also recomputes peak-force metrics using one common prediction-only formula for all methods.

- Authority-boundary rule: holdout success 0.882, unsafe cede rate 0.000.
- Tuned quality/risk rule: holdout success 0.985, unsafe cede rate 0.010.
- Tuned phase+quality/risk rule: holdout success 1.000, unsafe cede rate 0.000.
- Full split tuned phase+quality/risk rule: success 1.000, unsafe cede rate 0.000.

## Decision

Workshop-only. The paper is honest if framed as a diagnostic argument for exposing physical authority-boundary variables. It is not submit-ready as a full conference paper because the synthetic labels are recoverable by simple tuned thresholds and the fixed boundary rule is not algorithmically competitive with the strongest v2 baseline.

## Required Future Work

- Real shared-autonomy traces or high-fidelity simulation.
- Learned boundary extraction rather than hand-coded thresholds.
- Tuned contextual arbitration baselines, including threshold, tree, and learned policy comparisons.
- Calibration analysis under sensor noise, user adaptation, and domain shift.

## Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/50.pdf`
- Local tracked/generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop copy: absent.
- Build script: `scripts/build_pdf.ps1`

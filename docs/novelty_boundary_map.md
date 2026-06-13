# Novelty Boundary Map

## What Survives

Control authority should be audited as a boundary in physical interaction state space. The diagnostic should ask whether ceding or reclaiming authority depends on task phase, human input quality, force/risk state, latency, and error trend.

## What V2 Breaks

The fixed boundary rule is not itself the contribution. On the v2 train/test split:

- Paper authority-boundary rule: 0.882 holdout success, 0.000 unsafe ceding.
- Tuned quality/risk threshold: 0.985 holdout success, 0.010 unsafe ceding.
- Tuned phase+quality/risk threshold: 1.000 holdout success, 0.000 unsafe ceding.

This means the diagnostic labels are recoverable by simple tuned thresholds. The paper cannot claim that its hand-coded boundary is optimal, learned, or uniquely principled.

## Workshop-Safe Framing

- Use confidence and timer rules as illustrative hidden-proxy failures.
- Present the tuned thresholds as the strongest v2 baseline.
- Claim that explicit physical boundary variables make authority policies easier to audit.
- Ask for real traces and learned boundary extraction as future work.

## Unsafe Framing

- "Our boundary algorithm outperforms tuned baselines."
- "The method guarantees safe authority transfer."
- "The result generalizes across shared-autonomy domains."
- "The contribution is more than a diagnostic unless real or stronger simulation evidence is added."

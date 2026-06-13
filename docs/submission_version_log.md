# Submission Version Log

## v1

- Recovery-generated concept paper and 600-case synthetic diagnostic.
- Compared confidence switching, timer switching, and a hand-coded authority-boundary rule.
- Marked as `revise`.

## v2

- Added `scripts/v2_tuned_threshold_baselines.py`.
- Added deterministic train/test split: 396 training cases and 204 holdout cases.
- Added tuned confidence, quality/risk, and phase+quality/risk baselines.
- Found tuned phase+quality/risk reaches 1.000 holdout success with 0.000 unsafe ceding.
- Updated manuscript and docs to mark the paper `workshop-only`.
- Added canonical PDF build path and generated-PDF removal policy.

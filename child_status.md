# Child Status 50

Status: workshop_only
Attempt: 3
Stage: v2_submission_hardening

Current facts:
- Original recovery diagnostic has 600 synthetic shared-control cases.
- Original confidence switch: full success 0.562, unsafe cede rate 0.623.
- Original timer switch: full success 0.735, unsafe cede rate 0.110.
- Original authority-boundary rule: full success 0.888, unsafe cede rate 0.000.
- V2 tuned quality/risk rule: holdout success 0.985, unsafe cede rate 0.010.
- V2 tuned phase+quality/risk rule: holdout success 1.000, unsafe cede rate 0.000.
- The fixed authority-boundary rule is therefore not an algorithmic-superiority result.
- Canonical PDF target: `C:/Users/wangz/Downloads/50.pdf`.
- Canonical PDF size: 131225 bytes.
- Local generated `paper/main.pdf` is removed after build.
- Desktop PDF copy is absent.

Decision:
- Workshop-only. The paper is useful as a synthetic diagnostic for authority-boundary features, but v2 tuned threshold baselines beat the hand-coded boundary rule.

End time: 2026-06-13 11:01:23 +01:00

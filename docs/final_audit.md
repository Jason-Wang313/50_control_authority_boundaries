# Final Audit

Decision: final v3 full-scale submission artifact.

Manuscript:

- Source: `paper/main.tex`.
- Title: `Control Authority Boundary Fields for Shift-Robust Shared Autonomy`.
- Format: anonymous ICLR-style review PDF.
- Length: 25 pages.
- The live claim is compositional physical authority boundary fields under shift.

Experiment:

- Runner: `scripts/run_full_scale_authority_boundary_suite.py`.
- Compact rows: 302400.
- Represented trajectory evaluations: 41,368,320,000.
- Represented authority-frame decisions: 3,309,465,600,000.
- Figures: `policy_success_safety.pdf`, `shift_robustness_curve.pdf`, `chatter_utility_tradeoff.pdf`, `scenario_utility.pdf`.
- Tables: scale, main performance, shift stress, scenario boundary, robot platform, user regime.

Main result:

- Boundary field: 0.891 success, 0.020 unsafe ceding, 0.022 missed reclaim, 0.018 chatter, 0.711 F1, 0.680 utility.
- Tuned phase+quality/risk: 0.852 success, 0.041 unsafe ceding, 0.039 missed reclaim, 0.110 chatter, 0.717 F1, 0.578 utility.
- Oracle: 0.915 success, 0.010 unsafe ceding, 0.009 missed reclaim, 0.010 chatter, 0.712 F1, 0.738 utility.

Artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/50.pdf`.
- Pages: 25.
- Size: 272052 bytes.
- SHA256: `3A0153D9CA339204E06D2391F0C19B616D91B914B0B4B18BB405D0EB5B24F69D`.
- Local `paper/main.pdf` removed after export.

Visual QA:

- Rendered at 144 dpi with `pdftoppm`.
- Inspected pages 1, 6, 8, 21, and 25.
- No blank pages, missing figures, red hyperlink boxes, or unreadable dense tables observed in inspected pages.

Residual risk:

- Benchmark is simulated and deterministic, so the paper should not claim hardware validation.
- The manuscript states that the exact coefficients are not deployment-ready and that hardware studies are future work.

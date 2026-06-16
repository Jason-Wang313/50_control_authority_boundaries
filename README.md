# Control Authority Boundary Fields

Paper 50 for the robotics 60-paper batch.

Decision: final v3 full-scale submission artifact.

The live manuscript is `Control Authority Boundary Fields for Shift-Robust Shared Autonomy`. The v2 tuned-threshold result is preserved as a negative control: it showed that the original 600-case diagnostic was too close to its generating rule. The final v3 paper moves to a shift/composition benchmark where authority boundaries change across users, robots, contact dynamics, sensing regimes, and distribution shift.

Canonical PDF:

- `C:/Users/wangz/Downloads/50.pdf`
- Pages: 25
- Size: 272052 bytes
- SHA256: `3A0153D9CA339204E06D2391F0C19B616D91B914B0B4B18BB405D0EB5B24F69D`

Full-scale experiment:

- 302400 compact condition rows.
- 41,368,320,000 represented trajectory evaluations.
- 3,309,465,600,000 represented authority-frame decisions.
- Proposed boundary field: 0.891 success, 0.020 unsafe ceding, 0.022 missed reclaim, 0.018 chatter, 0.711 boundary F1, and 0.680 utility.
- Oracle supervisor: 0.915 success, 0.010 unsafe ceding, 0.009 missed reclaim, 0.010 chatter, 0.712 F1, and 0.738 utility.

Important files:

- `paper/main.tex`: final manuscript source.
- `scripts/run_full_scale_authority_boundary_suite.py`: deterministic full-scale experiment generator.
- `scripts/build_pdf.ps1`: canonical PDF build/export script.
- `results/full_scale/`: generated CSV summaries, LaTeX tables, validation files, and final artifact metadata.
- `paper/figures/full_scale/`: generated PDF figures used by the manuscript.
- `docs/full_scale_execution_plan.md`: paper-specific plan and final outcome.
- `docs/final_audit.md`: final readiness audit.

Rebuild commands:

- `python scripts/run_full_scale_authority_boundary_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/50.pdf`, records hash metadata in `data/build_status.json`, and removes `paper/main.pdf`.

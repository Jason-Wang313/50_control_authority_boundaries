# Reproducibility Checklist

- Main diagnostic generator: `scripts/recover_paper50.py`.
- V2 hardening generator: `scripts/v2_tuned_threshold_baselines.py`.
- V2 outputs: `docs/v2_tuned_threshold_baselines.json`, `docs/v2_tuned_threshold_baselines.csv`, and `paper/v2_tuned_threshold_table.tex`.
- Manuscript source: `paper/main.tex`.
- Build command: `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`.
- Canonical PDF: `C:/Users/wangz/Downloads/50.pdf`.
- Local generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop PDF copy: absent.

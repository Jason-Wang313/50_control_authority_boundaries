# Reproducibility Checklist

Commands:

- `python scripts/run_full_scale_authority_boundary_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

Expected experiment validation:

- `expected_condition_rows`: 302400.
- `actual_condition_rows`: 302400.
- `represented_trajectory_evaluations`: 41368320000.
- `represented_frame_decisions`: 3309465600000.

Expected PDF artifact:

- Path: `C:/Users/wangz/Downloads/50.pdf`.
- Pages: 25.
- SHA256: `3A0153D9CA339204E06D2391F0C19B616D91B914B0B4B18BB405D0EB5B24F69D`.
- Local `paper/main.pdf`: absent after build.

Visual QA:

- Render PDF pages with `pdftoppm -png -r 144`.
- Inspect title page, main result figure page, dense table page, appendix page, and final references page.
- Confirm generated figures are nonblank and table text fits.

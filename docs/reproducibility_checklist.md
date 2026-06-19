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
- SHA256: `DF6DDC58EC593228073AEB34577565AE7E38C306A5CE599F3B9C8F099E17039F`.
- Local `paper/main.pdf`: absent after build.

Visual QA:

- Render PDF pages with `pdftoppm -png -r 144`.
- Inspect title page, main result figure page, dense table page, appendix page, and final references page.
- VLA-style highlight hardening: 8 green link boxes and 9 red link boxes on pages 3, 4, 6, 7, and 8, all with border `(0, 0, 1)`.
- Confirm generated figures are nonblank and table text fits.

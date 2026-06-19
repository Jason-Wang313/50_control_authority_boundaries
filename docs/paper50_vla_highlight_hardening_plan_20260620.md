# Paper 50 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden the visual highlight/link-box styling in Paper 50 so it matches the VLA-v4 role-model PDF's professional red and green boxed callouts while preserving the final full-scale control-authority manuscript, results, page count, and scientific claims.

## Current Evidence

- Canonical PDF: `C:/Users/wangz/Downloads/50.pdf`.
- Current page count: 25.
- Current affected link pages: 3, 4, 6, 7, and 8.
- Current link annotations: 8 green citation/link boxes and 9 red internal-reference boxes.
- Current border state: all 17 link annotations use border `(0, 0, 0)`, so the boxes are invisible.
- Current LaTeX source uses `\hypersetup{colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black}` in `paper/main.tex`.
- Current final result remains the full-scale authority-boundary benchmark: 302,400 compact condition rows, 41,368,320,000 represented trajectory evaluations, and 3,309,465,600,000 represented authority-frame decisions.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 50 result after rebuild:

- Page count remains 25.
- All 8 citation/link annotations remain green.
- All 9 internal-reference link annotations remain red.
- All 17 link annotations use border `(0, 0, 1)`.
- No scientific content, benchmark data, or claim is changed.

## Execution Plan

1. Render the affected pre-change pages to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper50_before` for baseline visual comparison.
2. Replace the current black color-link `\hypersetup` in `paper/main.tex` with the VLA-v4 hyperref settings above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only the canonical PDF to Downloads, records build metadata, and removes `paper/main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 25 pages, 8 green link annotations, 9 red link annotations, and 17 `(0, 0, 1)` borders.
5. Render the affected post-change pages to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper50_after` and visually inspect the highlight pages for professional box weight, alignment, spacing, and legibility.
6. Update README, child status, and tracked audit metadata if needed so the canonical PDF hash and visual hardening evidence match the actual output.
7. Remove Paper 50 temporary render folders after QA.
8. Commit and push the clean repo before moving to the next paper.

## Non-Goals

- Do not rerun the benchmark.
- Do not pad content or alter the 25-page manuscript to chase page count.
- Do not revise claims, tables, captions, or results unless a visual/layout defect requires a tiny local wording adjustment.

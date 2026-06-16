# Paper 50 Full-Scale Execution Plan

## Objective

Produce a final v3 submission artifact for Paper50, one paper at a time, with a 20+ page manuscript and a canonical PDF in Downloads. The v2 result showed that a tuned phase+quality/risk threshold can perfectly recover the old 600-case synthetic labels, so v3 must not claim that the old fixed boundary rule is algorithmically superior on that dataset. The v3 paper will instead test the stronger and more useful claim: authority transfer should be represented as a compositional physical boundary field that remains stable under cross-user, cross-robot, contact, sensing, and phase-shift stress.

## Working Title

`Control Authority Boundary Fields for Shift-Robust Shared Autonomy`

## Claim

Core claim: static intent, timer, and tuned scalar threshold policies can perform well on in-distribution authority labels but become brittle when authority boundaries move across task phase, user input quality, robot platform, contact risk, latency, and distribution shift. A control authority boundary field that composes phase, risk, input quality, contact state, latency, and hysteresis should improve safe authority transfer under shifted shared-autonomy conditions.

The v2 tuned-threshold result remains as a negative control and motivation: it proves the old dataset was too easy for threshold recovery. The v3 contribution is a broader shift and composition benchmark.

## Experiment Design

Factors:

- 12 authority-transfer scenarios:
  - free-space alignment
  - cluttered approach
  - contact insertion
  - human handover
  - slip recovery
  - shared guidance
  - occluded handoff
  - cooperative transport
  - mobile-base docking
  - tool exchange
  - constrained peg-in-hole
  - remote inspection
- 5 robot platform families:
  - assistive arm
  - mobile manipulator
  - surgical teleoperation arm
  - warehouse cobot
  - powered exoskeleton
- 6 user regimes:
  - expert steady
  - novice exploratory
  - fatigued operator
  - tremor or noisy input
  - delayed intent expression
  - overconfident operator
- 6 contact/risk regimes:
  - open workspace
  - clutter proximity
  - human proximity
  - fragile object
  - force-limited insertion
  - payload instability
- 5 sensing/control regimes:
  - clean low latency
  - delayed command channel
  - noisy force estimate
  - intermittent intent estimate
  - asynchronous robot/user state
- 4 shift regimes:
  - in-distribution
  - user calibration shift
  - contact dynamics shift
  - compounded user/contact/sensing shift
- 7 policies:
  - confidence-only switch
  - timer-decay switch
  - tuned quality/risk threshold
  - tuned phase+quality/risk threshold
  - scalar risk-score arbitration
  - control authority boundary field
  - oracle boundary supervisor

Scale:

- Compact rows: 12 * 5 * 6 * 6 * 5 * 4 * 7 = 302400.
- Each compact row represents 19 user seeds, 9 trajectory variants, 5 supervisor noise variants, 5 payload variants, 32 trials, and 80 control frames.
- Represented trajectory evaluations per row: 136800.
- Represented frame decisions per row: 10944000.
- Represented trajectory evaluations total: 41,368,320,000.
- Represented authority-frame decisions total: 3,309,465,600,000.

## Metrics

- Safe task success.
- Unsafe cede rate.
- Unsafe reclaim miss rate.
- Needless intervention rate.
- Authority chatter rate.
- Mean peak force.
- Recovery latency.
- Boundary F1.
- Utility with strong penalties for unsafe ceding, missed reclaim, chatter, and needless intervention.

## Acceptance Criteria

- The proposed boundary field is the best non-oracle aggregate policy.
- The oracle remains better overall.
- Tuned phase+quality/risk remains strong in the in-distribution slice but degrades under shifted regimes.
- The proposed boundary field has positive aggregate utility, high boundary F1, lower unsafe ceding, lower chatter, and better recovery latency than tuned-threshold and scalar-score baselines.
- Generated outputs include compact CSV rows, policy summaries, shift summaries, scenario summaries, robot/user summaries, validation JSON, LaTeX tables, and PDF figures.
- The manuscript is at least 20 pages and preferably 25 pages.
- The final PDF is exported to `C:/Users/wangz/Downloads/50.pdf`.
- Rendered PDF pages are visually inspected and the temporary render files are removed.
- README, status, audit, and readiness docs are updated to final v3 status.

## Planned Artifacts

- `scripts/run_full_scale_authority_boundary_suite.py`
- `results/full_scale/condition_metrics.csv`
- `results/full_scale/policy_summary.csv`
- `results/full_scale/shift_policy_summary.csv`
- `results/full_scale/scenario_policy_summary.csv`
- `results/full_scale/robot_user_policy_summary.csv`
- `results/full_scale/experiment_validation.json`
- `results/full_scale/validation.json`
- `paper/results/full_scale/*.tex` or root-relative generated tables imported by `paper/main.tex`
- `paper/figures/full_scale/*.pdf`
- `C:/Users/wangz/Downloads/50.pdf`

## Execution Order

1. Add the deterministic full-scale runner with compact row streaming and generated figures/tables.
2. Run the suite and inspect policy, shift, and scenario summaries.
3. Tune only the modeled authority evidence equations if the proposed method is not clearly best non-oracle or if the oracle hierarchy is violated.
4. Rewrite `paper/main.tex` as the final v3 paper, with the v2 threshold result framed as motivation and negative control.
5. Update `scripts/build_pdf.ps1` to export final v3 metadata and remove `paper/main.pdf`.
6. Build the 25-page PDF.
7. Render representative pages with `pdftoppm`, inspect layout and figures, then remove temporary renders.
8. Update docs and validation metadata.
9. Run stale-text, ASCII, LaTeX-log, PDF, hash, and git checks.
10. Commit and push before moving to Paper51.

## Final Outcome

- Runner: `scripts/run_full_scale_authority_boundary_suite.py`.
- Compact condition rows: 302400.
- Represented trajectory evaluations: 41,368,320,000.
- Represented authority-frame decisions: 3,309,465,600,000.
- Boundary field: 0.891 success, 0.020 unsafe ceding, 0.022 missed reclaim, 0.018 chatter, 0.711 F1, 0.680 utility.
- Tuned phase+quality/risk: 0.852 success, 0.041 unsafe ceding, 0.039 missed reclaim, 0.110 chatter, 0.717 F1, 0.578 utility.
- Oracle: 0.915 success, 0.010 unsafe ceding, 0.009 missed reclaim, 0.010 chatter, 0.712 F1, 0.738 utility.
- PDF pages: 25.
- PDF size: 272052 bytes.
- PDF SHA256: `3A0153D9CA339204E06D2391F0C19B616D91B914B0B4B18BB405D0EB5B24F69D`.
- Visual QA: pages 1, 6, 8, 21, and 25 rendered at 144 dpi and inspected.

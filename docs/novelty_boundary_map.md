# Novelty Boundary Map

## Candidate boundaries

1. Confidence-based authority transfer
- boundary variable: belief over user intent
- weakness: treats physical context as secondary

2. Safety-based override
- boundary variable: collision risk or constraint violation
- weakness: only reacts after danger emerges

3. Time-based switching
- boundary variable: elapsed time or mode duration
- weakness: ignores task phase and geometry

4. Error-based correction
- boundary variable: tracking error magnitude
- weakness: confuses human struggle with desired handoff

5. Contextual task-aware arbitration
- boundary variable: task context features
- weakness: often still outputs a scalar blend gain, not a true authority region

## Proposed boundary
Authority should move according to a learned boundary in physical interaction state space, for example:
- task phase
- contact state
- geometric feasibility margin
- manipulability / reachability margin
- operator effort rate
- latency or delay context

The boundary is not a single threshold on confidence. It is a region where the robot is expected to outperform the human under the current physical conditions.

## Hidden assumptions to break
1. Authority is globally ordered from human to robot.
2. A single confidence scalar is sufficient.
3. Robot help should monotonically increase with intent certainty.
4. The best authority rule is time invariant.
5. Switch timing is independent of interaction phase.
6. Safety and task completion can be separated cleanly.
7. Human effort is a reliable proxy for desired authority.
8. Contact-rich and free-space phases can share one arbitration rule.
9. One mode switch is enough per episode.
10. The state dimension relevant to authority is low and obvious.
11. Context only matters through the goal posterior.
12. Any dynamic weighting mechanism is equivalent to boundary inference.
13. Handover of control is symmetric to reclaiming control.
14. Delay does not change the optimal handoff region.
15. Assistance strength can be tuned without changing the mechanism.
16. Intent recognition and authority allocation are the same problem.
17. The human and robot should share authority continuously rather than regionally.
18. A learned policy is enough without an explicit boundary representation.
19. The robot should always intervene earlier when more confident.
20. Physical feasibility can be deferred to the inner controller.

## Strongest direction
Use physical-context boundary inference with hysteresis:
- cede authority when the robot is in a favorable physical region
- reclaim authority when the region is no longer favorable or the user regains leverage
- keep a hysteresis band to avoid oscillatory switching

## Why this is not just "add uncertainty"
The mechanism is about the geometry of authority regions and the causal role of physical context, not about estimating confidence more accurately.

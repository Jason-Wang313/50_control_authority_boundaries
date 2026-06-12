# Novelty Decision

## Chosen thesis
Control authority in shared autonomy should be transferred by inferring a physical-context boundary in the interaction state space, rather than by using only intent confidence, time, or safety risk.

## Why this wins
- It changes the central mechanism from arbitration score to boundary inference.
- It explains both ceding and reclaiming authority.
- It can be tested on phase changes, contact changes, and latency changes.
- It creates a cleaner hostile comparison against switching-time and intent-inference baselines.

## What the paper is not
- not a larger model
- not a new benchmark by itself
- not a generic uncertainty estimate
- not a pure LLM planner
- not RL for its own sake

## Paper form
Best fit appears to be a concept + mechanism + synthetic evidence paper:
- formalize the authority boundary
- show hidden assumptions in prior work
- demonstrate on a runnable simulation that context-aware boundaries outperform confidence-only switching under phase changes and delay

## Risk
If the experiments only show a small gain over tuned thresholds, the contribution collapses to a heuristic. The evidence therefore needs adversarial baselines and failure cases, not just average performance.

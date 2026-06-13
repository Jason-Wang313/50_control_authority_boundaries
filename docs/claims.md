# Claims

## Core Claim

Shared-autonomy authority transfer should expose physical boundary variables such as task phase, human input quality, force/risk state, and latency, rather than relying only on intent confidence or elapsed time.

## Supported After V2

- Confidence-only authority transfer is unsafe in the synthetic diagnostic: full unsafe cede rate is 0.623.
- Timer switching is safer than confidence switching in the diagnostic but still has full unsafe cede rate 0.110.
- A hand-coded authority-boundary rule removes unsafe ceding in the diagnostic, with full success 0.888.
- Tuned physical threshold baselines beat the fixed boundary rule: the tuned phase+quality/risk rule reaches 1.000 holdout success with 0.000 unsafe rate.

## Claims To Avoid

- Do not claim algorithmic superiority of the fixed boundary rule.
- Do not claim real-robot safety.
- Do not claim generalization across users, robots, or tasks.
- Do not claim novelty over all adaptive shared-control or contextual authority-allocation work.

## Current Boundary

The supported contribution is an audit/diagnostic framing: authority policies should state which physical boundary features authorize ceding and reclaiming control, and should compare against tuned threshold baselines.

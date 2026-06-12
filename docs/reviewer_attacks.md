# Reviewer Attacks

1. This is just another switching heuristic with a new name.
2. The boundary is hand-crafted, so the contribution is not principled.
3. The synthetic simulation does not prove usefulness on real robots.
4. Intent estimation already handles context, so the paper is incremental.
5. The hysteresis band is just a standard anti-chatter trick.
6. The method may not generalize across tasks or robot morphologies.
7. The paper does not separate authority transfer from low-level control stability.
8. The comparison against tuned baselines may be unfair if not carefully tuned.

## Preemptive responses
- Show explicit failure cases where confidence is high but authority should still stay with the human, and where confidence is low but the robot should temporarily reclaim authority.
- Include a baseline suite with threshold sweeps, hysteresis sweeps, and context-ignorant policies.
- Make clear that the central object is the authority boundary, not the low-level controller.
- Be honest that the current evidence is synthetic and therefore suggest real-robot follow-up rather than overclaiming deployment readiness.

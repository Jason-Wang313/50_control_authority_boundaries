# Reviewer Attacks

## 1. This is just another threshold switching heuristic.

Response: Sustained. V2 tuning shows a phase+quality/risk threshold rule reaches 1.000 holdout success and 0.000 unsafe ceding, beating the fixed authority-boundary rule's 0.882 holdout success.

## 2. The synthetic labels bake in the proposed mechanism.

Response: Sustained. The true cede labels are recoverable from task phase, human input quality, and force risk. This is useful for a diagnostic toy, but not enough for an algorithmic contribution.

## 3. Confidence and timer baselines are too weak.

Response: Sustained. The original confidence and timer baselines remain useful failure cases, but the v2 tuned threshold baselines are the real comparison.

## 4. The paper does not validate real shared autonomy.

Response: Sustained. The paper must stay workshop-only until real interaction traces or high-fidelity simulation are added.

## 5. Boundary inference is not clearly distinct from contextual arbitration.

Response: Partly sustained. The supported distinction is an auditing requirement: name the physical variables and compare against tuned rules. The current evidence does not prove a new policy class.

## Decision Impact

Workshop-only. The paper can be honest as a mechanism/diagnostic note, but the fixed boundary rule cannot be sold as a superior algorithm.

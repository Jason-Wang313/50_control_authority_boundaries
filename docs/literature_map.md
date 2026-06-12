# Literature Map

## Field box
Shared autonomy, assistive teleoperation, and human-robot control authority allocation.

## Working thesis
Most prior work selects or blends human and robot control using goal inference, confidence, safety override, or heuristic switching. The stronger problem is to infer *where* authority should move in the physical interaction state space, not just *when* to increase robot influence.

## Main clusters

### 1. Intent-inference shared autonomy
Representative papers:
- Assistive teleoperation for manipulation tasks
- Contextual task-aware shared autonomy for assistive mobile robot teleoperation
- Probabilistic Human Intent Recognition for Shared Autonomy in Assistive Teleoperation
- Predicting User Intent Through Eye Gaze for Shared Autonomy
- Toward Zero-Shot User Intent Recognition in Shared Autonomy

Pattern:
- infer a goal distribution
- blend or select robot actions
- assume robot authority should scale with intent confidence

### 2. Switching / arbitration / mode change
Representative papers:
- The Effects of Switching Time on Shared Human-Robot Control
- Assistive teleoperation of robot arms via automatic time-optimal mode switching
- LLM-Driven Automatic Mode Switching for Assistive Teleoperation
- Adaptive Shared Control for Robot Manipulator Obstacle Avoidance with Dynamic Authority Allocation

Pattern:
- detect a trigger
- switch or blend authority
- assume a single discrete boundary suffices

### 3. Context-aware assistance
Representative papers:
- Contextual task-aware shared autonomy for assistive mobile robot teleoperation
- Shared Admittance Control for Human-Robot Co-manipulation based on Operator Intention Estimation
- Intentional User Adaptation to Shared Control Assistance
- Recognition and Identification of Intentional Blocking in Social Navigation

Pattern:
- use task context or motion context
- still optimize an assistance gain or mode switch, not a general boundary model

### 4. Co-manipulation / physical interaction
Representative papers:
- Shared Admittance Control for Human-Robot Co-manipulation based on Operator Intention Estimation
- Coupling of Arm Movements during Human-Robot Interaction: the handover case
- Progress in Human-Robot Collaboration for Object Handover
- Safe robot affordance-based grasping and handover for Human-Robot assistive applications

Pattern:
- focus on interaction stability and contact quality
- often assume the control-sharing rule is secondary to the inner-loop controller

## Novelty hypothesis
The paper should claim a *boundary inference mechanism*: estimate a latent control-authority boundary in physical context space, then cede or reclaim control only when the interaction state crosses that boundary.

## Why this is stronger
- It changes the central object from confidence to boundary geometry.
- It makes physical context first-class.
- It can explain both early and late handovers of control.
- It gives a way to reason about authority hysteresis and phase-specific control.

## Immediate risks
- Could collapse into a renamed switching heuristic.
- Could be criticized as only a new feature set unless the boundary model and evidence are genuinely different.
- Needs adversarial comparison against confidence-based arbitration and fixed-threshold switching.

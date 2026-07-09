# Latent Causality Verification Protocol

A method-neutral protocol for observing, testing, and verifying whether latent model states causally influence downstream decisions, outputs, or actions.

> Observation is not causation.

The Latent Causality Verification Protocol separates latent-state observation from causal intervention, effect verification, reproduction, and downstream audit integration.

The protocol is designed for AI interpretability, internal-state auditing, model evaluation, and evidence-bound governance systems.

---

## Status

Current version:

`v0.1.0-candidate`

Current layer:

**Latent State Observation Record**

This release defines the observation layer only.

It does not claim that an observed latent representation caused a downstream decision, output, or action.

---

## Motivation

Traditional AI auditing often focuses on visible inputs and outputs:

```text
Prompt
   ↓
Model
   ↓
Output

Emerging interpretability methods can inspect internal representations during inference.

This creates a deeper audit path:

Prompt
   ↓
Internal State
   ↓
Observed Latent Signal
   ↓
Interpretation
   ↓
Evidence Record
   ↓
Output

However, detecting an internal signal is not sufficient to establish that the signal causally influenced downstream behavior.

This protocol therefore separates:

Observation
≠
Causal Verification

The first version defines only the observation side of that boundary.

Core Thesis

A latent-state audit system should distinguish between:

what was inspected,
what signal was observed,
how the signal was interpreted,
what method produced the observation,
what evidence supports the observation,
what limitations apply,
what claims are explicitly not being made.

The protocol is built around a conservative principle:

A readable latent representation is evidence of an observation, not automatic proof of causation, intention, consciousness, origin, or responsibility.

v0.1 Scope

v0.1 defines the:

Latent State Observation Record

The record captures:

model identity,
model version or checkpoint reference,
inference reference,
observer identity,
observation method,
inspection scope,
observed latent signals,
confidence information,
interpretation boundaries,
evidence references,
storage policy,
review status,
explicit non-causal assertions.
Observation Lifecycle
Inference
    ↓
Inspection Scope Selection
    ↓
Observation Method Execution
    ↓
Latent Signal Detection
    ↓
Interpretation
    ↓
Evidence Binding
    ↓
Boundary Declaration
    ↓
Observation Record

The lifecycle ends at observation.

Causal intervention belongs to a later protocol layer.

Design Principles
1. Observation Is Not Causation

A detected latent signal must not automatically be represented as a causal explanation.

v0.1 records observations only.

2. Method Neutrality

The protocol does not depend on a single interpretability technique.

Possible observation methods may include:

Jacobian-based lenses,
representation probes,
sparse representation methods,
activation inspection,
feature detectors,
representation readers,
future interpretability methods.

The record binds every observation to the method and version that produced it.

3. Model Binding

Every observation must identify its model context.

At minimum:

Model
+
Inference Reference
+
Observation Method
+
Inspection Scope

An observation should not be treated as a universal statement about all versions of a model family.

4. Evidence Binding

Every observed signal must reference one or more evidence objects.

The protocol separates:

Observed Signal
        ↓
Evidence Reference
        ↓
Evidence Manifest

This prevents unsupported latent-state claims from appearing as self-contained assertions.

5. Explicit Epistemic Boundaries

The record must state its limitations.

Examples include:

method dependence,
incomplete layer coverage,
uncertain concept interpretation,
threshold sensitivity,
representation polysemanticity,
limited token-position coverage.
6. Raw Activations Are Not Required

The protocol does not require raw internal activations to be permanently stored.

A deployment may store:

raw activations,
derived representations,
evidence commitments,
metadata only,
externally governed evidence references.

Storage policy must be declared explicitly.

Record Architecture
Latent State Observation Record
│
├── Schema Identity
│
├── Observation Identity
│
├── Model Context
│
├── Observer
│
├── Observation Method
│
├── Inspection Scope
│
├── Observed Signals
│
├── Interpretation Boundary
│
├── Evidence Manifest
│
├── Storage Policy
│
├── Assertions
└── Review
Critical Safety Boundary

v0.1 explicitly prohibits the record from claiming:

Observed Signal
        =
Proven Cause

The following assertion fields are fixed to false:

assertions:
  causal_claim_made: false
  intervention_performed: false
  downstream_effect_claimed: false

A record that attempts to set these fields to true is invalid under the v0.1 schema.

Repository Structure
.
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── schemas/
│   └── latent-state-observation-record.schema.json
├── examples/
│   └── latent-state-observation-record.example.yaml
├── scripts/
│   └── validate_examples.py
└── .github/
    └── workflows/
        └── validate.yml
Validation

Install dependencies:

python -m pip install -r requirements.txt

Run validation:

python scripts/validate_examples.py

Expected result:

[validate] Latent State Observation Record
  schema : schemas/latent-state-observation-record.schema.json
  example: examples/latent-state-observation-record.example.yaml
[ok] latent-state-observation-record.example.yaml is valid
GitHub Actions

The repository automatically validates the example record on:

push,
pull request,
manual workflow dispatch.

The workflow validates:

JSON Schema structure,
YAML example structure,
schema compatibility,
semantic evidence references,
duplicate signal identifiers.
Non-Goals of v0.1

v0.1 does not:

prove causal influence,
perform internal-state interventions,
compare counterfactual runs,
determine model consciousness,
infer legal responsibility,
identify training-data origin,
calculate contribution percentages,
calculate royalties,
execute allocation or payment.

These concerns belong to separate layers.

Roadmap
v0.1 — Latent State Observation Record

Record method-bound observations of latent model states.

v0.2 — Causal Intervention Evidence

Record interventions and counterfactual behavioral differences.

v0.3 — Method and Model Binding

Strengthen reproducibility across model versions, checkpoints, methods, thresholds, and inspection scopes.

v0.4 — Verification Challenge and Reproduction

Allow causal claims to be challenged, independently reproduced, disputed, or partially confirmed.

v0.5 — Unified Latent Causality Lifecycle

Integrate:

Observe
→ Interpret
→ Intervene
→ Compare
→ Verify
→ Challenge
→ Reproduce
→ External Trace Binding
Relationship to a Broader Audit Architecture

The protocol is designed to support a vertical internal-causality axis:

Latent State
    ↓
Observation
    ↓
Intervention
    ↓
Effect Comparison
    ↓
Causal Verification
    ↓
Challenge
    ↓
Reproduction
    ↓
Audit Integration

This vertical axis can later connect to an external provenance and allocation axis:

Origin
→ Trace
→ Action
→ Artifact
→ Contribution
→ Audit
→ Allocation Readiness

The two axes solve different proof problems.

Internal use of a representation does not, by itself, establish the historical origin or ownership of that representation.

License

See LICENSE.

Summary

The Latent State Observation Record establishes the first boundary of latent-state auditing:

Observe first.
Bind the evidence.
Declare uncertainty.
Do not claim causation before testing it.

v0.1 begins with observation.

Causal verification comes next.

## v0.2 — Causal Intervention Evidence

v0.2 introduces the Causal Intervention Evidence Record.

The record connects a previous latent-state observation to:

- a falsifiable hypothesis,
- a declared intervention target,
- a reproducible intervention operation,
- a baseline run,
- an intervention run,
- outcome measurements,
- metric differences,
- replication statistics,
- bounded causal assessment,
- evidence references,
- review status.

The core lifecycle is:

```text
Observation
    ↓
Hypothesis
    ↓
Intervention
    ↓
Baseline / Intervention Comparison
    ↓
Effect Measurement
    ↓
Replication Summary
    ↓
Bounded Causal Assessment
Core Boundary

v0.2 permits a bounded causal assessment.

It does not permit the record to claim:

universal causality,
complete mechanism identification,
exhaustive explanation of model behavior,
historical origin attribution,
contribution ownership,
royalty entitlement.

The central principle is:

Intervention can support a causal claim.
It does not prove a universal mechanism.

Relationship to v0.1

v0.1 asks:

What latent signal was observed?

v0.2 asks:

What changed when the declared latent target was deliberately changed?

The protocol therefore separates:

Observation Evidence
        ≠
Causal Intervention Evidence

and connects them explicitly through:

observation_ref: lso-example-001
Supported Intervention Classes

The v0.2 schema supports method-neutral intervention categories:

ablation,
suppression,
activation,
injection,
swap,
replacement,
scaling,
patching,
other.

Specific mathematical implementations remain outside the normative core of the protocol.

Evidence Chain
Observed Signal
      ↓
Hypothesis
      ↓
Intervention Target
      ↓
Operation
      ↓
Baseline Run
      ↓
Intervention Run
      ↓
Metric Delta
      ↓
Replication Summary
      ↓
Causal Assessment
      ↓
Review
Epistemic Boundary

The following assertions are mandatory:

assertions:
  intervention_performed: true
  baseline_comparison_performed: true
  causal_effect_assessed: true
  universal_causal_claim_made: false
  mechanism_exhaustively_identified: false

A v0.2 record may support a causal contribution claim only within its explicitly declared scope.

The assessment must remain bound to the relevant:

model,
checkpoint,
task family,
intervention operation,
layer scope,
token scope,
component scope,
measurement procedure.
Next Layer

v0.3 will strengthen Method and Model Binding.

The protocol will move from:

We observed an effect

toward:

We observed this effect
on this model version
at this checkpoint
using this method version
with this configuration
under this threshold policy
within this inspection scope.

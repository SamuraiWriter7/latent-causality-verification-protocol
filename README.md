# Latent Causality Verification Protocol

A method-neutral protocol for observing, testing, binding, challenging, reproducing, and auditing claims about causal relationships between latent model states and downstream model behavior.

> Observation is not causation.
> Intervention does not imply universality.
> Verification must remain challengeable.

---

## Overview

The Latent Causality Verification Protocol defines a structured lifecycle for claims about latent model states.

The protocol begins with a simple distinction:

```text
Observed Internal Signal
        ≠
Proven Cause
```

An internal representation may be readable without being causal.

A causal intervention may produce an effect without identifying a complete mechanism.

A reproduced result may remain limited to a specific:

* model,
* checkpoint,
* tokenizer,
* method,
* configuration,
* threshold policy,
* layer scope,
* token scope,
* execution environment,
* task family,
* metric definition.

The protocol therefore separates latent-causality verification into five layers:

```text
v0.1  Observation
       ↓
v0.2  Intervention
       ↓
v0.3  Binding
       ↓
v0.4  Challenge / Reproduction
       ↓
v0.5  Unified Lifecycle
```

The complete first arc is:

```text
Observe
→ Interpret
→ Hypothesize
→ Intervene
→ Compare
→ Assess
→ Bind
→ Challenge
→ Reproduce
→ Resolve or Remain Disputed
→ External Trace Binding
```

---

## Status

Current protocol milestone:

`v0.5.0-candidate`

Current architecture:

**Unified Latent Causality Lifecycle**

The first protocol arc is complete from observation through external trace binding.

---

## Motivation

Traditional AI auditing often focuses on visible inputs and outputs:

```text
Prompt
   ↓
Model
   ↓
Output
```

Emerging interpretability methods make it increasingly possible to inspect internal model representations during inference.

This creates a deeper potential audit path:

```text
Prompt
   ↓
Internal State
   ↓
Observed Latent Signal
   ↓
Interpretation
   ↓
Intervention
   ↓
Effect Comparison
   ↓
Bounded Causal Assessment
   ↓
Challenge
   ↓
Reproduction
```

However, internal visibility introduces a new danger:

> A readable internal representation may be mistaken for a complete explanation.

This protocol is designed to prevent that collapse.

It distinguishes:

```text
Observation
≠
Interpretation
≠
Causal Evidence
≠
Mechanistic Explanation
≠
Origin Attribution
≠
Contribution Allocation
```

The protocol does not attempt to make AI systems completely transparent.

Its purpose is narrower:

> Turn claims about latent model causality into evidence-bound, reproducible, challengeable, and trace-connected records.

---

# Core Principles

## 1. Observation Is Not Causation

The protocol begins with the principle:

> Observation is not causation.

A latent signal may be observed without claiming that it caused a downstream decision, output, or action.

v0.1 enforces this boundary structurally.

```yaml
assertions:
  causal_claim_made: false
  intervention_performed: false
  downstream_effect_claimed: false
```

---

## 2. Causal Claims Require Intervention Evidence

A causal claim should not emerge merely because a representation correlates with an output.

The protocol requires a transition such as:

```text
Observed Signal
      ↓
Hypothesis
      ↓
Targeted Intervention
      ↓
Baseline Comparison
      ↓
Observed Effect Difference
      ↓
Bounded Causal Assessment
```

The central v0.2 principle is:

> Intervention can support a causal claim.
> It does not prove a universal mechanism.

---

## 3. Results Must Be Bound to Their Conditions

A result obtained under one model and method configuration must not automatically be generalized to another.

The protocol binds claims to:

```text
Model
+
Checkpoint
+
Tokenizer
+
Observation Method
+
Intervention Method
+
Code Snapshot
+
Configuration
+
Threshold Policy
+
Execution Environment
+
Input Set
+
Inspection Scope
+
Metric Definition
```

The v0.3 principle is:

> A causal result without binding is an anecdote.
> A causal result with binding becomes reproducible evidence.

---

## 4. Verifiable Claims Must Be Challengeable

Structured evidence should not become an unquestionable authority merely because it is machine-readable.

The protocol supports:

* challenge,
* replay,
* scoped replication,
* method variation,
* model variation,
* adversarial testing,
* partial reproduction,
* contradiction,
* unresolved disagreement.

The v0.4 principle is:

> A verifiable claim must also be challengeable.

---

## 5. Reproduction Outcomes Must Preserve Nuance

The protocol explicitly distinguishes:

```text
Challenge
≠
Disproof
```

```text
Failed Reproduction
≠
Automatic Falsification
```

```text
Successful Reproduction
≠
Universal Truth
```

```text
Partial Reproduction
≠
Failure
```

```text
Unresolved Dispute
≠
Protocol Failure
```

Scientific and audit disagreement may remain unresolved.

The unresolved state is preserved rather than artificially compressed into a binary result.

---

## 6. Unified Records Do Not Replace Source Evidence

The v0.5 lifecycle record is index-oriented.

It connects source records but does not copy or replace them.

```text
Source Evidence
      │
      ▼
Lifecycle References
      │
      ▼
State Summary
      │
      ▼
Disputes
      │
      ▼
Open Issues
      │
      ▼
External Trace Binding
```

The unified record is a map of the evidence chain, not a substitute for the evidence itself.

---

# Protocol Architecture

```text
                     Latent State

                          │
                          ▼

                ┌─────────────────┐
                │ Observation     │
                │ v0.1            │
                └────────┬────────┘
                         │
                         ▼
                    Interpretation
                         │
                         ▼
                     Hypothesis
                         │
                         ▼
                ┌─────────────────┐
                │ Intervention    │
                │ v0.2            │
                └────────┬────────┘
                         │
                 ┌───────┴───────┐
                 ▼               ▼
             Baseline        Intervention
                 │               │
                 └───────┬───────┘
                         ▼
                     Comparison
                         │
                         ▼
                 Causal Assessment
                         │
                         ▼
                ┌─────────────────┐
                │ Method / Model  │
                │ Binding v0.3    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Challenge       │
                │ Reproduction    │
                │ v0.4            │
                └────────┬────────┘
                         │
                         ▼
               Agreement / Dispute
                         │
                         ▼
                ┌─────────────────┐
                │ Unified         │
                │ Lifecycle v0.5  │
                └────────┬────────┘
                         │
                         ▼
                External Trace Binding
```

---

# Version Architecture

## v0.1 — Latent State Observation Record

v0.1 records what was observed.

It asks:

> What latent signal was detected, using what method, and within what inspection scope?

The record captures:

* model context,
* inference reference,
* observer identity,
* observation method,
* method version,
* inspection scope,
* observed signals,
* confidence,
* epistemic status,
* interpretation boundary,
* evidence references,
* storage policy,
* review status.

Lifecycle:

```text
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
```

### Boundary

v0.1 does not:

* prove causal influence,
* perform interventions,
* compare counterfactual outcomes,
* infer consciousness,
* assign responsibility,
* identify historical origin,
* calculate contribution percentages,
* calculate royalties.

---

## v0.2 — Causal Intervention Evidence

v0.2 asks:

> What changed when the declared latent target was deliberately changed?

The record connects an observation to:

* a falsifiable hypothesis,
* intervention target,
* intervention operation,
* control design,
* baseline run,
* intervention run,
* outcome measurements,
* metric differences,
* replication statistics,
* bounded causal assessment.

Lifecycle:

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
```

Supported intervention categories include:

* ablation,
* suppression,
* activation,
* injection,
* swap,
* replacement,
* scaling,
* patching,
* other.

### Boundary

v0.2 permits bounded causal assessment.

It does not establish:

* universal causality,
* complete mechanism identification,
* exhaustive explanation,
* model consciousness,
* legal responsibility,
* training-data provenance,
* origin ownership,
* contribution percentage,
* royalty entitlement.

---

## v0.3 — Method and Model Binding

v0.3 asks:

> Under exactly what model, method, configuration, environment, and experiment scope was the result obtained?

The binding record captures:

### Model Binding

* provider,
* model family,
* model ID,
* model version,
* checkpoint reference,
* checkpoint digest,
* tokenizer reference,
* tokenizer digest,
* architecture reference,
* access mode.

### Method Binding

* observation method,
* intervention method,
* method version,
* method family,
* code reference,
* code digest,
* configuration reference,
* configuration digest,
* parameter snapshot,
* threshold policy,
* deterministic status.

### Execution Environment

* runtime ID,
* framework,
* framework version,
* precision,
* hardware class,
* environment artifact,
* environment digest,
* optional container reference,
* seed policy.

### Experiment Binding

* task family,
* input set,
* input digest,
* prompt template,
* prompt digest,
* layer indexing convention,
* layer scope,
* token selection policy,
* component scope,
* metric specification.

Lifecycle position:

```text
Causal Evidence
       │
       ▼
Model Binding
       +
Method Binding
       +
Configuration Binding
       +
Environment Binding
       +
Experiment Binding
       │
       ▼
Reproducibility Status
```

### Reproducibility States

```text
complete
partial
unverifiable
```

A `complete` status means the protocol identifies the declared artifacts and conditions required for an authorized replay attempt.

It does not guarantee successful reproduction.

### Boundary

v0.3 does not establish:

* universal portability,
* cross-model equivalence,
* cross-checkpoint equivalence,
* independent reproduction,
* successful replication,
* complete mechanistic explanation.

---

## v0.4 — Verification Challenge and Reproduction

v0.4 asks:

> Can another party challenge, replay, vary, compare, and dispute the result?

The record supports:

* challenger identity,
* relationship to the original work,
* conflict disclosure,
* challenge type,
* challenge grounds,
* requested tests,
* reproduction plan,
* independence level,
* declared deviations,
* reproduction attempts,
* metric comparison,
* agreement scope,
* disagreement scope,
* uncertainty,
* resolution state.

Challenge types include:

* method dependency,
* threshold sensitivity,
* model binding mismatch,
* scope overreach,
* control design weakness,
* replication failure,
* evidence integrity,
* metric validity,
* other.

Reproduction types include:

```text
exact_replay
scoped_replication
method_variation
model_variation
adversarial_test
other
```

Comparison outcomes include:

```text
confirmed
substantially_confirmed
partially_reproduced
not_reproduced
contradicted
inconclusive
```

Resolution states include:

```text
open
resolved
unresolved_dispute
withdrawn
```

### Boundary

v0.4 does not assume that:

* failed reproduction automatically falsifies the original claim,
* successful reproduction proves universal causality,
* partial reproduction is equivalent to failure,
* every dispute must be resolved,
* organizational independence guarantees methodological independence.

---

## v0.5 — Unified Latent Causality Lifecycle

v0.5 integrates the first protocol arc.

It asks:

> What is the complete audit state of this latent-causality claim?

The unified lifecycle record references:

* v0.1 observation,
* v0.2 intervention evidence,
* v0.3 method/model binding,
* v0.4 challenge and reproduction.

It summarizes:

* lifecycle state,
* claim state,
* evidence chain,
* challenge status,
* reproduction status,
* resolution status,
* external trace relationships,
* open issues,
* closure state.

Lifecycle:

```text
Observe
→ Interpret
→ Hypothesize
→ Intervene
→ Compare
→ Assess
→ Bind
→ Challenge
→ Reproduce
→ Resolve or Remain Disputed
→ External Trace Binding
```

### Index-Oriented Design

The lifecycle record does not copy:

* raw activations,
* full observation artifacts,
* raw run output,
* intervention logs,
* reproduction artifacts.

Instead, it records:

```text
Record References
        +
State Synchronization
        +
Evidence Chain
        +
Open Issues
        +
External Trace Relationships
```

---

# External Trace Binding

v0.5 introduces a bridge from internal causality auditing to external trace systems.

Binding states:

```text
unbound
partial
bound
disputed
```

Relationship types:

```text
contextualizes
supports
challenges
derived_from
supersedes
references
other
```

Example:

```yaml
external_trace_binding:
  binding_status: bound

  trace_protocol_ref: trace-relay-protocol-v1

  trace_refs:
    - trace-example-origin-001
    - trace-example-transformation-001
```

External trace binding may provide:

* contextual history,
* inquiry history,
* transformation history,
* external evidence relationships,
* audit context.

However:

```text
External Trace Binding
        ≠
Origin Ownership
```

and:

```text
Internal Representation Use
        ≠
Contribution Percentage
```

and:

```text
Causal Evidence
        ≠
Royalty Entitlement
```

The intended broader path is:

```text
Internal Causality Verification
            ↓
External Trace Binding
            ↓
Origin Evidence
            ↓
Contribution Causality
            ↓
Allocation Readiness
            ↓
Royalty
```

Each transition requires separate evidence.

---

# Open Issue Model

The v0.5 lifecycle preserves unresolved questions.

Issue categories include:

* method,
* model,
* threshold,
* scope,
* metric,
* replication,
* evidence,
* trace binding,
* other.

Severity:

```text
low
medium
high
critical
```

Status:

```text
open
under_review
resolved
deferred
```

A lifecycle may remain active while issues remain unresolved.

The protocol does not require artificial certainty.

---

# Closure Model

A lifecycle can be closed only when:

```yaml
record_status: closed

closure:
  lifecycle_complete: true
  closure_reason: "..."
  closed_at: "..."
```

A closed lifecycle must not contain issues in:

```text
open
under_review
```

state.

A lifecycle may instead remain:

* active,
* under review,
* disputed.

---

# Epistemic Boundaries

The complete protocol preserves the following distinctions:

```text
Observation
≠
Causation
```

```text
Intervention Effect
≠
Complete Mechanism
```

```text
Method-Bound Result
≠
Universal Model Truth
```

```text
Reproduction
≠
Universal Portability
```

```text
External Trace
≠
Ownership
```

```text
Latent Causal Role
≠
Historical Origin Attribution
```

```text
Origin Evidence
≠
Automatic Royalty Entitlement
```

---

# Repository Structure

```text
.
├── README.md
├── CHANGELOG.md
├── requirements.txt
│
├── schemas/
│   ├── latent-state-observation-record.schema.json
│   ├── causal-intervention-evidence.schema.json
│   ├── method-model-binding-record.schema.json
│   ├── verification-challenge-reproduction.schema.json
│   └── unified-latent-causality-lifecycle.schema.json
│
├── examples/
│   ├── latent-state-observation-record.example.yaml
│   ├── causal-intervention-evidence.example.yaml
│   ├── method-model-binding-record.example.yaml
│   ├── verification-challenge-reproduction.example.yaml
│   └── unified-latent-causality-lifecycle.example.yaml
│
├── scripts/
│   └── validate_examples.py
│
└── .github/
    └── workflows/
        └── validate.yml
```

---

# Validation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run validation:

```bash
python scripts/validate_examples.py
```

Expected result:

```text
[validate] Latent State Observation Record
  schema : schemas/latent-state-observation-record.schema.json
  example: examples/latent-state-observation-record.example.yaml
[ok] latent-state-observation-record.example.yaml is valid

[validate] Causal Intervention Evidence Record
  schema : schemas/causal-intervention-evidence.schema.json
  example: examples/causal-intervention-evidence.example.yaml
[ok] causal-intervention-evidence.example.yaml is valid

[validate] Method and Model Binding Record
  schema : schemas/method-model-binding-record.schema.json
  example: examples/method-model-binding-record.example.yaml
[ok] method-model-binding-record.example.yaml is valid

[validate] Verification Challenge and Reproduction Record
  schema : schemas/verification-challenge-reproduction.schema.json
  example: examples/verification-challenge-reproduction.example.yaml
[ok] verification-challenge-reproduction.example.yaml is valid

[validate] Unified Latent Causality Lifecycle Record
  schema : schemas/unified-latent-causality-lifecycle.schema.json
  example: examples/unified-latent-causality-lifecycle.example.yaml
[ok] unified-latent-causality-lifecycle.example.yaml is valid

[ok] all protocol examples are valid
```

---

# Validation Layers

The validator performs both JSON Schema validation and cross-record semantic validation.

## v0.1 — Observation Integrity

```text
Signal ID Integrity
Evidence ID Integrity
Evidence Reference Integrity
```

## v0.2 — Intervention Integrity

```text
Run ID Integrity
Control Reference Integrity
Signal Target Integrity
Primary Metric Integrity
Metric Delta Arithmetic
Direction Consistency
Run / Comparison Consistency
Replication Arithmetic
Matched Baseline Integrity
```

## v0.3 — Binding Integrity

```text
Observation Reference Integrity
Intervention Reference Integrity
Model Identity Consistency
Observation Method Consistency
Intervention Method Consistency
Experiment Scope Consistency
Runtime Consistency
Reproducibility State Consistency
```

## v0.4 — Challenge Integrity

```text
Lifecycle Reference Chain
Attempt ID Integrity
Evidence Reference Integrity
Reproduction Metric Arithmetic
Tolerance Judgment
Completed Attempt State
Exact Replay Boundary
Resolution State Consistency
Outcome Consistency
```

## v0.5 — Lifecycle Integrity

```text
Full Record Chain
Claim Identity
Lifecycle State Synchronization
Resolution Mapping
Evidence Chain
External Trace Binding
Open Issue Integrity
Timestamp Order
Closure Rules
Origin Ownership Boundary
Royalty Inference Boundary
```

---

# GitHub Actions

The repository validates protocol examples on:

* push,
* pull request,
* manual workflow dispatch.

The workflow runs:

```bash
python scripts/validate_examples.py
```

A valid repository state requires all five protocol layers to pass.

---

# Method Neutrality

This protocol is intentionally method-neutral.

It may be used with current or future techniques including:

* representation probes,
* Jacobian-based lenses,
* sparse representation methods,
* activation inspection,
* feature detectors,
* representation readers,
* activation patching,
* latent-state intervention methods,
* other interpretability techniques.

The protocol standardizes evidence relationships.

It does not standardize one universal theory of model internals.

---

# Non-Goals

The protocol does not attempt to:

* reveal every internal computation,
* recover a complete hidden reasoning transcript,
* prove model consciousness,
* establish universal mechanistic explanations,
* automatically identify training-data origins,
* automatically determine authorship,
* automatically assign contribution percentages,
* automatically establish legal responsibility,
* automatically calculate royalties,
* automatically execute allocation or payment.

These questions require additional evidence and separate governance layers.

---

# First Arc Summary

```text
v0.1
What was observed?

        ↓

v0.2
What changed after intervention?

        ↓

v0.3
Under what exact conditions was the result obtained?

        ↓

v0.4
Can another party challenge and reproduce it?

        ↓

v0.5
What is the complete auditable lifecycle state?
```

Or more simply:

```text
See
↓
Touch
↓
Bind
↓
Challenge
↓
Connect
```

---

# Civilizational Position

The protocol represents a shift from:

```text
Black Box
    ↓
Trust the Operator
```

toward:

```text
Black Box
    ↓
Observation Claim
    ↓
Intervention Evidence
    ↓
Bound Conditions
    ↓
Challenge
    ↓
Reproduction
    ↓
Dispute Preservation
    ↓
External Trace Connection
```

The goal is not perfect transparency.

The goal is a stronger and more realistic form of accountability:

> A black box whose claims can be inspected, tested, challenged, reproduced, disputed, and connected to an external audit trail.

---

# License

See `LICENSE`.

---

# Summary

The Latent Causality Verification Protocol establishes a method-neutral architecture for internal causality auditing.

Its first arc is:

```text
Observation
→ Intervention
→ Binding
→ Challenge
→ Unified Lifecycle
```

Its governing boundaries are:

> Observe first.
> Test before claiming causation.
> Bind every result to its conditions.
> Allow every claim to be challenged.
> Preserve uncertainty and disagreement.
> Connect internal causality to external trace systems without confusing trace, origin, contribution, and royalty.

The protocol does not promise complete transparency.

It creates something more practical:

> A structured way to make claims about latent model causality evidence-bound, reproducible, challengeable, and auditable.

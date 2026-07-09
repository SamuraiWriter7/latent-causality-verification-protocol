# Changelog

All notable changes to the Latent Causality Verification Protocol will be documented in this file.

## [v0.4.0-candidate] - 2026-07-09

### Added

- Verification Challenge and Reproduction Record
- challenge subject binding
- target claim reference
- challenger identity declaration
- relationship-to-original-work declaration
- conflict disclosure
- challenge type registry
- challenge grounds
- requested test declarations
- reproduction plan
- reproduction type classification
- independence level declaration
- comparison target declaration
- reproduction deviation records
- reproduction attempt records
- binding snapshot references
- original versus reproduced metric comparison
- tolerance evaluation
- reproduction attempt outcome classification
- overall comparison outcome
- effect direction consistency
- magnitude consistency
- agreement scope
- disagreement scope
- uncertainty declaration
- challenge resolution status
- challenge disposition
- revised claim scope
- superseding record reference
- challenge evidence manifest
- cross-version lifecycle reference validation
- reproduction metric arithmetic validation
- tolerance consistency validation
- completed attempt integrity validation
- exact replay deviation validation
- resolution state consistency validation

### Boundary

v0.4 does not assume that:

- a failed reproduction automatically falsifies the original claim,
- a successful reproduction establishes universal causality,
- partial reproduction is equivalent to failure,
- disagreement must always be resolved,
- independent reproduction guarantees methodological independence.

### Core Principle

> A verifiable claim must also be challengeable.

### Lifecycle

```text
Observe
→ Intervene
→ Compare
→ Bind
→ Challenge
→ Reproduce
→ Resolve or Remain Disputed

## [v0.3.0-candidate] - 2026-07-09

### Added

- Method and Model Binding Record
- observation record reference binding
- intervention evidence reference binding
- model family binding
- model identifier binding
- model version binding
- checkpoint reference and digest
- tokenizer reference and digest
- architecture reference
- model access mode declaration
- observation method binding
- intervention method binding
- method version binding
- code artifact binding
- configuration artifact binding
- parameter snapshot reference
- threshold policy binding
- execution environment binding
- framework and framework version binding
- numerical precision declaration
- hardware class declaration
- environment artifact digest
- optional container binding
- random seed policy
- task family binding
- input set binding
- prompt template binding
- layer indexing convention
- inspection layer binding
- token selection policy
- component scope binding
- metric specification binding
- reproducibility status
- replay requirements
- missing binding declaration
- cross-record identity validation
- model consistency validation
- method consistency validation
- intervention operation binding validation
- experiment scope consistency validation

### Boundary

v0.3 binds evidence to declared conditions.

It does not establish:

- universal portability,
- cross-model equivalence,
- cross-checkpoint equivalence,
- independent reproduction,
- successful replication,
- complete mechanistic explanation.

### Core Principle

> A causal result without binding is an anecdote.
> A causal result with binding becomes reproducible evidence.

### Lifecycle

```text
Observe
→ Hypothesize
→ Intervene
→ Compare
→ Assess
→ Bind

## [v0.2.0-candidate] - 2026-07-09

### Added

- Causal Intervention Evidence Record
- observation-to-intervention reference binding
- falsifiable causal hypothesis structure
- intervention target declaration
- method-neutral intervention type registry
- intervention operation metadata
- control design declaration
- baseline run record
- intervention run record
- optional control runs
- outcome measurement structure
- metric delta comparison
- qualitative effect records
- replication summary
- bounded causal assessment
- alternative explanation records
- intervention evidence manifest
- causal evidence review status
- cross-reference validation
- metric delta arithmetic validation
- effect direction validation
- replication rate validation
- control run reference validation
- intervention target signal validation

### Changed

- Updated example validation script to validate both v0.1 and v0.2 records.
- Extended semantic validation beyond JSON Schema conformance.
- Added cross-record lifecycle progression from observation to intervention evidence.

### Boundary

v0.2 permits bounded causal assessment.

It does not establish:

- universal causal mechanisms,
- exhaustive internal explanations,
- model consciousness,
- legal responsibility,
- training-data provenance,
- origin ownership,
- contribution percentages,
- royalty entitlement.

### Core Principle

> Intervention can support a causal claim.
> It does not prove a universal mechanism.

### Lifecycle

```text
Observe
→ Hypothesize
→ Intervene
→ Compare
→ Measure
→ Replicate
→ Assess

## [Unreleased]

### Planned

- Causal Intervention Evidence
- Counterfactual effect comparison
- method and model binding extensions
- verification challenge records
- independent reproduction records
- external trace binding
- unified latent causality lifecycle

---

## [v0.1.0-candidate] - 2026-07-09

### Added

- Initial Latent State Observation Record specification
- JSON Schema Draft 2020-12 validation
- YAML example record
- model context binding
- observer identification
- observation method binding
- inspection scope declaration
- observed latent signal records
- signal confidence and epistemic status fields
- interpretation boundary
- evidence manifest
- storage policy declaration
- explicit non-causal assertion boundary
- review status
- Python example validator
- evidence reference integrity checks
- duplicate signal identifier checks
- GitHub Actions validation workflow
- initial protocol README
- initial roadmap from v0.1 through v0.5

### Boundary

v0.1 records latent-state observations only.

It does not:

- establish causal influence,
- perform interventions,
- compare counterfactual outcomes,
- infer consciousness,
- assign responsibility,
- attribute origin,
- calculate contribution,
- determine royalty allocation.

### Core Principle

> Observation is not causation.

A latent signal may be observed and recorded without claiming that the signal caused any downstream decision, output, or action.

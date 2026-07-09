# Changelog

All notable changes to the Latent Causality Verification Protocol are documented in this file.

The protocol follows a layered development model:

```text
v0.1  Observation
v0.2  Intervention
v0.3  Binding
v0.4  Challenge / Reproduction
v0.5  Unified Lifecycle
```

---

## [Unreleased]

### Planned

Possible future work may include:

* multi-observation lifecycle aggregation,
* multi-intervention causal graphs,
* cross-model reproduction matrices,
* method disagreement records,
* adversarial interpretability evaluation,
* longitudinal checkpoint comparison,
* external audit bridge specifications,
* independent trace evidence verification,
* stronger cryptographic evidence commitments,
* lifecycle federation across organizations.

### Boundary

Future versions should preserve the distinction between:

```text
Latent Causal Evidence
≠
Historical Origin Evidence
≠
Contribution Allocation
≠
Royalty Entitlement
```

---

## [v0.5.0-candidate] - 2026-07-09

### Added

* Unified Latent Causality Lifecycle Record
* complete v0.1 through v0.4 record reference chain
* lifecycle identity
* lifecycle state summary
* observation state
* intervention state
* binding state
* challenge state
* reproduction state
* resolution state
* overall lifecycle state
* claim summary
* causal scope declaration
* support status
* confidence field
* scope limitation records
* stage-oriented evidence chain
* observation stage binding
* intervention stage binding
* comparison stage binding
* method/model binding stage
* challenge stage
* reproduction stage
* resolution stage
* external trace stage
* external trace binding state
* external trace protocol reference
* trace reference list
* trace relationship classification
* trace relationship scope
* trace binding notes
* open issue registry
* issue category
* issue severity
* issue status
* issue relationship references
* lifecycle closure structure
* closure reason
* closure timestamp
* superseding lifecycle references
* lifecycle assertions
* explicit uncertainty preservation
* explicit dispute preservation
* explicit raw-state storage boundary
* explicit source-evidence preservation boundary
* explicit origin ownership boundary
* explicit royalty inference boundary
* full record-chain validation
* claim reference validation
* claim text consistency validation
* source-state synchronization
* intervention state synchronization
* binding status synchronization
* challenge status synchronization
* reproduction status synchronization
* resolution disposition mapping
* evidence-chain stage validation
* evidence-chain record reference validation
* duplicate evidence-chain stage checks
* external trace relationship validation
* duplicate open issue identifier validation
* timestamp ordering checks
* lifecycle closure consistency checks
* unresolved issue closure checks
* lifecycle-level epistemic boundary validation

### Changed

* Extended validation from independent protocol records to a unified lifecycle chain.
* Added cross-version status synchronization.
* Added lifecycle state mapping between v0.2, v0.3, v0.4, and v0.5.
* Added index-oriented lifecycle architecture.
* Added external trace integration without collapsing provenance, ownership, contribution, and allocation into latent-causality evidence.
* Added lifecycle closure rules.
* Added unresolved issue preservation.

### Core Principle

> A lifecycle record does not replace evidence.
> It binds evidence, disputes, uncertainty, and trace relationships into one auditable chain.

### Boundary

v0.5 does not assume that:

* internal observation reveals the complete model state,
* causal intervention identifies every mechanism,
* method/model binding guarantees reproduction,
* reproduction establishes universal causality,
* external trace binding establishes ownership,
* internal representation use determines contribution percentage,
* latent causal evidence establishes royalty entitlement.

### Lifecycle

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

### First Arc Completion

v0.5 closes the first protocol arc:

```text
v0.1  Observe
       ↓
v0.2  Intervene
       ↓
v0.3  Bind
       ↓
v0.4  Challenge / Reproduce
       ↓
v0.5  Unify
```

---

## [v0.4.0-candidate] - 2026-07-09

### Added

* Verification Challenge and Reproduction Record
* challenge identifier
* challenge subject references
* observation reference binding
* intervention evidence reference binding
* method/model binding reference
* optional target claim reference
* challenger identity
* challenger type
* relationship to original work
* conflict disclosure
* challenge type registry
* challenge summary
* challenge grounds
* requested test declarations
* reproduction plan
* reproduction type classification
* independence level declaration
* comparison target declaration
* reproduction deviation records
* deviation field path
* deviation type
* original value reference
* reproduction value reference
* deviation rationale
* reproduction attempt records
* attempt identifiers
* attempt status
* operator reference
* binding snapshot reference
* input reference
* output reference
* primary metric comparison
* original metric value
* reproduced metric value
* delta from original
* tolerance
* tolerance judgment
* reproduction outcome classification
* reproduction evidence references
* overall comparison result
* effect direction consistency
* magnitude consistency
* agreement scope
* disagreement scope
* uncertainty declaration
* resolution status
* resolution disposition
* resolution rationale
* revised claim scope
* superseding record references
* challenge evidence manifest
* challenge review status
* cross-version lifecycle reference validation
* hypothesis target claim validation
* reproduction attempt ID validation
* evidence reference integrity checks
* reproduction metric arithmetic validation
* tolerance consistency validation
* completed attempt state validation
* exact replay deviation validation
* resolution state consistency validation
* comparison outcome consistency validation

### Core Principle

> A verifiable claim must also be challengeable.

### Boundary

v0.4 does not assume that:

* challenge equals disproof,
* failed reproduction automatically falsifies the original claim,
* successful reproduction establishes universal truth,
* partial reproduction is equivalent to failure,
* unresolved disagreement is a protocol failure,
* independent teams necessarily use independent methods.

### Lifecycle

```text
Bound Claim
    ↓
Challenge
    ↓
Grounds
    ↓
Requested Tests
    ↓
Reproduction Plan
    ↓
Reproduction Attempts
    ↓
Comparison
    ↓
Resolution or Unresolved Dispute
```

### Reproduction Types

Added support for:

* exact replay,
* scoped replication,
* method variation,
* model variation,
* adversarial test,
* other.

### Comparison Outcomes

Added:

* confirmed,
* substantially confirmed,
* partially reproduced,
* not reproduced,
* contradicted,
* inconclusive.

### Resolution States

Added:

* open,
* resolved,
* unresolved dispute,
* withdrawn.

---

## [v0.3.0-candidate] - 2026-07-09

### Added

* Method and Model Binding Record
* observation record reference binding
* intervention evidence reference binding
* model provider binding
* model family binding
* model identifier binding
* model version binding
* checkpoint reference
* checkpoint digest
* tokenizer reference
* tokenizer digest
* architecture reference
* model access mode declaration
* observation method binding
* intervention method binding
* method identifiers
* method version binding
* method family binding
* code artifact reference
* code digest
* configuration reference
* configuration digest
* parameter snapshot reference
* threshold policy binding
* method determinism declaration
* execution environment binding
* runtime identifier
* framework name
* framework version
* numerical precision declaration
* hardware class declaration
* environment artifact reference
* environment digest
* optional container binding
* container digest
* random seed policy
* task family binding
* input set reference
* input set digest
* prompt template reference
* prompt template digest
* layer indexing convention
* layer scope binding
* token selection policy
* component scope binding
* metric specification reference
* metric specification digest
* reproducibility status
* replay requirements
* missing binding declaration
* binding notes
* cross-record reference validation
* model identity consistency checks
* observation method consistency checks
* intervention operation binding validation
* experiment scope consistency validation
* runtime consistency validation
* reproducibility consistency validation

### Core Principle

> A causal result without binding is an anecdote.
> A causal result with binding becomes reproducible evidence.

### Boundary

v0.3 binds claims to declared conditions.

It does not establish:

* universal portability,
* cross-model equivalence,
* cross-checkpoint equivalence,
* successful independent reproduction,
* complete mechanistic explanation.

### Lifecycle

```text
Observe
→ Hypothesize
→ Intervene
→ Compare
→ Assess
→ Bind
```

### Reproducibility States

Added:

```text
complete
partial
unverifiable
```

A `complete` record identifies the declared artifacts and conditions required for an authorized replay attempt.

It does not guarantee reproduction success.

---

## [v0.2.0-candidate] - 2026-07-09

### Added

* Causal Intervention Evidence Record
* observation-to-intervention reference binding
* falsifiable hypothesis structure
* hypothesis identifier
* source signal references
* target causal claim
* expected effect
* falsification condition
* intervention type registry
* intervention target declaration
* target signal references
* target layer scope
* target token scope
* target component scope
* intervention operation metadata
* operation reference
* source label
* target label
* intervention magnitude
* clamp policy
* intervention duration scope
* seed declaration
* control design declaration
* control type
* control run references
* control design notes
* baseline run record
* intervention run record
* optional control runs
* run identifiers
* input references
* output references
* outcome measurements
* run evidence references
* primary comparison metric
* metric delta comparison
* baseline metric value
* intervention metric value
* delta arithmetic
* effect direction
* qualitative change records
* replication summary
* trial count
* effect count
* success rate
* bounded causal assessment
* causal support status
* causal confidence
* causal scope statement
* causal rationale
* alternative explanation records
* causal evidence references
* intervention evidence manifest
* review status
* explicit universal-causality boundary
* explicit complete-mechanism boundary
* evidence reference integrity validation
* duplicate evidence identifier validation
* duplicate run identifier validation
* control run reference validation
* intervention target signal validation
* primary metric validation
* metric delta arithmetic validation
* effect direction validation
* run/comparison value consistency validation
* replication rate validation
* matched baseline validation

### Changed

* Extended the validation script to support both observation and intervention records.
* Added cross-field semantic validation beyond JSON Schema conformance.
* Added observation-to-intervention lifecycle progression.

### Core Principle

> Intervention can support a causal claim.
> It does not prove a universal mechanism.

### Boundary

v0.2 permits bounded causal assessment.

It does not establish:

* universal causal mechanisms,
* exhaustive internal explanations,
* model consciousness,
* legal responsibility,
* training-data provenance,
* origin ownership,
* contribution percentages,
* royalty entitlement.

### Lifecycle

```text
Observe
→ Hypothesize
→ Intervene
→ Compare
→ Measure
→ Replicate
→ Assess
```

---

## [v0.1.0-candidate] - 2026-07-09

### Added

* Initial Latent State Observation Record specification
* JSON Schema Draft 2020-12 validation
* YAML example record
* schema identity
* record type
* record status
* observation identifier
* creation timestamp
* model context
* model provider
* model identifier
* model version
* checkpoint reference
* runtime reference
* inference reference
* observer identity
* observer type
* tool reference
* observation method
* observation method version
* method family
* configuration reference
* threshold policy reference
* inspection scope
* layer references
* token references
* component references
* context reference
* observed latent signal records
* signal identifiers
* signal labels
* signal types
* signal score
* signal confidence
* signal rank
* activation direction
* epistemic status
* signal interpretation
* signal evidence references
* interpretation boundary
* interpretation summary
* method dependence note
* explicit limitations
* evidence manifest
* evidence type classification
* artifact URI
* evidence digest
* evidence description
* storage policy
* raw activation storage declaration
* derived representation storage declaration
* retention class
* access scope
* policy reference
* explicit non-causal assertions
* review state
* Python example validator
* duplicate signal identifier checks
* duplicate evidence identifier checks
* evidence reference integrity checks
* GitHub Actions validation workflow
* initial README
* initial roadmap through v0.5

### Core Principle

> Observation is not causation.

### Boundary

v0.1 records latent-state observations only.

It does not:

* establish causal influence,
* perform interventions,
* compare counterfactual outcomes,
* infer consciousness,
* assign legal responsibility,
* identify historical origin,
* calculate contribution percentages,
* determine royalty allocation.

### Lifecycle

```text
Inference
    ↓
Inspection
    ↓
Latent Signal Observation
    ↓
Interpretation
    ↓
Evidence Binding
    ↓
Boundary Declaration
```

---

# First Arc Summary

The protocol evolved through five distinct proof layers.

## v0.1

```text
What was observed?
```

## v0.2

```text
What changed after intervention?
```

## v0.3

```text
Under exactly what conditions was the result obtained?
```

## v0.4

```text
Can another party challenge and reproduce it?
```

## v0.5

```text
What is the complete auditable lifecycle state?
```

The first arc is therefore:

```text
Observation
→ Causal Intervention
→ Method / Model Binding
→ Challenge / Reproduction
→ Unified Lifecycle
```

Or, in compact form:

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

The protocol's central boundary remains:

> Internal causality evidence should be observable, testable, bound, challengeable, reproducible, and trace-connected without being confused with complete transparency, historical origin, ownership, contribution allocation, or royalty entitlement.

from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


RECORDS: list[dict[str, Any]] = [
    {
        "name": "Latent State Observation Record",
        "schema": (
            ROOT
            / "schemas"
            / "latent-state-observation-record.schema.json"
        ),
        "example": (
            ROOT
            / "examples"
            / "latent-state-observation-record.example.yaml"
        ),
        "semantic_validator": "observation",
    },
    {
        "name": "Causal Intervention Evidence Record",
        "schema": (
            ROOT
            / "schemas"
            / "causal-intervention-evidence.schema.json"
        ),
        "example": (
            ROOT
            / "examples"
            / "causal-intervention-evidence.example.yaml"
        ),
        "semantic_validator": "intervention",
    },
    {
        "name": "Method and Model Binding Record",
        "schema": (
            ROOT
            / "schemas"
            / "method-model-binding-record.schema.json"
        ),
        "example": (
            ROOT
            / "examples"
            / "method-model-binding-record.example.yaml"
        ),
        "semantic_validator": "binding",
    },
    {
        "name": "Verification Challenge and Reproduction Record",
        "schema": (
            ROOT
            / "schemas"
            / "verification-challenge-reproduction.schema.json"
        ),
        "example": (
            ROOT
            / "examples"
            / "verification-challenge-reproduction.example.yaml"
        ),
        "semantic_validator": "challenge",
    },
    {
        "name": "Unified Latent Causality Lifecycle Record",
        "schema": (
            ROOT
            / "schemas"
            / "unified-latent-causality-lifecycle.schema.json"
        ),
        "example": (
            ROOT
            / "examples"
            / "unified-latent-causality-lifecycle.example.yaml"
        ),
        "semantic_validator": "lifecycle",
    },
]


# ---------------------------------------------------------------------------
# File loading
# ---------------------------------------------------------------------------


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError as exc:
        raise RuntimeError(
            f"File not found: {path}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in {path}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            f"Expected JSON object in {path}"
        )

    return data


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from disk."""

    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

    except FileNotFoundError as exc:
        raise RuntimeError(
            f"File not found: {path}"
        ) from exc

    except yaml.YAMLError as exc:
        raise RuntimeError(
            f"Invalid YAML in {path}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            f"Expected YAML mapping in {path}"
        )

    return data


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def find_duplicates(
    values: list[str],
) -> set[str]:
    """Return duplicate string values."""

    seen: set[str] = set()
    duplicates: set[str] = set()

    for value in values:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    return duplicates


def parse_datetime(
    value: str,
) -> datetime:
    """Parse an ISO-8601 datetime string."""

    normalized = value.replace(
        "Z",
        "+00:00",
    )

    return datetime.fromisoformat(
        normalized
    )


def is_number(
    value: Any,
) -> bool:
    """Return True for int/float values but not bool."""

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


def validate_schema(
    schema: dict[str, Any],
    example: dict[str, Any],
) -> list[str]:
    """Validate an example against JSON Schema."""

    validator = Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )

    validation_errors = sorted(
        validator.iter_errors(example),
        key=lambda error: list(error.absolute_path),
    )

    messages: list[str] = []

    for error in validation_errors:
        path = ".".join(
            str(part)
            for part in error.absolute_path
        )

        location = path if path else "<root>"

        messages.append(
            f"{location}: {error.message}"
        )

    return messages


def get_manifest_ids(
    example: dict[str, Any],
) -> list[str]:
    """Collect evidence IDs from an evidence manifest."""

    manifest = example.get(
        "evidence_manifest",
        [],
    )

    return [
        item["evidence_id"]
        for item in manifest
        if isinstance(item, dict)
        and isinstance(
            item.get("evidence_id"),
            str,
        )
    ]


def validate_evidence_refs(
    refs: list[str],
    evidence_ids: set[str],
    context: str,
) -> list[str]:
    """Validate evidence references against a manifest."""

    errors: list[str] = []

    for evidence_ref in refs:
        if evidence_ref not in evidence_ids:
            errors.append(
                f"{context}: evidence reference "
                f"{evidence_ref!r} not found "
                "in evidence_manifest"
            )

    return errors


# ---------------------------------------------------------------------------
# v0.1 — Latent State Observation Record
# ---------------------------------------------------------------------------


def validate_observation_record(
    example: dict[str, Any],
) -> list[str]:
    """Run semantic checks for the v0.1 observation record."""

    errors: list[str] = []

    signals = example.get(
        "observed_signals",
        [],
    )

    # ------------------------------------------------------------------
    # Signal ID integrity
    # ------------------------------------------------------------------

    signal_ids = [
        signal["signal_id"]
        for signal in signals
        if isinstance(signal, dict)
        and isinstance(
            signal.get("signal_id"),
            str,
        )
    ]

    for signal_id in sorted(
        find_duplicates(signal_ids)
    ):
        errors.append(
            f"duplicate signal_id: {signal_id}"
        )

    # ------------------------------------------------------------------
    # Evidence manifest integrity
    # ------------------------------------------------------------------

    evidence_ids = get_manifest_ids(
        example
    )

    for evidence_id in sorted(
        find_duplicates(evidence_ids)
    ):
        errors.append(
            f"duplicate evidence_id: {evidence_id}"
        )

    evidence_id_set = set(
        evidence_ids
    )

    for signal in signals:
        if not isinstance(
            signal,
            dict,
        ):
            continue

        signal_id = signal.get(
            "signal_id",
            "<unknown-signal>",
        )

        refs = signal.get(
            "evidence_refs",
            [],
        )

        errors.extend(
            validate_evidence_refs(
                refs,
                evidence_id_set,
                str(signal_id),
            )
        )

    return errors


# ---------------------------------------------------------------------------
# v0.2 — Causal Intervention Evidence Record
# ---------------------------------------------------------------------------


def collect_runs(
    example: dict[str, Any],
) -> list[dict[str, Any]]:
    """Collect baseline, intervention, and control runs."""

    runs = example.get(
        "runs",
        {},
    )

    collected: list[dict[str, Any]] = []

    baseline = runs.get(
        "baseline"
    )

    intervention = runs.get(
        "intervention"
    )

    if isinstance(
        baseline,
        dict,
    ):
        collected.append(
            baseline
        )

    if isinstance(
        intervention,
        dict,
    ):
        collected.append(
            intervention
        )

    for control in runs.get(
        "controls",
        [],
    ):
        if isinstance(
            control,
            dict,
        ):
            collected.append(
                control
            )

    return collected


def collect_intervention_evidence_refs(
    example: dict[str, Any],
) -> list[str]:
    """Collect all evidence references from a v0.2 record."""

    refs: list[str] = []

    for run in collect_runs(
        example
    ):
        refs.extend(
            run.get(
                "evidence_refs",
                [],
            )
        )

    comparison = example.get(
        "comparison",
        {},
    )

    refs.extend(
        comparison.get(
            "evidence_refs",
            [],
        )
    )

    assessment = example.get(
        "causal_assessment",
        {},
    )

    refs.extend(
        assessment.get(
            "evidence_refs",
            [],
        )
    )

    return refs


def build_metric_map(
    run: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Build a metric_id to measurement mapping."""

    measurements = run.get(
        "outcome_measurements",
        [],
    )

    return {
        item["metric_id"]: item
        for item in measurements
        if isinstance(item, dict)
        and isinstance(
            item.get("metric_id"),
            str,
        )
    }


def validate_intervention_record(
    example: dict[str, Any],
) -> list[str]:
    """Run semantic checks for the v0.2 intervention record."""

    errors: list[str] = []

    # ------------------------------------------------------------------
    # Evidence manifest integrity
    # ------------------------------------------------------------------

    evidence_ids = get_manifest_ids(
        example
    )

    for evidence_id in sorted(
        find_duplicates(evidence_ids)
    ):
        errors.append(
            f"duplicate evidence_id: {evidence_id}"
        )

    evidence_id_set = set(
        evidence_ids
    )

    errors.extend(
        validate_evidence_refs(
            collect_intervention_evidence_refs(
                example
            ),
            evidence_id_set,
            "v0.2",
        )
    )

    # ------------------------------------------------------------------
    # Run ID integrity
    # ------------------------------------------------------------------

    runs = collect_runs(
        example
    )

    run_ids = [
        run["run_id"]
        for run in runs
        if isinstance(
            run.get("run_id"),
            str,
        )
    ]

    for run_id in sorted(
        find_duplicates(run_ids)
    ):
        errors.append(
            f"duplicate run_id: {run_id}"
        )

    run_id_set = set(
        run_ids
    )

    # ------------------------------------------------------------------
    # Control run reference integrity
    # ------------------------------------------------------------------

    control_design = (
        example
        .get("intervention_design", {})
        .get("control_design", {})
    )

    for control_ref in control_design.get(
        "control_run_refs",
        [],
    ):
        if control_ref not in run_id_set:
            errors.append(
                f"control_run_ref "
                f"{control_ref!r} does not resolve "
                "to a declared run"
            )

    # ------------------------------------------------------------------
    # Hypothesis and target consistency
    # ------------------------------------------------------------------

    hypothesis_signal_refs = set(
        example
        .get("hypothesis", {})
        .get("source_signal_refs", [])
    )

    target_signal_refs = set(
        example
        .get("intervention_design", {})
        .get("target", {})
        .get("signal_refs", [])
    )

    unknown_targets = (
        target_signal_refs
        - hypothesis_signal_refs
    )

    for signal_ref in sorted(
        unknown_targets
    ):
        errors.append(
            f"intervention target signal "
            f"{signal_ref!r} is not declared "
            "in hypothesis.source_signal_refs"
        )

    # ------------------------------------------------------------------
    # Metric comparison integrity
    # ------------------------------------------------------------------

    comparison = example.get(
        "comparison",
        {},
    )

    primary_metric_id = comparison.get(
        "primary_metric_id"
    )

    metric_deltas = comparison.get(
        "metric_deltas",
        [],
    )

    delta_metric_ids = {
        item.get("metric_id")
        for item in metric_deltas
        if isinstance(
            item,
            dict,
        )
    }

    if (
        isinstance(
            primary_metric_id,
            str,
        )
        and primary_metric_id
        not in delta_metric_ids
    ):
        errors.append(
            f"primary_metric_id "
            f"{primary_metric_id!r} not found "
            "in comparison.metric_deltas"
        )

    runs_object = example.get(
        "runs",
        {},
    )

    baseline = runs_object.get(
        "baseline",
        {},
    )

    intervention = runs_object.get(
        "intervention",
        {},
    )

    baseline_metrics = build_metric_map(
        baseline
        if isinstance(baseline, dict)
        else {}
    )

    intervention_metrics = build_metric_map(
        intervention
        if isinstance(intervention, dict)
        else {}
    )

    for metric_delta in metric_deltas:
        if not isinstance(
            metric_delta,
            dict,
        ):
            continue

        metric_id = metric_delta.get(
            "metric_id"
        )

        baseline_measurement = (
            baseline_metrics.get(
                metric_id
            )
        )

        intervention_measurement = (
            intervention_metrics.get(
                metric_id
            )
        )

        if baseline_measurement is None:
            errors.append(
                f"{metric_id!r} not found "
                "in baseline measurements"
            )

        if intervention_measurement is None:
            errors.append(
                f"{metric_id!r} not found "
                "in intervention measurements"
            )

        baseline_value = metric_delta.get(
            "baseline_value"
        )

        intervention_value = metric_delta.get(
            "intervention_value"
        )

        declared_delta = metric_delta.get(
            "delta"
        )

        if all(
            is_number(value)
            for value in [
                baseline_value,
                intervention_value,
                declared_delta,
            ]
        ):
            expected_delta = (
                intervention_value
                - baseline_value
            )

            if not math.isclose(
                declared_delta,
                expected_delta,
                rel_tol=1e-9,
                abs_tol=1e-9,
            ):
                errors.append(
                    f"{metric_id}: declared delta "
                    f"{declared_delta} does not match "
                    "intervention - baseline "
                    f"({expected_delta})"
                )

            direction = metric_delta.get(
                "direction"
            )

            if expected_delta > 0:
                expected_direction = "increase"

            elif expected_delta < 0:
                expected_direction = "decrease"

            else:
                expected_direction = "no_change"

            if direction != expected_direction:
                errors.append(
                    f"{metric_id}: direction "
                    f"{direction!r} does not match "
                    f"delta direction "
                    f"{expected_direction!r}"
                )

        # Comparison values must match run measurements.

        if (
            baseline_measurement is not None
            and is_number(
                baseline_measurement.get("value")
            )
            and baseline_value
            != baseline_measurement.get("value")
        ):
            errors.append(
                f"{metric_id}: baseline_value "
                "does not match the baseline run "
                "measurement"
            )

        if (
            intervention_measurement is not None
            and is_number(
                intervention_measurement.get("value")
            )
            and intervention_value
            != intervention_measurement.get("value")
        ):
            errors.append(
                f"{metric_id}: intervention_value "
                "does not match the intervention run "
                "measurement"
            )

    # ------------------------------------------------------------------
    # Replication arithmetic
    # ------------------------------------------------------------------

    replication = comparison.get(
        "replication_summary",
        {},
    )

    trial_count = replication.get(
        "trial_count"
    )

    effect_count = replication.get(
        "effect_count"
    )

    success_rate = replication.get(
        "success_rate"
    )

    if (
        isinstance(trial_count, int)
        and not isinstance(trial_count, bool)
        and isinstance(effect_count, int)
        and not isinstance(effect_count, bool)
    ):
        if effect_count > trial_count:
            errors.append(
                "replication_summary.effect_count "
                "cannot exceed trial_count"
            )

        if (
            trial_count > 0
            and is_number(success_rate)
        ):
            expected_rate = (
                effect_count
                / trial_count
            )

            if not math.isclose(
                success_rate,
                expected_rate,
                rel_tol=1e-9,
                abs_tol=1e-9,
            ):
                errors.append(
                    "replication_summary.success_rate "
                    f"{success_rate} does not match "
                    "effect_count / trial_count "
                    f"({expected_rate})"
                )

    # ------------------------------------------------------------------
    # Matched baseline consistency
    # ------------------------------------------------------------------

    if (
        control_design.get("control_type")
        == "matched_baseline"
    ):
        baseline_input = (
            baseline.get("input_ref")
            if isinstance(baseline, dict)
            else None
        )

        intervention_input = (
            intervention.get("input_ref")
            if isinstance(intervention, dict)
            else None
        )

        if (
            baseline_input
            and intervention_input
            and baseline_input
            != intervention_input
        ):
            errors.append(
                "matched_baseline design requires "
                "baseline and intervention input_ref "
                "to match"
            )

    return errors


# ---------------------------------------------------------------------------
# v0.3 — Method and Model Binding Record
# ---------------------------------------------------------------------------


def validate_method_model_binding(
    binding: dict[str, Any],
) -> list[str]:
    """Run cross-record checks for the v0.3 binding record."""

    errors: list[str] = []

    observation_path = (
        ROOT
        / "examples"
        / "latent-state-observation-record.example.yaml"
    )

    intervention_path = (
        ROOT
        / "examples"
        / "causal-intervention-evidence.example.yaml"
    )

    try:
        observation = load_yaml(
            observation_path
        )

        intervention = load_yaml(
            intervention_path
        )

    except RuntimeError as exc:
        return [
            str(exc)
        ]

    # ------------------------------------------------------------------
    # Record reference consistency
    # ------------------------------------------------------------------

    subject_refs = binding.get(
        "subject_refs",
        {},
    )

    observation_ref = subject_refs.get(
        "observation_ref"
    )

    intervention_ref = subject_refs.get(
        "intervention_evidence_ref"
    )

    if observation_ref != observation.get(
        "observation_id"
    ):
        errors.append(
            "subject_refs.observation_ref does not "
            "match the v0.1 observation_id"
        )

    if intervention_ref != intervention.get(
        "intervention_evidence_id"
    ):
        errors.append(
            "subject_refs.intervention_evidence_ref "
            "does not match the v0.2 "
            "intervention_evidence_id"
        )

    if intervention.get(
        "observation_ref"
    ) != observation_ref:
        errors.append(
            "v0.2 observation_ref does not match "
            "v0.3 subject_refs.observation_ref"
        )

    # ------------------------------------------------------------------
    # Model identity consistency
    # ------------------------------------------------------------------

    binding_model = binding.get(
        "model_binding",
        {},
    )

    observation_model = observation.get(
        "model_context",
        {},
    )

    intervention_model = intervention.get(
        "model_context",
        {},
    )

    model_identity_fields = [
        "model_id",
        "model_version",
        "checkpoint_ref",
    ]

    for field in model_identity_fields:
        bound_value = binding_model.get(
            field
        )

        observation_value = (
            observation_model.get(
                field
            )
        )

        intervention_value = (
            intervention_model.get(
                field
            )
        )

        if bound_value != observation_value:
            errors.append(
                f"model_binding.{field} does not "
                "match the v0.1 observation record"
            )

        if bound_value != intervention_value:
            errors.append(
                f"model_binding.{field} does not "
                "match the v0.2 intervention record"
            )

    # ------------------------------------------------------------------
    # Observation method consistency
    # ------------------------------------------------------------------

    observation_method_binding = (
        binding
        .get("method_bindings", {})
        .get("observation_method", {})
    )

    source_observation_method = observation.get(
        "observation_method",
        {},
    )

    observation_method_fields = [
        "name",
        "version",
        "method_family",
    ]

    for field in observation_method_fields:
        bound_value = (
            observation_method_binding.get(
                field
            )
        )

        source_value = (
            source_observation_method.get(
                field
            )
        )

        if bound_value != source_value:
            errors.append(
                f"observation method {field!r} "
                "does not match the v0.1 record"
            )

    # ------------------------------------------------------------------
    # Intervention method consistency
    # ------------------------------------------------------------------

    intervention_method_binding = (
        binding
        .get("method_bindings", {})
        .get("intervention_method", {})
    )

    operation_ref = (
        intervention
        .get("intervention_design", {})
        .get("operation", {})
        .get("operation_ref")
    )

    if (
        intervention_method_binding.get(
            "method_id"
        )
        != operation_ref
    ):
        errors.append(
            "intervention_method.method_id does not "
            "match the v0.2 operation_ref"
        )

    # ------------------------------------------------------------------
    # Experiment scope consistency
    # ------------------------------------------------------------------

    experiment_binding = binding.get(
        "experiment_binding",
        {},
    )

    intervention_target = (
        intervention
        .get("intervention_design", {})
        .get("target", {})
    )

    for field in [
        "layer_refs",
        "component_refs",
    ]:
        bound_values = experiment_binding.get(
            field,
            [],
        )

        target_values = intervention_target.get(
            field,
            [],
        )

        if set(
            bound_values
        ) != set(
            target_values
        ):
            errors.append(
                f"experiment_binding.{field} does not "
                "match the v0.2 intervention target"
            )

    # ------------------------------------------------------------------
    # Runtime consistency
    # ------------------------------------------------------------------

    execution_environment = binding.get(
        "execution_environment",
        {},
    )

    runtime_id = execution_environment.get(
        "runtime_id"
    )

    intervention_runtime_ref = (
        intervention_model.get(
            "runtime_ref"
        )
    )

    if (
        runtime_id
        and intervention_runtime_ref
        and runtime_id
        != intervention_runtime_ref
    ):
        errors.append(
            "execution_environment.runtime_id does "
            "not match the v0.2 runtime_ref"
        )

    # ------------------------------------------------------------------
    # Reproducibility consistency
    # ------------------------------------------------------------------

    reproducibility = binding.get(
        "reproducibility",
        {},
    )

    reproducibility_status = (
        reproducibility.get(
            "status"
        )
    )

    missing_bindings = reproducibility.get(
        "missing_bindings",
        [],
    )

    replay_requirements = reproducibility.get(
        "replay_requirements",
        [],
    )

    if (
        reproducibility_status == "complete"
        and missing_bindings
    ):
        errors.append(
            "reproducibility.status is complete "
            "but missing_bindings is not empty"
        )

    if (
        reproducibility_status == "complete"
        and not replay_requirements
    ):
        errors.append(
            "reproducibility.status is complete "
            "but replay_requirements is empty"
        )

    return errors


# ---------------------------------------------------------------------------
# v0.4 — Verification Challenge and Reproduction Record
# ---------------------------------------------------------------------------


def validate_verification_challenge(
    record: dict[str, Any],
) -> list[str]:
    """Run cross-record and semantic checks for the v0.4 record."""

    errors: list[str] = []

    observation_path = (
        ROOT
        / "examples"
        / "latent-state-observation-record.example.yaml"
    )

    intervention_path = (
        ROOT
        / "examples"
        / "causal-intervention-evidence.example.yaml"
    )

    binding_path = (
        ROOT
        / "examples"
        / "method-model-binding-record.example.yaml"
    )

    try:
        observation = load_yaml(
            observation_path
        )

        intervention = load_yaml(
            intervention_path
        )

        binding = load_yaml(
            binding_path
        )

    except RuntimeError as exc:
        return [
            str(exc)
        ]

    # ------------------------------------------------------------------
    # Subject reference integrity
    # ------------------------------------------------------------------

    subject_refs = record.get(
        "subject_refs",
        {},
    )

    if (
        subject_refs.get(
            "observation_ref"
        )
        != observation.get(
            "observation_id"
        )
    ):
        errors.append(
            "subject_refs.observation_ref does not "
            "match the v0.1 observation_id"
        )

    if (
        subject_refs.get(
            "intervention_evidence_ref"
        )
        != intervention.get(
            "intervention_evidence_id"
        )
    ):
        errors.append(
            "subject_refs.intervention_evidence_ref "
            "does not match the v0.2 record"
        )

    if (
        subject_refs.get(
            "binding_ref"
        )
        != binding.get(
            "binding_id"
        )
    ):
        errors.append(
            "subject_refs.binding_ref does not "
            "match the v0.3 binding_id"
        )

    target_claim_ref = subject_refs.get(
        "target_claim_ref"
    )

    hypothesis_id = (
        intervention
        .get("hypothesis", {})
        .get("hypothesis_id")
    )

    if (
        target_claim_ref is not None
        and target_claim_ref
        != hypothesis_id
    ):
        errors.append(
            "subject_refs.target_claim_ref does not "
            "match the v0.2 hypothesis_id"
        )

    # ------------------------------------------------------------------
    # Lifecycle chain integrity
    # ------------------------------------------------------------------

    binding_subject_refs = binding.get(
        "subject_refs",
        {},
    )

    if (
        binding_subject_refs.get(
            "observation_ref"
        )
        != subject_refs.get(
            "observation_ref"
        )
    ):
        errors.append(
            "v0.3 binding observation_ref does not "
            "match the v0.4 subject chain"
        )

    if (
        binding_subject_refs.get(
            "intervention_evidence_ref"
        )
        != subject_refs.get(
            "intervention_evidence_ref"
        )
    ):
        errors.append(
            "v0.3 intervention reference does not "
            "match the v0.4 subject chain"
        )

    # ------------------------------------------------------------------
    # Attempt ID integrity
    # ------------------------------------------------------------------

    attempts = record.get(
        "reproduction_attempts",
        [],
    )

    attempt_ids = [
        attempt["attempt_id"]
        for attempt in attempts
        if isinstance(attempt, dict)
        and isinstance(
            attempt.get("attempt_id"),
            str,
        )
    ]

    for attempt_id in sorted(
        find_duplicates(attempt_ids)
    ):
        errors.append(
            f"duplicate attempt_id: {attempt_id}"
        )

    # ------------------------------------------------------------------
    # Evidence manifest integrity
    # ------------------------------------------------------------------

    evidence_ids = get_manifest_ids(
        record
    )

    for evidence_id in sorted(
        find_duplicates(evidence_ids)
    ):
        errors.append(
            f"duplicate evidence_id: {evidence_id}"
        )

    evidence_id_set = set(
        evidence_ids
    )

    evidence_refs: list[str] = []

    for attempt in attempts:
        if not isinstance(
            attempt,
            dict,
        ):
            continue

        evidence_refs.extend(
            attempt.get(
                "evidence_refs",
                [],
            )
        )

    evidence_refs.extend(
        record
        .get("comparison", {})
        .get("evidence_refs", [])
    )

    errors.extend(
        validate_evidence_refs(
            evidence_refs,
            evidence_id_set,
            "v0.4",
        )
    )

    # ------------------------------------------------------------------
    # Reproduction metric arithmetic
    # ------------------------------------------------------------------

    for attempt in attempts:
        if not isinstance(
            attempt,
            dict,
        ):
            continue

        attempt_id = attempt.get(
            "attempt_id",
            "<unknown-attempt>",
        )

        metric = attempt.get(
            "primary_metric",
            {},
        )

        original_value = metric.get(
            "original_value"
        )

        reproduced_value = metric.get(
            "reproduced_value"
        )

        declared_delta = metric.get(
            "delta_from_original"
        )

        tolerance = metric.get(
            "tolerance"
        )

        within_tolerance = metric.get(
            "within_tolerance"
        )

        if all(
            is_number(value)
            for value in [
                original_value,
                reproduced_value,
                declared_delta,
                tolerance,
            ]
        ):
            expected_delta = (
                reproduced_value
                - original_value
            )

            if not math.isclose(
                declared_delta,
                expected_delta,
                rel_tol=1e-9,
                abs_tol=1e-9,
            ):
                errors.append(
                    f"{attempt_id}: "
                    "delta_from_original does not match "
                    "reproduced_value - original_value"
                )

            expected_within_tolerance = (
                abs(expected_delta)
                <= tolerance
            )

            if (
                within_tolerance
                != expected_within_tolerance
            ):
                errors.append(
                    f"{attempt_id}: within_tolerance "
                    "does not match the declared "
                    "delta and tolerance"
                )

    # ------------------------------------------------------------------
    # Completed attempt integrity
    # ------------------------------------------------------------------

    for attempt in attempts:
        if not isinstance(
            attempt,
            dict,
        ):
            continue

        attempt_id = attempt.get(
            "attempt_id",
            "<unknown-attempt>",
        )

        if attempt.get(
            "status"
        ) == "completed":
            if attempt.get(
                "output_ref"
            ) is None:
                errors.append(
                    f"{attempt_id}: "
                    "completed attempt requires "
                    "output_ref"
                )

            if (
                attempt.get(
                    "outcome"
                )
                == "not_evaluated"
            ):
                errors.append(
                    f"{attempt_id}: "
                    "completed attempt cannot have "
                    "outcome not_evaluated"
                )

    # ------------------------------------------------------------------
    # Exact replay deviation boundary
    # ------------------------------------------------------------------

    reproduction_plan = record.get(
        "reproduction_plan",
        {},
    )

    if (
        reproduction_plan.get(
            "reproduction_type"
        )
        == "exact_replay"
    ):
        for deviation in reproduction_plan.get(
            "deviations",
            [],
        ):
            if (
                isinstance(deviation, dict)
                and deviation.get(
                    "deviation_type"
                )
                != "none"
            ):
                errors.append(
                    "exact_replay cannot declare "
                    "non-none deviations"
                )

    # ------------------------------------------------------------------
    # Resolution consistency
    # ------------------------------------------------------------------

    resolution = record.get(
        "resolution",
        {},
    )

    status = resolution.get(
        "status"
    )

    disposition = resolution.get(
        "disposition"
    )

    if (
        status == "open"
        and disposition
        not in {
            "pending",
            "no_resolution",
        }
    ):
        errors.append(
            "open resolution must use pending "
            "or no_resolution disposition"
        )

    if (
        status == "resolved"
        and disposition
        in {
            "pending",
            "no_resolution",
        }
    ):
        errors.append(
            "resolved status requires a final "
            "disposition"
        )

    if (
        status == "unresolved_dispute"
        and disposition
        not in {
            "pending",
            "no_resolution",
        }
    ):
        errors.append(
            "unresolved_dispute status must use "
            "pending or no_resolution disposition"
        )

    # ------------------------------------------------------------------
    # Overall outcome consistency
    # ------------------------------------------------------------------

    comparison = record.get(
        "comparison",
        {},
    )

    overall_outcome = comparison.get(
        "overall_outcome"
    )

    completed_attempts = [
        attempt
        for attempt in attempts
        if isinstance(attempt, dict)
        and attempt.get(
            "status"
        )
        == "completed"
    ]

    if (
        overall_outcome != "inconclusive"
        and not completed_attempts
    ):
        errors.append(
            "non-inconclusive overall_outcome "
            "requires at least one completed "
            "reproduction attempt"
        )

    return errors


# ---------------------------------------------------------------------------
# v0.5 — Unified Latent Causality Lifecycle Record
# ---------------------------------------------------------------------------


def validate_unified_lifecycle(
    lifecycle: dict[str, Any],
) -> list[str]:
    """Run full-chain and semantic checks for the v0.5 lifecycle."""

    errors: list[str] = []

    observation_path = (
        ROOT
        / "examples"
        / "latent-state-observation-record.example.yaml"
    )

    intervention_path = (
        ROOT
        / "examples"
        / "causal-intervention-evidence.example.yaml"
    )

    binding_path = (
        ROOT
        / "examples"
        / "method-model-binding-record.example.yaml"
    )

    challenge_path = (
        ROOT
        / "examples"
        / "verification-challenge-reproduction.example.yaml"
    )

    try:
        observation = load_yaml(
            observation_path
        )

        intervention = load_yaml(
            intervention_path
        )

        binding = load_yaml(
            binding_path
        )

        challenge = load_yaml(
            challenge_path
        )

    except RuntimeError as exc:
        return [
            str(exc)
        ]

    # ------------------------------------------------------------------
    # Record reference integrity
    # ------------------------------------------------------------------

    record_refs = lifecycle.get(
        "record_refs",
        {},
    )

    expected_refs = {
        "observation_ref": observation.get(
            "observation_id"
        ),
        "intervention_evidence_ref": intervention.get(
            "intervention_evidence_id"
        ),
        "binding_ref": binding.get(
            "binding_id"
        ),
        "challenge_ref": challenge.get(
            "challenge_id"
        ),
    }

    for field, expected_value in expected_refs.items():
        actual_value = record_refs.get(
            field
        )

        if actual_value != expected_value:
            errors.append(
                f"record_refs.{field} does not match "
                "the source record identifier"
            )

    # ------------------------------------------------------------------
    # Full lifecycle chain integrity
    # ------------------------------------------------------------------

    if (
        intervention.get(
            "observation_ref"
        )
        != record_refs.get(
            "observation_ref"
        )
    ):
        errors.append(
            "v0.2 observation_ref does not match "
            "the lifecycle observation_ref"
        )

    binding_refs = binding.get(
        "subject_refs",
        {},
    )

    if (
        binding_refs.get(
            "observation_ref"
        )
        != record_refs.get(
            "observation_ref"
        )
    ):
        errors.append(
            "v0.3 observation_ref does not match "
            "the lifecycle chain"
        )

    if (
        binding_refs.get(
            "intervention_evidence_ref"
        )
        != record_refs.get(
            "intervention_evidence_ref"
        )
    ):
        errors.append(
            "v0.3 intervention reference does not "
            "match the lifecycle chain"
        )

    challenge_refs = challenge.get(
        "subject_refs",
        {},
    )

    if (
        challenge_refs.get(
            "observation_ref"
        )
        != record_refs.get(
            "observation_ref"
        )
    ):
        errors.append(
            "v0.4 observation_ref does not match "
            "the lifecycle chain"
        )

    if (
        challenge_refs.get(
            "intervention_evidence_ref"
        )
        != record_refs.get(
            "intervention_evidence_ref"
        )
    ):
        errors.append(
            "v0.4 intervention reference does not "
            "match the lifecycle chain"
        )

    if (
        challenge_refs.get(
            "binding_ref"
        )
        != record_refs.get(
            "binding_ref"
        )
    ):
        errors.append(
            "v0.4 binding_ref does not match "
            "the lifecycle chain"
        )

    # ------------------------------------------------------------------
    # Claim integrity
    # ------------------------------------------------------------------

    claim_summary = lifecycle.get(
        "claim_summary",
        {},
    )

    hypothesis = intervention.get(
        "hypothesis",
        {},
    )

    if (
        claim_summary.get(
            "claim_ref"
        )
        != hypothesis.get(
            "hypothesis_id"
        )
    ):
        errors.append(
            "claim_summary.claim_ref does not match "
            "the v0.2 hypothesis_id"
        )

    if (
        claim_summary.get(
            "claim_text"
        )
        != hypothesis.get(
            "target_claim"
        )
    ):
        errors.append(
            "claim_summary.claim_text does not match "
            "the v0.2 target_claim"
        )

    # ------------------------------------------------------------------
    # Lifecycle state consistency
    # ------------------------------------------------------------------

    lifecycle_state = lifecycle.get(
        "lifecycle_state",
        {},
    )

    intervention_status = (
        intervention
        .get("causal_assessment", {})
        .get("status")
    )

    if (
        lifecycle_state.get(
            "intervention_status"
        )
        != intervention_status
    ):
        errors.append(
            "lifecycle_state.intervention_status "
            "does not match the v0.2 causal assessment"
        )

    reproducibility_status = (
        binding
        .get("reproducibility", {})
        .get("status")
    )

    if (
        lifecycle_state.get(
            "binding_status"
        )
        != reproducibility_status
    ):
        errors.append(
            "lifecycle_state.binding_status does not "
            "match the v0.3 reproducibility status"
        )

    challenge_resolution_status = (
        challenge
        .get("resolution", {})
        .get("status")
    )

    if (
        lifecycle_state.get(
            "challenge_status"
        )
        != challenge_resolution_status
    ):
        errors.append(
            "lifecycle_state.challenge_status does "
            "not match the v0.4 resolution status"
        )

    reproduction_outcome = (
        challenge
        .get("comparison", {})
        .get("overall_outcome")
    )

    if (
        lifecycle_state.get(
            "reproduction_status"
        )
        != reproduction_outcome
    ):
        errors.append(
            "lifecycle_state.reproduction_status "
            "does not match the v0.4 comparison outcome"
        )

    resolution_disposition = (
        challenge
        .get("resolution", {})
        .get("disposition")
    )

    disposition_map = {
        "pending": "pending",
        "original_claim_upheld": "claim_upheld",
        "original_claim_narrowed": "claim_narrowed",
        "original_claim_revised": "claim_revised",
        "original_claim_rejected": "claim_rejected",
        "challenge_rejected": "challenge_rejected",
        "no_resolution": "no_resolution",
    }

    expected_resolution_status = disposition_map.get(
        resolution_disposition
    )

    if (
        expected_resolution_status is not None
        and lifecycle_state.get(
            "resolution_status"
        )
        != expected_resolution_status
    ):
        errors.append(
            "lifecycle_state.resolution_status does "
            "not match the v0.4 resolution disposition"
        )

    # ------------------------------------------------------------------
    # Evidence chain integrity
    # ------------------------------------------------------------------

    evidence_chain = lifecycle.get(
        "evidence_chain",
        [],
    )

    stages = [
        entry.get("stage")
        for entry in evidence_chain
        if isinstance(
            entry,
            dict,
        )
    ]

    required_stages = {
        "observation",
        "intervention",
        "binding",
        "challenge",
        "reproduction",
    }

    missing_stages = (
        required_stages
        - set(stages)
    )

    for stage in sorted(
        missing_stages
    ):
        errors.append(
            f"evidence_chain missing required "
            f"stage: {stage}"
        )

    duplicate_stages = find_duplicates(
        [
            stage
            for stage in stages
            if isinstance(stage, str)
        ]
    )

    for stage in sorted(
        duplicate_stages
    ):
        errors.append(
            f"duplicate evidence_chain stage: {stage}"
        )

    stage_record_expectations = {
        "observation": record_refs.get(
            "observation_ref"
        ),
        "intervention": record_refs.get(
            "intervention_evidence_ref"
        ),
        "comparison": record_refs.get(
            "intervention_evidence_ref"
        ),
        "binding": record_refs.get(
            "binding_ref"
        ),
        "challenge": record_refs.get(
            "challenge_ref"
        ),
        "reproduction": record_refs.get(
            "challenge_ref"
        ),
        "resolution": record_refs.get(
            "challenge_ref"
        ),
    }

    for entry in evidence_chain:
        if not isinstance(
            entry,
            dict,
        ):
            continue

        stage = entry.get(
            "stage"
        )

        expected_record_ref = (
            stage_record_expectations.get(
                stage
            )
        )

        if (
            expected_record_ref is not None
            and entry.get(
                "record_ref"
            )
            != expected_record_ref
        ):
            errors.append(
                f"evidence_chain stage "
                f"{stage!r} has an unexpected "
                "record_ref"
            )

    # ------------------------------------------------------------------
    # External trace binding integrity
    # ------------------------------------------------------------------

    external_binding = lifecycle.get(
        "external_trace_binding",
        {},
    )

    trace_binding_status = external_binding.get(
        "binding_status"
    )

    trace_refs = external_binding.get(
        "trace_refs",
        [],
    )

    relationships = external_binding.get(
        "relationships",
        [],
    )

    if (
        trace_binding_status == "bound"
        and not trace_refs
    ):
        errors.append(
            "bound external trace state requires "
            "at least one trace_ref"
        )

    if (
        trace_binding_status == "bound"
        and not relationships
    ):
        errors.append(
            "bound external trace state requires "
            "at least one relationship"
        )

    declared_trace_refs = set(
        trace_refs
    )

    for relationship in relationships:
        if not isinstance(
            relationship,
            dict,
        ):
            continue

        trace_ref = relationship.get(
            "trace_ref"
        )

        if trace_ref not in declared_trace_refs:
            errors.append(
                f"external trace relationship "
                f"{trace_ref!r} is not declared "
                "in trace_refs"
            )

    # ------------------------------------------------------------------
    # Open issue integrity
    # ------------------------------------------------------------------

    open_issues = lifecycle.get(
        "open_issues",
        [],
    )

    issue_ids = [
        issue["issue_id"]
        for issue in open_issues
        if isinstance(issue, dict)
        and isinstance(
            issue.get("issue_id"),
            str,
        )
    ]

    for issue_id in sorted(
        find_duplicates(issue_ids)
    ):
        errors.append(
            f"duplicate issue_id: {issue_id}"
        )

    # ------------------------------------------------------------------
    # Timestamp consistency
    # ------------------------------------------------------------------

    created_at = lifecycle.get(
        "created_at"
    )

    updated_at = lifecycle.get(
        "updated_at"
    )

    if (
        isinstance(created_at, str)
        and isinstance(updated_at, str)
    ):
        try:
            created_datetime = parse_datetime(
                created_at
            )

            updated_datetime = parse_datetime(
                updated_at
            )

            if (
                updated_datetime
                < created_datetime
            ):
                errors.append(
                    "updated_at cannot be earlier "
                    "than created_at"
                )

        except ValueError:
            # JSON Schema format validation will report
            # malformed date-time strings.
            pass

    # ------------------------------------------------------------------
    # Closure consistency
    # ------------------------------------------------------------------

    closure = lifecycle.get(
        "closure",
        {},
    )

    lifecycle_complete = closure.get(
        "lifecycle_complete"
    )

    record_status = lifecycle.get(
        "record_status"
    )

    closed_at = closure.get(
        "closed_at"
    )

    closure_reason = closure.get(
        "closure_reason"
    )

    if (
        lifecycle_complete is True
        and record_status != "closed"
    ):
        errors.append(
            "lifecycle_complete true requires "
            "record_status closed"
        )

    if (
        record_status == "closed"
        and lifecycle_complete is not True
    ):
        errors.append(
            "record_status closed requires "
            "lifecycle_complete true"
        )

    if (
        lifecycle_complete is False
        and closed_at is not None
    ):
        errors.append(
            "incomplete lifecycle must not declare "
            "closed_at"
        )

    if (
        lifecycle_complete is False
        and closure_reason is not None
    ):
        errors.append(
            "incomplete lifecycle must not declare "
            "closure_reason"
        )

    if lifecycle_complete is True:
        if not isinstance(
            closure_reason,
            str,
        ) or not closure_reason.strip():
            errors.append(
                "complete lifecycle requires "
                "a non-empty closure_reason"
            )

        if not isinstance(
            closed_at,
            str,
        ):
            errors.append(
                "complete lifecycle requires "
                "closed_at"
            )

    # ------------------------------------------------------------------
    # Open issue and closure relationship
    # ------------------------------------------------------------------

    unresolved_issues = [
        issue
        for issue in open_issues
        if isinstance(issue, dict)
        and issue.get("status")
        in {
            "open",
            "under_review",
        }
    ]

    if (
        lifecycle_complete is True
        and unresolved_issues
    ):
        errors.append(
            "complete lifecycle cannot contain "
            "open or under_review issues"
        )

    # ------------------------------------------------------------------
    # Claim support boundary
    # ------------------------------------------------------------------

    assertions = lifecycle.get(
        "assertions",
        {},
    )

    if (
        assertions.get(
            "external_trace_implies_origin_ownership"
        )
        is not False
    ):
        errors.append(
            "external trace binding must not imply "
            "origin ownership"
        )

    if (
        assertions.get(
            "royalty_entitlement_inferred"
        )
        is not False
    ):
        errors.append(
            "latent causality lifecycle must not "
            "infer royalty entitlement"
        )

    if (
        assertions.get(
            "lifecycle_record_replaces_source_evidence"
        )
        is not False
    ):
        errors.append(
            "lifecycle record must not replace "
            "source evidence"
        )

    if (
        assertions.get(
            "universal_causal_claim_made"
        )
        is not False
    ):
        errors.append(
            "universal causal claims are outside "
            "the v0.5 lifecycle boundary"
        )

    return errors


# ---------------------------------------------------------------------------
# Record dispatcher
# ---------------------------------------------------------------------------


def validate_record(
    record: dict[str, Any],
) -> bool:
    """Validate one schema/example pair."""

    print(
        f"[validate] {record['name']}"
    )

    schema_path = record[
        "schema"
    ]

    example_path = record[
        "example"
    ]

    print(
        "  schema : "
        f"{schema_path.relative_to(ROOT)}"
    )

    print(
        "  example: "
        f"{example_path.relative_to(ROOT)}"
    )

    try:
        schema = load_json(
            schema_path
        )

        example = load_yaml(
            example_path
        )

    except RuntimeError as exc:
        print(
            f"Error: {exc}"
        )

        print(
            f"[failed] {example_path.name}"
        )

        return False

    errors = validate_schema(
        schema,
        example,
    )

    validator_name = record[
        "semantic_validator"
    ]

    if validator_name == "observation":
        errors.extend(
            validate_observation_record(
                example
            )
        )

    elif validator_name == "intervention":
        errors.extend(
            validate_intervention_record(
                example
            )
        )

    elif validator_name == "binding":
        errors.extend(
            validate_method_model_binding(
                example
            )
        )

    elif validator_name == "challenge":
        errors.extend(
            validate_verification_challenge(
                example
            )
        )

    elif validator_name == "lifecycle":
        errors.extend(
            validate_unified_lifecycle(
                example
            )
        )

    else:
        errors.append(
            f"unknown semantic validator: "
            f"{validator_name!r}"
        )

    if errors:
        for error in errors:
            print(
                f"Error: {error}"
            )

        print(
            f"[failed] {example_path.name}"
        )

        return False

    print(
        f"[ok] {example_path.name} "
        "is valid"
    )

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Validate all protocol examples."""

    all_valid = True

    for index, record in enumerate(
        RECORDS
    ):
        if index > 0:
            print()

        valid = validate_record(
            record
        )

        if not valid:
            all_valid = False

    print()

    if not all_valid:
        print(
            "[failed] one or more protocol "
            "examples are invalid"
        )

        return 1

    print(
        "[ok] all protocol examples are valid"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )

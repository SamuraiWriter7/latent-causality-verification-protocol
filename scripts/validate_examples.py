from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


RECORDS = [
    {
        "name": "Latent State Observation Record",
        "schema": ROOT
        / "schemas"
        / "latent-state-observation-record.schema.json",
        "example": ROOT
        / "examples"
        / "latent-state-observation-record.example.yaml",
        "semantic_validator": "observation",
    },
    {
        "name": "Causal Intervention Evidence Record",
        "schema": ROOT
        / "schemas"
        / "causal-intervention-evidence.schema.json",
        "example": ROOT
        / "examples"
        / "causal-intervention-evidence.example.yaml",
        "semantic_validator": "intervention",
    },
]


def load_json(path: Path) -> dict[str, Any]:
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


def validate_schema(
    schema: dict[str, Any],
    example: dict[str, Any],
) -> list[str]:
    validator = Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )

    errors = sorted(
        validator.iter_errors(example),
        key=lambda error: list(error.absolute_path),
    )

    messages: list[str] = []

    for error in errors:
        path = ".".join(
            str(part)
            for part in error.absolute_path
        )

        location = path if path else "<root>"

        messages.append(
            f"{location}: {error.message}"
        )

    return messages


def find_duplicates(
    values: list[str],
) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()

    for value in values:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    return duplicates


def validate_observation_record(
    example: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    signals = example.get(
        "observed_signals",
        [],
    )

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

    manifest = example.get(
        "evidence_manifest",
        [],
    )

    manifest_ids = {
        item.get("evidence_id")
        for item in manifest
        if isinstance(item, dict)
    }

    for signal in signals:
        if not isinstance(signal, dict):
            continue

        signal_id = signal.get(
            "signal_id",
            "<unknown-signal>",
        )

        for evidence_ref in signal.get(
            "evidence_refs",
            [],
        ):
            if evidence_ref not in manifest_ids:
                errors.append(
                    f"{signal_id}: evidence reference "
                    f"{evidence_ref!r} not found "
                    "in evidence_manifest"
                )

    return errors


def collect_runs(
    example: dict[str, Any],
) -> list[dict[str, Any]]:
    runs = example.get(
        "runs",
        {},
    )

    collected: list[dict[str, Any]] = []

    baseline = runs.get("baseline")
    intervention = runs.get("intervention")

    if isinstance(baseline, dict):
        collected.append(baseline)

    if isinstance(intervention, dict):
        collected.append(intervention)

    for control in runs.get(
        "controls",
        [],
    ):
        if isinstance(control, dict):
            collected.append(control)

    return collected


def collect_evidence_refs(
    example: dict[str, Any],
) -> list[str]:
    refs: list[str] = []

    for run in collect_runs(example):
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


def validate_intervention_record(
    example: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    manifest = example.get(
        "evidence_manifest",
        [],
    )

    evidence_ids = [
        item["evidence_id"]
        for item in manifest
        if isinstance(item, dict)
        and isinstance(
            item.get("evidence_id"),
            str,
        )
    ]

    for evidence_id in sorted(
        find_duplicates(evidence_ids)
    ):
        errors.append(
            f"duplicate evidence_id: {evidence_id}"
        )

    evidence_id_set = set(evidence_ids)

    for evidence_ref in collect_evidence_refs(
        example
    ):
        if evidence_ref not in evidence_id_set:
            errors.append(
                f"evidence reference "
                f"{evidence_ref!r} not found "
                "in evidence_manifest"
            )

    runs = collect_runs(example)

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

    run_id_set = set(run_ids)

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
        if isinstance(item, dict)
    }

    if (
        primary_metric_id
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

    baseline_metrics = {
        item.get("metric_id"): item
        for item in baseline.get(
            "outcome_measurements",
            [],
        )
        if isinstance(item, dict)
    }

    intervention_metrics = {
        item.get("metric_id"): item
        for item in intervention.get(
            "outcome_measurements",
            [],
        )
        if isinstance(item, dict)
    }

    for metric_delta in metric_deltas:
        if not isinstance(
            metric_delta,
            dict,
        ):
            continue

        metric_id = metric_delta.get(
            "metric_id"
        )

        if metric_id not in baseline_metrics:
            errors.append(
                f"{metric_id!r} not found "
                "in baseline measurements"
            )

        if metric_id not in intervention_metrics:
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
            isinstance(value, (int, float))
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
                    f"intervention - baseline "
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
        and isinstance(effect_count, int)
    ):
        if effect_count > trial_count:
            errors.append(
                "replication_summary.effect_count "
                "cannot exceed trial_count"
            )

        if (
            trial_count > 0
            and isinstance(
                success_rate,
                (int, float),
            )
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
                    f"effect_count / trial_count "
                    f"({expected_rate})"
                )

    if (
        control_design.get("control_type")
        == "matched_baseline"
    ):
        baseline_input = baseline.get(
            "input_ref"
        )

        intervention_input = intervention.get(
            "input_ref"
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


def validate_record(
    record: dict[str, Any],
) -> bool:
    print(
        f"[validate] {record['name']}"
    )

    schema_path = record["schema"]
    example_path = record["example"]

    print(
        f"  schema : "
        f"{schema_path.relative_to(ROOT)}"
    )

    print(
        f"  example: "
        f"{example_path.relative_to(ROOT)}"
    )

    try:
        schema = load_json(schema_path)
        example = load_yaml(example_path)
    except RuntimeError as exc:
        print(f"Error: {exc}")
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


def main() -> int:
    all_valid = True

    for record in RECORDS:
        valid = validate_record(record)

        if not valid:
            all_valid = False

    if not all_valid:
        return 1

    print(
        "[ok] all protocol examples are valid"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())

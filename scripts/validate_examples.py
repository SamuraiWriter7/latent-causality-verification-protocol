from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "latent-state-observation-record.schema.json"
)

EXAMPLE_PATH = (
    ROOT
    / "examples"
    / "latent-state-observation-record.example.yaml"
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"File not found: {path}") from exc
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
        raise RuntimeError(f"File not found: {path}") from exc
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
            str(part) for part in error.absolute_path
        )

        location = path if path else "<root>"

        messages.append(
            f"{location}: {error.message}"
        )

    return messages


def validate_unique_signal_ids(
    example: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    signals = example.get("observed_signals", [])

    ids = [
        signal.get("signal_id")
        for signal in signals
        if isinstance(signal, dict)
    ]

    duplicates = {
        signal_id
        for signal_id in ids
        if ids.count(signal_id) > 1
    }

    for signal_id in sorted(duplicates):
        errors.append(
            f"duplicate signal_id: {signal_id}"
        )

    return errors


def validate_evidence_references(
    example: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    manifest = example.get("evidence_manifest", [])

    manifest_ids = {
        item.get("evidence_id")
        for item in manifest
        if isinstance(item, dict)
    }

    for signal in example.get("observed_signals", []):
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


def main() -> int:
    print(
        "[validate] Latent State Observation Record"
    )
    print(
        "  schema : "
        "schemas/"
        "latent-state-observation-record.schema.json"
    )
    print(
        "  example: "
        "examples/"
        "latent-state-observation-record.example.yaml"
    )

    try:
        schema = load_json(SCHEMA_PATH)
        example = load_yaml(EXAMPLE_PATH)
    except RuntimeError as exc:
        print(f"[error] {exc}")
        return 1

    errors: list[str] = []

    errors.extend(
        validate_schema(schema, example)
    )

    errors.extend(
        validate_unique_signal_ids(example)
    )

    errors.extend(
        validate_evidence_references(example)
    )

    if errors:
        for error in errors:
            print(f"Error: {error}")

        print(
            "[failed] "
            "latent-state-observation-record.example.yaml"
        )

        return 1

    print(
        "[ok] "
        "latent-state-observation-record.example.yaml "
        "is valid"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())

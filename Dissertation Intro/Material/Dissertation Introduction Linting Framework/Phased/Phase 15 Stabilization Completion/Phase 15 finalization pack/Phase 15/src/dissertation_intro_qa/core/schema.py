from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from dissertation_intro_qa.core.envelope import is_enveloped
from dissertation_intro_qa.core.errors import ArtifactTypeError, SchemaError

SCHEMA_MAP = {
    "artifact_envelope": "artifact_envelope.schema.json",
    "audit_report": "audit_report.schema.json",
    "comparison_report": "comparison_report.schema.json",
    "gate_result": "gate_result.schema.json",
    "history_index": "history_index.schema.json",
    "benchmark_summary": "benchmark_summary.schema.json",
    "leaderboard": "leaderboard.schema.json",
    "run_manifest": "run_manifest.schema.json",
    "workflow_plan": "workflow_plan.schema.json",
    "session": "session.schema.json",
    "run_registry": "run_registry.schema.json",
    "project_dashboard": "project_dashboard.schema.json",
    "release_manifest": "release_manifest.schema.json",
}


def _schema_dir() -> Path:
  return Path(__file__).resolve().parents[3] / "schemas"


def load_schema(artifact_type: str) -> Dict[str, Any]:
  try:
    name = SCHEMA_MAP[artifact_type]
  except KeyError as exc:
    raise ArtifactTypeError(f"Unknown artifact type: {artifact_type}") from exc
  path = _schema_dir() / name
  return json.loads(path.read_text(encoding="utf-8"))


def validate_payload(payload: Dict[str, Any], artifact_type: str) -> None:
  schema = load_schema(artifact_type)
  try:
    validate(instance=payload, schema=schema)
  except ValidationError as exc:
    raise SchemaError(f"Payload validation failed for {artifact_type}: {exc.message}") from exc


def validate_envelope(data: Dict[str, Any]) -> None:
  schema = load_schema("artifact_envelope")
  try:
    validate(instance=data, schema=schema)
  except ValidationError as exc:
    raise SchemaError(f"Envelope validation failed: {exc.message}") from exc


def assert_valid_artifact(
    data: Dict[str, Any],
    expected_type: str | None = None,
    allow_legacy: bool = True,
) -> None:
  if is_enveloped(data):
    validate_envelope(data)
    artifact_type = data["artifact_type"]
    if expected_type is not None and artifact_type != expected_type:
      raise ArtifactTypeError(f"Unexpected artifact type: {artifact_type} != {expected_type}")
    validate_payload(data["payload"], artifact_type)
    return

  if not allow_legacy:
    raise SchemaError("Legacy flat artifact is not allowed.")
  if expected_type is None:
    raise SchemaError("Cannot validate legacy artifact without expected_type.")
  validate_payload(data, expected_type)

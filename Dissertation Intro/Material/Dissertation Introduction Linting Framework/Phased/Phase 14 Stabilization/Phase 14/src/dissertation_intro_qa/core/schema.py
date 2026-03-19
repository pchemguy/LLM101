"""Schema validation layer placeholder."""

from __future__ import annotations

from typing import Dict

SCHEMA_MAP = {
    "artifact_envelope": "schemas/artifact_envelope.schema.json",
    "audit_report": "schemas/audit_report.schema.json",
}


def load_schema_name(artifact_type: str) -> str:
  return SCHEMA_MAP[artifact_type]


def assert_valid_artifact(data: Dict, artifact_type: str) -> None:
  if not isinstance(data, dict):
    raise TypeError("Artifact must be dict")
  if artifact_type not in SCHEMA_MAP:
    raise KeyError(f"Unknown artifact type: {artifact_type}")

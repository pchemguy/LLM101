from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.core.envelope import is_enveloped
from dissertation_intro_qa.core.errors import ArtifactTypeError, SchemaError

REQUIRED_PAYLOAD_KEYS = {
    "audit_report": ["metadata", "scores", "defects", "gost_compliance", "summary"],
    "comparison_report": [
        "from_version",
        "to_version",
        "resolved_defects",
        "remaining_defects",
        "new_defects",
        "score_diff",
        "regression_warnings",
        "overall_assessment",
    ],
    "gate_result": ["profile", "passed", "failed_checks", "summary", "scores"],
    "history_index": ["reports", "defect_frequency", "severity_frequency"],
}


def validate_envelope(data: Dict[str, Any]) -> None:
  required = ["artifact_type", "schema_version", "generated_at", "producer", "payload"]
  missing = [key for key in required if key not in data]
  if missing:
    raise SchemaError(f"Invalid envelope, missing keys: {missing}")


def validate_payload(payload: Dict[str, Any], artifact_type: str) -> None:
  required = REQUIRED_PAYLOAD_KEYS.get(artifact_type, [])
  missing = [key for key in required if key not in payload]
  if missing:
    raise SchemaError(
        f"Invalid payload for {artifact_type}, missing keys: {missing}"
    )


def assert_valid_artifact(
    data: Dict[str, Any],
    expected_type: str | None = None,
    allow_legacy: bool = True,
) -> None:
  if is_enveloped(data):
    validate_envelope(data)
    artifact_type = data["artifact_type"]
    if expected_type is not None and artifact_type != expected_type:
      raise ArtifactTypeError(
          f"Unexpected artifact type: {artifact_type} != {expected_type}"
      )
    validate_payload(data["payload"], artifact_type)
    return

  if not allow_legacy:
    raise SchemaError("Legacy flat artifact is not allowed.")
  if expected_type is None:
    raise SchemaError("Cannot validate legacy artifact without expected_type.")
  validate_payload(data, expected_type)

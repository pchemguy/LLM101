from __future__ import annotations
from typing import Any, Dict
from dissertation_intro_qa.core.envelope import is_enveloped

REQUIRED_PAYLOAD_KEYS = {
    "audit_report": ["metadata", "scores", "defects", "gost_compliance", "summary"],
    "gate_result": ["profile", "passed", "failed_checks", "summary", "scores"],
    "history_index": ["reports", "defect_frequency", "severity_frequency"],
    "provider_result": ["provider_label", "document_id", "status"],
    "prompt_run_manifest": [
        "run_id", "timestamp", "provider_mode", "provider_label", "document_id",
        "document_path", "template_path", "rendered_prompt_path",
        "provider_result_path", "status"
    ],
}

def assert_valid_artifact(data: Dict[str, Any], expected_type: str | None = None) -> None:
  if not is_enveloped(data):
    raise ValueError("Expected enveloped artifact.")
  artifact_type = data["artifact_type"]
  if expected_type is not None and artifact_type != expected_type:
    raise ValueError(f"Unexpected artifact type: {artifact_type} != {expected_type}")
  payload = data["payload"]
  missing = [k for k in REQUIRED_PAYLOAD_KEYS.get(artifact_type, []) if k not in payload]
  if missing:
    raise ValueError(f"Missing keys in payload for {artifact_type}: {missing}")

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from dissertation_intro_qa.version import __version__


def wrap_artifact(
    artifact_type: str,
    payload: Dict[str, Any],
    schema_version: str = "1.0.0",
    tool: str = "dissertation_intro_qa",
) -> Dict[str, Any]:
  return {
      "artifact_type": artifact_type,
      "schema_version": schema_version,
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "producer": {"tool": tool, "version": __version__},
      "payload": payload,
  }


def is_enveloped(data: Dict[str, Any]) -> bool:
  return all(
      k in data
      for k in ["artifact_type", "schema_version", "generated_at", "producer", "payload"]
  )


def unwrap_artifact(
    data: Dict[str, Any],
    expected_type: str | None = None,
) -> Dict[str, Any]:
  if is_enveloped(data):
    if expected_type is not None and data["artifact_type"] != expected_type:
      raise ValueError(
          f"Unexpected artifact type: {data['artifact_type']} != {expected_type}"
      )
    return data["payload"]
  return data

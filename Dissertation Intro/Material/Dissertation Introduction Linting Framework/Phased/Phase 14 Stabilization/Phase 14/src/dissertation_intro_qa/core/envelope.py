"""Artifact envelope helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


def wrap_artifact(
    artifact_type: str,
    payload: Dict,
    schema_version: str,
    producer: Dict[str, str],
) -> Dict:
  return {
      "artifact_type": artifact_type,
      "schema_version": schema_version,
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "producer": producer,
      "payload": payload,
  }


def is_enveloped(data: Dict) -> bool:
  return all(k in data for k in ["artifact_type", "schema_version", "generated_at", "producer", "payload"])


def unwrap_artifact(data: Dict, expected_type: str | None = None) -> Dict:
  if is_enveloped(data):
    if expected_type is not None and data["artifact_type"] != expected_type:
      raise ValueError(f"Unexpected artifact type: {data['artifact_type']} != {expected_type}")
    return data["payload"]
  return data

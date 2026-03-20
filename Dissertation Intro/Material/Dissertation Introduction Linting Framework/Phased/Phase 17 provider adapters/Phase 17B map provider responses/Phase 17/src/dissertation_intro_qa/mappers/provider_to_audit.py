from __future__ import annotations
import json
from typing import Any, Dict
from dissertation_intro_qa.artifacts.audit import make_audit_artifact

def _normalize_audit_payload(payload: Dict[str, Any], document_id: str) -> Dict[str, Any]:
  payload = dict(payload)
  payload.setdefault("metadata", {})
  payload["metadata"].setdefault("document_id", document_id)
  payload["metadata"].setdefault("language", "ru")
  payload["metadata"].setdefault("audit_mode", "provider_mapped")
  payload["metadata"].setdefault("date", "2026-03-20")
  payload.setdefault("scores", {})
  payload.setdefault("defects", [])
  payload.setdefault("gost_compliance", {})
  payload.setdefault("summary", {})
  return payload

def map_provider_result_to_audit_artifact(
    provider_result: Dict[str, Any],
    *,
    document_id: str,
    mapping_config: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
  cfg = dict(mapping_config or {})
  mode = cfg.get("mode", "demo_structured")

  if mode == "demo_structured":
    if "structured_audit" not in provider_result:
      raise ValueError("Provider result missing 'structured_audit' for demo_structured mode.")
    payload = _normalize_audit_payload(provider_result["structured_audit"], document_id)
    return make_audit_artifact(payload)

  if mode == "json_payload":
    field_name = cfg.get("field_name", "audit_payload")
    if field_name not in provider_result:
      raise ValueError(f"Provider result missing mapping field: {field_name}")
    raw = provider_result[field_name]
    if isinstance(raw, str):
      raw = json.loads(raw)
    if not isinstance(raw, dict):
      raise ValueError("Mapped provider payload must be a JSON object.")
    payload = _normalize_audit_payload(raw, document_id)
    return make_audit_artifact(payload)

  raise ValueError(f"Unsupported provider mapping mode: {mode}")

from __future__ import annotations
from typing import Dict, Any
from dissertation_intro_qa.artifacts.audit import make_audit_artifact
from dissertation_intro_qa.artifacts.gate import make_gate_artifact
from dissertation_intro_qa.artifacts.history import make_history_artifact
from dissertation_intro_qa.core.aggregation import history_index
from dissertation_intro_qa.core.envelope import unwrap_artifact
from dissertation_intro_qa.core.io import read_json, write_json, write_text
from dissertation_intro_qa.core.render import render_audit_md, render_dashboard_md, render_gate_md, render_repair_plan_md
from dissertation_intro_qa.pipeline.provider_audit_bridge import run_provider_backed_audit

def _demo_local_audit_payload(document_id: str) -> Dict[str, Any]:
  return {
      "metadata": {
          "document_id": document_id,
          "language": "ru",
          "audit_mode": "pipeline_local_demo",
          "date": "2026-03-20",
      },
      "scores": {"SC1": 1, "LC1": 1},
      "defects": [{
          "code": "GAP-02",
          "severity": "major",
          "section": "Степень разработанности / пробел",
          "description": "Пробел не сформулирован явно.",
          "evidence": "Формулировка пробела отсутствует.",
          "recommendation": "Сформулировать конкретный научный пробел.",
      }],
      "gost_compliance": {
          "relevance": True,
          "degree_of_development": True,
          "goals_tasks": True,
          "novelty": True,
          "significance": True,
          "methods": False,
          "defense_propositions": False,
          "reliability": False,
          "approbation": True,
      },
      "summary": {
          "critical_count": 0,
          "major_count": 1,
          "moderate_count": 0,
          "minor_count": 0,
          "overall_verdict": "pipeline_local_demo",
      },
  }

def step_audit(context: Dict[str, Any]) -> Dict[str, Any]:
  pipeline_cfg = context["config"].get("pipeline", {})
  audit_mode = pipeline_cfg.get("audit_mode", "local_demo")
  input_cfg = context["config"].get("input", {})
  document_id = input_cfg.get("document_id", "unknown_document")

  if audit_mode == "provider_bridge":
    bridged = run_provider_backed_audit(config=context["config"], run_dir=context["run_dir"])
    artifact = bridged["artifact"]
    payload = bridged["payload"]
  elif audit_mode == "local_demo":
    payload = _demo_local_audit_payload(document_id)
    artifact = make_audit_artifact(payload)
  else:
    raise ValueError(f"Unsupported pipeline audit_mode: {audit_mode}")

  path = context["run_dir"] / "audit.json"
  write_json(path, artifact)
  write_text(context["run_dir"] / "audit.md", render_audit_md(payload))
  context["artifacts"]["audit_report"] = path
  return {"artifact_type": "audit_report", "path": str(path)}

def step_gate(context: Dict[str, Any]) -> Dict[str, Any]:
  audit_path = context["artifacts"]["audit_report"]
  audit_payload = unwrap_artifact(read_json(audit_path), expected_type="audit_report")
  summary = audit_payload.get("summary", {})
  failed = []
  if summary.get("critical_count", 0) > 0:
    failed.append("critical_count > 0")
  if not audit_payload.get("gost_compliance", {}).get("methods", False):
    failed.append("missing_gost_component=methods")
  payload = {
      "profile": "strict",
      "passed": not failed,
      "failed_checks": failed,
      "summary": summary,
      "scores": audit_payload.get("scores", {}),
  }
  artifact = make_gate_artifact(payload)
  path = context["run_dir"] / "gate.json"
  write_json(path, artifact)
  write_text(context["run_dir"] / "gate.md", render_gate_md(payload))
  context["artifacts"]["gate_result"] = path
  return {"artifact_type": "gate_result", "path": str(path)}

def step_repair_plan(context: Dict[str, Any]) -> Dict[str, Any]:
  audit_path = context["artifacts"]["audit_report"]
  audit_payload = unwrap_artifact(read_json(audit_path), expected_type="audit_report")
  path = context["run_dir"] / "repair_plan.md"
  write_text(path, render_repair_plan_md(audit_payload))
  context["artifacts"]["repair_plan"] = path
  return {"artifact_type": "repair_plan_md", "path": str(path)}

def step_history_index(context: Dict[str, Any]) -> Dict[str, Any]:
  payload = history_index([context["artifacts"]["audit_report"]])
  artifact = make_history_artifact(payload)
  path = context["run_dir"] / "history_index.json"
  write_json(path, artifact)
  context["artifacts"]["history_index"] = path
  return {"artifact_type": "history_index", "path": str(path)}

def step_dashboard(context: Dict[str, Any]) -> Dict[str, Any]:
  history_path = context["artifacts"]["history_index"]
  payload = unwrap_artifact(read_json(history_path), expected_type="history_index")
  path = context["run_dir"] / "dashboard.md"
  write_text(path, render_dashboard_md(payload))
  context["artifacts"]["dashboard"] = path
  return {"artifact_type": "dashboard_md", "path": str(path)}

STEP_REGISTRY = {
    "audit": step_audit,
    "gate": step_gate,
    "repair-plan": step_repair_plan,
    "history-index": step_history_index,
    "dashboard": step_dashboard,
}

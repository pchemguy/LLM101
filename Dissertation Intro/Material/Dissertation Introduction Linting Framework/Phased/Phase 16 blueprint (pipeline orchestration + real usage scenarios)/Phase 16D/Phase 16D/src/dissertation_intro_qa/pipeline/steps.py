from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from dissertation_intro_qa.artifacts.gate import make_gate_artifact
from dissertation_intro_qa.artifacts.history import make_history_artifact
from dissertation_intro_qa.core.aggregation import history_index
from dissertation_intro_qa.core.envelope import unwrap_artifact
from dissertation_intro_qa.core.io import read_json, write_json, write_text
from dissertation_intro_qa.core.render import (
    render_audit_md,
    render_dashboard_md,
    render_gate_md,
    render_repair_plan_md,
)
from dissertation_intro_qa.executors.factory import build_audit_executor


def step_audit(context: Dict[str, Any]) -> Dict[str, Any]:
  pipeline_cfg = context["config"].get("pipeline", {})
  executor_cfg = dict(pipeline_cfg.get("audit_executor", {}))
  input_cfg = context["config"].get("input", {})
  input_path = Path(input_cfg.get("path", ""))
  document_id = input_cfg.get("document_id", input_path.stem or "unknown_document")

  executor = build_audit_executor(executor_cfg)
  artifact = executor.execute(
      input_path=input_path,
      document_id=document_id,
      work_dir=context["run_dir"],
      executor_config=executor_cfg,
  )

  path = context["run_dir"] / "audit.json"
  write_json(path, artifact)
  payload = unwrap_artifact(artifact, expected_type="audit_report")
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

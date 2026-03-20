from __future__ import annotations

from typing import Dict


def render_audit_md(report: Dict) -> str:
  lines = ["# Audit Report", ""]
  lines.append(f"- document_id: {report.get('metadata', {}).get('document_id', '')}")
  lines.append("")
  lines.append("## Defects")
  for defect in report.get("defects", []):
    lines.append(f"- {defect.get('code', '')}: {defect.get('description', '')}")
  return "\n".join(lines) + "\n"


def render_gate_md(gate: Dict) -> str:
  lines = ["# Gate Result", ""]
  lines.append(f"- profile: {gate.get('profile', '')}")
  lines.append(f"- passed: {gate.get('passed', False)}")
  lines.append("")
  lines.append("## Failed checks")
  for item in gate.get("failed_checks", []):
    lines.append(f"- {item}")
  return "\n".join(lines) + "\n"


def render_dashboard_md(index: Dict) -> str:
  lines = ["# Dashboard", "", "## Reports"]
  for item in index.get("reports", []):
    lines.append(f"- {item.get('document_id', '')}")
  return "\n".join(lines) + "\n"


def render_repair_plan_md(report: Dict) -> str:
  lines = ["# Repair Plan", ""]
  for defect in report.get("defects", []):
    lines.append(f"- {defect.get('code', '')}: {defect.get('recommendation', '')}")
  return "\n".join(lines) + "\n"

from __future__ import annotations

from typing import Any, Dict


def render_audit_md(report: Dict[str, Any]) -> str:
  meta = report.get("metadata", {})
  lines = [
      "# Audit Report",
      "",
      f"- Document ID: {meta.get('document_id', '')}",
      f"- Language: {meta.get('language', '')}",
      f"- Audit mode: {meta.get('audit_mode', '')}",
      f"- Date: {meta.get('date', '')}",
      "",
      "## Scores",
  ]
  for key, value in sorted(report.get("scores", {}).items()):
    lines.append(f"- {key}: {value}")
  lines.extend(["", "## Defects"])
  defects = sorted(report.get("defects", []), key=lambda d: (d.get("severity", ""), d.get("code", ""), d.get("section", "")))
  if not defects:
    lines.append("- No defects listed.")
  else:
    for defect in defects:
      lines.extend([
          f"- [{defect.get('severity', '').upper()}] {defect.get('code', '')}",
          f"  - Section: {defect.get('section', '')}",
          f"  - Description: {defect.get('description', '')}",
          f"  - Evidence: {defect.get('evidence', '')}",
          f"  - Recommendation: {defect.get('recommendation', '')}",
      ])
  return "\n".join(lines) + "\n"


def render_comparison_md(comp: Dict[str, Any]) -> str:
  lines = [f"# Comparison: {comp.get('from_version', '')} → {comp.get('to_version', '')}", "", "## Resolved defects"]
  lines.extend(f"- {item}" for item in comp.get("resolved_defects", []))
  lines.extend(["", "## Remaining defects"])
  lines.extend(f"- {item}" for item in comp.get("remaining_defects", []))
  lines.extend(["", "## New defects"])
  lines.extend(f"- {item}" for item in comp.get("new_defects", []))
  return "\n".join(lines) + "\n"


def render_gate_md(gate: Dict[str, Any]) -> str:
  lines = [f"# Gate Result: {gate.get('profile', '')}", "", f"- Passed: {gate.get('passed', False)}", "", "## Failed checks"]
  failed = gate.get("failed_checks", [])
  lines.extend([f"- {item}" for item in failed] or ["- None"])
  return "\n".join(lines) + "\n"


def render_dashboard_md(index: Dict[str, Any]) -> str:
  lines = ["# QA Dashboard", "", "## Reports"]
  for item in sorted(index.get("reports", []), key=lambda x: x.get("document_id", "")):
    summary = item.get("summary", {})
    lines.append(
        f"- {item.get('document_id', '')}: critical={summary.get('critical_count', 0)}, "
        f"major={summary.get('major_count', 0)}, moderate={summary.get('moderate_count', 0)}, "
        f"minor={summary.get('minor_count', 0)}"
    )
  return "\n".join(lines) + "\n"

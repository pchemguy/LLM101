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
  for key, value in report.get("scores", {}).items():
    lines.append(f"- {key}: {value}")
  lines.extend(["", "## Defects"])
  defects = report.get("defects", [])
  if not defects:
    lines.append("- No defects listed.")
  else:
    defects = sorted(defects, key=lambda d: (d.get("severity", ""), d.get("code", ""), d.get("section", "")))
    for defect in defects:
      lines.extend([
          f"- [{defect.get('severity', '').upper()}] {defect.get('code', '')}",
          f"  - Section: {defect.get('section', '')}",
          f"  - Description: {defect.get('description', '')}",
          f"  - Evidence: {defect.get('evidence', '')}",
          f"  - Recommendation: {defect.get('recommendation', '')}",
      ])
  lines.extend(["", "## Summary"])
  for key, value in report.get("summary", {}).items():
    lines.append(f"- {key}: {value}")
  return "\n".join(lines) + "\n"


def render_comparison_md(comp: Dict[str, Any]) -> str:
  lines = [
      f"# Comparison: {comp.get('from_version', '')} → {comp.get('to_version', '')}",
      "",
      "## Resolved defects",
  ]
  for item in comp.get("resolved_defects", []):
    lines.append(f"- {item}")
  lines.extend(["", "## Remaining defects"])
  for item in comp.get("remaining_defects", []):
    lines.append(f"- {item}")
  lines.extend(["", "## New defects"])
  for item in comp.get("new_defects", []):
    lines.append(f"- {item}")
  lines.extend(["", "## Score delta"])
  for key, delta in comp.get("score_diff", {}).items():
    lines.append(f"- {key}: {delta:+}")
  lines.extend(["", "## Regression warnings"])
  for item in comp.get("regression_warnings", []):
    lines.append(f"- {item}")
  lines.extend(["", "## Overall assessment", comp.get("overall_assessment", "")])
  return "\n".join(lines) + "\n"


def render_gate_md(gate: Dict[str, Any]) -> str:
  lines = [
      f"# Gate Result: {gate.get('profile', '')}",
      "",
      f"- Passed: {gate.get('passed', False)}",
      "",
      "## Failed checks",
  ]
  failed = gate.get("failed_checks", [])
  if failed:
    lines.extend(f"- {item}" for item in failed)
  else:
    lines.append("- None")
  lines.extend(["", "## Summary"])
  for key, value in gate.get("summary", {}).items():
    lines.append(f"- {key}: {value}")
  lines.extend(["", "## Scores"])
  for key, value in gate.get("scores", {}).items():
    lines.append(f"- {key}: {value}")
  return "\n".join(lines) + "\n"


def render_dashboard_md(index: Dict[str, Any]) -> str:
  lines = ["# QA Dashboard", "", "## Reports"]
  reports = sorted(index.get("reports", []), key=lambda x: x.get("document_id", ""))
  for item in reports:
    summary = item.get("summary", {})
    lines.append(
        f"- {item.get('document_id', '')}: critical={summary.get('critical_count', 0)}, "
        f"major={summary.get('major_count', 0)}, moderate={summary.get('moderate_count', 0)}, "
        f"minor={summary.get('minor_count', 0)}"
    )
  lines.extend(["", "## Defect frequency"])
  for code, count in sorted(index.get("defect_frequency", {}).items()):
    lines.append(f"- {code}: {count}")
  lines.extend(["", "## Severity frequency"])
  for sev, count in sorted(index.get("severity_frequency", {}).items()):
    lines.append(f"- {sev}: {count}")
  return "\n".join(lines) + "\n"

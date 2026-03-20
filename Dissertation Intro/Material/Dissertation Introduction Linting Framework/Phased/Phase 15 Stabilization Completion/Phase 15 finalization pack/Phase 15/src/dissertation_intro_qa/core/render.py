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


def render_benchmark_summary_md(summary: Dict[str, Any]) -> str:
  lines = [
      f"# Benchmark Summary: {summary.get('run_label', '')}",
      "",
      f"- case_count: {summary.get('case_count', 0)}",
      f"- macro_recall: {summary.get('macro_recall', 0.0)}",
      f"- macro_precision: {summary.get('macro_precision', 0.0)}",
      "",
      "## Most missed expected codes",
  ]
  missed = summary.get("most_missed_codes", {})
  lines.extend([f"- {code}: {count}" for code, count in sorted(missed.items())] or ["- None"])
  lines.extend(["", "## Most extra codes"])
  extra = summary.get("most_extra_codes", {})
  lines.extend([f"- {code}: {count}" for code, count in sorted(extra.items())] or ["- None"])
  return "\n".join(lines) + "\n"


def render_leaderboard_md(data: Dict[str, Any]) -> str:
  lines = ["# Prompt / Run Leaderboard", ""]
  for row in data.get("leaderboard", []):
    lines.append(
        f"- #{row['rank']} {row['run_label']}: macro_recall={row['macro_recall']}, "
        f"macro_precision={row['macro_precision']}, case_count={row['case_count']}"
    )
  return "\n".join(lines) + "\n"


def render_run_manifest_md(manifest: Dict[str, Any]) -> str:
  lines = [
      f"# Run Manifest: {manifest.get('run_label', '')}",
      "",
      f"- prompt_variant: {manifest.get('prompt_variant', '')}",
      f"- profile: {manifest.get('profile', '')}",
      f"- generated_at: {manifest.get('generated_at', '')}",
      f"- case_count: {manifest.get('case_count', 0)}",
      "",
      "## Cases",
  ]
  for item in manifest.get("items", []):
    lines.extend([
      f"### {item.get('case_id', '')}",
      f"- case_file: {item.get('case_file', '')}",
      f"- expected_file: {item.get('expected_file', '')}",
      f"- result_json_target: {item.get('result_json_target', '')}",
      f"- status: {item.get('status', '')}",
      "",
    ])
  return "\n".join(lines) + "\n"


def render_workflow_plan_md(plan: Dict[str, Any]) -> str:
  wf = plan.get("workflow", {})
  lines = [
      f"# Benchmark Workflow Plan: {wf.get('run_label', '')}",
      "",
      f"- benchmark_root: {wf.get('benchmark_root', '')}",
      f"- prompt_variant: {wf.get('prompt_variant', '')}",
      f"- profile: {wf.get('profile', '')}",
      "",
      f"- case_count: {plan.get('case_discovery', {}).get('case_count', 0)}",
      "",
      "## Score command",
      "```bash",
      plan.get("score_command", ""),
      "```",
  ]
  return "\n".join(lines) + "\n"


def render_registry_md(data: Dict[str, Any]) -> str:
  lines = [
      "# Run Registry",
      "",
      f"- session_count: {data.get('session_count', 0)}",
      f"- total_runs: {data.get('total_runs', 0)}",
      "",
      "## Sessions",
  ]
  for item in data.get("sessions", []):
    lines.extend([
      f"### {item.get('session_id', '')}",
      f"- description: {item.get('description', '')}",
      f"- run_count: {item.get('run_count', 0)}",
      "",
    ])
  return "\n".join(lines) + "\n"


def render_project_dashboard_md(data: Dict[str, Any]) -> str:
  best = data.get("best_run", {})
  lines = [
      "# Consolidated Project Dashboard",
      "",
      f"- run_count: {data.get('run_count', 0)}",
      "",
      "## Best run",
      f"- run_label: {best.get('run_label', '')}",
      f"- macro_recall: {best.get('macro_recall', 0.0)}",
      f"- macro_precision: {best.get('macro_precision', 0.0)}",
  ]
  return "\n".join(lines) + "\n"


def render_release_manifest_md(data: Dict[str, Any]) -> str:
  lines = [
      "# Release Bundle Manifest",
      "",
      f"- project_root: {data.get('project_root', '')}",
      f"- out_dir: {data.get('out_dir', '')}",
      f"- include_demo: {data.get('include_demo', False)}",
      "",
      "## Copied items",
  ]
  for item in data.get("copied_items", []):
    lines.append(f"- {item}")
  return "\n".join(lines) + "\n"

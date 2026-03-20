from __future__ import annotations

from typing import Any, Dict


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

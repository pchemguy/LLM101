from __future__ import annotations
from typing import Dict

def render_dashboard_md(index: Dict) -> str:
  lines = ["# Dashboard", "", "## Reports"]
  for item in index.get("reports", []):
    summary = item.get("summary", {})
    lines.append(
        f"- {item.get('document_id', '')}: "
        f"critical={summary.get('critical_count', 0)}, "
        f"major={summary.get('major_count', 0)}, "
        f"moderate={summary.get('moderate_count', 0)}, "
        f"minor={summary.get('minor_count', 0)}"
    )
  return "\n".join(lines) + "\n"

def render_batch_dashboard_md(batch: Dict) -> str:
  lines = [
      f"# Batch Dashboard: {batch.get('batch_id', '')}",
      "",
      f"- run_count: {batch.get('run_count', 0)}",
      f"- failed_run_count: {batch.get('failed_run_count', 0)}",
      f"- gate_failed_count: {batch.get('gate_failed_count', 0)}",
      "",
      "## Runs",
  ]
  for run in batch.get("runs", []):
    lines.append(
        f"- {run.get('document_id', '')}: exit_code={run.get('exit_code', '')}, run_dir={run.get('run_dir', '')}"
    )
  return "\n".join(lines) + "\n"

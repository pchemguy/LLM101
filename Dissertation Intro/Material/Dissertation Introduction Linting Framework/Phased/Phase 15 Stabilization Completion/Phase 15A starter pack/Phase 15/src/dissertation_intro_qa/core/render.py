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
  if missed:
    for code, count in sorted(missed.items()):
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Most extra codes"])
  extra = summary.get("most_extra_codes", {})
  if extra:
    for code, count in sorted(extra.items()):
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Severity failures"])
  sev = summary.get("severity_failure_codes", {})
  if sev:
    for code, count in sorted(sev.items()):
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Case results"])
  for case in summary.get("cases", []):
    lines.extend([
        f"### {case.get('case_id', '')}",
        f"- recall: {case.get('recall', 0.0)}",
        f"- precision: {case.get('precision', 0.0)}",
        f"- matched_codes: {', '.join(case.get('matched_codes', [])) or 'None'}",
        f"- missed_expected_codes: {', '.join(case.get('missed_expected_codes', [])) or 'None'}",
        f"- extra_codes: {', '.join(case.get('extra_codes', [])) or 'None'}",
        "",
    ])
  return "\n".join(lines) + "\n"


def render_leaderboard_md(data: Dict[str, Any]) -> str:
  lines = ["# Prompt / Run Leaderboard", ""]
  for row in data.get("leaderboard", []):
    lines.append(
        f"- #{row['rank']} {row['run_label']}: macro_recall={row['macro_recall']}, "
        f"macro_precision={row['macro_precision']}, case_count={row['case_count']}"
    )
  return "\n".join(lines) + "\n"

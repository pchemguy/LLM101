#!/usr/bin/env python3
"""Phase 10 orchestration layer for benchmark workflow.

This runner ties together:
- benchmark case discovery
- run manifest recording
- benchmark scorer invocation planning
- leaderboard assembly planning
- regression summary generation

It does not call remote LLMs. Instead, it orchestrates local artifacts and
produces machine-readable manifests and markdown summaries around benchmark runs.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
  with path.open("r", encoding="utf-8") as f:
    return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def write_text(path: Path, text: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(text, encoding="utf-8")


def discover_cases(cases_dir: Path, expected_dir: Path) -> Dict[str, Any]:
  cases = []
  expected_map = {p.stem: p for p in expected_dir.glob("*.json")}
  for case_path in sorted(cases_dir.glob("*.md")):
    case_id = case_path.stem
    expected_path = expected_map.get(case_id)
    cases.append(
        {
            "case_id": case_id,
            "case_file": str(case_path),
            "expected_file": str(expected_path) if expected_path else "",
            "has_expected": expected_path is not None,
        }
    )
  return {"case_count": len(cases), "cases": cases}


def build_run_manifest(
    run_label: str,
    prompt_variant: str,
    profile: str,
    cases_info: Dict[str, Any],
    results_dir: Path,
) -> Dict[str, Any]:
  items = []
  for case in cases_info.get("cases", []):
    case_id = case["case_id"]
    items.append(
        {
            "case_id": case_id,
            "case_file": case["case_file"],
            "expected_file": case["expected_file"],
            "result_json_target": str(results_dir / f"{case_id}.json"),
            "status": "pending",
        }
    )
  return {
      "run_label": run_label,
      "prompt_variant": prompt_variant,
      "profile": profile,
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "case_count": len(items),
      "items": items,
  }


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
    lines.extend(
        [
            f"### {item.get('case_id', '')}",
            f"- case_file: {item.get('case_file', '')}",
            f"- expected_file: {item.get('expected_file', '')}",
            f"- result_json_target: {item.get('result_json_target', '')}",
            f"- status: {item.get('status', '')}",
            "",
        ]
    )
  return "\n".join(lines) + "\n"


def collect_run_summaries(summaries: List[Path]) -> Dict[str, Any]:
  runs = []
  for path in summaries:
    data = read_json(path)
    runs.append(
        {
            "run_label": data.get("run_label", path.stem),
            "case_count": data.get("case_count", 0),
            "macro_recall": data.get("macro_recall", 0.0),
            "macro_precision": data.get("macro_precision", 0.0),
            "most_missed_codes": data.get("most_missed_codes", {}),
            "most_extra_codes": data.get("most_extra_codes", {}),
            "severity_failure_codes": data.get("severity_failure_codes", {}),
        }
    )
  return {"run_count": len(runs), "runs": runs}


def render_regression_summary_md(data: Dict[str, Any]) -> str:
  lines = ["# Regression Summary", "", f"- run_count: {data.get('run_count', 0)}", "", "## Runs"]
  for run in sorted(data.get("runs", []), key=lambda x: x.get("run_label", "")):
    lines.extend(
        [
            f"### {run.get('run_label', '')}",
            f"- case_count: {run.get('case_count', 0)}",
            f"- macro_recall: {run.get('macro_recall', 0.0)}",
            f"- macro_precision: {run.get('macro_precision', 0.0)}",
        ]
    )
    mm = run.get("most_missed_codes", {})
    if mm:
      lines.append("- most_missed_codes:")
      for code, count in mm.items():
        lines.append(f"  - {code}: {count}")
    me = run.get("most_extra_codes", {})
    if me:
      lines.append("- most_extra_codes:")
      for code, count in me.items():
        lines.append(f"  - {code}: {count}")
    sf = run.get("severity_failure_codes", {})
    if sf:
      lines.append("- severity_failure_codes:")
      for code, count in sf.items():
        lines.append(f"  - {code}: {count}")
    lines.append("")
  return "\n".join(lines) + "\n"


def build_workflow_plan(
    benchmark_root: Path,
    run_label: str,
    prompt_variant: str,
    profile: str,
) -> Dict[str, Any]:
  cases_dir = benchmark_root / "cases"
  expected_dir = benchmark_root / "expected"
  results_dir = benchmark_root / "results" / run_label
  cases_info = discover_cases(cases_dir, expected_dir)
  manifest = build_run_manifest(run_label, prompt_variant, profile, cases_info, results_dir)
  score_cmd = (
      "python benchmark_scorer.py score-run "
      f"--expected-dir {expected_dir} "
      f"--actual-dir {results_dir} "
      f"--run-label {run_label} "
      f"--out-json {benchmark_root / 'results' / (run_label + '.summary.json')} "
      f"--out-md {benchmark_root / 'results' / (run_label + '.summary.md')}"
  )
  return {
      "workflow": {
          "benchmark_root": str(benchmark_root),
          "run_label": run_label,
          "prompt_variant": prompt_variant,
          "profile": profile,
      },
      "case_discovery": cases_info,
      "manifest": manifest,
      "score_command": score_cmd,
  }


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
      "",
      "## Cases",
  ]
  for case in plan.get("case_discovery", {}).get("cases", []):
    lines.append(
        f"- {case.get('case_id', '')}: has_expected={case.get('has_expected', False)}"
    )
  return "\n".join(lines) + "\n"


def main() -> int:
  parser = argparse.ArgumentParser(prog="benchmark_orchestrator")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("discover")
  p.add_argument("--cases-dir", required=True)
  p.add_argument("--expected-dir", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("manifest")
  p.add_argument("--benchmark-root", required=True)
  p.add_argument("--run-label", required=True)
  p.add_argument("--prompt-variant", required=True)
  p.add_argument("--profile", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("workflow-plan")
  p.add_argument("--benchmark-root", required=True)
  p.add_argument("--run-label", required=True)
  p.add_argument("--prompt-variant", required=True)
  p.add_argument("--profile", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("regression-summary")
  p.add_argument("summaries", nargs="+")
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  args = parser.parse_args()

  if args.cmd == "discover":
    data = discover_cases(Path(args.cases_dir), Path(args.expected_dir))
    write_json(Path(args.out_json), data)
    if args.out_md:
      lines = ["# Case Discovery", "", f"- case_count: {data.get('case_count', 0)}", ""]
      for case in data.get("cases", []):
        lines.append(
            f"- {case.get('case_id', '')}: has_expected={case.get('has_expected', False)}"
        )
      write_text(Path(args.out_md), "\n".join(lines) + "\n")
    return 0

  if args.cmd == "manifest":
    cases_info = discover_cases(
        Path(args.benchmark_root) / "cases",
        Path(args.benchmark_root) / "expected",
    )
    manifest = build_run_manifest(
        args.run_label,
        args.prompt_variant,
        args.profile,
        cases_info,
        Path(args.benchmark_root) / "results" / args.run_label,
    )
    write_json(Path(args.out_json), manifest)
    if args.out_md:
      write_text(Path(args.out_md), render_run_manifest_md(manifest))
    return 0

  if args.cmd == "workflow-plan":
    plan = build_workflow_plan(
        Path(args.benchmark_root),
        args.run_label,
        args.prompt_variant,
        args.profile,
    )
    write_json(Path(args.out_json), plan)
    if args.out_md:
      write_text(Path(args.out_md), render_workflow_plan_md(plan))
    return 0

  if args.cmd == "regression-summary":
    data = collect_run_summaries([Path(p) for p in args.summaries])
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), render_regression_summary_md(data))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

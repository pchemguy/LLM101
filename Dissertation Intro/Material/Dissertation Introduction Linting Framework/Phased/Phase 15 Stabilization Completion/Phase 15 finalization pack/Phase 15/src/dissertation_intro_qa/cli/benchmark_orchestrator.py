from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from dissertation_intro_qa.artifacts.benchmark import make_run_manifest_artifact, make_workflow_plan_artifact
from dissertation_intro_qa.core.aggregation import build_run_manifest, collect_run_summaries, discover_cases
from dissertation_intro_qa.core.errors import ArtifactTypeError, ConfigurationError, ContractViolation, SchemaError
from dissertation_intro_qa.core.exit_codes import INTERNAL_ERROR, SCHEMA_ERROR, SUCCESS, USER_ERROR
from dissertation_intro_qa.core.io import write_json, write_text
from dissertation_intro_qa.core.render import render_run_manifest_md, render_workflow_plan_md
from dissertation_intro_qa.core.schema import assert_valid_artifact


def build_workflow_plan(benchmark_root: Path, run_label: str, prompt_variant: str, profile: str) -> dict:
  cases_dir = benchmark_root / "cases"
  expected_dir = benchmark_root / "expected"
  results_dir = benchmark_root / "results" / run_label
  cases_info = discover_cases(cases_dir, expected_dir)
  manifest = build_run_manifest(run_label, prompt_variant, profile, cases_info, results_dir)
  score_cmd = (
      "benchmark-scorer score-run "
      f"--expected-dir {expected_dir} "
      f"--actual-dir {results_dir} "
      f"--run-label {run_label} "
      f"--out-json {benchmark_root / 'results' / (run_label + '.summary.json')}"
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


def main(argv: List[str] | None = None) -> int:
  try:
    parser = argparse.ArgumentParser(prog="benchmark-orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("discover")
    p.add_argument("--cases-dir", required=True)
    p.add_argument("--expected-dir", required=True)
    p.add_argument("--out-json", required=True)

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

    args = parser.parse_args(argv)

    if args.cmd == "discover":
      data = discover_cases(Path(args.cases_dir), Path(args.expected_dir))
      write_json(Path(args.out_json), data)
      return SUCCESS

    if args.cmd == "manifest":
      cases_info = discover_cases(Path(args.benchmark_root) / "cases", Path(args.benchmark_root) / "expected")
      payload = build_run_manifest(args.run_label, args.prompt_variant, args.profile, cases_info, Path(args.benchmark_root) / "results" / args.run_label)
      artifact = make_run_manifest_artifact(payload)
      assert_valid_artifact(artifact, expected_type="run_manifest", allow_legacy=False)
      write_json(Path(args.out_json), artifact)
      if args.out_md:
        write_text(Path(args.out_md), render_run_manifest_md(payload))
      return SUCCESS

    if args.cmd == "workflow-plan":
      payload = build_workflow_plan(Path(args.benchmark_root), args.run_label, args.prompt_variant, args.profile)
      artifact = make_workflow_plan_artifact(payload)
      assert_valid_artifact(artifact, expected_type="workflow_plan", allow_legacy=False)
      write_json(Path(args.out_json), artifact)
      if args.out_md:
        write_text(Path(args.out_md), render_workflow_plan_md(payload))
      return SUCCESS

    if args.cmd == "regression-summary":
      payload = collect_run_summaries([Path(p) for p in args.summaries])
      write_json(Path(args.out_json), payload)
      return SUCCESS

    return USER_ERROR

  except (SchemaError, ArtifactTypeError, ContractViolation):
    return SCHEMA_ERROR
  except (FileNotFoundError, ValueError, ConfigurationError):
    return USER_ERROR
  except Exception:
    return INTERNAL_ERROR


if __name__ == "__main__":
  raise SystemExit(main())

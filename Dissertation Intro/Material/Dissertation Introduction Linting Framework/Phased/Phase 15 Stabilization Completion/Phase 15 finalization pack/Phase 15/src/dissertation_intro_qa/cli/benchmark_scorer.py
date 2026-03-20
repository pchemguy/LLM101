from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from dissertation_intro_qa.artifacts.benchmark import (
    make_benchmark_summary_artifact,
    make_leaderboard_artifact,
)
from dissertation_intro_qa.core.aggregation import aggregate_case_diffs, build_leaderboard, case_diff
from dissertation_intro_qa.core.envelope import unwrap_artifact
from dissertation_intro_qa.core.errors import ArtifactTypeError, ConfigurationError, ContractViolation, SchemaError
from dissertation_intro_qa.core.exit_codes import INTERNAL_ERROR, SCHEMA_ERROR, SUCCESS, USER_ERROR
from dissertation_intro_qa.core.io import read_json, write_json, write_text
from dissertation_intro_qa.core.render import render_benchmark_summary_md, render_leaderboard_md
from dissertation_intro_qa.core.schema import assert_valid_artifact


def infer_case_id_from_filename(path: Path) -> str:
  return path.stem.split(".")[0]


def score_run(expected_dir: Path, actual_dir: Path, run_label: str) -> dict:
  expected_files = sorted(expected_dir.glob("*.json"))
  actual_map = {infer_case_id_from_filename(path): path for path in sorted(actual_dir.glob("*.json"))}
  case_diffs = []

  for exp_path in expected_files:
    expected = read_json(exp_path)
    case_id = expected.get("case_id", exp_path.stem)
    actual_path = actual_map.get(case_id)
    if actual_path is None:
      case_diffs.append({
          "case_id": case_id,
          "matched_codes": [],
          "missed_expected_codes": expected.get("expected_defect_codes", []),
          "extra_codes": [],
          "severity_failures": [],
          "recall": 0.0,
          "precision": 0.0,
          "expected_notes": expected.get("notes", ""),
      })
      continue

    actual_raw = read_json(actual_path)
    if isinstance(actual_raw, dict) and "artifact_type" in actual_raw:
      try:
        assert_valid_artifact(actual_raw, expected_type="audit_report", allow_legacy=True)
        actual = unwrap_artifact(actual_raw, expected_type="audit_report")
      except Exception:
        actual = actual_raw.get("payload", actual_raw)
    else:
      actual = actual_raw
    case_diffs.append(case_diff(expected, actual))

  return aggregate_case_diffs(case_diffs, run_label)


def main(argv: List[str] | None = None) -> int:
  try:
    parser = argparse.ArgumentParser(prog="benchmark-scorer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("score-run")
    p.add_argument("--expected-dir", required=True)
    p.add_argument("--actual-dir", required=True)
    p.add_argument("--run-label", required=True)
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-md")

    p = sub.add_parser("leaderboard")
    p.add_argument("summaries", nargs="+")
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-md")

    args = parser.parse_args(argv)

    if args.cmd == "score-run":
      payload = score_run(Path(args.expected_dir), Path(args.actual_dir), args.run_label)
      artifact = make_benchmark_summary_artifact(payload)
      assert_valid_artifact(artifact, expected_type="benchmark_summary", allow_legacy=False)
      write_json(Path(args.out_json), artifact)
      if args.out_md:
        write_text(Path(args.out_md), render_benchmark_summary_md(payload))
      return SUCCESS

    if args.cmd == "leaderboard":
      summaries = []
      for raw_path in args.summaries:
        raw = read_json(Path(raw_path))
        assert_valid_artifact(raw, expected_type="benchmark_summary", allow_legacy=True)
        summaries.append(unwrap_artifact(raw, expected_type="benchmark_summary"))
      payload = build_leaderboard(summaries)
      artifact = make_leaderboard_artifact(payload)
      assert_valid_artifact(artifact, expected_type="leaderboard", allow_legacy=False)
      write_json(Path(args.out_json), artifact)
      if args.out_md:
        write_text(Path(args.out_md), render_leaderboard_md(payload))
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

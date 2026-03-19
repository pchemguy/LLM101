#!/usr/bin/env python3
"""Phase 9 benchmark scorer.

Compares expected defect targets with actual audit JSON outputs and builds:
- per-case diff
- aggregated benchmark summary
- simple prompt leaderboard scaffold
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set


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


SEVERITY_ORDER = {
    "minor": 1,
    "moderate": 2,
    "major": 3,
    "critical": 4,
}


def load_actual_codes(report: Dict[str, Any]) -> Dict[str, str]:
  result = {}
  for defect in report.get("defects", []):
    code = defect.get("code", "")
    severity = defect.get("severity", "")
    if not code:
      continue
    prev = result.get(code)
    if prev is None or SEVERITY_ORDER.get(severity, 0) > SEVERITY_ORDER.get(prev, 0):
      result[code] = severity
  return result


def case_diff(expected: Dict[str, Any], actual_report: Dict[str, Any]) -> Dict[str, Any]:
  expected_codes: Set[str] = set(expected.get("expected_defect_codes", []))
  expected_floor = expected.get("expected_min_severity", {})
  actual_codes = load_actual_codes(actual_report)
  actual_code_set = set(actual_codes.keys())

  matched = sorted(expected_codes & actual_code_set)
  missed = sorted(expected_codes - actual_code_set)
  extra = sorted(actual_code_set - expected_codes)

  severity_failures = []
  for code, min_sev in expected_floor.items():
    actual_sev = actual_codes.get(code)
    if actual_sev is None:
      continue
    if SEVERITY_ORDER.get(actual_sev, 0) < SEVERITY_ORDER.get(min_sev, 0):
      severity_failures.append(
          {
              "code": code,
              "expected_min_severity": min_sev,
              "actual_severity": actual_sev,
          }
      )

  expected_count = len(expected_codes)
  recall = (len(matched) / expected_count) if expected_count else 1.0
  precision = (len(matched) / len(actual_code_set)) if actual_code_set else (1.0 if not expected_codes else 0.0)

  return {
      "case_id": expected.get("case_id", ""),
      "matched_codes": matched,
      "missed_expected_codes": missed,
      "extra_codes": extra,
      "severity_failures": severity_failures,
      "recall": round(recall, 4),
      "precision": round(precision, 4),
      "expected_notes": expected.get("notes", ""),
  }


def aggregate_case_diffs(case_diffs: List[Dict[str, Any]], run_label: str) -> Dict[str, Any]:
  total_cases = len(case_diffs)
  macro_recall = round(sum(d["recall"] for d in case_diffs) / total_cases, 4) if total_cases else 0.0
  macro_precision = round(sum(d["precision"] for d in case_diffs) / total_cases, 4) if total_cases else 0.0

  missed_counter: Counter[str] = Counter()
  extra_counter: Counter[str] = Counter()
  severity_failure_counter: Counter[str] = Counter()

  for diff in case_diffs:
    for code in diff.get("missed_expected_codes", []):
      missed_counter[code] += 1
    for code in diff.get("extra_codes", []):
      extra_counter[code] += 1
    for item in diff.get("severity_failures", []):
      severity_failure_counter[item["code"]] += 1

  return {
      "run_label": run_label,
      "case_count": total_cases,
      "macro_recall": macro_recall,
      "macro_precision": macro_precision,
      "most_missed_codes": dict(missed_counter.most_common()),
      "most_extra_codes": dict(extra_counter.most_common()),
      "severity_failure_codes": dict(severity_failure_counter.most_common()),
      "cases": case_diffs,
  }


def benchmark_summary_md(summary: Dict[str, Any]) -> str:
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
    for code, count in missed.items():
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Most extra codes"])
  extra = summary.get("most_extra_codes", {})
  if extra:
    for code, count in extra.items():
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Severity failures"])
  sev = summary.get("severity_failure_codes", {})
  if sev:
    for code, count in sev.items():
      lines.append(f"- {code}: {count}")
  else:
    lines.append("- None")
  lines.extend(["", "## Case results"])
  for case in summary.get("cases", []):
    lines.extend(
        [
            f"### {case.get('case_id', '')}",
            f"- recall: {case.get('recall', 0.0)}",
            f"- precision: {case.get('precision', 0.0)}",
            f"- matched_codes: {', '.join(case.get('matched_codes', [])) or 'None'}",
            f"- missed_expected_codes: {', '.join(case.get('missed_expected_codes', [])) or 'None'}",
            f"- extra_codes: {', '.join(case.get('extra_codes', [])) or 'None'}",
        ]
    )
    sf = case.get("severity_failures", [])
    if sf:
      lines.append("- severity_failures:")
      for item in sf:
        lines.append(
            f"  - {item['code']}: expected>={item['expected_min_severity']}, actual={item['actual_severity']}"
        )
    lines.append("")
  return "\n".join(lines) + "\n"


def build_leaderboard(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
  sorted_runs = sorted(
      summaries,
      key=lambda s: (s.get("macro_recall", 0.0), s.get("macro_precision", 0.0)),
      reverse=True,
  )
  rows = []
  rank = 1
  for item in sorted_runs:
    rows.append(
        {
            "rank": rank,
            "run_label": item.get("run_label", ""),
            "macro_recall": item.get("macro_recall", 0.0),
            "macro_precision": item.get("macro_precision", 0.0),
            "case_count": item.get("case_count", 0),
        }
    )
    rank += 1
  return {"leaderboard": rows}


def leaderboard_md(data: Dict[str, Any]) -> str:
  lines = ["# Prompt / Run Leaderboard", ""]
  for row in data.get("leaderboard", []):
    lines.append(
        f"- #{row['rank']} {row['run_label']}: "
        f"macro_recall={row['macro_recall']}, "
        f"macro_precision={row['macro_precision']}, "
        f"case_count={row['case_count']}"
    )
  return "\n".join(lines) + "\n"


def infer_case_id_from_filename(path: Path) -> str:
  name = path.stem
  # Allows report files like case_gap_missing.audit.json or case_gap_missing.json
  return name.split(".")[0]


def main() -> int:
  parser = argparse.ArgumentParser(prog="benchmark_scorer")
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

  args = parser.parse_args()

  if args.cmd == "score-run":
    expected_dir = Path(args.expected_dir)
    actual_dir = Path(args.actual_dir)

    expected_files = sorted(expected_dir.glob("*.json"))
    actual_map = {}
    for path in actual_dir.glob("*.json"):
      actual_map[infer_case_id_from_filename(path)] = path

    case_diffs = []
    for exp_path in expected_files:
      expected = read_json(exp_path)
      case_id = expected.get("case_id", exp_path.stem)
      actual_path = actual_map.get(case_id)
      if actual_path is None:
        case_diffs.append(
            {
                "case_id": case_id,
                "matched_codes": [],
                "missed_expected_codes": expected.get("expected_defect_codes", []),
                "extra_codes": [],
                "severity_failures": [],
                "recall": 0.0,
                "precision": 0.0,
                "expected_notes": expected.get("notes", ""),
                "status": "missing_actual_report",
            }
        )
        continue
      actual = read_json(actual_path)
      diff = case_diff(expected, actual)
      diff["status"] = "ok"
      case_diffs.append(diff)

    summary = aggregate_case_diffs(case_diffs, args.run_label)
    write_json(Path(args.out_json), summary)
    if args.out_md:
      write_text(Path(args.out_md), benchmark_summary_md(summary))
    return 0

  if args.cmd == "leaderboard":
    summaries = [read_json(Path(p)) for p in args.summaries]
    data = build_leaderboard(summaries)
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), leaderboard_md(data))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Set

SEVERITY_ORDER = {"minor": 1, "moderate": 2, "major": 3, "critical": 4}


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
  return dict(sorted(result.items()))


def case_diff(expected: Dict[str, Any], actual_report: Dict[str, Any]) -> Dict[str, Any]:
  expected_codes: Set[str] = set(expected.get("expected_defect_codes", []))
  expected_floor = expected.get("expected_min_severity", {})
  actual_codes = load_actual_codes(actual_report)
  actual_code_set = set(actual_codes.keys())

  matched = sorted(expected_codes & actual_code_set)
  missed = sorted(expected_codes - actual_code_set)
  extra = sorted(actual_code_set - expected_codes)

  severity_failures = []
  for code, min_sev in sorted(expected_floor.items()):
    actual_sev = actual_codes.get(code)
    if actual_sev is None:
      continue
    if SEVERITY_ORDER.get(actual_sev, 0) < SEVERITY_ORDER.get(min_sev, 0):
      severity_failures.append(
          {"code": code, "expected_min_severity": min_sev, "actual_severity": actual_sev}
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
      "most_missed_codes": dict(sorted(missed_counter.items())),
      "most_extra_codes": dict(sorted(extra_counter.items())),
      "severity_failure_codes": dict(sorted(severity_failure_counter.items())),
      "cases": case_diffs,
  }


def build_leaderboard(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
  sorted_runs = sorted(
      summaries,
      key=lambda s: (s.get("macro_recall", 0.0), s.get("macro_precision", 0.0), s.get("run_label", "")),
      reverse=True,
  )
  rows = []
  for idx, item in enumerate(sorted_runs, start=1):
    rows.append(
        {
            "rank": idx,
            "run_label": item.get("run_label", ""),
            "macro_recall": item.get("macro_recall", 0.0),
            "macro_precision": item.get("macro_precision", 0.0),
            "case_count": item.get("case_count", 0),
        }
    )
  return {"leaderboard": rows}

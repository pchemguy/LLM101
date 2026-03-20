from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

from dissertation_intro_qa.core.io import read_json

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
    rows.append({
        "rank": idx,
        "run_label": item.get("run_label", ""),
        "macro_recall": item.get("macro_recall", 0.0),
        "macro_precision": item.get("macro_precision", 0.0),
        "case_count": item.get("case_count", 0),
    })
  return {"leaderboard": rows}


def discover_cases(cases_dir: Path, expected_dir: Path) -> Dict[str, Any]:
  expected_map = {p.stem: p for p in expected_dir.glob("*.json")}
  cases = []
  for case_path in sorted(cases_dir.glob("*.md")):
    case_id = case_path.stem
    expected_path = expected_map.get(case_id)
    cases.append({
        "case_id": case_id,
        "case_file": str(case_path),
        "expected_file": str(expected_path) if expected_path else "",
        "has_expected": expected_path is not None,
    })
  return {"case_count": len(cases), "cases": cases}


def build_run_manifest(run_label: str, prompt_variant: str, profile: str, cases_info: Dict[str, Any], results_dir: Path) -> Dict[str, Any]:
  items = []
  for case in cases_info.get("cases", []):
    case_id = case["case_id"]
    items.append({
        "case_id": case_id,
        "case_file": case["case_file"],
        "expected_file": case["expected_file"],
        "result_json_target": str(results_dir / f"{case_id}.json"),
        "status": "pending",
    })
  return {
      "run_label": run_label,
      "prompt_variant": prompt_variant,
      "profile": profile,
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "case_count": len(items),
      "items": items,
  }


def collect_run_summaries(summaries: List[Path]) -> Dict[str, Any]:
  runs = []
  for path in summaries:
    data = read_json(path)
    payload = data.get("payload", data)
    runs.append({
        "run_label": payload.get("run_label", path.stem),
        "case_count": payload.get("case_count", 0),
        "macro_recall": payload.get("macro_recall", 0.0),
        "macro_precision": payload.get("macro_precision", 0.0),
        "most_missed_codes": payload.get("most_missed_codes", {}),
        "most_extra_codes": payload.get("most_extra_codes", {}),
        "severity_failure_codes": payload.get("severity_failure_codes", {}),
    })
  return {"run_count": len(runs), "runs": runs}


def create_session(session_id: str, description: str, benchmark_root: str, prompts: List[str], profiles: List[str]) -> Dict[str, Any]:
  return {
      "session_id": session_id,
      "description": description,
      "benchmark_root": benchmark_root,
      "prompts": prompts,
      "profiles": profiles,
      "created_at": datetime.utcnow().isoformat() + "Z",
      "runs": [],
      "notes": [],
  }


def register_run(session: Dict[str, Any], run_label: str, manifest_path: str, summary_path: str, prompt_variant: str, profile: str) -> Dict[str, Any]:
  session.setdefault("runs", []).append({
      "run_label": run_label,
      "manifest_path": manifest_path,
      "summary_path": summary_path,
      "prompt_variant": prompt_variant,
      "profile": profile,
      "registered_at": datetime.utcnow().isoformat() + "Z",
  })
  session["runs"] = sorted(session["runs"], key=lambda x: x["run_label"])
  return session


def build_run_registry(session_files: List[Path]) -> Dict[str, Any]:
  sessions = []
  total_runs = 0
  for path in session_files:
    data = read_json(path)
    payload = data.get("payload", data)
    run_count = len(payload.get("runs", []))
    total_runs += run_count
    sessions.append({
        "session_id": payload.get("session_id", path.stem),
        "description": payload.get("description", ""),
        "benchmark_root": payload.get("benchmark_root", ""),
        "created_at": payload.get("created_at", ""),
        "run_count": run_count,
        "prompts": payload.get("prompts", []),
        "profiles": payload.get("profiles", []),
    })
  sessions = sorted(sessions, key=lambda x: x["session_id"])
  return {
      "session_count": len(sessions),
      "total_runs": total_runs,
      "sessions": sessions,
      "generated_at": datetime.utcnow().isoformat() + "Z",
  }


def build_project_dashboard(registry: Dict[str, Any], run_summaries: List[Path]) -> Dict[str, Any]:
  runs = []
  for path in run_summaries:
    raw = read_json(path)
    data = raw.get("payload", raw)
    runs.append({
        "run_label": data.get("run_label", path.stem),
        "case_count": data.get("case_count", 0),
        "macro_recall": data.get("macro_recall", 0.0),
        "macro_precision": data.get("macro_precision", 0.0),
        "most_missed_codes": data.get("most_missed_codes", {}),
        "most_extra_codes": data.get("most_extra_codes", {}),
        "severity_failure_codes": data.get("severity_failure_codes", {}),
    })
  runs = sorted(runs, key=lambda x: x["run_label"])
  best_run = max(runs, key=lambda x: (x["macro_recall"], x["macro_precision"]), default={})
  worst_run = min(runs, key=lambda x: (x["macro_recall"], x["macro_precision"]), default={})
  return {
      "registry": registry,
      "run_count": len(runs),
      "best_run": best_run,
      "worst_run": worst_run,
      "runs": runs,
      "generated_at": datetime.utcnow().isoformat() + "Z",
  }

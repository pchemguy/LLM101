from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from dissertation_intro_qa.artifacts.comparison import make_comparison_artifact
from dissertation_intro_qa.artifacts.gate import make_gate_artifact
from dissertation_intro_qa.core.aggregation import compare_reports, history_index
from dissertation_intro_qa.core.envelope import is_enveloped, unwrap_artifact
from dissertation_intro_qa.core.io import read_json, write_json, write_text
from dissertation_intro_qa.core.render import (
    render_audit_md,
    render_comparison_md,
    render_gate_md,
    render_dashboard_md,
)
from dissertation_intro_qa.core.schema import assert_valid_artifact


def load_yaml_like_profiles(path: Path) -> dict:
  text = path.read_text(encoding="utf-8").splitlines()
  profiles = {}
  current_profile = None
  current_block = None
  for raw in text:
    line = raw.rstrip()
    if not line or line.lstrip().startswith("#") or line.startswith("profiles:"):
      continue
    if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
      current_profile = line.strip()[:-1]
      profiles[current_profile] = {}
      current_block = None
      continue
    if current_profile is None:
      continue
    stripped = line.strip()
    if stripped.endswith(":") and ":" not in stripped[:-1]:
      current_block = stripped[:-1]
      profiles[current_profile][current_block] = {}
      continue
    if stripped.startswith("- "):
      profiles[current_profile].setdefault(current_block, [])
      profiles[current_profile][current_block].append(stripped[2:].strip())
      continue
    if ":" in stripped:
      key, value = stripped.split(":", 1)
      key, value = key.strip(), value.strip()
      try:
        value_obj = int(value)
      except ValueError:
        try:
          value_obj = float(value)
        except ValueError:
          value_obj = value.lower() == "true" if value.lower() in {"true", "false"} else value
      if current_block and line.startswith("      "):
        profiles[current_profile][current_block][key] = value_obj
      else:
        profiles[current_profile][key] = value_obj
  return {"profiles": profiles}


def run_gate(report: dict, config: dict, profile_name: str) -> dict:
  profile = config.get("profiles", {}).get(profile_name)
  if profile is None:
    raise ValueError(f"Profile not found: {profile_name}")
  summary = report.get("summary", {})
  scores = report.get("scores", {})
  gost = report.get("gost_compliance", {})
  failed = []

  if summary.get("critical_count", 0) > profile.get("max_critical", 10**9):
    failed.append(f"critical_count={summary.get('critical_count', 0)} > {profile.get('max_critical')}")
  if summary.get("major_count", 0) > profile.get("max_major", 10**9):
    failed.append(f"major_count={summary.get('major_count', 0)} > {profile.get('max_major')}")
  for key, threshold in profile.get("min_scores", {}).items():
    if scores.get(key, 0) < threshold:
      failed.append(f"score {key}={scores.get(key, 0)} < {threshold}")
  for gost_key in profile.get("require_gost", []):
    if not gost.get(gost_key, False):
      failed.append(f"missing_gost_component={gost_key}")

  return {
      "profile": profile_name,
      "passed": not failed,
      "failed_checks": failed,
      "summary": summary,
      "scores": scores,
  }


def gather_report_paths(inputs: List[str]) -> List[Path]:
  paths = []
  for raw in inputs:
    p = Path(raw)
    if p.is_dir():
      paths.extend(sorted(p.glob("*.json")))
    else:
      paths.append(p)
  return paths


def generate_repair_plan(report: dict) -> str:
  grouped = {}
  severity_order = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
  for defect in report.get("defects", []):
    grouped.setdefault(defect.get("section", "UNSPECIFIED"), []).append(defect)

  lines = ["# Repair Plan", ""]
  for section in sorted(grouped):
    lines.append(f"## {section}")
    defects = sorted(
        grouped[section],
        key=lambda d: (severity_order.get(d.get("severity", ""), 99), d.get("code", "")),
    )
    for defect in defects:
      lines.extend([
          f"- [{defect.get('severity', '').upper()}] {defect.get('code', '')}",
          f"  - Problem: {defect.get('description', '')}",
          f"  - Evidence: {defect.get('evidence', '')}",
          f"  - Recommendation: {defect.get('recommendation', '')}",
      ])
    lines.append("")
  return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="intro-qa")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("compare")
  p.add_argument("report1")
  p.add_argument("report2")
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("gate")
  p.add_argument("report")
  p.add_argument("--profiles", required=True)
  p.add_argument("--profile", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("render-report")
  p.add_argument("report")
  p.add_argument("--out-md", required=True)

  p = sub.add_parser("render-comparison")
  p.add_argument("comparison")
  p.add_argument("--out-md", required=True)

  p = sub.add_parser("render-gate")
  p.add_argument("gate")
  p.add_argument("--out-md", required=True)

  p = sub.add_parser("repair-plan")
  p.add_argument("report")
  p.add_argument("--out-md", required=True)

  p = sub.add_parser("history-index")
  p.add_argument("inputs", nargs="+")
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("dashboard")
  p.add_argument("history_index")
  p.add_argument("--out-md", required=True)

  return parser


def main(argv: List[str] | None = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)

  if args.cmd == "compare":
    data1 = read_json(Path(args.report1))
    data2 = read_json(Path(args.report2))
    assert_valid_artifact(data1, expected_type="audit_report", allow_legacy=True)
    assert_valid_artifact(data2, expected_type="audit_report", allow_legacy=True)
    report1 = unwrap_artifact(data1, expected_type="audit_report")
    report2 = unwrap_artifact(data2, expected_type="audit_report")
    payload = compare_reports(report1, report2)
    artifact = make_comparison_artifact(payload)
    write_json(Path(args.out_json), artifact)
    if args.out_md:
      write_text(Path(args.out_md), render_comparison_md(payload))
    return 0

  if args.cmd == "gate":
    raw = read_json(Path(args.report))
    assert_valid_artifact(raw, expected_type="audit_report", allow_legacy=True)
    report = unwrap_artifact(raw, expected_type="audit_report")
    config = load_yaml_like_profiles(Path(args.profiles))
    payload = run_gate(report, config, args.profile)
    artifact = make_gate_artifact(payload)
    write_json(Path(args.out_json), artifact)
    if args.out_md:
      write_text(Path(args.out_md), render_gate_md(payload))
    return 0

  if args.cmd == "render-report":
    raw = read_json(Path(args.report))
    assert_valid_artifact(raw, expected_type="audit_report", allow_legacy=True)
    report = unwrap_artifact(raw, expected_type="audit_report")
    write_text(Path(args.out_md), render_audit_md(report))
    return 0

  if args.cmd == "render-comparison":
    raw = read_json(Path(args.comparison))
    assert_valid_artifact(raw, expected_type="comparison_report", allow_legacy=True)
    payload = unwrap_artifact(raw, expected_type="comparison_report")
    write_text(Path(args.out_md), render_comparison_md(payload))
    return 0

  if args.cmd == "render-gate":
    raw = read_json(Path(args.gate))
    assert_valid_artifact(raw, expected_type="gate_result", allow_legacy=True)
    payload = unwrap_artifact(raw, expected_type="gate_result")
    write_text(Path(args.out_md), render_gate_md(payload))
    return 0

  if args.cmd == "repair-plan":
    raw = read_json(Path(args.report))
    assert_valid_artifact(raw, expected_type="audit_report", allow_legacy=True)
    report = unwrap_artifact(raw, expected_type="audit_report")
    write_text(Path(args.out_md), generate_repair_plan(report))
    return 0

  if args.cmd == "history-index":
    paths = gather_report_paths(args.inputs)
    payload = history_index(paths)
    write_json(Path(args.out_json), {
        "artifact_type": "history_index",
        "schema_version": "1.0.0",
        "generated_at": "manual",
        "producer": {"tool": "intro_qa", "version": "0.14.0a1"},
        "payload": payload,
    })
    return 0

  if args.cmd == "dashboard":
    raw = read_json(Path(args.history_index))
    assert_valid_artifact(raw, expected_type="history_index", allow_legacy=True)
    payload = unwrap_artifact(raw, expected_type="history_index")
    write_text(Path(args.out_md), render_dashboard_md(payload))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

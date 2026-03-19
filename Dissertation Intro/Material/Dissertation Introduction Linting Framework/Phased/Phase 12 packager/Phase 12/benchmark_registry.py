#!/usr/bin/env python3
"""Phase 11 manifest-aware run registry and consolidated dashboard tools."""

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


def create_session(
    session_id: str,
    description: str,
    benchmark_root: str,
    prompts: List[str],
    profiles: List[str],
) -> Dict[str, Any]:
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


def register_run(
    session: Dict[str, Any],
    run_label: str,
    manifest_path: str,
    summary_path: str,
    prompt_variant: str,
    profile: str,
) -> Dict[str, Any]:
  run_entry = {
      "run_label": run_label,
      "manifest_path": manifest_path,
      "summary_path": summary_path,
      "prompt_variant": prompt_variant,
      "profile": profile,
      "registered_at": datetime.utcnow().isoformat() + "Z",
  }
  session.setdefault("runs", []).append(run_entry)
  return session


def build_run_registry(session_files: List[Path]) -> Dict[str, Any]:
  sessions = []
  total_runs = 0
  for path in session_files:
    data = read_json(path)
    run_count = len(data.get("runs", []))
    total_runs += run_count
    sessions.append(
        {
            "session_id": data.get("session_id", path.stem),
            "description": data.get("description", ""),
            "benchmark_root": data.get("benchmark_root", ""),
            "created_at": data.get("created_at", ""),
            "run_count": run_count,
            "prompts": data.get("prompts", []),
            "profiles": data.get("profiles", []),
        }
    )
  return {
      "session_count": len(sessions),
      "total_runs": total_runs,
      "sessions": sessions,
      "generated_at": datetime.utcnow().isoformat() + "Z",
  }


def build_project_dashboard(
    registry: Dict[str, Any],
    run_summaries: List[Path],
) -> Dict[str, Any]:
  runs = []
  best_run = None
  worst_run = None

  for path in run_summaries:
    data = read_json(path)
    item = {
        "run_label": data.get("run_label", path.stem),
        "case_count": data.get("case_count", 0),
        "macro_recall": data.get("macro_recall", 0.0),
        "macro_precision": data.get("macro_precision", 0.0),
        "most_missed_codes": data.get("most_missed_codes", {}),
        "most_extra_codes": data.get("most_extra_codes", {}),
        "severity_failure_codes": data.get("severity_failure_codes", {}),
    }
    runs.append(item)

  if runs:
    best_run = max(runs, key=lambda x: (x["macro_recall"], x["macro_precision"]))
    worst_run = min(runs, key=lambda x: (x["macro_recall"], x["macro_precision"]))

  return {
      "registry": registry,
      "run_count": len(runs),
      "best_run": best_run or {},
      "worst_run": worst_run or {},
      "runs": runs,
      "generated_at": datetime.utcnow().isoformat() + "Z",
  }


def render_registry_md(data: Dict[str, Any]) -> str:
  lines = [
      "# Run Registry",
      "",
      f"- session_count: {data.get('session_count', 0)}",
      f"- total_runs: {data.get('total_runs', 0)}",
      f"- generated_at: {data.get('generated_at', '')}",
      "",
      "## Sessions",
  ]
  for item in data.get("sessions", []):
    lines.extend(
        [
            f"### {item.get('session_id', '')}",
            f"- description: {item.get('description', '')}",
            f"- benchmark_root: {item.get('benchmark_root', '')}",
            f"- created_at: {item.get('created_at', '')}",
            f"- run_count: {item.get('run_count', 0)}",
            f"- prompts: {', '.join(item.get('prompts', [])) or 'None'}",
            f"- profiles: {', '.join(item.get('profiles', [])) or 'None'}",
            "",
        ]
    )
  return "\n".join(lines) + "\n"


def render_project_dashboard_md(data: Dict[str, Any]) -> str:
  best = data.get("best_run", {})
  worst = data.get("worst_run", {})
  lines = [
      "# Consolidated Project Dashboard",
      "",
      f"- run_count: {data.get('run_count', 0)}",
      f"- generated_at: {data.get('generated_at', '')}",
      "",
      "## Best run",
      f"- run_label: {best.get('run_label', '')}",
      f"- macro_recall: {best.get('macro_recall', 0.0)}",
      f"- macro_precision: {best.get('macro_precision', 0.0)}",
      "",
      "## Worst run",
      f"- run_label: {worst.get('run_label', '')}",
      f"- macro_recall: {worst.get('macro_recall', 0.0)}",
      f"- macro_precision: {worst.get('macro_precision', 0.0)}",
      "",
      "## Runs",
  ]
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


def main() -> int:
  parser = argparse.ArgumentParser(prog="benchmark_registry")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("create-session")
  p.add_argument("--session-id", required=True)
  p.add_argument("--description", required=True)
  p.add_argument("--benchmark-root", required=True)
  p.add_argument("--prompts", nargs="*", default=[])
  p.add_argument("--profiles", nargs="*", default=[])
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("register-run")
  p.add_argument("--session-json", required=True)
  p.add_argument("--run-label", required=True)
  p.add_argument("--manifest-path", required=True)
  p.add_argument("--summary-path", required=True)
  p.add_argument("--prompt-variant", required=True)
  p.add_argument("--profile", required=True)
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("build-registry")
  p.add_argument("sessions", nargs="+")
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("project-dashboard")
  p.add_argument("--registry-json", required=True)
  p.add_argument("summaries", nargs="+")
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  args = parser.parse_args()

  if args.cmd == "create-session":
    data = create_session(
        session_id=args.session_id,
        description=args.description,
        benchmark_root=args.benchmark_root,
        prompts=args.prompts,
        profiles=args.profiles,
    )
    write_json(Path(args.out_json), data)
    return 0

  if args.cmd == "register-run":
    session = read_json(Path(args.session_json))
    updated = register_run(
        session=session,
        run_label=args.run_label,
        manifest_path=args.manifest_path,
        summary_path=args.summary_path,
        prompt_variant=args.prompt_variant,
        profile=args.profile,
    )
    write_json(Path(args.out_json), updated)
    return 0

  if args.cmd == "build-registry":
    data = build_run_registry([Path(p) for p in args.sessions])
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), render_registry_md(data))
    return 0

  if args.cmd == "project-dashboard":
    registry = read_json(Path(args.registry_json))
    data = build_project_dashboard(registry, [Path(p) for p in args.summaries])
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), render_project_dashboard_md(data))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

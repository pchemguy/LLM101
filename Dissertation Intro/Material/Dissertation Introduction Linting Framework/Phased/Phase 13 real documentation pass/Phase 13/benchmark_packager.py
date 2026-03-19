#!/usr/bin/env python3
"""Phase 12 packager / release layer.

Provides:
- scaffold-generator: one-command project bootstrap
- demo-pipeline-plan: build a reproducible demo run plan
- release-bundle: collect core artifacts into a handoff/release package
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


CORE_DIRS = [
    "standards",
    "prompts",
    "configs",
    "schemas",
    "inputs",
    "reports",
    "comparisons",
    "repair",
    "templates",
    "history",
    "dashboard",
    "benchmark",
    "regression",
    "registry",
    "sessions",
    "project_dashboard",
]


def write_text(path: Path, text: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Dict[str, Any]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
  return json.loads(path.read_text(encoding="utf-8"))


def bootstrap_project(target: Path) -> Dict[str, Any]:
  created = []
  for rel in CORE_DIRS:
    p = target / rel
    p.mkdir(parents=True, exist_ok=True)
    created.append(str(p))
  # Keep dirs
  for rel in ["reports", "comparisons", "repair", "history", "dashboard",
              "benchmark/results", "benchmark/leaderboard",
              "regression/results", "registry", "sessions", "project_dashboard"]:
    p = target / rel
    p.mkdir(parents=True, exist_ok=True)
    (p / ".gitkeep").write_text("", encoding="utf-8")
  # Basic placeholders
  (target / "inputs" / "intro_example.md").write_text(
      "# Intro Example\n\nПоместите сюда текст введения диссертации.\n",
      encoding="utf-8",
  )
  return {
      "target": str(target),
      "created_at": datetime.utcnow().isoformat() + "Z",
      "created_directories": created,
      "status": "ok",
  }


def build_demo_pipeline_plan(project_root: Path) -> Dict[str, Any]:
  return {
      "project_root": str(project_root),
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "steps": [
          {
              "step": 1,
              "name": "Prepare benchmark discovery",
              "command": "python benchmark_orchestrator.py discover "
                         "--cases-dir benchmark/cases "
                         "--expected-dir benchmark/expected "
                         "--out-json benchmark/discovery.json "
                         "--out-md benchmark/discovery.md",
          },
          {
              "step": 2,
              "name": "Create benchmark session",
              "command": "python benchmark_registry.py create-session "
                         "--session-id session_demo "
                         '--description "Demo benchmark session" '
                         "--benchmark-root benchmark "
                         "--prompts strict_prompt_variant soft_control_prompt_variant "
                         "--profiles strict supervisor "
                         "--out-json sessions/session_demo.json",
          },
          {
              "step": 3,
              "name": "Build strict run workflow plan",
              "command": "python benchmark_orchestrator.py workflow-plan "
                         "--benchmark-root benchmark "
                         "--run-label strict_prompt_demo "
                         "--prompt-variant strict_prompt_variant "
                         "--profile strict "
                         "--out-json benchmark/results/strict_prompt_demo.workflow.json "
                         "--out-md benchmark/results/strict_prompt_demo.workflow.md",
          },
          {
              "step": 4,
              "name": "Score benchmark run",
              "command": "python benchmark_scorer.py score-run "
                         "--expected-dir benchmark/expected "
                         "--actual-dir benchmark/results/run_strict "
                         "--run-label strict_prompt_demo "
                         "--out-json benchmark/results/strict_prompt_demo.summary.json "
                         "--out-md benchmark/results/strict_prompt_demo.summary.md",
          },
          {
              "step": 5,
              "name": "Register scored run",
              "command": "python benchmark_registry.py register-run "
                         "--session-json sessions/session_demo.json "
                         "--run-label strict_prompt_demo "
                         "--manifest-path benchmark/results/strict_prompt_demo.manifest.json "
                         "--summary-path benchmark/results/strict_prompt_demo.summary.json "
                         "--prompt-variant strict_prompt_variant "
                         "--profile strict "
                         "--out-json sessions/session_demo.json",
          },
          {
              "step": 6,
              "name": "Build consolidated dashboard",
              "command": "python benchmark_registry.py build-registry "
                         "sessions/session_demo.json "
                         "--out-json registry/run_registry.json "
                         "--out-md registry/run_registry.md",
          },
      ],
  }


def release_bundle(
    project_root: Path,
    out_dir: Path,
    include_demo: bool = True,
) -> Dict[str, Any]:
  out_dir.mkdir(parents=True, exist_ok=True)

  include_paths: List[Path] = []
  for rel in [
      "intro_qa.py",
      "benchmark_scorer.py",
      "benchmark_orchestrator.py",
      "benchmark_registry.py",
      "pyproject.toml",
      "README.md",
      "benchmark",
      "regression",
      "tests",
  ]:
    p = project_root / rel
    if p.exists():
      include_paths.append(p)

  if include_demo:
    for rel in ["sessions", "registry", "project_dashboard"]:
      p = project_root / rel
      if p.exists():
        include_paths.append(p)

  copied = []
  for src in include_paths:
    dst = out_dir / src.relative_to(project_root)
    if src.is_dir():
      if dst.exists():
        shutil.rmtree(dst)
      shutil.copytree(src, dst)
      copied.append(str(dst))
    else:
      dst.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(src, dst)
      copied.append(str(dst))

  manifest = {
      "project_root": str(project_root),
      "out_dir": str(out_dir),
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "include_demo": include_demo,
      "copied_items": copied,
  }
  write_json(out_dir / "release_manifest.json", manifest)
  return manifest


def render_demo_plan_md(plan: Dict[str, Any]) -> str:
  lines = [
      "# Demo Pipeline Plan",
      "",
      f"- project_root: {plan.get('project_root', '')}",
      f"- generated_at: {plan.get('generated_at', '')}",
      "",
      "## Steps",
  ]
  for step in plan.get("steps", []):
    lines.extend(
        [
            f"### Step {step.get('step', '')}: {step.get('name', '')}",
            "```bash",
            step.get("command", ""),
            "```",
            "",
        ]
    )
  return "\n".join(lines) + "\n"


def render_release_manifest_md(data: Dict[str, Any]) -> str:
  lines = [
      "# Release Bundle Manifest",
      "",
      f"- project_root: {data.get('project_root', '')}",
      f"- out_dir: {data.get('out_dir', '')}",
      f"- generated_at: {data.get('generated_at', '')}",
      f"- include_demo: {data.get('include_demo', False)}",
      "",
      "## Copied items",
  ]
  for item in data.get("copied_items", []):
    lines.append(f"- {item}")
  return "\n".join(lines) + "\n"


def main() -> int:
  parser = argparse.ArgumentParser(prog="benchmark_packager")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("bootstrap")
  p.add_argument("--target", required=True)
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("demo-plan")
  p.add_argument("--project-root", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  p = sub.add_parser("release-bundle")
  p.add_argument("--project-root", required=True)
  p.add_argument("--out-dir", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")
  p.add_argument("--no-demo", action="store_true")

  args = parser.parse_args()

  if args.cmd == "bootstrap":
    data = bootstrap_project(Path(args.target))
    write_json(Path(args.out_json), data)
    return 0

  if args.cmd == "demo-plan":
    data = build_demo_pipeline_plan(Path(args.project_root))
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), render_demo_plan_md(data))
    return 0

  if args.cmd == "release-bundle":
    data = release_bundle(
        project_root=Path(args.project_root),
        out_dir=Path(args.out_dir),
        include_demo=not args.no_demo,
    )
    write_json(Path(args.out_json), data)
    if args.out_md:
      write_text(Path(args.out_md), render_release_manifest_md(data))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

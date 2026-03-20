from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from dissertation_intro_qa.artifacts.release import make_release_manifest_artifact
from dissertation_intro_qa.core.io import write_json, write_text
from dissertation_intro_qa.core.render import render_release_manifest_md

CORE_DIRS = [
    "standards", "prompts", "configs", "schemas", "inputs", "reports", "comparisons",
    "repair", "templates", "history", "dashboard", "benchmark", "regression",
    "registry", "sessions", "project_dashboard",
]


def bootstrap_project(target: Path) -> dict:
  created = []
  for rel in CORE_DIRS:
    p = target / rel
    p.mkdir(parents=True, exist_ok=True)
    created.append(str(p))
  (target / "inputs" / "intro_example.md").write_text("# Intro Example\n", encoding="utf-8")
  return {"target": str(target), "created_at": datetime.utcnow().isoformat() + "Z", "created_directories": created, "status": "ok"}


def build_demo_pipeline_plan(project_root: Path) -> dict:
  return {
      "project_root": str(project_root),
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "steps": [
          {"step": 1, "name": "Create session"},
          {"step": 2, "name": "Build workflow plan"},
          {"step": 3, "name": "Score run"},
          {"step": 4, "name": "Build registry"},
      ],
  }


def release_bundle(project_root: Path, out_dir: Path, include_demo: bool = True) -> dict:
  out_dir.mkdir(parents=True, exist_ok=True)
  include_paths = []
  for rel in [
      "src", "schemas", "configs", "docs", "tests", "examples",
      "README.md", "CHANGELOG.md", "pyproject.toml",
  ]:
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

  return {
      "project_root": str(project_root),
      "out_dir": str(out_dir),
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "include_demo": include_demo,
      "copied_items": copied,
  }


def main(argv: List[str] | None = None) -> int:
  parser = argparse.ArgumentParser(prog="benchmark-packager")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("bootstrap")
  p.add_argument("--target", required=True)
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("demo-plan")
  p.add_argument("--project-root", required=True)
  p.add_argument("--out-json", required=True)

  p = sub.add_parser("release-bundle")
  p.add_argument("--project-root", required=True)
  p.add_argument("--out-dir", required=True)
  p.add_argument("--out-json", required=True)
  p.add_argument("--out-md")

  args = parser.parse_args(argv)

  if args.cmd == "bootstrap":
    payload = bootstrap_project(Path(args.target))
    write_json(Path(args.out_json), payload)
    return 0

  if args.cmd == "demo-plan":
    payload = build_demo_pipeline_plan(Path(args.project_root))
    write_json(Path(args.out_json), payload)
    return 0

  if args.cmd == "release-bundle":
    payload = release_bundle(Path(args.project_root), Path(args.out_dir), include_demo=True)
    artifact = make_release_manifest_artifact(payload)
    write_json(Path(args.out_json), artifact)
    if args.out_md:
      write_text(Path(args.out_md), render_release_manifest_md(payload))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

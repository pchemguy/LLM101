from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from dissertation_intro_qa.artifacts.registry import (
    make_project_dashboard_artifact,
    make_run_registry_artifact,
    make_session_artifact,
)
from dissertation_intro_qa.core.aggregation import (
    build_project_dashboard,
    build_run_registry,
    create_session,
    register_run,
)
from dissertation_intro_qa.core.envelope import unwrap_artifact
from dissertation_intro_qa.core.io import read_json, write_json, write_text
from dissertation_intro_qa.core.render import render_project_dashboard_md, render_registry_md
from dissertation_intro_qa.core.schema import assert_valid_artifact


def main(argv: List[str] | None = None) -> int:
  parser = argparse.ArgumentParser(prog="benchmark-registry")
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

  args = parser.parse_args(argv)

  if args.cmd == "create-session":
    payload = create_session(args.session_id, args.description, args.benchmark_root, args.prompts, args.profiles)
    artifact = make_session_artifact(payload)
    write_json(Path(args.out_json), artifact)
    return 0

  if args.cmd == "register-run":
    raw = read_json(Path(args.session_json))
    assert_valid_artifact(raw, expected_type="session", allow_legacy=True)
    payload = unwrap_artifact(raw, expected_type="session")
    payload = register_run(payload, args.run_label, args.manifest_path, args.summary_path, args.prompt_variant, args.profile)
    artifact = make_session_artifact(payload)
    write_json(Path(args.out_json), artifact)
    return 0

  if args.cmd == "build-registry":
    payload = build_run_registry([Path(p) for p in args.sessions])
    artifact = make_run_registry_artifact(payload)
    write_json(Path(args.out_json), artifact)
    if args.out_md:
      write_text(Path(args.out_md), render_registry_md(payload))
    return 0

  if args.cmd == "project-dashboard":
    raw = read_json(Path(args.registry_json))
    assert_valid_artifact(raw, expected_type="run_registry", allow_legacy=True)
    registry = unwrap_artifact(raw, expected_type="run_registry")
    payload = build_project_dashboard(registry, [Path(p) for p in args.summaries])
    artifact = make_project_dashboard_artifact(payload)
    write_json(Path(args.out_json), artifact)
    if args.out_md:
      write_text(Path(args.out_md), render_project_dashboard_md(payload))
    return 0

  return 2


if __name__ == "__main__":
  raise SystemExit(main())

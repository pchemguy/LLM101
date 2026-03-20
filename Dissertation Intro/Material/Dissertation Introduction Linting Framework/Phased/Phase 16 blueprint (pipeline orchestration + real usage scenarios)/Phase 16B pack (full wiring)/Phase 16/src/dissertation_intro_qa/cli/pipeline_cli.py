from __future__ import annotations

import argparse
import json
from pathlib import Path

from dissertation_intro_qa.core.exit_codes import ExitCode
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner


def main(argv=None):
  parser = argparse.ArgumentParser(prog="intro-pipeline")
  sub = parser.add_subparsers(dest="cmd", required=True)

  run = sub.add_parser("run")
  run.add_argument("config")
  run.add_argument("--out-json")

  args = parser.parse_args(argv)

  if args.cmd == "run":
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    runner = PipelineRunner(Path(cfg.get("outputs", {}).get("base_dir", "./runs")))
    result = runner.run(cfg)
    if args.out_json:
      Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
      print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result["exit_code"])

  return ExitCode.USAGE_ERROR


if __name__ == "__main__":
  raise SystemExit(main())

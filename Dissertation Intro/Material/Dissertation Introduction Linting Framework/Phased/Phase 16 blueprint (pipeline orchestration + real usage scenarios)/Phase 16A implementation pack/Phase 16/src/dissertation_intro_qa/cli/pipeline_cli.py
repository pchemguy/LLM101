
from __future__ import annotations
import argparse, json
from pathlib import Path

from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner

def main():
    parser = argparse.ArgumentParser(prog="intro-pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("config")

    args = parser.parse_args()

    if args.cmd == "run":
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
        runner = PipelineRunner(Path(cfg.get("outputs", {}).get("base_dir", "./runs")))
        result = runner.run(cfg)
        print(json.dumps(result, indent=2))
        return 0

if __name__ == "__main__":
    raise SystemExit(main())

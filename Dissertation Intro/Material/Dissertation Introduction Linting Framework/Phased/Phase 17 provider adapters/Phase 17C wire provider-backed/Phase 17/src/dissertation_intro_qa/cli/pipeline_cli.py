from __future__ import annotations
import argparse
import json
from pathlib import Path
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner

def main(argv=None):
  parser = argparse.ArgumentParser(prog="intro-pipeline")
  parser.add_argument("config")
  parser.add_argument("--out-json")
  args = parser.parse_args(argv)
  cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
  runner = PipelineRunner(Path(cfg.get("outputs", {}).get("base_dir", "./runs")))
  result = runner.run(cfg)
  if args.out_json:
    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
  else:
    print(json.dumps(result, ensure_ascii=False, indent=2))
  return int(result["exit_code"])

if __name__ == "__main__":
  raise SystemExit(main())

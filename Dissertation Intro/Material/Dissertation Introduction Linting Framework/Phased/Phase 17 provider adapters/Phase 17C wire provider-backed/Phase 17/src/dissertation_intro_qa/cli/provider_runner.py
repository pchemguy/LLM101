from __future__ import annotations
import argparse
import json
from pathlib import Path
from dissertation_intro_qa.runner.prompt_runner import PromptRunner

def main(argv=None):
  parser = argparse.ArgumentParser(prog="provider-runner")
  parser.add_argument("config")
  parser.add_argument("--out-json")
  args = parser.parse_args(argv)
  cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
  runner = PromptRunner(Path(cfg.get("output", {}).get("base_dir", "./provider_runs")))
  result = runner.run(cfg)
  if args.out_json:
    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
  else:
    print(json.dumps(result, ensure_ascii=False, indent=2))
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

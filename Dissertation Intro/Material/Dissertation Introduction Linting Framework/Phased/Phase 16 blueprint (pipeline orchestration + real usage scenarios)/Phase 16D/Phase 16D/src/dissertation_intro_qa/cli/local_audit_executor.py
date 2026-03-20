from __future__ import annotations

import argparse
from pathlib import Path

from dissertation_intro_qa.executors.demo_executor import DemoAuditExecutor
from dissertation_intro_qa.core.io import write_json


def main(argv=None):
  parser = argparse.ArgumentParser(prog="local-audit-executor")
  parser.add_argument("--input-path", required=True)
  parser.add_argument("--document-id", required=True)
  parser.add_argument("--work-dir", required=True)
  parser.add_argument("--out-json", required=True)
  args = parser.parse_args(argv)

  executor = DemoAuditExecutor()
  artifact = executor.execute(
      input_path=Path(args.input_path),
      document_id=args.document_id,
      work_dir=Path(args.work_dir),
      executor_config={},
  )
  write_json(Path(args.out_json), artifact)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

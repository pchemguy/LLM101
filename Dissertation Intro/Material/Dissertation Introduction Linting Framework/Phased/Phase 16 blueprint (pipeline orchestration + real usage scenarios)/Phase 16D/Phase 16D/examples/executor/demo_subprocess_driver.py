from __future__ import annotations

import argparse
from pathlib import Path

from dissertation_intro_qa.cli.local_audit_executor import main as executor_main


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input-path", required=True)
  parser.add_argument("--document-id", required=True)
  parser.add_argument("--work-dir", required=True)
  parser.add_argument("--out-json", required=True)
  args = parser.parse_args()

  raise SystemExit(executor_main([
      "--input-path", args.input_path,
      "--document-id", args.document_id,
      "--work-dir", args.work_dir,
      "--out-json", args.out_json,
  ]))

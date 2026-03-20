from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--prompt-file", required=True)
  parser.add_argument("--document-path", required=True)
  parser.add_argument("--document-id", required=True)
  parser.add_argument("--work-dir", required=True)
  parser.add_argument("--out-json", required=True)
  args = parser.parse_args()

  prompt_preview = Path(args.prompt_file).read_text(encoding="utf-8")[:120]
  result = {
      "provider_label": "demo_subprocess_provider",
      "document_id": args.document_id,
      "document_path": args.document_path,
      "prompt_preview": prompt_preview,
      "raw_response_text": "SUBPROCESS_RESPONSE: prompt accepted",
      "status": "ok",
  }
  Path(args.out_json).write_text(
      json.dumps(result, ensure_ascii=False, indent=2),
      encoding="utf-8",
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

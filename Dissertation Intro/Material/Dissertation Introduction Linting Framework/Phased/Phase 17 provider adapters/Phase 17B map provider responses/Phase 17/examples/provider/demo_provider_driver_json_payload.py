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
  result = {
      "provider_label": "demo_subprocess_provider",
      "document_id": args.document_id,
      "status": "ok",
      "audit_payload": {
          "metadata": {
              "document_id": args.document_id,
              "language": "ru",
              "audit_mode": "provider_json_payload",
              "date": "2026-03-20",
          },
          "scores": {"SC1": 1},
          "defects": [{
              "code": "GAP-02",
              "severity": "major",
              "section": "Степень разработанности / пробел",
              "description": "Пробел не сформулирован явно.",
              "evidence": "Формулировка пробела отсутствует.",
              "recommendation": "Сформулировать конкретный научный пробел.",
          }],
          "gost_compliance": {"methods": False},
          "summary": {
              "critical_count": 0,
              "major_count": 1,
              "moderate_count": 0,
              "minor_count": 0,
              "overall_verdict": "provider_json_payload",
          },
      },
  }
  Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

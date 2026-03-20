from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, List

from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.core.envelope import unwrap_artifact


def history_index(report_paths: List[Path]) -> Dict:
  items = []
  defect_frequency = Counter()
  severity_frequency = Counter()
  for path in sorted(report_paths, key=lambda p: p.name):
    report = unwrap_artifact(read_json(path), expected_type="audit_report")
    meta = report.get("metadata", {})
    defects = report.get("defects", [])
    for defect in defects:
      defect_frequency[defect.get("code", "")] += 1
      severity_frequency[defect.get("severity", "")] += 1
    items.append({
        "document_id": meta.get("document_id", path.stem),
        "summary": report.get("summary", {}),
    })
  return {
      "reports": items,
      "defect_frequency": dict(sorted(defect_frequency.items())),
      "severity_frequency": dict(sorted(severity_frequency.items())),
  }

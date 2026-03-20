from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.core.envelope import unwrap_artifact


def defect_key(defect: Dict[str, Any]) -> Tuple[str, str]:
  return defect.get("code", ""), defect.get("section", "")


def compare_reports(report1: Dict[str, Any], report2: Dict[str, Any]) -> Dict[str, Any]:
  defects1 = {defect_key(d): d for d in report1.get("defects", [])}
  defects2 = {defect_key(d): d for d in report2.get("defects", [])}
  keys1 = set(defects1)
  keys2 = set(defects2)

  scores1 = report1.get("scores", {})
  scores2 = report2.get("scores", {})
  score_diff = {key: scores2.get(key, 0) - scores1.get(key, 0) for key in sorted(set(scores1) | set(scores2))}
  regressions = [f"Снижение score по {key}: {delta}" for key, delta in score_diff.items() if delta < 0]

  return {
      "from_version": report1.get("metadata", {}).get("document_id", "v1"),
      "to_version": report2.get("metadata", {}).get("document_id", "v2"),
      "resolved_defects": [k[0] for k in sorted(keys1 - keys2)],
      "remaining_defects": [k[0] for k in sorted(keys1 & keys2)],
      "new_defects": [k[0] for k in sorted(keys2 - keys1)],
      "score_diff": score_diff,
      "regression_warnings": regressions,
      "overall_assessment": "",
  }


def history_index(report_paths: List[Path]) -> Dict[str, Any]:
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
        "date": meta.get("date", ""),
        "summary": report.get("summary", {}),
        "scores": report.get("scores", {}),
    })
  return {
      "reports": items,
      "defect_frequency": dict(sorted(defect_frequency.items())),
      "severity_frequency": dict(sorted(severity_frequency.items())),
  }

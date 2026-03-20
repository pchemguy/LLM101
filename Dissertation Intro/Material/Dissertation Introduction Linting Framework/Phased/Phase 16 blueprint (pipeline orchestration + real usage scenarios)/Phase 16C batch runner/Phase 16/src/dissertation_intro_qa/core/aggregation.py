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
    items.append({"document_id": meta.get("document_id", path.stem), "summary": report.get("summary", {})})
  return {
      "reports": items,
      "defect_frequency": dict(sorted(defect_frequency.items())),
      "severity_frequency": dict(sorted(severity_frequency.items())),
  }

def batch_summary(batch_id: str, results: List[Dict]) -> Dict:
  failed_run_count = sum(1 for item in results if int(item.get("exit_code", 0)) != 0)
  gate_failed_count = sum(1 for item in results if int(item.get("exit_code", 0)) == 1)
  return {
      "batch_id": batch_id,
      "run_count": len(results),
      "runs": results,
      "failed_run_count": failed_run_count,
      "gate_failed_count": gate_failed_count,
  }

def batch_history_from_run_dirs(run_dirs: List[Path]) -> Dict:
  audit_paths = []
  source_runs = []
  for run_dir in sorted(run_dirs, key=lambda p: p.name):
    audit = run_dir / "audit.json"
    if audit.exists():
      audit_paths.append(audit)
      source_runs.append(run_dir.name)
  hist = history_index(audit_paths)
  hist["source_runs"] = source_runs
  return hist

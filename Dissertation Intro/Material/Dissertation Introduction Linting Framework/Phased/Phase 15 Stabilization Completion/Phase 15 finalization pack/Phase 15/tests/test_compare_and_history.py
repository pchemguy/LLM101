from pathlib import Path
import json

from dissertation_intro_qa.core.aggregation import compare_reports, history_index


def test_compare_reports_basic():
  r1 = {"metadata": {"document_id": "v1"}, "scores": {"SC1": 1}, "defects": [{"code": "GAP-02", "section": "A", "severity": "major"}]}
  r2 = {"metadata": {"document_id": "v2"}, "scores": {"SC1": 2}, "defects": [{"code": "GAP-02", "section": "A", "severity": "major"}, {"code": "GOAL-03", "section": "B", "severity": "major"}]}
  comp = compare_reports(r1, r2)
  assert comp["from_version"] == "v1"
  assert comp["to_version"] == "v2"
  assert "GOAL-03" in comp["new_defects"]


def test_history_index_reads_enveloped(tmp_path: Path):
  payload = {"metadata": {"document_id": "x", "date": "2026-03-19"}, "scores": {}, "defects": [{"code": "GAP-02", "severity": "major"}], "gost_compliance": {}, "summary": {}}
  artifact = {"artifact_type": "audit_report", "schema_version": "1.0.0", "generated_at": "x", "producer": {"tool": "t", "version": "v"}, "payload": payload}
  path = tmp_path / "audit.json"
  path.write_text(json.dumps(artifact), encoding="utf-8")
  idx = history_index([path])
  assert idx["reports"][0]["document_id"] == "x"
  assert idx["defect_frequency"]["GAP-02"] == 1

from pathlib import Path
import json

from dissertation_intro_qa.core.aggregation import build_project_dashboard, build_run_registry, create_session, register_run


def test_session_register_and_registry(tmp_path: Path):
  session = create_session("s1", "desc", "benchmark", ["p1"], ["strict"])
  session = register_run(session, "run1", "m.json", "s.json", "p1", "strict")
  path = tmp_path / "session.json"
  path.write_text(json.dumps(session), encoding="utf-8")
  registry = build_run_registry([path])
  assert registry["session_count"] == 1
  assert registry["total_runs"] == 1


def test_project_dashboard(tmp_path: Path):
  registry = {"session_count": 1, "total_runs": 1, "sessions": [], "generated_at": "x"}
  summary = {
      "run_label": "run1",
      "case_count": 1,
      "macro_recall": 0.8,
      "macro_precision": 0.9,
      "most_missed_codes": {},
      "most_extra_codes": {},
      "severity_failure_codes": {},
      "cases": [],
  }
  path = tmp_path / "summary.json"
  path.write_text(json.dumps(summary), encoding="utf-8")
  dashboard = build_project_dashboard(registry, [path])
  assert dashboard["run_count"] == 1
  assert dashboard["best_run"]["run_label"] == "run1"

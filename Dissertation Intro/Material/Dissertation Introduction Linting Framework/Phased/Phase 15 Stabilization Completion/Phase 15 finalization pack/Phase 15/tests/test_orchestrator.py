from pathlib import Path

from dissertation_intro_qa.core.aggregation import build_run_manifest, discover_cases


def test_discover_cases_and_manifest(tmp_path: Path):
  cases = tmp_path / "cases"
  expected = tmp_path / "expected"
  results = tmp_path / "results"
  cases.mkdir()
  expected.mkdir()
  results.mkdir()
  (cases / "case_a.md").write_text("# Case A", encoding="utf-8")
  (expected / "case_a.json").write_text('{"case_id":"case_a"}', encoding="utf-8")
  info = discover_cases(cases, expected)
  assert info["case_count"] == 1
  manifest = build_run_manifest("run1", "strict", "strict", info, results)
  assert manifest["run_label"] == "run1"

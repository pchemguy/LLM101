from pathlib import Path

from dissertation_intro_qa.cli.benchmark_scorer import score_run


def test_score_run_on_example_files(tmp_path: Path):
  expected_dir = tmp_path / "expected"
  actual_dir = tmp_path / "actual"
  expected_dir.mkdir()
  actual_dir.mkdir()

  (expected_dir / "case_gap_missing.json").write_text(
      '{"case_id":"case_gap_missing","expected_defect_codes":["GAP-01"],"expected_min_severity":{"GAP-01":"critical"},"notes":""}',
      encoding="utf-8",
  )
  (actual_dir / "case_gap_missing.json").write_text(
      '{"defects":[{"code":"GAP-01","severity":"critical"}]}',
      encoding="utf-8",
  )

  summary = score_run(expected_dir, actual_dir, "demo")
  assert summary["run_label"] == "demo"
  assert summary["case_count"] == 1

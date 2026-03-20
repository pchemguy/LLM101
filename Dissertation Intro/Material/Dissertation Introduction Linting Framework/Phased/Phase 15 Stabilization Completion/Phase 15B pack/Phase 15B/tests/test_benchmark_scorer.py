from dissertation_intro_qa.core.aggregation import case_diff, aggregate_case_diffs, build_leaderboard


def test_case_diff_detects_matches_and_misses():
  expected = {
      "case_id": "case_1",
      "expected_defect_codes": ["GAP-01", "GOAL-03"],
      "expected_min_severity": {"GAP-01": "critical"},
      "notes": "",
  }
  actual = {"defects": [{"code": "GAP-01", "severity": "critical"}, {"code": "TASK-04", "severity": "moderate"}]}
  diff = case_diff(expected, actual)
  assert diff["matched_codes"] == ["GAP-01"]
  assert diff["missed_expected_codes"] == ["GOAL-03"]
  assert diff["extra_codes"] == ["TASK-04"]


def test_aggregate_and_leaderboard():
  summary1 = aggregate_case_diffs([{"case_id": "a", "matched_codes": [], "missed_expected_codes": [], "extra_codes": [], "severity_failures": [], "recall": 0.8, "precision": 0.9, "expected_notes": ""}], "run_a")
  summary2 = aggregate_case_diffs([{"case_id": "b", "matched_codes": [], "missed_expected_codes": [], "extra_codes": [], "severity_failures": [], "recall": 0.5, "precision": 0.6, "expected_notes": ""}], "run_b")
  leaderboard = build_leaderboard([summary1, summary2])
  assert leaderboard["leaderboard"][0]["run_label"] == "run_a"

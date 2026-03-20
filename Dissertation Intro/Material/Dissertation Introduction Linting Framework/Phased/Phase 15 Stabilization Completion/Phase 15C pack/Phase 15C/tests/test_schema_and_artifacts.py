from dissertation_intro_qa.core.schema import assert_valid_artifact
from dissertation_intro_qa.core.envelope import wrap_artifact


def test_valid_comparison_artifact():
  payload = {
      "from_version": "a",
      "to_version": "b",
      "resolved_defects": [],
      "remaining_defects": [],
      "new_defects": [],
      "score_diff": {},
      "regression_warnings": [],
      "overall_assessment": "",
  }
  artifact = wrap_artifact("comparison_report", payload)
  assert_valid_artifact(artifact, expected_type="comparison_report", allow_legacy=False)


def test_valid_gate_artifact():
  payload = {
      "profile": "strict",
      "passed": True,
      "failed_checks": [],
      "summary": {},
      "scores": {},
  }
  artifact = wrap_artifact("gate_result", payload)
  assert_valid_artifact(artifact, expected_type="gate_result", allow_legacy=False)

import pytest

from dissertation_intro_qa.core.taxonomy import validate_defects_against_taxonomy


def test_unknown_code_rejected_when_enabled():
  taxonomy = {"groups": {"GAP": {"GAP-01": {"default_severity_floor": "critical"}}}}
  defects = [{"code": "UNKNOWN-01", "severity": "major"}]
  with pytest.raises(Exception):
    validate_defects_against_taxonomy(defects, taxonomy, reject_unknown=True, enforce_floor=False)


def test_severity_floor_enforced():
  taxonomy = {"groups": {"GAP": {"GAP-01": {"default_severity_floor": "critical"}}}}
  defects = [{"code": "GAP-01", "severity": "major"}]
  with pytest.raises(Exception):
    validate_defects_against_taxonomy(defects, taxonomy, reject_unknown=False, enforce_floor=True)

import pytest

from dissertation_intro_qa.core.envelope import wrap_artifact
from dissertation_intro_qa.core.errors import SchemaError
from dissertation_intro_qa.core.schema import assert_valid_artifact


def test_valid_enveloped_audit_passes():
  payload = {
      "taxonomy_version": "1.0.0",
      "metadata": {
          "document_id": "x",
          "language": "ru",
          "audit_mode": "full",
          "date": "2026-03-19",
      },
      "extraction": {},
      "scores": {},
      "defects": [],
      "gost_compliance": {},
      "summary": {},
  }
  artifact = wrap_artifact("audit_report", payload)
  assert_valid_artifact(artifact, expected_type="audit_report", allow_legacy=False)


def test_invalid_enveloped_audit_fails():
  bad = {
      "artifact_type": "audit_report",
      "schema_version": "1.0.0",
      "generated_at": "now",
      "producer": {"tool": "x", "version": "y"},
      "payload": {"metadata": {}},
  }
  with pytest.raises(SchemaError):
    assert_valid_artifact(bad, expected_type="audit_report", allow_legacy=False)

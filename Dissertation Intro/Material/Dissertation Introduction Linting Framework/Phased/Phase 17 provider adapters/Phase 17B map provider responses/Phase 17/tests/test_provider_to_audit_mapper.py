from dissertation_intro_qa.core.schema import assert_valid_artifact
from dissertation_intro_qa.mappers.provider_to_audit import map_provider_result_to_audit_artifact

def test_demo_structured_mapping():
  provider_result = {
      "provider_label": "demo",
      "document_id": "doc1",
      "status": "ok",
      "structured_audit": {
          "metadata": {"document_id": "doc1"},
          "scores": {},
          "defects": [],
          "gost_compliance": {},
          "summary": {},
      },
  }
  artifact = map_provider_result_to_audit_artifact(provider_result, document_id="doc1", mapping_config={"mode": "demo_structured"})
  assert_valid_artifact(artifact, expected_type="audit_report")

def test_json_payload_mapping():
  provider_result = {
      "provider_label": "demo",
      "document_id": "doc1",
      "status": "ok",
      "audit_payload": {
          "metadata": {"document_id": "doc1"},
          "scores": {},
          "defects": [],
          "gost_compliance": {},
          "summary": {},
      },
  }
  artifact = map_provider_result_to_audit_artifact(provider_result, document_id="doc1", mapping_config={"mode": "json_payload", "field_name": "audit_payload"})
  assert_valid_artifact(artifact, expected_type="audit_report")

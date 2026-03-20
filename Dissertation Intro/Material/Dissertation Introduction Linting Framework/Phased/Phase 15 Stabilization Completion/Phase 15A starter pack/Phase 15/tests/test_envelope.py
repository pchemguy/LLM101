from dissertation_intro_qa.core.envelope import wrap_artifact, is_enveloped, unwrap_artifact


def test_wrap_and_unwrap_roundtrip():
  payload = {"a": 1}
  artifact = wrap_artifact("audit_report", payload)
  assert is_enveloped(artifact) is True
  assert unwrap_artifact(artifact, expected_type="audit_report") == payload

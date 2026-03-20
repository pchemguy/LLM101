from pathlib import Path

from dissertation_intro_qa.executors.demo_executor import DemoAuditExecutor
from dissertation_intro_qa.core.schema import assert_valid_artifact


def test_demo_executor_returns_valid_audit(tmp_path: Path):
  input_path = tmp_path / "intro.txt"
  input_path.write_text("Введение", encoding="utf-8")
  executor = DemoAuditExecutor()
  artifact = executor.execute(
      input_path=input_path,
      document_id="demo_doc",
      work_dir=tmp_path,
      executor_config={},
  )
  assert_valid_artifact(artifact, expected_type="audit_report")

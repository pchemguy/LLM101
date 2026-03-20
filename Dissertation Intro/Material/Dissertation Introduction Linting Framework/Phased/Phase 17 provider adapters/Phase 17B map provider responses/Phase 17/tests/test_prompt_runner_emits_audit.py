from pathlib import Path
from dissertation_intro_qa.runner.prompt_runner import PromptRunner
from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.core.schema import assert_valid_artifact

def test_prompt_runner_demo_emits_mapped_audit(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("ID={document_id}\n{document_text}", encoding="utf-8")
  doc_path = tmp_path / "intro.txt"
  doc_path.write_text("Введение", encoding="utf-8")

  cfg = {
      "provider": {"mode": "demo", "label": "demo_provider"},
      "prompt": {"template_path": str(prompt_path)},
      "input": {"document_path": str(doc_path), "document_id": "demo_doc"},
      "output": {
          "base_dir": str(tmp_path / "runs"),
          "emit_audit_artifact": True,
          "provider_mapping": {"mode": "demo_structured"},
      },
  }
  runner = PromptRunner(tmp_path / "runs")
  result = runner.run(cfg)
  mapped = read_json(Path(result["mapped_audit_path"]))
  assert_valid_artifact(mapped, expected_type="audit_report")

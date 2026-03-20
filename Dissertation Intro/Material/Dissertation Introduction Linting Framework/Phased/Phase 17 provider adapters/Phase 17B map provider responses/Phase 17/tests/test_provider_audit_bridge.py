from pathlib import Path
from dissertation_intro_qa.pipeline.provider_audit_bridge import run_provider_backed_audit
from dissertation_intro_qa.core.schema import assert_valid_artifact

def test_provider_backed_audit_bridge(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("ID={document_id}\n{document_text}", encoding="utf-8")
  doc_path = tmp_path / "intro.txt"
  doc_path.write_text("Введение", encoding="utf-8")

  cfg = {
      "pipeline": {
          "audit_provider_bridge": {
              "runner_config": {
                  "provider": {"mode": "demo", "label": "demo_provider"},
                  "prompt": {"template_path": str(prompt_path)},
                  "input": {"document_path": str(doc_path), "document_id": "demo_doc"},
                  "output": {
                      "base_dir": str(tmp_path / "provider_runs"),
                      "emit_audit_artifact": True,
                      "provider_mapping": {"mode": "demo_structured"},
                  },
              }
          }
      }
  }
  result = run_provider_backed_audit(config=cfg, run_dir=tmp_path / "run")
  assert_valid_artifact(result["artifact"], expected_type="audit_report")
  assert result["payload"]["metadata"]["document_id"] == "demo_doc"

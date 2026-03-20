from pathlib import Path
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner

def test_pipeline_provider_demo_mode(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("ID={document_id}\n{document_text}", encoding="utf-8")
  doc_path = tmp_path / "intro.txt"
  doc_path.write_text("Введение", encoding="utf-8")

  cfg = {
      "input": {"path": str(doc_path), "document_id": "demo_doc"},
      "pipeline": {
          "steps": ["audit", "gate", "repair-plan", "history-index", "dashboard"],
          "audit_mode": "provider_bridge",
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
          },
      },
      "outputs": {"base_dir": str(tmp_path / "runs")},
  }

  runner = PipelineRunner(tmp_path / "runs")
  result = runner.run(cfg)
  run_dir = Path(result["run_dir"])
  assert result["audit_mode"] == "provider_bridge"
  assert (run_dir / "audit.json").exists()
  assert (run_dir / "gate.json").exists()
  assert (run_dir / "history_index.json").exists()

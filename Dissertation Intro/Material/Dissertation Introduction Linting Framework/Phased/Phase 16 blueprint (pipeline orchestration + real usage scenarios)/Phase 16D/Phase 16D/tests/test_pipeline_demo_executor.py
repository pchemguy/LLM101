from pathlib import Path

from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner


def test_pipeline_with_demo_executor(tmp_path: Path):
  input_path = tmp_path / "intro.txt"
  input_path.write_text("Введение", encoding="utf-8")
  cfg = {
      "input": {"path": str(input_path), "document_id": "demo_v1"},
      "pipeline": {
          "steps": ["audit", "gate", "repair-plan", "history-index", "dashboard"],
          "audit_executor": {"mode": "demo"},
      },
      "outputs": {"base_dir": str(tmp_path / "runs")},
  }
  runner = PipelineRunner(tmp_path / "runs")
  result = runner.run(cfg)
  run_dir = Path(result["run_dir"])
  assert (run_dir / "audit.json").exists()
  assert (run_dir / "gate.json").exists()

from pathlib import Path

from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner


def test_pipeline_runner_creates_run(tmp_path: Path):
  cfg = {
      "input": {"path": "intro.txt", "document_id": "demo_v1"},
      "pipeline": {"steps": ["audit", "gate", "repair-plan", "history-index", "dashboard"]},
      "outputs": {"base_dir": str(tmp_path / "runs")},
  }
  runner = PipelineRunner(tmp_path / "runs")
  result = runner.run(cfg)
  run_dir = Path(result["run_dir"])
  assert run_dir.exists()
  assert (run_dir / "audit.json").exists()
  assert (run_dir / "gate.json").exists()
  assert (run_dir / "history_index.json").exists()

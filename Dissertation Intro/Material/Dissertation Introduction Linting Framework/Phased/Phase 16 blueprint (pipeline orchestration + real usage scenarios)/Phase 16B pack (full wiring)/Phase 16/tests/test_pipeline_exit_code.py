from pathlib import Path

from dissertation_intro_qa.core.exit_codes import ExitCode
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner


def test_pipeline_gate_failure_exit_code(tmp_path: Path):
  cfg = {
      "input": {"path": "intro.txt", "document_id": "demo_v1"},
      "pipeline": {"steps": ["audit", "gate"]},
      "outputs": {"base_dir": str(tmp_path / "runs")},
  }
  runner = PipelineRunner(tmp_path / "runs")
  result = runner.run(cfg)
  assert result["exit_code"] == ExitCode.GATE_FAILED

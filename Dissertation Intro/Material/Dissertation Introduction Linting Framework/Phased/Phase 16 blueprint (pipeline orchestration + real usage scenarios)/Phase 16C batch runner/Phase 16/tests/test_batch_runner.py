from pathlib import Path
from dissertation_intro_qa.pipeline.batch_runner import run_batch

def test_batch_runner_creates_batch_outputs(tmp_path: Path):
  input_dir = tmp_path / "input_docs"
  output_dir = tmp_path / "runs"
  input_dir.mkdir()
  output_dir.mkdir()
  (input_dir / "intro_01.txt").write_text("Введение 1", encoding="utf-8")
  (input_dir / "intro_02.txt").write_text("Введение 2", encoding="utf-8")
  cfg = {
      "input": {"path": "", "document_id": ""},
      "pipeline": {"steps": ["audit", "gate", "repair-plan", "history-index", "dashboard"]},
      "outputs": {"base_dir": str(output_dir)},
  }
  result = run_batch(cfg, input_dir, output_dir, "batch_test")
  batch_dir = Path(result["batch_dir"])
  assert batch_dir.exists()
  assert (batch_dir / "batch_summary.json").exists()
  assert (batch_dir / "batch_history.json").exists()
  assert (batch_dir / "batch_dashboard.md").exists()
  assert (batch_dir / "aggregated_dashboard.md").exists()

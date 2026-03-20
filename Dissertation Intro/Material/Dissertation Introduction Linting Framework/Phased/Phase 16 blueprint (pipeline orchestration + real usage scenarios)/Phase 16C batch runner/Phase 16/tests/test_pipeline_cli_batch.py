from pathlib import Path
from dissertation_intro_qa.cli.pipeline_cli import main

def test_pipeline_cli_batch_run(tmp_path: Path):
  input_dir = tmp_path / "docs"
  out_dir = tmp_path / "runs"
  input_dir.mkdir()
  out_dir.mkdir()
  (input_dir / "doc1.txt").write_text("Text", encoding="utf-8")
  config_path = tmp_path / "config.json"
  config_path.write_text(
      '{"input":{"path":"","document_id":""},"pipeline":{"steps":["audit","gate","repair-plan","history-index","dashboard"]},"outputs":{"base_dir":"%s"}}'
      % str(out_dir).replace("\\", "/"),
      encoding="utf-8",
  )
  exit_code = main([
      "batch-run",
      str(config_path),
      "--input-dir",
      str(input_dir),
      "--output-dir",
      str(out_dir),
      "--batch-id",
      "demo_batch",
      "--out-json",
      str(tmp_path / "result.json"),
  ])
  assert exit_code in (0, 1)
  assert (tmp_path / "result.json").exists()

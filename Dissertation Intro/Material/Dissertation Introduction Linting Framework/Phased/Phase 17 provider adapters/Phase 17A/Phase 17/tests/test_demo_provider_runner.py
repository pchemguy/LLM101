from pathlib import Path

from dissertation_intro_qa.runner.prompt_runner import PromptRunner


def test_prompt_runner_demo(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("ID={document_id}\n{document_text}", encoding="utf-8")
  doc_path = tmp_path / "intro.txt"
  doc_path.write_text("Введение", encoding="utf-8")

  cfg = {
      "provider": {"mode": "demo", "label": "demo_provider"},
      "prompt": {"template_path": str(prompt_path)},
      "input": {"document_path": str(doc_path), "document_id": "demo_doc"},
      "output": {"base_dir": str(tmp_path / "runs")},
  }
  runner = PromptRunner(tmp_path / "runs")
  result = runner.run(cfg)
  run_dir = Path(result["run_dir"])
  assert (run_dir / "rendered_prompt.txt").exists()
  assert (run_dir / "provider_result.json").exists()
  assert (run_dir / "prompt_run_manifest.json").exists()

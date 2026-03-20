from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dissertation_intro_qa.artifacts.batch import make_batch_history_artifact, make_batch_summary_artifact
from dissertation_intro_qa.core.aggregation import batch_history_from_run_dirs, batch_summary
from dissertation_intro_qa.core.io import write_json, write_text
from dissertation_intro_qa.core.render import render_batch_dashboard_md, render_dashboard_md
from dissertation_intro_qa.core.schema import assert_valid_artifact
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner

def load_batch_documents(input_dir: Path) -> List[Path]:
  docs = []
  for ext in ("*.txt", "*.md"):
    docs.extend(sorted(input_dir.glob(ext)))
  docs = sorted({p.resolve() for p in docs})
  return [Path(p) for p in docs]

def make_document_config(template_cfg: Dict[str, Any], doc_path: Path) -> Dict[str, Any]:
  cfg = dict(template_cfg)
  cfg["input"] = dict(template_cfg.get("input", {}))
  cfg["input"]["path"] = str(doc_path)
  cfg["input"]["document_id"] = doc_path.stem
  return cfg

def run_batch(template_cfg: Dict[str, Any], input_dir: Path, output_dir: Path, batch_id: str) -> Dict[str, Any]:
  docs = load_batch_documents(input_dir)
  runner = PipelineRunner(output_dir)
  results = []
  run_dirs = []
  for doc_path in docs:
    cfg = make_document_config(template_cfg, doc_path)
    result = runner.run(cfg)
    results.append({"document_id": result.get("document_id", doc_path.stem), "run_dir": result["run_dir"], "exit_code": result["exit_code"]})
    run_dirs.append(Path(result["run_dir"]))

  payload = batch_summary(batch_id, results)
  artifact = make_batch_summary_artifact(payload)
  assert_valid_artifact(artifact, expected_type="batch_summary")
  batch_dir = output_dir / f"batch_{batch_id}"
  batch_dir.mkdir(parents=True, exist_ok=True)
  write_json(batch_dir / "batch_summary.json", artifact)
  write_text(batch_dir / "batch_dashboard.md", render_batch_dashboard_md(payload))

  hist_payload = batch_history_from_run_dirs(run_dirs)
  hist_artifact = make_batch_history_artifact(hist_payload)
  assert_valid_artifact(hist_artifact, expected_type="batch_history")
  write_json(batch_dir / "batch_history.json", hist_artifact)
  write_text(batch_dir / "aggregated_dashboard.md", render_dashboard_md(hist_payload))

  return {
      "batch_dir": str(batch_dir),
      "run_count": len(results),
      "failed_run_count": payload["failed_run_count"],
      "gate_failed_count": payload["gate_failed_count"],
  }

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.core.envelope import unwrap_artifact
from dissertation_intro_qa.runner.prompt_runner import PromptRunner

def run_provider_backed_audit(*, config: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
  audit_bridge_cfg = dict(config.get("pipeline", {}).get("audit_provider_bridge", {}))
  runner_cfg = dict(audit_bridge_cfg.get("runner_config", {}))
  if not runner_cfg:
    raise ValueError("Missing pipeline.audit_provider_bridge.runner_config")
  runner_cfg.setdefault("output", {})
  runner_cfg["output"]["base_dir"] = str(run_dir / "provider_runs")
  prompt_runner = PromptRunner(run_dir / "provider_runs")
  result = prompt_runner.run(runner_cfg)
  mapped_audit_path = result.get("mapped_audit_path", "")
  if not mapped_audit_path:
    raise RuntimeError("Prompt runner did not emit mapped audit artifact.")
  artifact = read_json(Path(mapped_audit_path))
  payload = unwrap_artifact(artifact, expected_type="audit_report")
  return {"artifact": artifact, "payload": payload, "provider_run": result}

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from dissertation_intro_qa.core.exit_codes import ExitCode
from dissertation_intro_qa.core.io import read_json, write_json
from dissertation_intro_qa.core.schema import assert_valid_artifact
from dissertation_intro_qa.pipeline.steps import STEP_REGISTRY

CONTRACT_STEPS = {
    "audit": "audit_report",
    "gate": "gate_result",
    "history-index": "history_index",
}

class PipelineRunner:
  def __init__(self, base_dir: Path):
    self.base_dir = base_dir

  def _new_run_dir(self) -> Path:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    run_dir = self.base_dir / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

  def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
    run_dir = self._new_run_dir()
    metadata = {
        "run_id": run_dir.name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "document_id": config.get("input", {}).get("document_id"),
        "steps": config.get("pipeline", {}).get("steps", []),
    }
    context = {"config": config, "run_dir": run_dir, "artifacts": {}, "step_results": {}}
    write_json(run_dir / "metadata.json", metadata)

    for step in metadata["steps"]:
      fn = STEP_REGISTRY[step]
      result = fn(context)
      context["step_results"][step] = result
      if step in CONTRACT_STEPS:
        expected_type = CONTRACT_STEPS[step]
        data = read_json(Path(result["path"]))
        assert_valid_artifact(data, expected_type=expected_type)

    gate_path = context["artifacts"].get("gate_result")
    gate_passed = True
    if gate_path is not None:
      gate_data = read_json(Path(gate_path))
      gate_passed = bool(gate_data["payload"]["passed"])

    return {
        "run_dir": str(run_dir),
        "results": context["step_results"],
        "exit_code": ExitCode.SUCCESS if gate_passed else ExitCode.GATE_FAILED,
        "document_id": config.get("input", {}).get("document_id"),
    }

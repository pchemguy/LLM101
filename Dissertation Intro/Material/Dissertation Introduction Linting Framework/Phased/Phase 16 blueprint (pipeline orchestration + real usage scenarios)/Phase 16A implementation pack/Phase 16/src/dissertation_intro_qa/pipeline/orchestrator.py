
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json

class PipelineRunner:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _new_run_dir(self):
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_dir = self.base_dir / f"run_{ts}"
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def run(self, config: dict) -> dict:
        run_dir = self._new_run_dir()

        metadata = {
            "run_id": run_dir.name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "document_id": config.get("input", {}).get("document_id"),
            "steps": config.get("pipeline", {}).get("steps", []),
        }

        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        results = {}

        for step in metadata["steps"]:
            results[step] = f"executed:{step}"

        return {
            "run_dir": str(run_dir),
            "results": results,
        }

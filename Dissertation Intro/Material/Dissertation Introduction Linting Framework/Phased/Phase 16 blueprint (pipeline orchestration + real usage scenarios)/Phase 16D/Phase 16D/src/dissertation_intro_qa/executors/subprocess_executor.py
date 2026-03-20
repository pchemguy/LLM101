from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.executors.base import AuditExecutor


class SubprocessAuditExecutor(AuditExecutor):
  def execute(
      self,
      *,
      input_path: Path,
      document_id: str,
      work_dir: Path,
      executor_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    command: List[str] = list(executor_config.get("command", []))
    if not command:
      raise ValueError("Subprocess executor requires non-empty command.")
    out_json = work_dir / "executor_audit_output.json"
    command = [
        part.replace("{input_path}", str(input_path))
            .replace("{document_id}", document_id)
            .replace("{work_dir}", str(work_dir))
            .replace("{out_json}", str(out_json))
        for part in command
    ]
    completed = subprocess.run(command, cwd=str(work_dir), check=False, capture_output=True, text=True)
    if completed.returncode != 0:
      raise RuntimeError(
          "Local audit subprocess failed with return code "
          f"{completed.returncode}: {completed.stderr}"
      )
    if not out_json.exists():
      raise RuntimeError("Subprocess executor did not produce expected out_json.")
    return read_json(out_json)

from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Any, Dict, List
from dissertation_intro_qa.core.io import read_json
from dissertation_intro_qa.providers.base import ProviderAdapter

class SubprocessProviderAdapter(ProviderAdapter):
  def run_prompt(
      self,
      *,
      prompt_text: str,
      document_path: Path,
      document_id: str,
      work_dir: Path,
      provider_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    command: List[str] = list(provider_config.get("command", []))
    if not command:
      raise ValueError("Subprocess provider requires non-empty command.")
    prompt_file = work_dir / "rendered_prompt.txt"
    prompt_file.write_text(prompt_text, encoding="utf-8")
    out_json = work_dir / "provider_result_raw.json"
    command = [
        part.replace("{prompt_file}", str(prompt_file))
            .replace("{document_path}", str(document_path))
            .replace("{document_id}", document_id)
            .replace("{work_dir}", str(work_dir))
            .replace("{out_json}", str(out_json))
        for part in command
    ]
    completed = subprocess.run(command, cwd=str(work_dir), check=False, capture_output=True, text=True)
    if completed.returncode != 0:
      raise RuntimeError(f"Provider subprocess failed with return code {completed.returncode}: {completed.stderr}")
    if not out_json.exists():
      raise RuntimeError("Provider subprocess did not produce expected out_json.")
    return read_json(out_json)

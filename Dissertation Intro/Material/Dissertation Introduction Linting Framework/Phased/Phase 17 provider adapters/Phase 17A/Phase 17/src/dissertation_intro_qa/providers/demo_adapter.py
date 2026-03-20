from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from dissertation_intro_qa.providers.base import ProviderAdapter


class DemoProviderAdapter(ProviderAdapter):
  def run_prompt(
      self,
      *,
      prompt_text: str,
      document_path: Path,
      document_id: str,
      work_dir: Path,
      provider_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    preview = prompt_text[:120]
    return {
        "provider_label": provider_config.get("label", "demo_provider"),
        "document_id": document_id,
        "document_path": str(document_path),
        "prompt_preview": preview,
        "raw_response_text": "DEMO_RESPONSE: prompt accepted",
        "status": "ok",
    }

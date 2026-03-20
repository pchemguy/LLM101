from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class ProviderAdapter(ABC):
  @abstractmethod
  def run_prompt(
      self,
      *,
      prompt_text: str,
      document_path: Path,
      document_id: str,
      work_dir: Path,
      provider_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    raise NotImplementedError

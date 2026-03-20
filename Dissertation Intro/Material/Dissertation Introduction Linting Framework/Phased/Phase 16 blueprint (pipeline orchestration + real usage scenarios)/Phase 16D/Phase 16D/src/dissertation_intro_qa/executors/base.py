from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class AuditExecutor(ABC):
  @abstractmethod
  def execute(
      self,
      *,
      input_path: Path,
      document_id: str,
      work_dir: Path,
      executor_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    raise NotImplementedError

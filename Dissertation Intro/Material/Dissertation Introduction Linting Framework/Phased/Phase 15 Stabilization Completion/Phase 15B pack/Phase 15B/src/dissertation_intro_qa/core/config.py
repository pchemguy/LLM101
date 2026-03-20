from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from dissertation_intro_qa.core.errors import ConfigurationError


def load_config(path: Path) -> Dict[str, Any]:
  try:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
  except Exception as exc:
    raise ConfigurationError(f"Failed to load config: {path}") from exc
  if not isinstance(data, dict):
    raise ConfigurationError("Config must be a mapping.")
  return data

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from dissertation_intro_qa.core.errors import ConfigurationError


def load_taxonomy(path: Path) -> Dict[str, Any]:
  try:
    data = json.loads(path.read_text(encoding="utf-8"))
  except Exception as exc:
    raise ConfigurationError(f"Failed to load taxonomy: {path}") from exc
  if not isinstance(data, dict):
    raise ConfigurationError("Taxonomy must be an object.")
  return data


def known_codes(taxonomy: Dict[str, Any]) -> set[str]:
  codes = set()
  for group in taxonomy.get("groups", {}).values():
    codes.update(group.keys())
  return codes


def severity_floor(taxonomy: Dict[str, Any], code: str) -> Optional[str]:
  for group in taxonomy.get("groups", {}).values():
    if code in group:
      return group[code].get("default_severity_floor")
  return None

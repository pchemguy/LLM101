from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from dissertation_intro_qa.core.errors import ConfigurationError, ContractViolation

SEVERITY_ORDER = {"minor": 1, "moderate": 2, "major": 3, "critical": 4}


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


def validate_defects_against_taxonomy(
    defects: list[dict],
    taxonomy: Dict[str, Any],
    reject_unknown: bool = False,
    enforce_floor: bool = False,
) -> None:
  codes = known_codes(taxonomy)
  for defect in defects:
    code = defect.get("code", "")
    sev = defect.get("severity", "")
    if code not in codes and reject_unknown:
      raise ContractViolation(f"Unknown defect code: {code}")
    floor = severity_floor(taxonomy, code)
    if floor is not None and enforce_floor:
      if SEVERITY_ORDER.get(sev, 0) < SEVERITY_ORDER.get(floor, 0):
        raise ContractViolation(
            f"Severity below taxonomy floor for {code}: {sev} < {floor}"
        )

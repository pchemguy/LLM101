from __future__ import annotations

from pathlib import Path
from typing import Dict


def load_prompt_template(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def render_prompt(template: str, variables: Dict[str, str]) -> str:
  text = template
  for key, value in variables.items():
    text = text.replace("{" + key + "}", value)
  return text

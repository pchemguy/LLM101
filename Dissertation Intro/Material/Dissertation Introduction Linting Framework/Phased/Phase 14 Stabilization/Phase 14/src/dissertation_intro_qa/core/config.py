"""Configuration loader placeholder."""

from __future__ import annotations

from pathlib import Path


def load_config(path: Path) -> dict:
  return {"raw_text": path.read_text(encoding="utf-8")}

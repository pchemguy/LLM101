from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.core.envelope import wrap_artifact


def make_benchmark_summary_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("benchmark_summary", payload)


def make_leaderboard_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("leaderboard", payload)

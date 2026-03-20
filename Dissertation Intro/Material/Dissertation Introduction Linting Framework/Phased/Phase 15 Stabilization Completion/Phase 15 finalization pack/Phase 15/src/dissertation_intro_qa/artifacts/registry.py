from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.core.envelope import wrap_artifact


def make_session_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("session", payload)


def make_run_registry_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("run_registry", payload)


def make_project_dashboard_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("project_dashboard", payload)

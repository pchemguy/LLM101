from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.core.envelope import wrap_artifact


def make_release_manifest_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("release_manifest", payload)

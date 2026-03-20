from __future__ import annotations
from typing import Dict
from dissertation_intro_qa.core.envelope import wrap_artifact

def make_provider_result_artifact(payload: Dict) -> Dict:
  return wrap_artifact("provider_result", payload)

def make_prompt_run_manifest(payload: Dict) -> Dict:
  return wrap_artifact("prompt_run_manifest", payload)

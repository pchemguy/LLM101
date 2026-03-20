from __future__ import annotations
from typing import Dict
from dissertation_intro_qa.core.envelope import wrap_artifact

def make_history_artifact(payload: Dict) -> Dict:
  return wrap_artifact("history_index", payload)

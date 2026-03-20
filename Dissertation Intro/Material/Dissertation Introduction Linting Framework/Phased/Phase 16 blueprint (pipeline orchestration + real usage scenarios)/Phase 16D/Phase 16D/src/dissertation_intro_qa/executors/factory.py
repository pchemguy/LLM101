from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.executors.base import AuditExecutor
from dissertation_intro_qa.executors.demo_executor import DemoAuditExecutor
from dissertation_intro_qa.executors.subprocess_executor import SubprocessAuditExecutor


def build_audit_executor(config: Dict[str, Any]) -> AuditExecutor:
  mode = config.get("mode", "demo")
  if mode == "demo":
    return DemoAuditExecutor()
  if mode == "subprocess":
    return SubprocessAuditExecutor()
  raise ValueError(f"Unsupported audit executor mode: {mode}")

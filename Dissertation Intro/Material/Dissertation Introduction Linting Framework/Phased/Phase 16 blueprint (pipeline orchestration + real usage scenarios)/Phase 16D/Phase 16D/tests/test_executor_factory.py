import pytest

from dissertation_intro_qa.executors.factory import build_audit_executor
from dissertation_intro_qa.executors.demo_executor import DemoAuditExecutor
from dissertation_intro_qa.executors.subprocess_executor import SubprocessAuditExecutor


def test_factory_builds_demo():
  executor = build_audit_executor({"mode": "demo"})
  assert isinstance(executor, DemoAuditExecutor)


def test_factory_builds_subprocess():
  executor = build_audit_executor({"mode": "subprocess", "command": ["python", "x.py"]})
  assert isinstance(executor, SubprocessAuditExecutor)


def test_factory_rejects_unknown():
  with pytest.raises(ValueError):
    build_audit_executor({"mode": "unknown"})

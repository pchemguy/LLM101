import pytest

from dissertation_intro_qa.providers.demo_adapter import DemoProviderAdapter
from dissertation_intro_qa.providers.factory import build_provider_adapter
from dissertation_intro_qa.providers.subprocess_adapter import SubprocessProviderAdapter


def test_factory_builds_demo():
  adapter = build_provider_adapter({"mode": "demo"})
  assert isinstance(adapter, DemoProviderAdapter)


def test_factory_builds_subprocess():
  adapter = build_provider_adapter({"mode": "subprocess", "command": ["python", "x.py"]})
  assert isinstance(adapter, SubprocessProviderAdapter)


def test_factory_rejects_unknown():
  with pytest.raises(ValueError):
    build_provider_adapter({"mode": "unknown"})

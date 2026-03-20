from __future__ import annotations

from typing import Any, Dict

from dissertation_intro_qa.providers.base import ProviderAdapter
from dissertation_intro_qa.providers.demo_adapter import DemoProviderAdapter
from dissertation_intro_qa.providers.subprocess_adapter import SubprocessProviderAdapter


def build_provider_adapter(config: Dict[str, Any]) -> ProviderAdapter:
  mode = config.get("mode", "demo")
  if mode == "demo":
    return DemoProviderAdapter()
  if mode == "subprocess":
    return SubprocessProviderAdapter()
  raise ValueError(f"Unsupported provider mode: {mode}")

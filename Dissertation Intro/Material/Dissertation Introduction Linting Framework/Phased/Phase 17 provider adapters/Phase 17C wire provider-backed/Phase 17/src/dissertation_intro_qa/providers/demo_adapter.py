from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
from dissertation_intro_qa.providers.base import ProviderAdapter

class DemoProviderAdapter(ProviderAdapter):
  def run_prompt(
      self,
      *,
      prompt_text: str,
      document_path: Path,
      document_id: str,
      work_dir: Path,
      provider_config: Dict[str, Any],
  ) -> Dict[str, Any]:
    return {
        "provider_label": provider_config.get("label", "demo_provider"),
        "document_id": document_id,
        "document_path": str(document_path),
        "prompt_preview": prompt_text[:120],
        "status": "ok",
        "structured_audit": {
            "metadata": {
                "document_id": document_id,
                "language": "ru",
                "audit_mode": "provider_demo_structured",
                "date": "2026-03-20",
            },
            "scores": {"SC1": 1, "LC1": 1},
            "defects": [{
                "code": "GAP-02",
                "severity": "major",
                "section": "Степень разработанности / пробел",
                "description": "Пробел не сформулирован явно.",
                "evidence": "Формулировка пробела отсутствует.",
                "recommendation": "Сформулировать конкретный научный пробел.",
            }],
            "gost_compliance": {
                "relevance": True,
                "degree_of_development": True,
                "goals_tasks": True,
                "novelty": True,
                "significance": True,
                "methods": False,
                "defense_propositions": False,
                "reliability": False,
                "approbation": True,
            },
            "summary": {
                "critical_count": 0,
                "major_count": 1,
                "moderate_count": 0,
                "minor_count": 0,
                "overall_verdict": "provider_demo_structured",
            },
        },
    }

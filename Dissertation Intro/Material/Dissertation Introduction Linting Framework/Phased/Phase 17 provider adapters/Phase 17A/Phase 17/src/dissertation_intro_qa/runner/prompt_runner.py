from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from dissertation_intro_qa.core.envelope import wrap_artifact
from dissertation_intro_qa.core.io import write_json, write_text
from dissertation_intro_qa.prompts.template import load_prompt_template, render_prompt
from dissertation_intro_qa.providers.factory import build_provider_adapter


def make_prompt_run_manifest(payload: Dict[str, Any]) -> Dict[str, Any]:
  return wrap_artifact("prompt_run_manifest", payload)


class PromptRunner:
  def __init__(self, base_dir: Path):
    self.base_dir = base_dir

  def _new_run_dir(self) -> Path:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    run_dir = self.base_dir / f"provider_run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

  def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
    provider_cfg = dict(config.get("provider", {}))
    prompt_cfg = dict(config.get("prompt", {}))
    input_cfg = dict(config.get("input", {}))

    document_path = Path(input_cfg["document_path"])
    document_id = input_cfg["document_id"]
    template_path = Path(prompt_cfg["template_path"])

    run_dir = self._new_run_dir()

    template = load_prompt_template(template_path)
    document_text = document_path.read_text(encoding="utf-8")
    prompt_text = render_prompt(
        template,
        {
            "document_id": document_id,
            "document_text": document_text,
            "document_path": str(document_path),
        },
    )
    write_text(run_dir / "rendered_prompt.txt", prompt_text)

    adapter = build_provider_adapter(provider_cfg)
    provider_result = adapter.run_prompt(
        prompt_text=prompt_text,
        document_path=document_path,
        document_id=document_id,
        work_dir=run_dir,
        provider_config=provider_cfg,
    )
    write_json(run_dir / "provider_result.json", provider_result)

    manifest_payload = {
        "run_id": run_dir.name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "provider_mode": provider_cfg.get("mode", "demo"),
        "provider_label": provider_cfg.get("label", ""),
        "document_id": document_id,
        "document_path": str(document_path),
        "template_path": str(template_path),
        "rendered_prompt_path": str(run_dir / "rendered_prompt.txt"),
        "provider_result_path": str(run_dir / "provider_result.json"),
        "status": provider_result.get("status", "ok"),
    }
    manifest = make_prompt_run_manifest(manifest_payload)
    write_json(run_dir / "prompt_run_manifest.json", manifest)

    return {
        "run_dir": str(run_dir),
        "manifest_path": str(run_dir / "prompt_run_manifest.json"),
        "provider_result_path": str(run_dir / "provider_result.json"),
        "status": manifest_payload["status"],
    }

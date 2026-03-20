from pathlib import Path

from dissertation_intro_qa.prompts.template import load_prompt_template, render_prompt


def test_prompt_template_render(tmp_path: Path):
  path = tmp_path / "prompt.txt"
  path.write_text("ID={document_id}\nTEXT={document_text}", encoding="utf-8")
  template = load_prompt_template(path)
  rendered = render_prompt(template, {"document_id": "doc1", "document_text": "hello"})
  assert "doc1" in rendered
  assert "hello" in rendered

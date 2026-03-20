from pathlib import Path

from dissertation_intro_qa.providers.subprocess_adapter import SubprocessProviderAdapter


def test_subprocess_provider_roundtrip(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("Prompt body", encoding="utf-8")
  doc_path = tmp_path / "intro.txt"
  doc_path.write_text("Введение", encoding="utf-8")
  driver_path = tmp_path / "driver.py"
  driver_path.write_text(
      "import json,sys\n"
      "from pathlib import Path\n"
      "args=sys.argv\n"
      "out=Path(args[args.index('--out-json')+1])\n"
      "doc=args[args.index('--document-id')+1]\n"
      "result={"
      "'provider_label':'subprocess_test',"
      "'document_id':doc,"
      "'document_path':'x',"
      "'prompt_preview':'p',"
      "'raw_response_text':'ok',"
      "'status':'ok'"
      "}\n"
      "out.write_text(json.dumps(result), encoding='utf-8')\n",
      encoding="utf-8",
  )

  adapter = SubprocessProviderAdapter()
  result = adapter.run_prompt(
      prompt_text=prompt_path.read_text(encoding="utf-8"),
      document_path=doc_path,
      document_id="demo_doc",
      work_dir=tmp_path,
      provider_config={
          "mode": "subprocess",
          "command": [
              "python",
              str(driver_path),
              "--prompt-file", "{prompt_file}",
              "--document-path", "{document_path}",
              "--document-id", "{document_id}",
              "--work-dir", "{work_dir}",
              "--out-json", "{out_json}",
          ],
      },
  )
  assert result["status"] == "ok"
  assert result["document_id"] == "demo_doc"

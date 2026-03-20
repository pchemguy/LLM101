from pathlib import Path
from dissertation_intro_qa.pipeline.orchestrator import PipelineRunner

def test_pipeline_provider_subprocess_json_payload(tmp_path: Path):
  prompt_path = tmp_path / "prompt.txt"
  prompt_path.write_text("ID={document_id}\n{document_text}", encoding="utf-8")
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
      "'status':'ok',"
      "'audit_payload':{"
      "'metadata':{'document_id':doc},"
      "'scores':{},"
      "'defects':[],"
      "'gost_compliance':{'methods':False},"
      "'summary':{}"
      "}"
      "}\n"
      "out.write_text(json.dumps(result), encoding='utf-8')\n",
      encoding="utf-8",
  )

  cfg = {
      "input": {"path": str(doc_path), "document_id": "demo_doc"},
      "pipeline": {
          "steps": ["audit", "gate"],
          "audit_mode": "provider_bridge",
          "audit_provider_bridge": {
              "runner_config": {
                  "provider": {
                      "mode": "subprocess",
                      "label": "subprocess_provider",
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
                  "prompt": {"template_path": str(prompt_path)},
                  "input": {"document_path": str(doc_path), "document_id": "demo_doc"},
                  "output": {
                      "base_dir": str(tmp_path / "provider_runs"),
                      "emit_audit_artifact": True,
                      "provider_mapping": {"mode": "json_payload", "field_name": "audit_payload"},
                  },
              }
          },
      },
      "outputs": {"base_dir": str(tmp_path / "runs")},
  }

  runner = PipelineRunner(tmp_path / "runs")
  result = runner.run(cfg)
  run_dir = Path(result["run_dir"])
  assert (run_dir / "audit.json").exists()
  assert (run_dir / "gate.json").exists()

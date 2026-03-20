from pathlib import Path

from dissertation_intro_qa.executors.subprocess_executor import SubprocessAuditExecutor
from dissertation_intro_qa.core.schema import assert_valid_artifact


def test_subprocess_executor_roundtrip(tmp_path: Path):
  input_path = tmp_path / "intro.txt"
  input_path.write_text("Введение", encoding="utf-8")
  driver_path = tmp_path / "driver.py"
  driver_path.write_text(
      "import json,sys\n"
      "from pathlib import Path\n"
      "args=sys.argv\n"
      "out=Path(args[args.index('--out-json')+1])\n"
      "doc=args[args.index('--document-id')+1]\n"
      "artifact={"
      "'artifact_type':'audit_report',"
      "'schema_version':'1.0.0',"
      "'generated_at':'x',"
      "'producer':{'tool':'t','version':'v'},"
      "'payload':{"
      "'metadata':{'document_id':doc},"
      "'scores':{},"
      "'defects':[],"
      "'gost_compliance':{},"
      "'summary':{}"
      "}"
      "}\n"
      "out.write_text(json.dumps(artifact), encoding='utf-8')\n",
      encoding="utf-8",
  )

  executor = SubprocessAuditExecutor()
  artifact = executor.execute(
      input_path=input_path,
      document_id="demo_doc",
      work_dir=tmp_path,
      executor_config={
          "mode": "subprocess",
          "command": [
              "python",
              str(driver_path),
              "--input-path", "{input_path}",
              "--document-id", "{document_id}",
              "--work-dir", "{work_dir}",
              "--out-json", "{out_json}",
          ],
      },
  )
  assert_valid_artifact(artifact, expected_type="audit_report")

# Usage

## Demo executor mode
intro-pipeline run examples/executor/pipeline_demo_executor.json

## Subprocess executor mode
intro-pipeline run examples/executor/pipeline_subprocess_executor.json

The subprocess executor must produce an enveloped `audit_report` artifact JSON at
the configured `{out_json}` path.

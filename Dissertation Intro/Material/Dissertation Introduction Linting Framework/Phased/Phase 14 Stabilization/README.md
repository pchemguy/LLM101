**Phase 14 refactor blueprint**

* [Архив Phase 14 blueprint](sandbox:/mnt/data/dissertation_intro_qa_cli_phase14_blueprint.zip)
* [Migration checklist](sandbox:/mnt/data/dissertation_intro_qa_cli_phase14_blueprint/docs/PHASE14_MIGRATION_CHECKLIST.md)
* [Artifact envelope schema](sandbox:/mnt/data/dissertation_intro_qa_cli_phase14_blueprint/schemas/artifact_envelope.schema.json)
* [Example migrated audit artifact](sandbox:/mnt/data/dissertation_intro_qa_cli_phase14_blueprint/examples/audit_report.enveloped.example.json)

Что внутри:

* target package layout under `src/dissertation_intro_qa/`
* core layer skeletons:

  * `io.py`
  * `errors.py`
  * `schema.py`
  * `envelope.py`
  * `config.py`
  * `render.py`
  * `aggregation.py`
  * `taxonomy.py`
  * `paths.py`
* CLI skeleton relocation plan
* machine-readable taxonomy seed
* default config seed
* legacy transition policy
* test plan skeleton

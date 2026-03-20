👉 [Скачать Phase 17C pack](sandbox:/mnt/data/dissertation_intro_qa_phase17c_pack.zip)

Ключевые файлы:

* [pipeline steps with alternate audit path](sandbox:/mnt/data/dissertation_intro_qa_phase17c_pack/src/dissertation_intro_qa/pipeline/steps.py)
* [provider-backed audit bridge](sandbox:/mnt/data/dissertation_intro_qa_phase17c_pack/src/dissertation_intro_qa/pipeline/provider_audit_bridge.py)
* [pipeline orchestrator](sandbox:/mnt/data/dissertation_intro_qa_phase17c_pack/src/dissertation_intro_qa/pipeline/orchestrator.py)
* [provider → audit mapper](sandbox:/mnt/data/dissertation_intro_qa_phase17c_pack/src/dissertation_intro_qa/mappers/provider_to_audit.py)

Что добавлено:

* `pipeline.audit_mode` with two paths:

  * `local_demo`
  * `provider_bridge`
* direct wiring of provider-backed mapped audit artifacts into the main pipeline
* end-to-end provider-bridge flow through:

  * audit
  * gate
  * repair-plan
  * history-index
  * dashboard
* example configs for:

  * demo provider bridge
  * subprocess JSON-payload provider bridge
* tests for:

  * pipeline with demo provider mode
  * pipeline with subprocess JSON-payload provider mode

Что это меняет practically:

* provider-backed audit is no longer separate from the QA pipeline
* the main pipeline can now consume normalized `audit_report` artifacts produced from provider responses
* this is the first true integrated path from prompt/provider execution into the dissertation-intro QA workflow

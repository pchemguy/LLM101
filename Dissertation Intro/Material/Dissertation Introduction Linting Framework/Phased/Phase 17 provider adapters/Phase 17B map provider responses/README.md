👉 [Скачать Phase 17B pack](sandbox:/mnt/data/dissertation_intro_qa_phase17b_pack.zip)

Ключевые файлы:

* [provider → audit mapper](sandbox:/mnt/data/dissertation_intro_qa_phase17b_pack/src/dissertation_intro_qa/mappers/provider_to_audit.py)
* [prompt runner with mapped audit emission](sandbox:/mnt/data/dissertation_intro_qa_phase17b_pack/src/dissertation_intro_qa/runner/prompt_runner.py)
* [provider-backed audit bridge](sandbox:/mnt/data/dissertation_intro_qa_phase17b_pack/src/dissertation_intro_qa/pipeline/provider_audit_bridge.py)
* [provider runner CLI](sandbox:/mnt/data/dissertation_intro_qa_phase17b_pack/src/dissertation_intro_qa/cli/provider_runner.py)

Что добавлено:

* mapping layer from provider response to normalized `audit_report`
* two mapping modes:

  * `demo_structured`
  * `json_payload`
* prompt runner now can emit `mapped_audit.json`
* provider-backed bridge for feeding mapped audit artifacts into the pipeline
* example configs for:

  * demo structured provider mapping
  * subprocess JSON-payload mapping
* tests for:

  * provider-to-audit mapping
  * prompt runner audit emission
  * provider-backed audit bridge

Что это меняет practically:

* provider layer is no longer isolated
* prompt/provider execution can now produce the same normalized `audit_report` contract expected by the QA pipeline
* this is the first clean bridge from provider output back into the stabilized dissertation-intro QA workflow


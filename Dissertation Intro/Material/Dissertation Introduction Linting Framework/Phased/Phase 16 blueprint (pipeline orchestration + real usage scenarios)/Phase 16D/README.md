👉 [Скачать Phase 16D pack](sandbox:/mnt/data/dissertation_intro_qa_phase16d_pack.zip)

Ключевые файлы:

* [executor factory](sandbox:/mnt/data/dissertation_intro_qa_phase16d_pack/src/dissertation_intro_qa/executors/factory.py)
* [subprocess executor bridge](sandbox:/mnt/data/dissertation_intro_qa_phase16d_pack/src/dissertation_intro_qa/executors/subprocess_executor.py)
* [audit step wired to executor bridge](sandbox:/mnt/data/dissertation_intro_qa_phase16d_pack/src/dissertation_intro_qa/pipeline/steps.py)
* [pipeline CLI](sandbox:/mnt/data/dissertation_intro_qa_phase16d_pack/src/dissertation_intro_qa/cli/pipeline_cli.py)

Что добавлено:

* `AuditExecutor` interface
* built-in `demo` executor
* `subprocess` executor for local command/script bridging
* executor selection through pipeline config
* audit step no longer hardcodes demo payload generation
* local helper CLI `local-audit-executor`
* example configs for:

  * demo executor mode
  * subprocess executor mode
* tests for:

  * executor factory
  * demo executor
  * subprocess executor
  * pipeline run with executor bridge

Что это меняет practically:

* pipeline теперь может быть подключён к реальному локальному audit backend
* bridge contract стал явным: local executor must output enveloped `audit_report`
* дальше можно уже подключать конкретный local LLM runner or wrapper script without reshaping the pipeline

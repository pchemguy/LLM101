**Phase 14A execution starter**

* [Архив Phase 14A execution starter](sandbox:/mnt/data/dissertation_intro_qa_phase14a_execution.zip)
* [Мигрированный `intro_qa` CLI в package layout](sandbox:/mnt/data/dissertation_intro_qa_phase14a_execution/src/dissertation_intro_qa/cli/intro_qa.py)
* [Пример enveloped audit artifact](sandbox:/mnt/data/dissertation_intro_qa_phase14a_execution/examples/audit_report.enveloped.example.json)
* [Execution notes](sandbox:/mnt/data/dissertation_intro_qa_phase14a_execution/docs/PHASE14A_EXECUTION_NOTES.md)

Что внутри уже реально сделано:

* `src/`-layout
* shared core modules:

  * `io.py`
  * `errors.py`
  * `envelope.py`
  * `schema.py`
  * `render.py`
  * `aggregation.py`
* legacy flat JSON read compatibility
* enveloped artifact write path
* deterministic JSON serialization
* migrated subset CLI-команд:

  * `compare`
  * `gate`
  * `render-report`
  * `render-comparison`
  * `render-gate`
  * `repair-plan`
  * `history-index`
  * `dashboard`

Что пока intentionally не завершено:

* полноценный `jsonschema` enforcement
* миграция benchmark/scorer/orchestrator/registry/packager слоев
* реальная test suite
* полная config/taxonomy integration

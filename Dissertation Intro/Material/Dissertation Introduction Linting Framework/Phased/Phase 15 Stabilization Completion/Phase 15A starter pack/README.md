**Phase 15A starter pack**

* [Архив Phase 15 starter](sandbox:/mnt/data/dissertation_intro_qa_phase15_starter.zip)
* [Реальный `jsonschema`-based validator](sandbox:/mnt/data/dissertation_intro_qa_phase15_starter/src/dissertation_intro_qa/core/schema.py)
* [Мигрированный `benchmark_scorer` в package layout](sandbox:/mnt/data/dissertation_intro_qa_phase15_starter/src/dissertation_intro_qa/cli/benchmark_scorer.py)
* [Минимальный pytest suite fragment](sandbox:/mnt/data/dissertation_intro_qa_phase15_starter/tests/test_benchmark_scorer.py)

Что внутри:

* expanded schema inventory:

  * `artifact_envelope`
  * `audit_report`
  * `comparison_report`
  * `gate_result`
  * `history_index`
  * `benchmark_summary`
  * `leaderboard`
* `core/schema.py` на базе `jsonschema`
* migrated `benchmark_scorer` writing enveloped artifacts
* minimal tests for:

  * envelope
  * schema validation
  * benchmark scorer logic
  * CLI smoke path
* migration note from Phase 14A
* config and taxonomy seeds

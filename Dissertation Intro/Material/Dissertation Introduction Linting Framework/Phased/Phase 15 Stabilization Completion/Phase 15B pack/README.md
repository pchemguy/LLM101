**Phase 15B pack**

* [Архив Phase 15B pack](sandbox:/mnt/data/dissertation_intro_qa_phase15b_pack.zip)
* [Migrated `benchmark_orchestrator.py`](sandbox:/mnt/data/dissertation_intro_qa_phase15b_pack/src/dissertation_intro_qa/cli/benchmark_orchestrator.py)
* [Migrated `benchmark_registry.py`](sandbox:/mnt/data/dissertation_intro_qa_phase15b_pack/src/dissertation_intro_qa/cli/benchmark_registry.py)
* [Migrated `benchmark_packager.py`](sandbox:/mnt/data/dissertation_intro_qa_phase15b_pack/src/dissertation_intro_qa/cli/benchmark_packager.py)

Что внутри:

* migrated benchmark stack under `src/dissertation_intro_qa/cli/`
* real YAML config loader
* taxonomy loader with helper functions
* expanded schemas for:

  * `run_manifest`
  * `workflow_plan`
  * `session`
  * `run_registry`
  * `project_dashboard`
  * `release_manifest`
* shared aggregation/render paths reused by the migrated CLIs
* expanded pytest fragments for:

  * config/taxonomy
  * orchestrator logic
  * registry logic
  * packager logic
  * benchmark scorer logic

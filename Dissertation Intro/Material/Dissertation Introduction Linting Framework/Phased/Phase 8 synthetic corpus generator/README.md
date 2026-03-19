**Phase 8: synthetic corpus generator + benchmark harness + regression suite for prompts/profiles**

* synthetic corpus generator spec
* benchmark harness scaffold
* benchmark cases
* expected defect targets
* regression suite scaffolding для prompt/profile comparison

Артефакты:

* [Архив Phase 8](sandbox:/mnt/data/dissertation_intro_qa_cli_phase8.zip)
* [README Phase 8](sandbox:/mnt/data/dissertation_intro_qa_cli_phase8/README.md)
* [Benchmark harness](sandbox:/mnt/data/dissertation_intro_qa_cli_phase8/benchmark/BENCHMARK_HARNESS.md)
* [Пример benchmark case: missing gap](sandbox:/mnt/data/dissertation_intro_qa_cli_phase8/benchmark/cases/case_gap_missing.md)
* [Expected targets for that case](sandbox:/mnt/data/dissertation_intro_qa_cli_phase8/benchmark/expected/case_gap_missing.json)

Что это дает practically:

* можно сравнивать prompt variants на одинаковом наборе кейсов;
* можно отслеживать регрессии после изменения prompt/standard/profile;
* появляется основа для внутреннего benchmark набора по качеству LLM-аудита.


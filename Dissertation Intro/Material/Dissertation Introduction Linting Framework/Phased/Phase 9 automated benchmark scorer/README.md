**Phase 9: automated benchmark scorer + expected-vs-actual defect diff + prompt leaderboard scaffold**

* automated benchmark scorer
* expected-vs-actual defect diff
* benchmark summary generation
* prompt/run leaderboard scaffold

Артефакты:

* [Архив Phase 9](sandbox:/mnt/data/dissertation_intro_qa_cli_phase9.zip)
* [`benchmark_scorer.py`](sandbox:/mnt/data/dissertation_intro_qa_cli_phase9/benchmark_scorer.py)
* [README Phase 9](sandbox:/mnt/data/dissertation_intro_qa_cli_phase9/README.md)
* [Smoke benchmark workflow](sandbox:/mnt/data/dissertation_intro_qa_cli_phase9/tests/phase9_smoke_benchmark.md)

Что это дает practically:

* можно автоматически сравнивать expected defect targets с actual audit outputs;
* можно считать per-case recall / precision;
* можно видеть missed expected codes, extra codes и severity failures;
* можно строить простой leaderboard для prompt variants или разных run configurations.

Теперь стек уже включает:

* audit pipeline
* defect taxonomy
* gates
* repair planning
* trends / dashboard
* benchmark corpus
* regression scaffolding
* automated benchmark scoring


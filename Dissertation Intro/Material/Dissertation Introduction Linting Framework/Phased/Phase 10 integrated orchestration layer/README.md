**Phase 10: integrated orchestration layer**


* benchmark case discovery
* run manifest generation
* workflow planning
* regression summary assembly

Артефакты:

* [Архив Phase 10](sandbox:/mnt/data/dissertation_intro_qa_cli_phase10.zip)
* [`benchmark_orchestrator.py`](sandbox:/mnt/data/dissertation_intro_qa_cli_phase10/benchmark_orchestrator.py)
* [README Phase 10](sandbox:/mnt/data/dissertation_intro_qa_cli_phase10/README.md)
* [Orchestration smoke test](sandbox:/mnt/data/dissertation_intro_qa_cli_phase10/tests/phase10_orchestration_smoke.md)

Новые команды:

```bash
python benchmark_orchestrator.py discover ...
python benchmark_orchestrator.py manifest ...
python benchmark_orchestrator.py workflow-plan ...
python benchmark_orchestrator.py regression-summary ...
```

Что это дает practically:

* каждый benchmark run теперь можно описывать через **manifest**;
* workflow plan заранее фиксирует case mapping и scorer command;
* benchmark и regression layer становятся заметно более reproducible;
* появляется coordination layer поверх cases, results, summaries и leaderboard logic.

На этой стадии у вас уже есть довольно полный stack:

* audit / lint / repair / compare / gates
* trends / dashboards / section analytics
* benchmark corpus / scorer / leaderboard
* orchestration layer for reproducible runs


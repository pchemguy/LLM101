**Phase 11: manifest-aware run registry + benchmark session metadata + consolidated project dashboard**

* manifest-aware run registry
* benchmark session metadata
* consolidated project dashboard

Артефакты:

* [Архив Phase 11](sandbox:/mnt/data/dissertation_intro_qa_cli_phase11.zip)
* [`benchmark_registry.py`](sandbox:/mnt/data/dissertation_intro_qa_cli_phase11/benchmark_registry.py)
* [README Phase 11](sandbox:/mnt/data/dissertation_intro_qa_cli_phase11/README.md)
* [Registry smoke test](sandbox:/mnt/data/dissertation_intro_qa_cli_phase11/tests/phase11_registry_smoke.md)

Новые команды:

```bash
python benchmark_registry.py create-session ...
python benchmark_registry.py register-run ...
python benchmark_registry.py build-registry ...
python benchmark_registry.py project-dashboard ...
```

Что это дает practically:

* benchmark runs теперь можно группировать в **sessions**;
* session хранит purpose, prompts, profiles и список зарегистрированных runs;
* registry агрегирует несколько sessions;
* consolidated dashboard собирает общую картину по runs и summaries на уровне проекта.

Теперь стек уже покрывает:

* audit / lint / repair / compare / gates
* trends / dashboards / analytics
* benchmark corpus / scorer / leaderboard
* orchestration
* session / registry / project-level dashboard


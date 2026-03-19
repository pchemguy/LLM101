**Phase 3 report templates + gate summary renderer + repair-plan generator from defect codes**:

* `render-gate` — рендер gate JSON → Markdown
* `repair-plan` — генерация Markdown-плана переработки из audit JSON
* обновленный `README` с примерами Phase 1–3

Артефакты:

* [Архив Phase 3](sandbox:/mnt/data/dissertation_intro_qa_cli_phase3.zip)
* [Обновленный `intro_qa.py`](sandbox:/mnt/data/dissertation_intro_qa_cli/intro_qa.py)
* [Обновленный `README.md`](sandbox:/mnt/data/dissertation_intro_qa_cli/README.md)

Что теперь уже есть в CLI:

* scaffold проекта
* scaffold audit/comparison JSON
* compare отчетов
* gate checks
* render audit/comparison/gate в Markdown
* pack bundle для следующего LLM-прогона
* generate repair plan from defect codes


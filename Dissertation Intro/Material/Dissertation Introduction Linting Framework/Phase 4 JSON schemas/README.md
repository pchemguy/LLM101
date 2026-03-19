**Phase 4 JSON schemas + sample templates + optional CSV defect export + trend summary across multiple reports**

* JSON schemas в scaffold-проект
* sample Markdown templates в `templates/`
* `export-defects-csv` — выгрузка дефектов из одного или нескольких audit JSON в CSV
* `trends` — сводка трендов по нескольким audit JSON, с JSON и optional Markdown output

Артефакты:

* [Архив Phase 4](sandbox:/mnt/data/dissertation_intro_qa_cli_phase4.zip)
* [Обновленный `intro_qa.py`](sandbox:/mnt/data/dissertation_intro_qa_cli/intro_qa.py)
* [Обновленный `README.md`](sandbox:/mnt/data/dissertation_intro_qa_cli/README.md)

Новые команды:

* `intro-qa export-defects-csv ... --out defects.csv`
* `intro-qa trends ... --out-json summary.json --out-md summary.md`

Это уже дает:

* машинно-обрабатываемый экспорт дефектов
* агрегированную картину по нескольким версиям или нескольким введениям
* удобную основу для дальнейшего dashboard / history / QA analytics слоя


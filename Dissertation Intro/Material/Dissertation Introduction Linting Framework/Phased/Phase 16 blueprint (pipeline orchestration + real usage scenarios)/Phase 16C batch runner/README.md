👉 [Скачать Phase 16C pack](sandbox:/mnt/data/dissertation_intro_qa_phase16c_pack.zip)

Что добавлено:

* batch runner for multi-document execution
* `batch_summary.json`
* `batch_history.json`
* aggregated dashboard markdown
* `intro-pipeline batch-run ...`
* GitHub Actions CI entrypoint scaffold

Что это уже позволяет:

* прогонять один и тот же pipeline по нескольким введениям
* собирать batch-level summary
* строить aggregated history/dashboard по нескольким run directories
* запускать batch flow из CI

Ключевые файлы:

* [batch runner](sandbox:/mnt/data/dissertation_intro_qa_phase16c_pack/src/dissertation_intro_qa/pipeline/batch_runner.py)
* [pipeline CLI](sandbox:/mnt/data/dissertation_intro_qa_phase16c_pack/src/dissertation_intro_qa/cli/pipeline_cli.py)
* [CI workflow scaffold](sandbox:/mnt/data/dissertation_intro_qa_phase16c_pack/.github/workflows/intro_qa_batch.yml)


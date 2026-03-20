👉 [Скачать Phase 17 pack](sandbox:/mnt/data/dissertation_intro_qa_phase17_pack.zip)

Ключевые файлы:

* [provider adapter factory](sandbox:/mnt/data/dissertation_intro_qa_phase17_pack/src/dissertation_intro_qa/providers/factory.py)
* [subprocess provider adapter](sandbox:/mnt/data/dissertation_intro_qa_phase17_pack/src/dissertation_intro_qa/providers/subprocess_adapter.py)
* [prompt runner](sandbox:/mnt/data/dissertation_intro_qa_phase17_pack/src/dissertation_intro_qa/runner/prompt_runner.py)
* [provider runner CLI](sandbox:/mnt/data/dissertation_intro_qa_phase17_pack/src/dissertation_intro_qa/cli/provider_runner.py)

Что добавлено:

* `ProviderAdapter` abstraction
* `demo` provider adapter
* `subprocess` provider adapter
* deterministic prompt template loading/rendering
* `prompt_run_manifest` artifact
* `PromptRunner` service
* CLI for prompt execution through provider adapters
* example configs for:

  * demo provider mode
  * subprocess provider mode
* tests for:

  * provider factory
  * prompt template rendering
  * demo provider runner
  * subprocess provider adapter

Что это меняет practically:

* теперь у тебя есть слой **provider abstraction above executor bridge**
* pipeline stack можно подключать не только к local audit executor, но и к **local prompt-driven provider wrappers**

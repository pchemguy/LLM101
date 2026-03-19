# Target Repository Layout

```text
project/
  pyproject.toml
  README.md
  CHANGELOG.md

  src/
    dissertation_intro_qa/
      __init__.py
      version.py

      core/
        io.py
        errors.py
        schema.py
        envelope.py
        config.py
        render.py
        aggregation.py
        taxonomy.py
        paths.py

      cli/
        intro_qa.py
        benchmark_scorer.py
        benchmark_orchestrator.py
        benchmark_registry.py
        benchmark_packager.py

      artifacts/
        audit.py
        comparison.py
        gate.py
        benchmark.py
        registry.py
        release.py

  schemas/
    artifact_envelope.schema.json
    audit_report.schema.json

  configs/
    default.yaml
    defect_taxonomy.json

  docs/
  tests/
  benchmark/
```

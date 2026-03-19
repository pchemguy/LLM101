# Phase 10 Orchestration Smoke Test

## Goal

Проверить интегрированный orchestration layer.

## Commands

### Discover
```bash
python benchmark_orchestrator.py discover   --cases-dir benchmark/cases   --expected-dir benchmark/expected   --out-json benchmark/discovery.json   --out-md benchmark/discovery.md
```

### Manifest
```bash
python benchmark_orchestrator.py manifest   --benchmark-root benchmark   --run-label strict_prompt_v2   --prompt-variant strict_prompt_variant   --profile strict   --out-json benchmark/results/strict_prompt_v2.manifest.json   --out-md benchmark/results/strict_prompt_v2.manifest.md
```

### Workflow plan
```bash
python benchmark_orchestrator.py workflow-plan   --benchmark-root benchmark   --run-label strict_prompt_v2   --prompt-variant strict_prompt_variant   --profile strict   --out-json benchmark/results/strict_prompt_v2.workflow.json   --out-md benchmark/results/strict_prompt_v2.workflow.md
```

### Regression summary
```bash
python benchmark_orchestrator.py regression-summary   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json regression/results/regression_summary.json   --out-md regression/results/regression_summary.md
```

## Expected result

- benchmark discovery file is generated
- run manifest is generated
- workflow plan includes a ready scorer command
- regression summary aggregates multiple run summaries

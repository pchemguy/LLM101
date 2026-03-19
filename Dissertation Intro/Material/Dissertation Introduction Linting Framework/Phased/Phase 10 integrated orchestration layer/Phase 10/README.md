# Dissertation Intro QA CLI — Phase 10

Phase 10 adds an integrated orchestration layer for benchmark workflows.

## New script

- `benchmark_orchestrator.py`

## What it does

Phase 10 ties together:
- benchmark case discovery
- run manifest generation
- workflow planning
- regression summary assembly

This is a reproducible coordination layer around:
- benchmark cases
- actual run outputs
- benchmark scorer summaries
- leaderboard / regression comparisons

## Main commands

### 1. Discover benchmark cases
```bash
python benchmark_orchestrator.py discover   --cases-dir benchmark/cases   --expected-dir benchmark/expected   --out-json benchmark/discovery.json   --out-md benchmark/discovery.md
```

### 2. Build run manifest
```bash
python benchmark_orchestrator.py manifest   --benchmark-root benchmark   --run-label strict_prompt_v2   --prompt-variant strict_prompt_variant   --profile strict   --out-json benchmark/results/strict_prompt_v2.manifest.json   --out-md benchmark/results/strict_prompt_v2.manifest.md
```

### 3. Build workflow plan
```bash
python benchmark_orchestrator.py workflow-plan   --benchmark-root benchmark   --run-label strict_prompt_v2   --prompt-variant strict_prompt_variant   --profile strict   --out-json benchmark/results/strict_prompt_v2.workflow.json   --out-md benchmark/results/strict_prompt_v2.workflow.md
```

### 4. Aggregate regression summaries
```bash
python benchmark_orchestrator.py regression-summary   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json regression/results/regression_summary.json   --out-md regression/results/regression_summary.md
```

## Why this matters

Phase 10 turns the benchmark layer into a reproducible workflow system:
- each run can be described by a manifest;
- each manifest points to expected case/result mapping;
- each workflow plan gives the scoring command to execute next;
- multiple benchmark summaries can be aggregated into regression summaries.

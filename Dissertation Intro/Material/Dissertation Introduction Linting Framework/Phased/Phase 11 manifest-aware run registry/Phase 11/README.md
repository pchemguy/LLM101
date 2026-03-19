# Dissertation Intro QA CLI — Phase 11

Phase 11 adds:

- manifest-aware run registry
- benchmark session metadata
- consolidated project dashboard

## New script

- `benchmark_registry.py`

## What it adds

Phase 11 introduces a higher-level management layer over benchmark/orchestration runs:

- benchmark sessions
- run registration
- registry building
- consolidated project dashboard across multiple runs

## Main commands

### 1. Create benchmark session
```bash
python benchmark_registry.py create-session   --session-id session_001   --description "Strict vs soft prompt comparison on benchmark corpus"   --benchmark-root benchmark   --prompts strict_prompt_variant soft_control_prompt_variant   --profiles strict supervisor   --out-json sessions/session_001.json
```

### 2. Register a run inside session
```bash
python benchmark_registry.py register-run   --session-json sessions/session_001.json   --run-label strict_prompt_v2   --manifest-path benchmark/results/strict_prompt_v2.manifest.json   --summary-path benchmark/results/strict_prompt_v2.summary.json   --prompt-variant strict_prompt_variant   --profile strict   --out-json sessions/session_001.json
```

### 3. Build run registry
```bash
python benchmark_registry.py build-registry   sessions/session_001.json sessions/session_002.json   --out-json registry/run_registry.json   --out-md registry/run_registry.md
```

### 4. Build consolidated project dashboard
```bash
python benchmark_registry.py project-dashboard   --registry-json registry/run_registry.json   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json project_dashboard/project_dashboard.json   --out-md project_dashboard/project_dashboard.md
```

## Why this matters

Phase 11 makes the benchmark system project-aware:

- runs can be grouped into sessions;
- sessions can describe experiment purpose and configuration;
- registered runs can be aggregated into a registry;
- registry + summaries can be rendered into a consolidated dashboard.

# Phase 11 Registry Smoke Test

## Goal

Проверить registry/session layer поверх benchmark orchestration.

## Commands

### Create session
```bash
python benchmark_registry.py create-session   --session-id session_001   --description "Strict vs soft comparison"   --benchmark-root benchmark   --prompts strict_prompt_variant soft_control_prompt_variant   --profiles strict supervisor   --out-json sessions/session_001.json
```

### Register runs
```bash
python benchmark_registry.py register-run   --session-json sessions/session_001.json   --run-label strict_prompt_v1   --manifest-path benchmark/results/strict_prompt_v1.manifest.json   --summary-path benchmark/results/strict_prompt_v1.summary.json   --prompt-variant strict_prompt_variant   --profile strict   --out-json sessions/session_001.json

python benchmark_registry.py register-run   --session-json sessions/session_001.json   --run-label soft_prompt_v1   --manifest-path benchmark/results/soft_prompt_v1.manifest.json   --summary-path benchmark/results/soft_prompt_v1.summary.json   --prompt-variant soft_control_prompt_variant   --profile supervisor   --out-json sessions/session_001.json
```

### Build registry
```bash
python benchmark_registry.py build-registry   sessions/session_001.json   --out-json registry/run_registry.json   --out-md registry/run_registry.md
```

### Build project dashboard
```bash
python benchmark_registry.py project-dashboard   --registry-json registry/run_registry.json   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json project_dashboard/project_dashboard.json   --out-md project_dashboard/project_dashboard.md
```

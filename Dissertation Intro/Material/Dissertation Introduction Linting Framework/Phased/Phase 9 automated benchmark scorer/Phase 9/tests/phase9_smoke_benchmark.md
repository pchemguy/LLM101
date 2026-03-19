# Phase 9 Smoke Benchmark

## Purpose

Проверить automated benchmark scoring на двух synthetic runs:
- run_strict
- run_soft

## Commands

### Score strict run
```bash
python benchmark_scorer.py score-run   --expected-dir benchmark/expected   --actual-dir benchmark/results/run_strict   --run-label strict_prompt_v1   --out-json benchmark/results/strict_prompt_v1.summary.json   --out-md benchmark/results/strict_prompt_v1.summary.md
```

### Score soft run
```bash
python benchmark_scorer.py score-run   --expected-dir benchmark/expected   --actual-dir benchmark/results/run_soft   --run-label soft_prompt_v1   --out-json benchmark/results/soft_prompt_v1.summary.json   --out-md benchmark/results/soft_prompt_v1.summary.md
```

### Build leaderboard
```bash
python benchmark_scorer.py leaderboard   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json benchmark/leaderboard/leaderboard.json   --out-md benchmark/leaderboard/leaderboard.md
```

## Expected qualitative result

- strict_prompt_v1 should outperform soft_prompt_v1 on recall
- soft_prompt_v1 should miss more expected codes

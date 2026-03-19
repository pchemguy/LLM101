# Dissertation Intro QA CLI — Phase 9

Phase 9 adds:

- automated benchmark scorer
- expected-vs-actual defect diff
- benchmark summary generation
- prompt/run leaderboard scaffold

## New script

- `benchmark_scorer.py`

## Main commands

### Score one benchmark run
```bash
python benchmark_scorer.py score-run   --expected-dir benchmark/expected   --actual-dir benchmark/results/run_strict   --run-label strict_prompt_v1   --out-json benchmark/results/strict_prompt_v1.summary.json   --out-md benchmark/results/strict_prompt_v1.summary.md
```

### Build leaderboard across multiple runs
```bash
python benchmark_scorer.py leaderboard   benchmark/results/strict_prompt_v1.summary.json   benchmark/results/soft_prompt_v1.summary.json   --out-json benchmark/leaderboard/leaderboard.json   --out-md benchmark/leaderboard/leaderboard.md
```

## What the scorer evaluates

For each benchmark case:
- matched expected defect codes
- missed expected defect codes
- extra defect codes
- severity failures
- recall
- precision

## Main practical use

Phase 9 is for:
1. comparing prompt variants more objectively;
2. checking whether a prompt misses important expected defects;
3. checking whether a prompt overproduces irrelevant extras;
4. building a simple leaderboard of run quality.

## Included scaffold

- `benchmark_scorer.py`
- `benchmark/leaderboard/`
- compatibility with Phase 8 benchmark cases and expected files

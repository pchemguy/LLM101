# Dissertation Intro QA CLI — Phase 8

Phase 8 adds:

- synthetic corpus generator specification
- benchmark harness scaffold
- regression suite scaffolding for prompts and acceptance profiles
- benchmark cases with expected defect targets

## New directories

- `benchmark/cases/` — synthetic benchmark introductions
- `benchmark/expected/` — expected defect codes and coarse expectations
- `benchmark/prompts/` — benchmark prompt variants
- `benchmark/results/` — place benchmark outputs here
- `regression/profiles/` — regression configurations
- `regression/results/` — store regression run summaries

## Main use

Phase 8 is intended for:
1. comparing prompt variants;
2. comparing different acceptance profiles;
3. checking whether changes in prompts worsen or improve defect detection;
4. building a stable internal benchmark for dissertation-intro auditing.

## Recommended benchmark workflow

### 1. Choose one benchmark case
```bash
# Example case file
benchmark/cases/case_gap_missing.md
```

### 2. Run your LLM audit manually using one prompt variant
Use:
- one file from `benchmark/prompts/`
- one benchmark case
- your standard and taxonomy

### 3. Save the produced JSON audit report
Place it into:
```bash
benchmark/results/
```

### 4. Compare detected defects to expected targets
Open the paired file in:
```bash
benchmark/expected/
```

### 5. Record prompt/profile performance
Use the benchmark summary template in:
```bash
regression/profiles/benchmark_matrix_template.json
```

## Included benchmark cases

- `case_gap_missing.md`
- `case_goal_process.md`
- `case_methods_formal.md`
- `case_novelty_trivial.md`
- `case_gost_missing.md`
- `case_balanced_strong.md`

## Included expected target files

Each benchmark case has a corresponding JSON file containing:
- expected key defect codes
- expected minimum severity pattern
- expected comments on structural weaknesses

## Included regression scaffolds

- `regression/profiles/benchmark_matrix_template.json`
- `regression/profiles/profile_comparison_template.json`

## Suggested next use

Use these cases to compare:
- strict vs softer prompts
- different anti-inference rules
- different scoring instructions
- different acceptance profiles

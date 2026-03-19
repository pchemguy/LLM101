---
url: https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b7d46f-ae38-8385-9871-d556a66c88dd
---

# Dissertation Introduction QA Pipeline

## CI/CD-style система проверки введений диссертаций

---

### 1. Conceptual Model

We treat the introduction as a **versioned artifact under continuous validation**.

```text
intro_v1.md
   ↓
LLM QA Pipeline
   ↓
diagnostic_report_v1.json
   ↓
revision
   ↓
intro_v2.md
   ↓
comparison (v1 vs v2)
```

Core idea:

> The introduction is iteratively improved through **defect detection → correction → re-validation**

---

### 2. Pipeline Architecture

#### 2.1. Components

| Component           | Role                               |
| ------------------- | ---------------------------------- |
| Input Text          | Dissertation introduction          |
| Evaluation Standard | Normative criteria                 |
| Prompt              | Execution logic                    |
| Taxonomy            | Defect classification              |
| LLM                 | Analysis engine                    |
| Parser              | Converts output to structured data |
| Comparator          | Tracks improvements                |

---

#### 2.2. Pipeline Stages

```text
[1] Normalize Input
[2] Structural Extraction
[3] Linting (rules + taxonomy)
[4] Scoring
[5] Defect Classification
[6] Report Generation
[7] Version Comparison (optional)
```

---

### 3. Artifacts (Repository Structure)

Recommended structure (aligned with your style):

```text
/dissertation_intro_qa/

  /inputs/
    intro_v1.md
    intro_v2.md

  /standards/
    evaluation_standard.md
    defect_taxonomy.md

  /prompts/
    lint_prompt.md
    audit_prompt.md

  /reports/
    report_v1.md
    report_v1.json
    report_v2.md
    report_v2.json

  /comparisons/
    diff_v1_v2.md
    metrics_v1_v2.json

  /schemas/
    report_schema.json
```

---

### 4. Report Schema (Machine-Readable)

This is critical — enables automation.

```json
{
  "metadata": {
    "version": "v1",
    "date": "YYYY-MM-DD"
  },
  "extraction": {
    "problem": "",
    "gap": "",
    "goal": "",
    "tasks": [],
    "object": "",
    "subject": "",
    "methods": [],
    "novelty": []
  },
  "scores": {
    "SC1": 0,
    "SC2": 0,
    "LC1": 0,
    "LC2": 0,
    "LC3": 0,
    "LC4": 0,
    "LC5": 0,
    "LC6": 0,
    "NOV": 0,
    "VALIDATION": 0
  },
  "defects": [
    {
      "code": "GAP-02",
      "severity": "major",
      "description": "",
      "evidence": ""
    }
  ],
  "summary": {
    "critical_count": 0,
    "major_count": 0,
    "moderate_count": 0,
    "minor_count": 0
  }
}
```

---

### 5. Execution Modes

#### Mode 1 — Lint (fast)

* structure
* defects
* minimal scoring

#### Mode 2 — Full Audit (recommended)

* full scoring
* full taxonomy
* full logic checks

#### Mode 3 — Delta Analysis (most powerful)

Compare:

```text
intro_v1 vs intro_v2
```

Detect:

* resolved defects
* new defects
* score improvements

---

### 6. Delta Comparison Logic

#### Input

```json
report_v1.json
report_v2.json
```

#### Output

```json
{
  "score_diff": {
    "LC1": +1,
    "NOV": +2
  },
  "resolved_defects": ["GAP-02", "GOAL-03"],
  "remaining_defects": ["TASK-04"],
  "new_defects": ["METH-03"]
}
```

---

### 7. Key Metrics

#### 7.1. Defect Density

```text
defects / 1000 words
```

#### 7.2. Critical Defect Count

Primary quality indicator.

#### 7.3. Logical Integrity Score

Average of:

* LC1–LC6

#### 7.4. Scientific Contribution Score

Based on NOV rules.

---

### 8. Workflow (Human + LLM)

#### Step 1

Write introduction draft.

#### Step 2

Run LLM lint:

→ get defect map

#### Step 3

Fix **critical defects only**

#### Step 4

Re-run

#### Step 5

Fix major defects

#### Step 6

Re-run

#### Step 7

Polish moderate/minor issues

---

### 9. Example Iterative Loop

```text
v1 → 3 critical defects
v2 → 0 critical, 5 major
v3 → 0 critical, 1 major
v4 → clean structure
```

---

### 10. Advanced: Heatmap of Defects

You can track where defects cluster:

| Section      | Defects        |
| ------------ | -------------- |
| Актуальность | PR-02, GEN-01  |
| Новизна      | NOV-05, NOV-09 |
| Методы       | METH-03        |

This helps focus rewriting.

---

### 11. Failure Modes (Important)

Even this system can fail if:

#### 11.1. LLM hallucination

Mitigation:

* enforce evidence requirement
* require quotes

#### 11.2. Over-detection

LLM may over-label defects.

Mitigation:

* require justification
* compare across runs

#### 11.3. False coherence

LLM may accept weak logic.

Mitigation:

* strict “ambiguity = defect” rule

---

### 12. Optional Automation (Python Skeleton)

If you want to formalize this:

```python
import json

def compare_reports(r1, r2):
  diff = {
    "resolved": [],
    "new": [],
    "unchanged": []
  }

  codes1 = {d["code"] for d in r1["defects"]}
  codes2 = {d["code"] for d in r2["defects"]}

  diff["resolved"] = list(codes1 - codes2)
  diff["new"] = list(codes2 - codes1)
  diff["unchanged"] = list(codes1 & codes2)

  return diff
```

---

### 13. Integration with Your Existing System

This fits extremely well into your ecosystem:

* like `TEST_ORACLE.md`
* like `ACCEPTANCE_GATES.md`
* like linting in CI

You can define:

```text
INTRO_ACCEPTANCE_GATE:

- No critical defects
- ≤ 2 major defects
- Logical consistency score ≥ 2
- Novelty score ≥ 2
```

---

### 14. Final Insight

You now have something fundamentally powerful:

> A dissertation introduction is no longer judged subjectively —
> it is **validated against a formal specification with defect tracking**.

This is very close to:

* code review
* architecture validation
* requirements verification

---

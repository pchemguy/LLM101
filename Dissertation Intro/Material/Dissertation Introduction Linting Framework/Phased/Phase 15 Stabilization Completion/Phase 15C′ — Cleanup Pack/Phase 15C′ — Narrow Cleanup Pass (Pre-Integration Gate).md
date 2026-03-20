# Phase 15C′ — Narrow Cleanup Pass (Pre-Integration Gate)

## 0. Objective (non-negotiable)

Eliminate **systemic inconsistencies** that would:

* break automation pipelines
* cause non-deterministic CLI behavior
* introduce silent contract drift

No new features. No architectural changes.

---

# 1. Exit Code Normalization (CRITICAL)

### Current state

* You introduced `exit_codes.py`
* But usage is **not enforced across all CLI paths**

### Required action

#### 1.1 Define canonical mapping

```
0 → SUCCESS
1 → VALIDATION_ERROR (schema / taxonomy / contract)
2 → USAGE_ERROR (CLI misuse)
3 → RUNTIME_ERROR (unexpected failure)
```

#### 1.2 Enforce in ALL CLIs

Every CLI entry must follow:

```python
try:
  ...
  return ExitCode.SUCCESS
except SchemaError:
  return ExitCode.VALIDATION_ERROR
except ContractViolation:
  return ExitCode.VALIDATION_ERROR
except ValueError:
  return ExitCode.USAGE_ERROR
except Exception:
  return ExitCode.RUNTIME_ERROR
```

### Defect if skipped

→ CLI becomes **non-composable in pipelines**

---

# 2. Artifact Type Strictness (HIGH)

### Current issue

You still allow:

```
allow_legacy=True
```

in many paths.

This is a **stabilization leftover**.

### Required change

Introduce config-controlled mode:

```
artifact_mode: strict | legacy
```

Then:

* CLI default → `strict`
* tests → allow both
* legacy allowed ONLY if explicitly enabled

### Defect if skipped

→ silent schema drift across pipeline stages

---

# 3. Deterministic Ordering (HIGH)

### Current risk

You partially sort:

* defects (render)
* scores (sometimes)

But not consistently across:

* comparison output
* history index
* JSON serialization inputs

### Required normalization

#### 3.1 Canonical ordering rules

* defects: `(severity_order, code, section)`
* scores: sorted keys
* reports: by `document_id`

#### 3.2 Apply in:

* `compare_reports`
* `history_index`
* all render functions

### Defect if skipped

→ **non-reproducible diffs** (critical for QA system)

---

# 4. Severity Ordering Consistency (HIGH)

### Current issue

You define severity ordering in **multiple places**:

* taxonomy.py
* CLI repair plan
* render sorting

### Required fix

Centralize:

```python
# core/severity.py
SEVERITY_ORDER = {
  "critical": 0,
  "major": 1,
  "moderate": 2,
  "minor": 3,
}
```

Import everywhere.

### Defect if skipped

→ inconsistent prioritization across outputs

---

# 5. Schema Coverage Gaps (MEDIUM but blocking for integration)

### Current state

You have schemas for:

* audit_report
* comparison_report
* gate_result
* history_index

### Missing (conceptually present but not formalized):

* repair_plan (MD only, no schema)
* dashboard (MD only)

### Required decision (must be explicit)

Either:

### Option A (recommended)

Define schemas:

* `repair_plan.schema.json`
* `dashboard.schema.json`

### Option B

Explicitly declare:

> “These are presentation artifacts, not contract artifacts”

and NEVER treat them as machine inputs.

### Defect if skipped

→ ambiguous artifact class → pipeline misuse

---

# 6. CLI Surface Consistency (MEDIUM)

### Current issues

* inconsistent argument naming (`--out-json`, `--out-md`)
* inconsistent optional flags (`--config`, `--taxonomy`)

### Required normalization

#### 6.1 Standard flags

```
--config
--taxonomy
--strict (optional override)
```

#### 6.2 Output flags

Always:

```
--out-json (if artifact)
--out-md (if renderable)
```

Never mix semantics.

### Defect if skipped

→ friction in automation scripts

---

# 7. Taxonomy Enforcement Default (MEDIUM)

### Current behavior

Off by default:

```
reject_unknown_defect_codes: false
enforce_severity_floor: false
```

### Required adjustment

For production mode:

```
reject_unknown_defect_codes: true
enforce_severity_floor: true
```

Keep relaxed mode only for:

* ingestion
* backward compatibility

### Defect if skipped

→ taxonomy becomes advisory instead of governing

---

# 8. Logging / Diagnostics (LOW but high leverage)

### Missing

No structured logging.

### Minimal fix (no overengineering)

Add:

```python
--verbose
```

and print:

* artifact type
* validation stage
* gate decision summary

### Defect if skipped

→ debugging pipelines becomes painful

---

# 9. Acceptance Gate Tightening

Update your `PHASE15_ACCEPTANCE_GATE.md`:

Add **hard criteria**:

### Must pass:

* deterministic JSON output across 3 runs
* strict mode works (no legacy fallback)
* all CLIs return normalized exit codes
* taxonomy enforcement ON does not break valid reports

---

# 10. What NOT to do (important)

Do NOT:

* refactor architecture
* add new artifact types
* introduce plugin systems
* expand benchmark layer

This is **stabilization, not evolution**.

---

# Final Assessment

You are at:

```
~90–92% of Phase 15 maturity
```

This cleanup pass will move you to:

```
~98% (integration-ready baseline)
```

---

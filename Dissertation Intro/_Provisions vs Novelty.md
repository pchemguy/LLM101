You’re right to isolate this — the distinction is **critical and often blurred even in real dissertations**. If you don’t formalize it, your protocol will silently degrade.

Below is a **precise, operational distinction** you can directly encode.

---

# 1. Core Difference

> **Научная новизна = что получено (results)**
> **Положения на защиту = что утверждается и выносится как защищаемые тезисы (claims based on results)**

---

# 2. Functional Roles

## Научная новизна (Scientific Novelty)

**Role:**

> Generate new knowledge

**Content:**

* methods
* models
* frameworks
* empirical findings
* classifications
* mechanisms

**Form:**

* descriptive
* result-oriented

---

## Положения на защиту (Provisions for Defense)

**Role:**

> Formalize what is being defended

**Content:**

* distilled claims derived from results
* statements that can be:

  * defended
  * challenged
  * validated

**Form:**

* declarative
* thesis-like
* concise

---

# 3. Structural Relationship

```id="core_relation"
Научная новизна → Положения на защиту
```

Meaning:

* provisions MUST be derived from novelty
* they are **not independent content**

---

# 4. Correct Transformation

Each novelty item should produce **one or more provisions**.

---

## Example

### Novelty

> Разработана методика оценки эффективности модернизации на основе многокритериального подхода.

---

### Provisions for defense

> 1. Предложенная методика оценки эффективности модернизации обеспечивает более точную интегральную оценку по сравнению с существующими подходами.
> 2. Использование многокритериального подхода позволяет учитывать противоречивые факторы при принятии решений.

---

## Key observation

* Novelty = **what was created**
* Provisions = **what is claimed about it**

---

# 5. Typical Defects (you should explicitly detect)

## ❌ Defect 1 — Duplication

Same text appears in both sections.

→ indicates no transformation

---

## ❌ Defect 2 — Independence

Provisions introduce ideas not present in novelty.

→ logical inconsistency

---

## ❌ Defect 3 — Missing provisions

Novelty exists, but no formal claims.

→ weak defensibility

---

## ❌ Defect 4 — Non-claim provisions

> “Разработана методика…”

This is NOT a provision — this is still a result.

---



---

# 7. Add New Criterion (you should)

You already introduced LC8 — this is exactly where it belongs.

---

### **LC8 — Novelty ↔ Provisions for Defense Consistency**

**Definition**

Provisions for defense must be derived from and consistent with scientific novelty.

---

**Evaluation Questions**

1. Does each provision correspond to a novelty item?
2. Does it express a **claim**, not a description?
3. Is there transformation (result → statement)?

---

**Scoring**

| Score | Interpretation                     |
| ----- | ---------------------------------- |
| 0     | no connection                      |
| 1     | weak / partial / duplication       |
| 2     | mostly consistent                  |
| 3     | clear transformation and alignment |

---

# 8. Practical Heuristic (very useful for LLM)

For each provision:

Ask:

```id="heuristic"
Can this statement be argued, challenged, or tested?
```

If **no**:

→ not a valid provision

---

# 9. Compact Comparison Table (for your standard)

| Aspect     | Научная новизна     | Положения на защиту |
| ---------- | ------------------- | ------------------- |
| Nature     | Results             | Claims              |
| Function   | Produce knowledge   | Defend knowledge    |
| Form       | Descriptive         | Declarative         |
| Dependency | Primary             | Derived             |
| Evaluation | Validity of results | Strength of claims  |

---

# 10. Bottom Line

* Novelty = **substance**
* Provisions = **defensive interface of that substance**

If they collapse into one:

> the dissertation loses **argumentative structure**

---

If you want next step, we can:

* enforce **1:N mapping rules (novelty → provisions)**
* or design **automatic detection of duplication vs transformation** (very feasible for LLMs)

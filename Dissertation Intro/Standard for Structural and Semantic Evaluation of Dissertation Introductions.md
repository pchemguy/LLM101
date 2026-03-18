---
URLs:
  - https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b7d46f-ae38-8385-9871-d556a66c88dd
  - https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b902d2-a2c8-838b-a60d-4e863e60bc7c
---

# Standard for Structural and Semantic Evaluation of Dissertation Introductions

---

## 1. Purpose

This document defines a **normative analytical standard** for assessing the methodological quality and structural completeness of dissertation introductions in the context of **Russian dissertation practice** and **VAK-regulated specialty alignment**. The standard is designed for use with **large language models (LLMs)** performing structured critical analysis.

The standard enables:

* systematic evaluation of dissertation introductions
* consistent identification of methodological deficiencies
* structured comparison across dissertations
* reproducible evaluation results

**Scope**

This standard does **not** define:

* scoring scale
* evaluation protocol
* output format

These components are included in a companion **protocol document**.

**Compliance**

The standard is compatible with the structural requirements of **ГОСТ Р 7.0.11 — Диссертация и автореферат диссертации. Структура и правила оформления**.

---

## 2. Structural Components

### GOST Р 7.0.11 Required Components

Section **5.3.1 of GOST Р 7.0.11** specifies that a dissertation introduction must include the following **core components**:

| Component                                     | Description                                    |
| --------------------------------------------- | ---------------------------------------------- |
| актуальность темы исследования                | Relevance / justification of problem           |
| степень разработанности проблемы              | Degree of development / literature positioning |
| цели и задачи исследования                    | Goals and operational tasks                    |
| научная новизна                               | Scientific novelty / key results               |
| теоретическая и практическая значимость       | Theoretical and practical significance         |
| методология и методы исследования             | Methodology and methods                        |
| положения, выносимые на защиту                | Provisions for defense                         |
| степень достоверности и апробация результатов | Reliability and approbation                    |

These components constitute the **minimum required structure**.

---

### Extended Analytical Structure

While not universally mandatory, Russian dissertation practice typically also includes:

| Section                   | Role                                |
| ------------------------- | ----------------------------------- |
| Актуальность              | justification of problem importance |
| Степень разработанности   | literature positioning              |
| Исследовательский пробел  | unresolved scientific issue         |
| Цель исследования         | research objective                  |
| Задачи исследования       | operational research plan           |
| Объект исследования       | domain of investigation             |
| Предмет исследования      | analytical focus                    |
| Теоретическая основа      | conceptual framework                |
| Методология и методы      | analytical methods                  |
| Информационная база       | empirical data sources              |
| Научная новизна           | scientific novelty (key results)    |
| Положения на защиту       | formal statement of contributions   |
| Теоретическая значимость  | theoretical contribution            |
| Практическая значимость   | applied value                       |
| Достоверность результатов | reliability justification           |
| Апробация результатов     | validation and dissemination        |
| Публикации                | scholarly output                    |
| Структура диссертации     | document structural statistics      |

Absence of these extended components may reduce analytical clarity and can be evaluated as **moderate or minor structural defects**.

---

## 3. Core Research Logic

The introduction must express a **coherent research argument**, which can be represented as a **semantic dependency chain**:

```
Problem  
→ State of knowledge  
→ Gap  
→ Object  
→ Subject  
→ Goal  
→ Tasks  
→ Methods  
→ Novelty (Results)  
→ Significance  
→ Validation
```

**Dependency constraints:**

```
Object → Subject (containment constraint)
Novelty → Provisions for Defense (transformation constraint)
```

### Notes

* Each node must be **explicitly identifiable**.
* Each node must be **logically derived from its predecessor(s)**.
* Violation of any dependency constitutes a **logical defect** and should trigger downgrade in the corresponding **Logical Consistency (LC) criteria**.

**Interpretation**

This chain is **semantic**, not a required textual order.
The actual text of a dissertation may present nodes in a different sequence, but logical dependencies must hold.

---

## 4. Specialty Alignment (VAK Passport)

Dissertations defended in Russia must comply with **VAK regulations**. This standard acknowledges that:

* each dissertation must **formally declare its specialty**
* each dissertation must **substantively align with the VAK specialty passport** for that declared specialty

Specialty alignment is assessed in the **companion protocol**, using explicit mapping between dissertation elements and passport components.

---

## 5. Evaluation Dimensions

The introduction must be evaluated across the following **analytical dimensions**, each corresponding to a distinct aspect of methodological quality.

| Dimension                      | Description                                                                                                    |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Structural completeness        | presence, explicitness, and separability of required (GOST) and extended components                            |
| Research problem justification | clarity, specificity, and validity of problem relevance (актуальность)                                         |
| Literature positioning         | adequacy of synthesis of prior research and its role in supporting gap identification                          |
| Research design coherence      | logical consistency of the core chain: gap → object → subject → goal → tasks                                   |
| Methodological adequacy        | alignment of methods with stated tasks and their ability to produce valid results                              |
| Scientific novelty             | clarity, specificity, independence, and credibility of claimed scientific results                              |
| Significance justification     | explicit, non-generic derivation of theoretical and practical significance from specific novelty items         |
| Provisions for defense quality | validity of claims derived from novelty; presence of transformation (result → claim), clarity, and testability |
| Validation and dissemination   | credibility of results supported by approbation, publications, discussion, or implementation                   |
| Specialty alignment            | consistency of topic, gap, object, subject, methods, and results with the VAK specialty passport               |

---

### Interpretation Notes

* Each dimension must be evaluated **independently**, but with awareness of **cross-dependencies** defined in the research logic (Section 3).
* Dimensions are **analytically distinct but logically interconnected**.
* Weakness in one dimension (e.g., novelty) may propagate into others (e.g., significance, provisions for defense).

---

## 6. Evidence Requirement

All evaluation decisions must be **explicitly evidence-based**.

Paraphrasing or implicit interpretation is not sufficient.

---

### Mandatory Evidence Structure

Each evaluative finding must include:

1. **Identification of the evaluated element or criterion**
2. **Direct textual evidence** (minimal sufficient quote)
3. **Analytical explanation**
4. **Evaluative conclusion**

---

### Example

```
Criterion: Research Gap

Evidence:
"Несмотря на значительное количество исследований..."

Analysis:
The statement indicates the existence of prior research but does not
identify a конкретная нерешённая научная проблема. The gap remains
implicitly defined and lacks operational clarity.

Conclusion:
Weak formulation of research gap; does not meet methodological requirements.
```

---

### Strict Rules

* Evidence MUST be:
    * direct quotation
    * minimally sufficient (no excessive text)
* Generic references (e.g., “the author notes that…”) are NOT acceptable
* Absence of evidence invalidates the evaluation

---

### Missing Element Rule

If a required component is absent:

```
Criterion: [component name]

Evidence:
[отсутствует]

Analysis:
The component is not identifiable in the introduction.

Conclusion:
Component absent; constitutes a structural or methodological defect.
```

---

### Ambiguity Rule

If a component is present but vague:

* it must still be quoted
* the insufficiency must be explicitly justified

---

### Important Clarification

This standard defines **evidence requirements and analytical structure only**.

* Scoring is defined in the **protocol**
* Output formatting is defined in the **protocol**

---

## 7. Structural Completeness Criteria (SC)

### SC1 — Required GOST components

The introduction must include all components defined in the **GOST Р 7.0.11** section above.

Absence of any required component constitutes a **major structural defect**.

---

### SC2 — Extended structural elements

Additional components (defined in the *Extended Analytical Structure*) are not universally mandatory.

However, their absence typically reduces analytical clarity and must be evaluated as a defect **unless their functional role is clearly fulfilled elsewhere in the text**.

---

## 8. Specialty Alignment Criteria (SA)

Each specialty alignment criterion must be evaluated through **explicit mapping** between dissertation introduction components and corresponding elements of the specialty passport.

---

### SA1 — Topic–Specialty Alignment

The research topic must fall within the scope of the specialty domain.

---

### SA2 — Object/Subject–Specialty Alignment

The object and subject must correspond to:

* the object of the specialty
* the subject of the specialty

---

### SA3 — Methods–Specialty Alignment

The methods must be appropriate for investigating problems within the specialty domain.

---

### SA4 — Novelty–Specialty Alignment

The claimed scientific novelty (results) must belong to the specialty domain.

---

### SA5 — Passport justification quality

If a **"соответствие специальности"** section exists:

* it must provide **substantive justification**, not merely declarative statements

---

### SA6 — Research Gap–Specialty Alignment

The identified research gap must fall within the scope of the specialty.

---

### Critical Rule

If any **core research component** (topic, gap, object, subject, methods, or results) falls outside the specialty domain:

→ this constitutes a **critical defect of misalignment**

---

## 9. Logical Consistency Criteria (LC)

### LC1 — Problem–Gap Consistency

The research gap must logically follow from the **state of knowledge** as presented in the introduction.

Failure indicates weak or unsubstantiated problem formulation.

---

### LC2 — Gap–Goal Consistency

The research goal must directly address the identified research gap.

---

### LC3 — Goal–Task Consistency

```
Tasks must collectively achieve the research goal.
```

Tasks unrelated to the goal indicate a **defective research design**.

---

### LC4 — Object–Subject Consistency

```
Subject ⊂ Object
```

The subject must represent a **specific analytical aspect** of the object.

---

### LC5 — Tasks–Methods Consistency

The selected methods must be capable of solving the stated research tasks.

---

### LC6 — Goal–Novelty Consistency

Scientific novelty (results) must directly correspond to and fulfill the stated research objective.

---

### **LC7 — Novelty–Significance Consistency**

Theoretical and practical significance must be **explicitly and logically derived from scientific novelty**.

---

#### Formal requirements

1. Each significance statement must reference:
    * a specific novelty item
2. Each novelty item must be associated with:
    * at least one articulated significance statement (theoretical and/or practical)

---

#### Valid linkage

A valid novelty–significance relationship requires:

* explicit reference (not implicit association)
* logical derivation (not rhetorical assertion)
* non-generic formulation

---

#### Violations

| Violation                   | Interpretation |
| --------------------------- | -------------- |
| significance without result | invalid        |
| result without significance | incomplete     |
| generic significance        | weak           |

---

#### Critical rule

If scientific novelty does not contain **specific and identifiable results**, then significance is considered **unsubstantiated**.

---

#### Scope limitation

LC7 evaluates:

* **linkage between results and significance**

LC7 does **not evaluate**:

* whether the result itself is valid → (RC1)
* whether the novelty block is structurally sound → (RC3)

---

### LC8 — Novelty–Provisions for Defense Consistency

Provisions for defense must be **derived from scientific novelty**.

Scientific novelty describes results; provisions for defense formulate **defensible claims about those results**.

---

#### Formal Requirements

Each provision must:

* be based on a specific novelty item
* express a **defendable claim**, not a descriptive statement

---

#### Evaluation Questions

1. Does each provision correspond to a novelty item?
2. Does it express a claim rather than a result?
3. Is there a clear transformation (result → claim)?

---

#### Practical Heuristic

For each provision:

```
Can this statement be derived from results, argued, challenged, and tested?
```

If **no** → invalid provision.

---

#### Typical Defects

| Category             | Symptom                              | Interpretation              |
| -------------------- | ------------------------------------ | --------------------------- |
| Duplication          | Same text appears in both sections   | No transformation           |
| Independence         | New ideas appear only in provisions  | Logical inconsistency       |
| Missing provisions   | Novelty exists, but no formal claims | Weak defensibility          |
| Non-claim provisions | "Разработана методика…"              | Still a result, not a claim |

---

## 10. Results Criteria (RC)

### **RC1 — Scientific Novelty (Results)**

Each novelty statement must represent a **distinct, concrete scientific result**.

A statement is not accepted as scientific novelty merely because it appears under a “novelty” heading. Its status must be justified analytically at the level of the individual item.

---

#### Core validity requirement

A valid novelty item must:

1. represent **one primary result** (not a bundle of results)
2. be formulated with sufficient precision to determine:
    * what exactly was obtained
    * what is methodologically new
3. allow identification of its **comparative novelty basis**

If any of these conditions are not satisfied, the item must be classified as:

* weak
* overloaded
* misclassified
* or invalid

---

#### Requirements

A valid novelty item must be:

* ✔ **Specific**
* ✔ **Self-contained**
* ✔ **Independently interpretable**
* ✔ **Methodologically identifiable**

---

#### Interpretive definitions

**Specific**
The result must be clearly identifiable. Vague or generic formulations are insufficient.

**Self-contained**
Each item must correspond to **one result**.
Multiple independent results within one statement constitute an **overloaded item**.

**Independently interpretable**
It must be possible to understand the nature of the result without reconstructing hidden assumptions.

**Methodologically identifiable**
The result must belong to a clear scientific category (e.g., method, model, classification, mechanism).

---

#### Recommended structure

```
Result:
[what is created/discovered]

Mechanism:
[what is new / how it works]

Implication:
[why it matters]
```

---

#### Item-level defect patterns

The following patterns indicate weak or invalid novelty at the **individual item level**:

##### 1. Overloaded item

One statement contains multiple independent results (e.g., definition + typology + factors + method).
→ Reduces clarity and testability.

---

##### 2. Weak novelty language

Use of verbs such as:

- "обобщены",
- "рассмотрены",
- "выявлены",
- "сформулированы рекомендации"

without additional specification of a scientific result.

---

##### 3. Descriptive systematization

Ordering or grouping without:

* a new classificatory principle
* a new structural relation
* or a new analytical mechanism

---

##### 4. Factor listing without structure

“Factors identified” without:

* structure
* ranking
* model
* or causal integration

---

##### 5. Review or sectoral analysis presented as novelty

Generalized trends, industry descriptions, or summaries that do not produce a new analytical result.

---

##### 6. Case description presented as novelty

Empirical analysis of a specific object without:

* generalization
* methodological contribution
* or transferable result

---

##### 7. Recommendations without scientific basis

Recommendations not grounded in:

* a model
* a method
* or a generalized mechanism

---

##### 8. Authorial definition of a broad mature concept

Definitions that:

* do not resolve a theoretical problem
* do not enable new analysis
* do not introduce an operational concept

→ typically **pseudo-novelty**

---

##### 9. Scale mismatch

The novelty operates at a conceptual level inconsistent with the actual research object.

---

#### Evaluation requirement

For each novelty item, the evaluator must determine:

1. What exactly is the result?
2. What type of result is it?
3. Does it contain multiple independent results?
4. What is the comparative basis of novelty?
5. Is it a scientific result, or misclassified material?

If any answer is unclear → classify as **defect**.

---

### RC2 — Validation and Approbation

The introduction must demonstrate credibility of results through:

* conference presentations
* academic discussion
* publications
* implementation or empirical testing (if applicable)

Absence or weak formulation reduces credibility.

---

### **RC3 — Inflation and Substantive Quality of Novelty and Significance**

This criterion evaluates the **novelty and significance sections as a whole**, not individual items.

---

#### Evaluation dimensions

1. **Number of items**
2. **Independence of items**
3. **Substantive depth of items**
4. **Conceptual purity of sections**

---

#### Block-level defect patterns

##### 1. Inflation

Large number of weak, vague, or low-substance items.

---

##### 2. Structural overload

Systematic presence of **multi-result (overloaded) items** across the block.

---

##### 3. Mixing of result classes

The novelty section contains heterogeneous material:

* scientific results
* literature review elements
* empirical case descriptions
* practical recommendations

→ indicates **methodological impurity**

---

##### 4. Substitution of novelty

Novelty is replaced by:

* analysis
* usefulness
* description
* or general discussion

---

##### 5. Imbalance

* many weak items + few meaningful ones
* or dominance of one weak type (e.g., recommendations)

---

#### Interpretation patterns

| Pattern         | Interpretation               |
| --------------- | ---------------------------- |
| many weak items | artificial inflation         |
| few strong      | acceptable structure         |
| mixed           | requires detailed evaluation |

---

#### Dependency

RC3 must be interpreted in conjunction with:

* **RC1** — to assess validity of individual items
* **LC7** — to assess result–significance linkage

---

#### Scope limitation

RC3 evaluates:

* overall structure and quality of sections

RC3 does **not evaluate**:

* individual item validity → (RC1)
* correctness of significance derivation → (LC7)

---

## 11. Defect Severity Classification

Defect severity must be assigned with explicit reference to:

1. the **criterion violated** (SC, SA, LC, RC), and
2. the **degree to which the defect undermines**:
    * logical coherence
    * methodological validity
    * disciplinary admissibility (specialty alignment)

---

### Severity Levels

| Severity     | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| **Critical** | fundamental violation invalidating the research specification         |
| **Major**    | structural or logical defect significantly weakening research design  |
| **Moderate** | clear methodological weakness with limited impact on overall validity |
| **Minor**    | local imperfection not affecting core research logic                  |

---

### Critical defects

Defects that **invalidate the introduction as a research specification**:

* absence of research gap (LC1 failure)
* absence of research objective (LC2 failure)
* absence of scientific novelty (RC1 failure)
* specialty mismatch (SA critical rule violation)
* incoherent research chain (broken dependency graph)

---

### Major defects

Defects that **compromise research design or argument structure**:

* tasks not achieving the goal (LC3 violation)
* subject not contained within object (LC4 violation)
* methods not capable of solving tasks (LC5 violation)
* novelty not derived from goal (LC6 violation)
* novelty–significance disconnect (LC7 violation)
* provisions not derived from novelty (LC8 violation)
* weak or non-specific novelty (RC1 deficiency)
* misalignment with specialty (SA1–SA6 partial failure)

---

### Moderate defects

Defects that **reduce clarity, precision, or evidential strength**:

* vague or generic problem justification (SC/LC1)
* weak literature synthesis (LC1 support failure)
* implicit or weakly stated research gap
* incomplete validation/approbation (RC2)
* partial or inconsistent significance derivation (LC7 partial failure)

---

### Minor defects

Defects that **do not affect methodological validity**:

* stylistic redundancy
* terminological inconsistency
* overly generic wording (without logical consequences)
* minor structural omissions (SC2)

---

### Severity Assignment Rule (IMPORTANT)

Severity MUST be determined by **impact on the dependency graph**:

```
If defect breaks the chain → Critical
If defect distorts the chain → Major
If defect weakens interpretation → Moderate
If defect is local → Minor
```

---

## 12. Anti-Inference Rule

The evaluator must strictly adhere to the following rule:

> No methodological element may be assumed unless it is explicitly or unambiguously expressed in the text.

---

### Formal constraints

The evaluator MUST NOT:

* infer missing components
* interpret generic statements as fulfilling formal requirements
* reconstruct intended meaning beyond textual evidence

---

### Operational implication

If a component is:

* vague
* implicit
* generic
* partially expressed

→ it MUST be treated as **defective**, not as compliant.

---

### Examples

| Case                                       | Evaluation                     |
| ------------------------------------------ | ------------------------------ |
| "The issue remains insufficiently studied" | NOT a valid research gap       |
| "The goal is to study…"                    | NOT a valid research objective |
| "Recommendations are proposed"             | NOT a valid scientific result  |

---

## 13. Intended Use Cases

This standard is designed for:

* AI-assisted dissertation diagnostics
* automated pre-screening systems
* methodological training of graduate students
* supervisory review support
* structured academic peer review

---

### Important clarification

The standard is **diagnostic**, not descriptive.

Its purpose is:

* to detect defects
* to expose methodological weaknesses
* to support correction and improvement

---

## 14. Key Insight

A dissertation introduction must function as a **compressed and self-sufficient research specification**.

---

### Diagnostic criterion

A valid introduction must allow reconstruction of the full research logic:

```
Problem  
→ State of knowledge  
→ Gap  
→ Goal  
→ Tasks  
→ Methods  
→ Results (Scientific Novelty)  
→ Significance  
→ Validation
```

---

### Minimal evaluability test

A reader must be able to answer:

1. Why is the problem important?
2. What is known?
3. What is unresolved?
4. What is the research objective?
5. How will the research be conducted?
6. What new knowledge is produced?

---

### Failure condition

If any of these questions cannot be answered **clearly and directly from the text**:

→ the introduction is methodologically defective.

---

### Critical extension

```
If novelty is not reconstructible → results are undefined  
If results are undefined → significance is invalid  
If significance is invalid → contribution is unsubstantiated
```

---

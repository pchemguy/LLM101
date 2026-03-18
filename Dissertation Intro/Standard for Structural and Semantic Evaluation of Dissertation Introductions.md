---
URLs:
  - https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b7d46f-ae38-8385-9871-d556a66c88dd
  - https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b902d2-a2c8-838b-a60d-4e863e60bc7c
---
# Standard for Structural and Semantic Evaluation of Dissertation Introductions

---

## 1. Purpose

This document defines a normative analytical standard for assessing the methodological quality and structural completeness of dissertation introductions in the context of Russian dissertation practice and VAK-regulated specialty alignment. The standard is designed specifically for use with **large language models (LLMs)** performing structured critical analysis.

The standard supports:

* systematic evaluation of dissertation introductions
* consistent identification of methodological deficiencies
* structured comparison across dissertations
* reproducible evaluation results

This standard does not define

- scoring scale
- evaluation protocol
- output format.
 
These components belong in a companion "protocol" document.

The standard is compatible with the structural requirements of **ГОСТ Р 7.0.11 — Диссертация и автореферат диссертации. Структура и правила оформления.**

---

## 2. Mandatory Structural Requirements

Section **5.3.1 of GOST Р 7.0.11** specifies that the introduction must contain the following key components:

|                                               |                                    |
| --------------------------------------------- | ---------------------------------- |
| актуальность темы исследования                | relevance                          |
| степень разработанности проблемы              | degree of development              |
| цели и задачи исследования                    | goals and tasks                    |
| научная новизна                               | scientific novelty                 |
| теоретическая и практическая значимость       | theoretical/practical significance |
| методология и методы исследования             | methodology and methods            |
| положения, выносимые на защиту                | provisions for defense             |
| степень достоверности и апробация результатов | reliability and approbation        |

These elements constitute the **minimum mandatory structure**.

However, Russian dissertation practice typically contains additional sections, which must also be evaluated when present.

## 3. Specialty Alignment Requirements

Any dissertation defended in Russia must generally comply with regulations developed by VAK. Among those regulations is the requirement that every dissertation must

- formally declare its specialty classification and
- substantively comply with scope/domain defined by the VAK passport of the declared specialty, according to `Specialty Alignment Criteria` (SA#).

---

## 4. Extended Analytical Structure

In practice, the introduction usually includes the following extended elements:

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

The evaluation must consider both:

* **ГОСТ-required components**
* **extended methodological components**

---

## 5. Core Research Logic

The introduction must instantiate the following research logic as an ordered semantic structure. The following chain represents a semantic dependency structure rather than a mandatory textual order of presentation.

```
Problem  
→ State of knowledge  
→ Gap  
→ Object  
→ Subject  
→ Goal  
→ Tasks  
→ Methods  
→ Novelty  
→ Significance  
→ Validation
```

Failure of this chain indicates **methodological weakness**.

In addition to the ordered semantic chain, the following dependency constraints must hold.

```
Problem
  ↓
State of knowledge
  ↓
Gap
  ↓
Goal
  ↓
Tasks
  ↓
Methods
  ↓
Results (Scientific Novelty)
  ↓
Significance
  ↓
Validation

Object → Subject (containment constraint)
Novelty → Provisions for Defense (transformation constraint)
```

Each node must:

1. be explicitly identifiable
2. be logically derived from its predecessor(s)

Violation of dependencies results in:

* logical defect classification
* downgrade in corresponding `Logical Consistency` (LC) criteria (described below)

---

## 6. Evaluation Dimensions

The introduction must be evaluated across the following dimensions.

| Dimension                      | Description                                                                            |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| Structural completeness        | presence and explicitness of required (GOST) and extended components                   |
| Research problem justification | clarity and validity of problem relevance (актуальность)                               |
| Literature positioning         | adequacy of synthesis of prior research and support for gap identification             |
| Research design coherence      | internal consistency of gap–goal–tasks–object–subject relationships                    |
| Methodological adequacy        | alignment of methods with stated tasks and research design                             |
| Scientific novelty             | clarity, specificity, and credibility of claimed scientific results                    |
| Significance justification     | explicit and logical derivation of theoretical and practical significance from novelty |
| Provisions for defense quality | validity of claims derived from novelty; clarity, testability, and non-duplication     |
| Validation and dissemination   | credibility of results through approbation, publications, and verification             |
| Specialty alignment            | consistency of topic, object, subject, methods, and results with VAK passport          |

---

## 7. Evidence Requirement

For each evaluation decision, the evaluator must provide direct textual evidence (quotes). Paraphrasing alone is not sufficient.

Each finding must include:

1. identification of relevant passage
2. explanation of evaluation
3. evaluative conclusion

Example format:

```
Criterion: Research Gap

Evidence:
"Несмотря на значительное количество исследований..."

Assessment:
The sentence identifies unresolved issues but does not specify
the exact scientific problem.

Score: 1
```

---

## 8. Structural Completeness Criteria (SC)

### SC1 — Required GOST components

The introduction must include all components defined in the `GOST Р 7.0.11` section above.  
Absence of any of these is a **major structural defect**.

---

### SC2 — Extended structural elements

Additional components (defined in `Extended Analytical Structure`) are not universally mandatory, but their absence typically reduces analytical clarity and should be evaluated as a defect unless their function is clearly fulfilled elsewhere in the text.

---

## 9. Specialty Alignment Criteria (SA)

Each specialty alignment criterion must be evaluated through explicit mapping between dissertation introduction components and corresponding elements of the specialty passport.

### SA1 — Topic–Specialty Alignment

Does the research topic fall within the specialty domain?

---

### SA2 — Object/Subject–Specialty Alignment

Do object and subject correspond to:

* object of specialty
* subject of specialty

---

### SA3 — Methods–Specialty Alignment

Are methods appropriate for the specialty domain?

---

### SA4 — Novelty–Specialty Alignment

Does the claimed scientific novelty belong to the specialty?

---

### SA5 — Passport justification quality

If a "соответствие специальности" section exists:

* is it substantive or declarative?

---

### SA6 — Research Gap–Specialty Alignment

Does the identified research gap belong to the specialty?

---

### Critical Rule

 If any core component falls outside the specialty domain, this constitutes a **critical defect of misalignment**.

---

## 10. Logical Consistency Criteria (LC)

### LC1 — Problem–Gap Consistency

The research gap must logically follow from the state of knowledge as presented in the introduction.

Failure indicates weak problem definition.

---

### LC2 — Gap–Goal Consistency

The research goal must directly address the research gap.

---

### LC3 — Goal–Task Consistency

```
Tasks must collectively achieve the research goal.
```

Tasks unrelated to the goal indicate design errors.

---

### LC4 — Object–Subject Consistency

```
Subject ⊂ Object
```

The subject must represent a specific aspect of the object.

---

### LC5 — Tasks–Methods Consistency

Methods must allow the solution of the stated tasks.

---

### LC6 — Goal–Novelty Consistency

Scientific novelty must correspond to the research objective.

---

### LC7 — Novelty–Significance Consistency

Theoretical and practical significance must be logically and explicitly derived from the scientific novelty.

1. Each significance statement must reference:
    * a specific novelty item
2. Each novelty item must support:
    * at least one articulated statement of significance (theoretical or practical).

**Violations**:

| Violation                   | Interpretation |
| --------------------------- | -------------- |
| significance without result | invalid        |
| result without significance | incomplete     |
| generic significance        | weak           |


If the novelty does not contain specific, identifiable, and explicitly linked results, the significance is considered unsubstantiated and must be evaluated as weak or invalid.  

---

### LC8 — Novelty–Provisions for Defense Consistency

Provisions for defense must be logically derived from the scientific novelty. Scientific novelty describes the obtained results, while provisions for defense formulate explicit claims about these results.

Each provision must:

* be based on a specific novelty item
* express a defendable statement (not merely restate the result)

**Evaluation Questions**

1. Does each provision correspond to a novelty item?
2. Does it express a **claim**, not a description?
3. Is there transformation (result → statement)?

**Practical Heuristic**

For each provision:

Ask:

```
Can this statement be derived from claimed results, argued, challenged, and tested?
```

If **no**:

→ not a valid provision

**Typical Defects**

| Category             | Symptom                                            | Interpretation                                    |
| -------------------- | -------------------------------------------------- | ------------------------------------------------- |
| Duplication          | Same text appears in both sections.                | Indicates no transformation                       |
| Independence         | Provisions introduce ideas not present in novelty. | Logical inconsistency                             |
| Missing provisions   | Novelty exists, but no formal claims.              | Weak defensibility                                |
| Non-claim provisions | "Разработана методика…"                            | This is NOT a provision — this is still a result. |

---

## 11. Results Criteria (RC)

### RC1 — Novelty

Each novelty statement must represent a distinct, concrete scientific result, which is sufficiently defined to support explicit theoretical and/or practical significance.

A valid novelty item must be:

- ✔ Specific
    - Not: "the concept is clarified"
    - But: *what exactly is clarified, how, and with what consequence*
- ✔ Self-contained
  It must stand as an independent contribution:
    * method
    * model
    * framework
    * classification
    * empirical finding
    * mechanism
- ✔ Independently verifiable
  There must be a way to:
    * apply it
    * test it
    * interpret it

Each item should typically include:

```
Result:
[what is created/discovered]

Mechanism:
[how it works / what is new]

Implication:
[why it matters]
```

Typical acceptable novelty categories:

* conceptual clarification
* methodological development
* systematization of factors
* empirical findings

Generic statements without explicit contributions receive low scores.

"Developed recommendations" is a novelty result often included in certain applied fields. In fact, recommendations may be a valid result of dissertation work and may be even a useful one, BUT recommendations rarely can be considered a valid item to be included as a scientific novelty item. Recommendations are a type of primary result of consulting projects. Unless recommendations have a clear demonstrated general nature, have been scientifically and rigorously validated in the course of dissertation research, and have demonstrated GENERAL significance, such a result is usually a typical low quality item used to inflate the novelty section.

Each novelty item must be evaluated individually for:

* specificity
* independence
* ability to support significance

If a novelty item cannot produce:
   
* theoretical implication, OR
* practical application
  
  it is likely:
  
* trivial
* descriptive
* pseudo-novelty

If a novelty statement does not support meaningful articulated significance, it must be considered weak or invalid:

- either sound explicit significance must be added OR
- such result should be removed from the novelty section.

For each novelty item (stated result / contribution), answer:

1. What exactly is the result?
2. What changes because of it?
3. Can I derive significance from it?

If any answer is unclear:

→ mark as **defect**, providing specific argument(s) for such a decision.

---

### RC2 — Validation and Approbation

The introduction must demonstrate:

* presentation of results at conferences
* discussion in academic community
* publications
* implementation or testing (when applicable)

---

### RC3 — Inflation and Substantive Quality of Novelty and Significance

This criterion is strongly linked to analysis `LC7 — Novelty–Significance Consistency` and `RC1 — Novelty`. Its purpose is to assess the overall quality of scientific novelty and significance sections (each should get a separate score).

Evaluate:

1. Number of novelty/significance items (within each group independently)
2. Their independence
3. Their substance

**Defect patterns**:

| Pattern         | Meaning                 |
| --------------- | ----------------------- |
| many weak items | inflation               |
| few but strong  | acceptable              |
| mixed           | flag for further review |

---

## 12. Defect Severity Classification

Defect severity must be assigned with reference to the criterion affected and the degree to which the defect undermines the coherence, defensibility, or disciplinary admissibility of the dissertation introduction.

| Severity     | Description                                |
| ------------ | ------------------------------------------ |
| **Critical** | fundamental methodological flaw            |
| **Major**    | serious weakness affecting research design |
| **Moderate** | noticeable but non-fatal issue             |
| **Minor**    | stylistic or structural imperfection       |

---

### Critical defects

Examples:

* no research gap
* no research objective
* no scientific novelty
* specialty mismatch

---

### Major defects

Examples:

* tasks unrelated to goal
* subject not part of object
* novelty unrelated to objective
* logical inconsistencies
* weak novelty
* poor alignment

---

### Moderate defects

Examples:

* vague problem justification
* weak literature synthesis
* incomplete validation section

---

### Minor defects

Examples:

* stylistic redundancy
* overly generic significance statements

---

## 13. Anti-Inference Rule

The evaluator must follow the following rule:

> Elements must not be inferred unless they are explicitly or clearly implicitly present in the text.

Generic statements must not be interpreted as fulfilling methodological requirements unless they explicitly perform the required function.

---

## 14. Intended Use Cases

This standard is designed for:

* AI-assisted dissertation review
* automated pre-screening of dissertations
* methodological training of graduate students
* supervisor support tools
* structured academic peer review

---

## 15. Key Insight

A dissertation introduction is effectively a **compressed research specification**.

If the introduction is well structured, a reader should be able to answer the following questions quickly:

1. Why is the research problem important?
2. What is already known?
3. What remains unresolved?
4. What does the dissertation aim to achieve?
5. How will the research be conducted?
6. What new knowledge is produced?

If these questions cannot be answered clearly, the introduction is methodologically weak.

---

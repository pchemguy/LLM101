# PROTOCOL

## Protocol for Structural, Semantic, and Specialty Alignment Evaluation of Dissertation Introductions

---

### 0. Role and Evaluation Stance

You are acting as a **methodological expert performing a strict diagnostic audit** of a dissertation introduction.

Your task is:

* **NOT** to praise
* **NOT** to summarize superficially
* **BUT** to identify **methodological defects, logical inconsistencies, structural weaknesses, ambiguities, and disciplinary misalignment**

Your stance must be:

* analytical
* critical
* diagnostic

Ambiguity, vagueness, or generic academic phrasing MUST be treated as **defects**.

---

### 1. Required Input Documents (MANDATORY PRE-CHECK)

Before performing any evaluation, you MUST verify that the following three documents are available within your context:

#### Required documents

1. **Evaluation Standard**
   [Standard for Structural and Semantic Evaluation of Dissertation Introductions](Standard%20for%20Structural%20and%20Semantic%20Evaluation%20of%20Dissertation%20Introductions.md)
2. **VAK Specialty Passport**
   *(паспорт специальности ВАК)*
3. **Dissertation Introduction Text**

---

#### Accepted ways documents may be provided

* embedded in the prompt
* attached files
* earlier messages in the conversation

---

#### Validation Rule (STRICT)

You MUST:

* explicitly confirm presence of all three documents
* identify each document actually available in context

If **ANY** required document is missing:

* STOP the evaluation immediately
* output only the following block:

```text
EVALUATION ABORTED

Missing required documents:
[list]

The protocol requires all three inputs:
1. Evaluation Standard
2. VAK Specialty Passport
3. Dissertation Introduction
```

Do **NOT** continue with any analytical stages.

---

### 2. Normative Basis

You MUST use the provided **Evaluation Standard** as the primary normative reference.

You MUST NOT:

* invent criteria outside the standard, except where this protocol explicitly operationalizes **specialty alignment**
* infer missing elements
* treat generic academic phrasing as methodological compliance

---

### 3. Core Evaluation Principle

The introduction must be treated as a **compressed research specification**.

You must reconstruct and evaluate the following **semantic dependency chain**:

```text
Problem → State of knowledge → Gap → Object → Subject → Goal → Tasks → Methods → Novelty → Significance → Validation
```

Additional dependency constraints:

```text
Object → Subject
Novelty → Provisions for Defense
```

#### Interpretation Rule

This chain represents a **semantic dependency structure**, not a mandatory textual order of presentation.

The state of knowledge must synthesize prior research and explicitly support identification of the research gap.

A valid research gap is:

> a clearly formulated unresolved scientific problem (basic or applied)

Not acceptable:

* “insufficient research exists”
* generic statements of relevance
* vague claims of complexity

If the gap is not explicitly defined, this MUST be recorded as a **defect**.

---

### 4. Evaluation Procedure

You MUST follow all stages in order.

---

#### **Stage 0 — Analytical Summary (Sanity Check)**

Reconstruct, in your own words and strictly from the provided introduction text:

* research problem
* research gap
* research goal
* claimed scientific novelty

##### Rule

If any of these cannot be clearly reconstructed:

→ this is evidence of **methodological opacity**
→ it MUST be recorded as a defect

---

#### **Stage 1 — Structural Extraction (SC)**

Identify all structural components present in the introduction.

Check both:

* **SC1** — GOST-required components
* **SC2** — extended methodological components

List:

* detected sections
* missing elements

This stage is **extractive only**.
Do not yet assign final adequacy judgments beyond basic presence/absence notes.

---

#### **Stage 2 — Structural Compliance Check (SC)**

For each required and extended structural component:

* locate evidence in the text
* quote the relevant passage (**mandatory**)
* determine whether the component is:
    * present
    * missing
    * present but weak
    * present and adequate
* evaluate whether its methodological function is actually fulfilled

This stage must explicitly cover:

* all GOST-required elements (SC1)
* all extended structural elements relevant to SC2

---

#### **Stage 3 — Specialty Alignment Analysis (SA)**

You MUST evaluate alignment between the dissertation introduction and the VAK specialty passport for each **SA1–SA6** criterion.

##### Step 1 — Extract passport structure

Identify, if present:

* formula of specialty
* object of specialty
* subject of specialty
* areas / branches / subdivisions
* methodological scope

##### Step 2 — Extract dissertation alignment elements from the introduction

Identify:

* research topic
* research gap
* object
* subject
* methods
* novelty / results
* declared specialty (if present)

##### Step 3 — Perform explicit mapping

For each relevant dissertation component, you MUST:

* map it against the corresponding specialty passport component
* cite the relevant passport fragment
* cite the relevant introduction fragment
* assess and score compliance under SA1–SA6

If a relevant passport component is absent, evaluate alignment using only available passport elements and explicitly record this as a **limitation of specialty analysis**, not as automatic non-compliance.

---

#### **Stage 4 — Research Logic Analysis (LC)**

Evaluate logical consistency for each **LC1–LC8** criterion.

For each criterion, you MUST:

* identify the relevant linked components
* quote the relevant passage(s) (**mandatory**)
* explain whether the dependency is:
    * explicit and valid
    * implicit but acceptable
    * weak
    * broken
* identify the corresponding defect if the dependency fails

This stage must explicitly cover:

* LC1 — Problem → Gap
* LC2 — Gap → Goal
* LC3 — Goal → Tasks
* LC4 — Object ⊃ Subject
* LC5 — Tasks → Methods
* LC6 — Goal → Novelty
* LC7 — Novelty → Significance
* LC8 — Novelty → Provisions for Defense

---

#### **Stage 5 — Results Analysis (RC)**

This stage analyzes the quality of the claimed scientific results and related sections.

Theoretical and practical significance must be logically derived from scientific novelty. Provisions for defense must be treated as **derived claims**, not as novelty items.

##### Evaluation Procedure

1. Identify all statements of **scientific novelty**
2. Separate them into distinct claimed **results**
3. Identify all statements of:
    * theoretical significance
    * practical significance
4. Identify any **provisions for defense**, if present
5. Evaluate:
    * whether novelty items are specific and defensible
    * whether significance is explicitly derived from novelty
    * whether provisions for defense are transformed claims rather than duplicated results
6. Complete checks for:
    * **RC1** — Scientific Novelty
    * **RC2** — Validation and Approbation
    * **RC3** — Inflation and Substantive Quality of Novelty and Significance
    * **RC4** — Ordering and Priority of Results
    * **RC5** — Internal Structure of a Novelty Item

##### Typical weak novelty items

* **Definitions without consequence**
  e.g. “An author’s definition is proposed…”
  If it does not:

    * change interpretation
    * enable modeling
    * improve analysis
  
  → not a real result
* **Literature summaries**
  e.g. “Trends are generalized…”
  → review, not novelty
* **Factor listings**
  e.g. “Factors are identified…”
  without:

    * model
    * structure
    * causal logic

  → weak result
* **Recommendations without method**
  e.g. “Recommendations are proposed…”
  → applied commentary, not scientific result

##### Critical Rule

If scientific novelty does not contain **specific results**, significance MUST be downgraded.

---

#### **Stage 6 — Defect Identification**

Classify all detected defects according to the **Defect Severity Classification** defined in the standard.

Each defect must be linked to:

* the affected criterion or criteria
* the relevant evidence
* its severity level:
    * Critical
    * Major
    * Moderate
    * Minor

---

#### **Stage 7 — Coverage Consistency Check**

Before producing the final summary, verify that the evaluation is complete.

You MUST confirm that:

* all required GOST components have been analyzed
* all relevant extended structural elements have been considered
* all SA1–SA6 criteria have been addressed
* all LC1–LC8 criteria have been addressed
* all novelty items have been analyzed
* all significance statements have been analyzed
* all provisions for defense have been mapped to novelty, if present
* all RC1–RC3 criteria have been addressed
* all scores are supported by explicit evidence

If any part of this coverage is incomplete, state the incompleteness explicitly.

---

#### **Stage 8 — Diagnostic Summary**

Provide a final diagnostic summary covering:

1. methodological soundness
2. structural completeness
3. research design quality
4. credibility of results
5. specialty alignment adequacy

#### Revision Priorities

List the most important corrections required to bring the introduction to a methodologically strong standard.

---

### 5. Criterion Scoring

The scoring scale is universal across all criteria (**SC, SA, LC, RC**), but each score must be interpreted relative to the **analytical nature of the criterion**.

| Score | SC (Structure)                    | SA (Specialty)                | LC (Logic)                  | RC (Results)                        |
| ----- | --------------------------------- | ----------------------------- | --------------------------- | ----------------------------------- |
| **0** | missing                           | outside specialty             | no logical connection       | no real result                      |
| **1** | present but poorly defined        | weak or indirect fit          | weak / implicit / broken    | vague / generic / non-scientific    |
| **2** | present and adequate              | acceptable alignment          | mostly consistent           | partially valid result              |
| **3** | clearly and explicitly structured | strong and explicit alignment | explicit and well-justified | clear, specific, defensible results |

Each score MUST include:

* evidence
* explanation

---

### 6. Anti-Inference Rule

You MUST NOT:

* assume missing elements
* interpret generic wording as compliance
* reconstruct intended meaning beyond textual evidence

If an element is vague, generic, implicit, or only partially expressed, it must be treated as **defective**, not as compliant.

---

### 7. Output Format (STRICT, IN RUSSIAN)

If any required input document is missing, output only the predefined `EVALUATION ABORTED` block and do not proceed further.

Otherwise, the report MUST follow this structure:

```
# КРИТИЧЕСКИЙ АНАЛИЗ ВВЕДЕНИЯ ДИССЕРТАЦИИ

Данный анализ рассматривает введение диссертации как сжатую и формализуемую спецификацию исследования, в которой должны быть явно представлены ключевые элементы научной работы: проблема, степень ее разработанности, исследовательский разрыв, цель и задачи, методы, научная новизна и значимость результатов. Основная задача анализа — выявить структурные дефекты, логические несоответствия, методологические слабости и возможное несоответствие специальности. Принципиально важно, что анализ проводится в критическом режиме: любые неясности, обобщенные или двусмысленные формулировки не интерпретируются в пользу автора и рассматриваются как дефекты. Элементы не допускается домысливать; их наличие и функция должны быть выражены явно.

Оценка выполняется по четырем группам критериев: полнота структуры (SC), соответствие специальности (SA), логическая согласованность (LC) и качество научной новизны и значимости (RC). Введение должно образовывать непротиворечивую логическую цепочку от постановки проблемы к формулировке результатов и их значимости. Особое внимание уделяется тому, что научная новизна должна быть представлена в виде конкретных, идентифицируемых результатов, а значимость — логически выведена из этих результатов, а не заявлена декларативно. Все выявленные дефекты классифицируются по степени серьезности от критических до незначительных, а оценка по каждому критерию производится по шкале от 0 до 3, отражающей степень полноты и корректности выполнения. Если введение не позволяет однозначно реконструировать логику исследования и проверить его элементы по данным критериям, оно рассматривается как методологически слабое независимо от объема и стилистического качества текста.

## СТРУКТУРНЫЙ АНАЛИЗ [SC]

[обнаруженные разделы]
[отсутствующие элементы]

### ПРОВЕРКА СООТВЕТСТВИЯ ГОСТ [SC1]

[анализ по каждому элементу]
SC1 (Обязательные элементы ГОСТ):

### РАСШИРЕННЫЙ СТРУКТУРНЫЙ АНАЛИЗ [SC2]

[анализ по каждому элементу]
SC2 (Расширенная структура):

## ПРОВЕРКА СООТВЕТСТВИЯ ПАСПОРТУ СПЕЦИАЛЬНОСТИ [SA]

[анализ по каждому элементу]
SA1 (Тема ↔ Специальность):
SA2 (Объект/Предмет ↔ Специальность):
SA3 (Методы ↔ Специальность):
SA4 (Научная новизна ↔ Специальность):
SA5 (Обоснование соответствия специальности):
SA6 (Исследовательский пробел ↔ Специальность):

## АНАЛИЗ ЛОГИКИ ИССЛЕДОВАНИЯ [LC]

[разбор связей]
LC1 (Проблема → Исследовательский пробел):
LC2 (Исследовательский пробел → Цель):
LC3 (Цель ↔ Задачи):
LC4 (Объект ⊃ Предмет):
LC5 (Задачи ↔ Методы):
LC6 (Цель ↔ Научная новизна):
LC7 (Научная новизна ↔ Значимость):
LC8 (Научная новизна ↔ Положения на защиту):

## АНАЛИЗ РЕЗУЛЬТАТОВ [RC]

[анализ по каждому результату]
RC1 (Научная новизна):
RC2 (Достоверность и апробация / валидация):
RC3 (Инфляция и содержательное качество научной новизны и значимости):
RC4 (Порядок / приоритизация результатов):
RC5 (Внутренняя структура результатов):

## КРИТИЧЕСКИЕ ДЕФЕКТЫ

[список]

## СУЩЕСТВЕННЫЕ ДЕФЕКТЫ

[список]

## УМЕРЕННЫЕ ДЕФЕКТЫ

[список]

## НЕЗНАЧИТЕЛЬНЫЕ ДЕФЕКТЫ

[список]

## ИТОГОВАЯ ДИАГНОСТИЧЕСКАЯ ОЦЕНКА

[вывод]

## ПРИОРИТЕТЫ ДОРАБОТКИ

[список]
```

---

### 8. Evidence Traceability Requirement (MANDATORY)

For every identified component, analytical claim, and score, you MUST provide explicit textual evidence.

#### Mandatory requirements

1. Use a **direct quote**, not paraphrase
2. Quote must be **minimally sufficient**
3. Evidence must be mapped explicitly to evaluation

Each analytical statement MUST follow this structure:

```text
Элемент: [название компонента]

Фрагмент:
"[точная цитата из текста]"

Анализ:
[объяснение]

Оценка:
[балл]
```

#### Strict Rules

* paraphrasing instead of quoting is NOT allowed
* generic references such as “the author states that…” are NOT allowed
* missing evidence invalidates the evaluation

#### Coverage Requirement

Evidence MUST be provided for:

* all GOST components
* all structural findings
* all specialty alignment checks
* all logical relationships
* all novelty claims
* all scored criteria

#### Missing Element Rule

If a component is absent:

```text
Элемент: [название]

Фрагмент:
[отсутствует]

Анализ:
[объяснение отсутствия]

Оценка:
0
```

#### Ambiguity Rule

If evidence is vague or indirect:

* quote it anyway
* explicitly state why it is insufficient

---

### 9. Prompt Template

```
# PROTOCOL

[PROTOCOL]

---

# EVALUATION STANDARD

[STANDRAD]

---

# SPECIALTY PASSPORT

[PASSPORT]

---

# DISSERTATION INTRODUCTION

[INTRODUCTION]
```

---

### 10. Final Instruction

Your objective is:

> to produce the most diagnostically useful critique possible

You are **not** writing a polite review.  
You are **not** writing encouragement.  
You are performing a **methodological audit** whose purpose is to expose weaknesses clearly and precisely so they can be corrected.

---


# EVALUATION STANDARD

## Standard for Structural and Semantic Evaluation of Dissertation Introductions

---

### 1. Purpose

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

### 2. Structural Components

#### GOST Р 7.0.11 Required Components

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

#### Extended Analytical Structure

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

### 3. Core Research Logic

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

#### Notes

* Each node must be **explicitly identifiable**.
* Each node must be **logically derived from its predecessor(s)**.
* Violation of any dependency constitutes a **logical defect** and should trigger downgrade in the corresponding **Logical Consistency (LC) criteria**.

**Interpretation**

This chain is **semantic**, not a required textual order.
The actual text of a dissertation may present nodes in a different sequence, but logical dependencies must hold.

---

### 4. Specialty Alignment (VAK Passport)

Dissertations defended in Russia must comply with **VAK regulations**. This standard acknowledges that:

* each dissertation must **formally declare its specialty**
* each dissertation must **substantively align with the VAK specialty passport** for that declared specialty

Specialty alignment is assessed in the **companion protocol**, using explicit mapping between dissertation elements and passport components.

---

### 5. Evaluation Dimensions

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

#### Interpretation Notes

* Each dimension must be evaluated **independently**, but with awareness of **cross-dependencies** defined in the research logic (Section 3).
* Dimensions are **analytically distinct but logically interconnected**.
* Weakness in one dimension (e.g., novelty) may propagate into others (e.g., significance, provisions for defense).

---

### 6. Evidence Requirement

All evaluation decisions must be **explicitly evidence-based**.

Paraphrasing or implicit interpretation is not sufficient.

---

#### Mandatory Evidence Structure

Each evaluative finding must include:

1. **Identification of the evaluated element or criterion**
2. **Direct textual evidence** (minimal sufficient quote)
3. **Analytical explanation**
4. **Evaluative conclusion**

---

#### Example

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

#### Strict Rules

* Evidence MUST be:
    * direct quotation
    * minimally sufficient (no excessive text)
* Generic references (e.g., “the author notes that…”) are NOT acceptable
* Absence of evidence invalidates the evaluation

---

#### Missing Element Rule

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

#### Ambiguity Rule

If a component is present but vague:

* it must still be quoted
* the insufficiency must be explicitly justified

---

#### Important Clarification

This standard defines **evidence requirements and analytical structure only**.

* Scoring is defined in the **protocol**
* Output formatting is defined in the **protocol**

---

### 7. Structural Completeness Criteria (SC)

#### SC1 — Required GOST components

The introduction must include all components defined in the **GOST Р 7.0.11** section above.

Absence of any required component constitutes a **major structural defect**.

---

#### SC2 — Extended structural elements

Additional components (defined in the *Extended Analytical Structure*) are not universally mandatory.

However, their absence typically reduces analytical clarity and must be evaluated as a defect **unless their functional role is clearly fulfilled elsewhere in the text**.

---

### 8. Specialty Alignment Criteria (SA)

Each specialty alignment criterion must be evaluated through **explicit mapping** between dissertation introduction components and corresponding elements of the specialty passport.

---

#### SA1 — Topic–Specialty Alignment

The research topic must fall within the scope of the specialty domain.

---

#### SA2 — Object/Subject–Specialty Alignment

The object and subject must correspond to:

* the object of the specialty
* the subject of the specialty

---

#### SA3 — Methods–Specialty Alignment

The methods must be appropriate for investigating problems within the specialty domain.

---

#### SA4 — Novelty–Specialty Alignment

The claimed scientific novelty (results) must belong to the specialty domain.

---

#### SA5 — Passport justification quality

If a **"соответствие специальности"** section exists:

* it must provide **substantive justification**, not merely declarative statements

---

#### SA6 — Research Gap–Specialty Alignment

The identified research gap must fall within the scope of the specialty.

---

#### Critical Rule

If any **core research component** (topic, gap, object, subject, methods, or results) falls outside the specialty domain:

→ this constitutes a **critical defect of misalignment**

---

### 9. Logical Consistency Criteria (LC)

#### LC1 — Problem–Gap Consistency

The research gap must logically follow from the **state of knowledge** as presented in the introduction.

Failure indicates weak or unsubstantiated problem formulation.

---

#### LC2 — Gap–Goal Consistency

The research goal must directly address the identified research gap.

---

#### LC3 — Goal–Task Consistency

```
Tasks must collectively achieve the research goal.
```

Tasks unrelated to the goal indicate a **defective research design**.

---

#### LC4 — Object–Subject Consistency

```
Subject ⊂ Object
```

The subject must represent a **specific analytical aspect** of the object.

---

#### LC5 — Tasks–Methods Consistency

The selected methods must be capable of solving the stated research tasks.

---

#### LC6 — Goal–Novelty Consistency

Scientific novelty (results) must directly correspond to and fulfill the stated research objective.

---

#### LC7 — Novelty–Significance Consistency

Theoretical and practical significance must be **explicitly and logically derived from scientific novelty**.

**Formal requirements**

1. Each significance statement must reference:
    * a specific novelty item
2. Each novelty item must be associated with:
    * at least one articulated significance statement (theoretical and/or practical)

**Valid linkage**

A valid novelty–significance relationship requires:

* explicit reference (not implicit association)
* logical derivation (not rhetorical assertion)
* non-generic formulation

**Violations**

| Violation                   | Interpretation |
| --------------------------- | -------------- |
| significance without result | invalid        |
| result without significance | incomplete     |
| generic significance        | weak           |

**Critical rule**

If scientific novelty does not contain **specific and identifiable results**, then significance is considered **unsubstantiated**.

**Scope limitation**

LC7 evaluates:

* **linkage between results and significance**

LC7 does **not evaluate**:

* whether the result itself is valid → (RC1)
* whether the novelty block is structurally sound → (RC3)

---

#### LC8 — Novelty–Provisions for Defense Consistency

Provisions for defense must be **derived from scientific novelty**.

Scientific novelty describes results; provisions for defense formulate **defensible claims about those results**.

**Formal Requirements**

Each provision must:

* be based on a specific novelty item
* express a **defendable claim**, not a descriptive statement

**Evaluation Questions**

1. Does each provision correspond to a novelty item?
2. Does it express a claim rather than a result?
3. Is there a clear transformation (result → claim)?

**Practical Heuristic**

For each provision:

```
Can this statement be derived from results, argued, challenged, and tested?
```

If **no** → invalid provision.

**Typical Defects**

| Category             | Symptom                              | Interpretation              |
| -------------------- | ------------------------------------ | --------------------------- |
| Duplication          | Same text appears in both sections   | No transformation           |
| Independence         | New ideas appear only in provisions  | Logical inconsistency       |
| Missing provisions   | Novelty exists, but no formal claims | Weak defensibility          |
| Non-claim provisions | "Разработана методика…"              | Still a result, not a claim |

---

### 10. Results Criteria (RC)

#### RC1 — Scientific Novelty (Results)

Each novelty statement must represent a **distinct, concrete scientific result**.

A statement is not accepted as scientific novelty merely because it appears under a “novelty” heading. Its status must be justified analytically at the level of the individual item.

---

##### Core validity requirement

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

##### Requirements

A valid novelty item must be:

* ✔ **Specific**
* ✔ **Self-contained**
* ✔ **Independently interpretable**
* ✔ **Methodologically identifiable**

---

##### Interpretive definitions

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

##### Recommended structure

```
Result:
[what is created/discovered]

Mechanism:
[what is new / how it works]

Implication:
[why it matters]
```

---

##### Item-level defect patterns

The following patterns indicate weak or invalid novelty at the **individual item level**:

1. Overloaded item
    One statement contains multiple independent results (e.g., definition + typology + factors + method).
    → Reduces clarity and testability.
    
2. Weak novelty language
    Use of verbs such as:
    
    - "обобщены",
    - "рассмотрены",
    - "выявлены",
    - "сформулированы рекомендации"
    
    without additional specification of a scientific result.
    
3. Descriptive systematization
    Ordering or grouping without:
    
    * a new classificatory principle
    * a new structural relation
    * or a new analytical mechanism
    
4. Factor listing without structure
    “Factors identified” without:
    
    * structure
    * ranking
    * model
    * or causal integration
    
5. Review or sectoral analysis presented as novelty
    Generalized trends, industry descriptions, or summaries that do not produce a new analytical result.
    
6. Case description presented as novelty
    Empirical analysis of a specific object without:
    
    * generalization
    * methodological contribution
    * or transferable result
    
7. Recommendations without scientific basis
    Recommendations not grounded in:
    
    * a model
    * a method
    * or a generalized mechanism
    
8. Authorial definition of a broad mature concept
    Definitions that:
    
    * do not resolve a theoretical problem
    * do not enable new analysis
    * do not introduce an operational concept
    
    → typically **pseudo-novelty**
    
9. Scale mismatch
    The novelty operates at a conceptual level inconsistent with the actual research object.

---

##### Evaluation requirement

For each novelty item, the evaluator must determine:

1. What exactly is the result?
2. What type of result is it?
3. Does it contain multiple independent results?
4. What is the comparative basis of novelty?
5. Is it a scientific result, or misclassified material?

If any answer is unclear → classify as **defect**.

---

#### RC2 — Validation and Approbation

The introduction must demonstrate credibility of results through:

* conference presentations
* academic discussion
* publications
* implementation or empirical testing (if applicable)

Absence or weak formulation reduces credibility.

---

#### RC3 — Inflation and Substantive Quality of Novelty and Significance

This criterion evaluates the **novelty and significance sections as a whole**, not individual items.

**Evaluation dimensions**

1. **Number of items**
2. **Independence of items**
3. **Substantive depth of items**
4. **Conceptual purity of sections**

---

##### Block-level defect patterns

1. Inflation
    Large number of weak, vague, or low-substance items.
2. Structural overload
    Systematic presence of **multi-result (overloaded) items** across the block.
3. Mixing of result classes
    The novelty section contains heterogeneous material:
    
    * scientific results
    * literature review elements
    * empirical case descriptions
    * practical recommendations
    
    → indicates **methodological impurity**
4. Substitution of novelty
    Novelty is replaced by:
    
    * analysis
    * usefulness
    * description
    * or general discussion
5. Imbalance
    * many weak items + few meaningful ones
    * or dominance of one weak type (e.g., recommendations)

---

##### Interpretation patterns

| Pattern         | Interpretation               |
| --------------- | ---------------------------- |
| many weak items | artificial inflation         |
| few strong      | acceptable structure         |
| mixed           | requires detailed evaluation |

---

##### Dependency

RC3 must be interpreted in conjunction with:

* **RC1** — to assess validity of individual items
* **LC7** — to assess result–significance linkage

---

##### Scope limitation

RC3 evaluates:

* overall structure and quality of sections

RC3 does **not evaluate**:

* individual item validity → (RC1)
* correctness of significance derivation → (LC7)

---

#### RC4 — Ordering and Priority of Results

This criterion evaluates whether novelty items are arranged in a **descending order of scientific strength and significance**.

**Principle**

Scientific novelty must be presented as a **prioritized set of results**, not as an unordered list.

The strongest and most consequential results must appear first. Secondary, derivative, or weaker results must follow.

**Requirements**

A valid ordering must satisfy:

* Results are arranged from:
    * **highest theoretical / methodological significance** to
    * **lowest (applied, contextual, or auxiliary) significance**
* The ordering must be consistent with:
    * **RC1 (result quality)**
    * **LC7 (result → significance linkage)**
    * **RC3 (absence of inflation)**

**Evaluation logic**

The evaluator must:

1. Rank all novelty items by:
    * conceptual depth (theory > method > application > case)
    * transferability / generality
    * strength of derived significance (LC7)
2. Compare this ranking with the actual order in the text
3. Identify mismatches

**Critical rule**

If ordering does not reflect **actual epistemic weight**, the novelty block is considered **methodologically degraded**, even if individual items are valid.

---

#### RC5 — Internal Structure of a Novelty Item

This criterion evaluates the **compositional correctness of individual novelty statements**.

**Principle**

Each novelty item must be structured as:

> **result → mechanism → implication → (optional support)**

The **result must appear first** before any supporting material.

**Requirements**

A valid novelty item statement must:

* lead with a **clear, identifiable scientific result**
* present that result as the **prominent dominant clause**
* include supporting elements (if any) **only after the result is stated**

**Evaluation logic**

For each novelty item:

1. Identify the **first clause**
2. Determine whether it is:
    * a scientific result (acceptable), or
    * a supporting / descriptive element (defect)
3. Check whether:
    * the result is explicit and dominant
    * supporting material is subordinate and placed after

**Critical rule**

If a novelty item does not begin with a **clearly identifiable result**, it must be classified as **defective regardless of content quality**.

---

### 11. Defect Severity Classification

Defect severity must be assigned with explicit reference to:

1. the **criterion violated** (SC, SA, LC, RC), and
2. the **degree to which the defect undermines**:
    * logical coherence
    * methodological validity
    * disciplinary admissibility (specialty alignment)

---

#### Severity Levels

| Severity     | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| **Critical** | fundamental violation invalidating the research specification         |
| **Major**    | structural or logical defect significantly weakening research design  |
| **Moderate** | clear methodological weakness with limited impact on overall validity |
| **Minor**    | local imperfection not affecting core research logic                  |

---

#### Critical defects

Defects that **invalidate the introduction as a research specification**:

* absence of research gap (LC1 failure)
* absence of research objective (LC2 failure)
* absence of scientific novelty (RC1 failure)
* specialty mismatch (SA critical rule violation)
* incoherent research chain (broken dependency graph)

---

#### Major defects

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

#### Moderate defects

Defects that **reduce clarity, precision, or evidential strength**:

* vague or generic problem justification (SC/LC1)
* weak literature synthesis (LC1 support failure)
* implicit or weakly stated research gap
* incomplete validation/approbation (RC2)
* partial or inconsistent significance derivation (LC7 partial failure)

---

#### Minor defects

Defects that **do not affect methodological validity**:

* stylistic redundancy
* terminological inconsistency
* overly generic wording (without logical consequences)
* minor structural omissions (SC2)

---

#### Severity Assignment Rule (IMPORTANT)

Severity MUST be determined by **impact on the dependency graph**:

```
If defect breaks the chain → Critical
If defect distorts the chain → Major
If defect weakens interpretation → Moderate
If defect is local → Minor
```

---

### 12. Anti-Inference Rule

The evaluator must strictly adhere to the following rule:

> No methodological element may be assumed unless it is explicitly or unambiguously expressed in the text.

---

#### Formal constraints

The evaluator MUST NOT:

* infer missing components
* interpret generic statements as fulfilling formal requirements
* reconstruct intended meaning beyond textual evidence

---

#### Operational implication

If a component is:

* vague
* implicit
* generic
* partially expressed

→ it MUST be treated as **defective**, not as compliant.

---

#### Examples

| Case                                       | Evaluation                     |
| ------------------------------------------ | ------------------------------ |
| "The issue remains insufficiently studied" | NOT a valid research gap       |
| "The goal is to study…"                    | NOT a valid research objective |
| "Recommendations are proposed"             | NOT a valid scientific result  |

---

### 13. Intended Use Cases

This standard is designed for:

* AI-assisted dissertation diagnostics
* automated pre-screening systems
* methodological training of graduate students
* supervisory review support
* structured academic peer review

---

#### Important clarification

The standard is **diagnostic**, not descriptive.

Its purpose is:

* to detect defects
* to expose methodological weaknesses
* to support correction and improvement

---

### 14. Key Insight

A dissertation introduction must function as a **compressed and self-sufficient research specification**.

---

#### Diagnostic criterion

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

#### Minimal evaluability test

A reader must be able to answer:

1. Why is the problem important?
2. What is known?
3. What is unresolved?
4. What is the research objective?
5. How will the research be conducted?
6. What new knowledge is produced?

---

#### Failure condition

If any of these questions cannot be answered **clearly and directly from the text**:

→ the introduction is methodologically defective.

---

#### Critical extension

```
If novelty is not reconstructible → results are undefined  
If results are undefined → significance is invalid  
If significance is invalid → contribution is unsubstantiated
```

---


# SPECIALTY PASSPORT

## Паспорт специальности ВАК - 08.00.05 - Экономика и управление народным хозяйством (экономика, организация и управление предприятиями, отраслями, комплексами - промышленность)

- **Шифр специальности**: 08.00.05
- **Название специальности**: Экономика и управление народным хозяйством
- **Формула специальности**:
    - В рамках данной специальности исследуются экономические системы, их генезис, формирование, развитие, прогнозирование.
    - Разграничительным признаком специальности 08.00.05 по отношению к другим экономическим специальностям, и в частности 08.00.01 – Экономическая теория, является изучение экономических систем в качестве объектов управления.
- **Объект исследования**:
    - могут служить экономические системы различного масштаба, уровня, сфер действия, форм собственности.
    - национальные, отраслевые, региональные и отдельные экономические системы, сложившиеся и формирующиеся в результате институциональных преобразований в первичных и агрегированных звеньях промышленности (предприятия, хозяйственные ассоциации,
    - финансово-промышленные объединения топливно-энергетического, машиностроительного, металлургического и др. комплексов народного хозяйства).
- **Компоненты специальности 08.00.05**:
    - теоретические и методологические принципы, методы и способы управления этими системами, а также институциональные и инфраструктурные аспекты развития экономических систем. 
    - различные аспекты изучения субъектов управления экономическими системами (государственные, транснациональные, региональные, корпоративные управленческие структуры, а также менеджеры как субъекты управления).
- **Предмет исследования специальности**: являются управленческие отношения, возникающие в процессе формирования, развития (стабилизации) и разрушения экономических систем.
- **Область исследований:**
    - Экономика, организация и управление предприятиями, отраслями, комплексами - Промышленность.
    - Экономические отношения, возникающие в процессе развития народного хозяйства; методы, механизмы, инструменты и технологии функционирования экономических систем и институциональных преобразований в условиях рыночной экономики с учетом тенденций глобализации экономических процессов в отраслях промышленности.
- **Подразделы**:

| Код    | Название                                                                                                                                                                                                                        |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.1.1  | Разработка новых и адаптация существующих методов, механизмов и инструментов функционирования экономики, организации и управления хозяйственными образованиями в промышленности.                                                |
| 1.1.2  | Формирование механизмов устойчивого развития экономики промышленных отраслей, комплексов, предприятий.                                                                                                                          |
| 1.1.3  | Механизмы формирования корпоративных образований в российской экономике с учетом глобализации мировой экономики.                                                                                                                |
| 1.1.4  | Инструменты внутрифирменного и стратегического планирования на промышленных предприятиях, отраслях и комплексах.                                                                                                                |
| 1.1.5  | Гармонизация промышленной и торговой политики с учетом экономической безопасности.                                                                                                                                              |
| 1.1.6  | Государственное управление структурными преобразованиями в народном хозяйстве.                                                                                                                                                  |
| 1.1.7  | Механизмы изменения форм собственности (приватизация, национализация, интеграция, демонополизация и др.) хозяйственных образований.                                                                                             |
| 1.1.8  | Совершенствование организационно-правовых форм хозяйствования в корпоративных образованиях.                                                                                                                                     |
| 1.1.9  | Инструменты функционирования товарных рынков с ограниченной и развитой конкуренцией в условиях глобализации мировой экономики и свободной торговли.                                                                             |
| 1.1.10 | Внешнеторговая деятельность предприятий в условиях либерализации внешнеэкономической деятельности.                                                                                                                              |
| 1.1.11 | Оценки и страхование рисков хозяйствующих субъектов.                                                                                                                                                                            |
| 1.1.12 | Условия и инструменты создания транснациональных корпораций, механизмы их адаптации к российским условиям хозяйствования.                                                                                                       |
| 1.1.13 | Инструменты и методы менеджмента промышленных предприятий, отраслей, комплексов.                                                                                                                                                |
| 1.1.14 | Диверсификация вертикально- и горизонтально-интегрированных хозяйственных структур.                                                                                                                                             |
| 1.1.15 | Теоретические и методологические основы эффективности развития предприятий, отраслей и комплексов народного хозяйства.                                                                                                          |
| 1.1.16 | Промышленная политика на макро- и микроуровне.                                                                                                                                                                                  |
| 1.1.17 | Теоретические и методологические основы мониторинга развития экономических систем народного хозяйства.                                                                                                                          |
| 1.1.18 | Проблемы повышения энергетической безопасности и экономически устойчивого развития ТЭК. Энергоэффективность.                                                                                                                    |
| 1.1.19 | Методологические и методические подходы к решению проблем в области экономики, организации управления отраслями и предприятиями топливно-энергетического комплекса.                                                             |
| 1.1.20 | Состояние и перспективы развития отраслей топливно-энергетического, машиностроительного, металлургического комплексов.                                                                                                          |
| 1.1.21 | Состояние и основные направления инвестиционной политики в топливно-энергетическом, машиностроительном и металлургическом комплексах.                                                                                           |
| 1.1.22 | Методология развития бизнес-процессов и бизнес-планирования в электроэнергетике, нефтегазовой, угольной, металлургической, машиностроительной и других отраслях промышленности.                                                 |
| 1.1.23 | Методологические и методические вопросы прогнозирования топливно-энергетического баланса страны, территориально-административного образования.                                                                                  |
| 1.1.24 | Тарифная политика в отраслях топливно-энергетического комплекса. Методологические и методические подходы к решению проблем в области экономики, организации и управления отраслями и предприятиями металлургического комплекса. |
| 1.1.25 | Методологические и методические подходы к решению проблем в области экономики, организации и управления отраслями и предприятиями машиностроительного комплекса.                                                                |
| 1.1.26 | Теоретические и методические подходы к созданию системы контроллинга в промышленной организации.                                                                                                                                |
| 1.1.27 | Управление производственной программой в различных условиях хозяйствования подразделения организации.                                                                                                                           |
| 1.1.28 | Проблемы реструктуризации отраслей и предприятий промышленности.                                                                                                                                                                |
| 1.1.29 | Методологические проблемы экономики промышленности как науки.                                                                                                                                                                   |



---

# DISSERTATION INTRODUCTION

## Введение

**Актуальность темы исследования**. Объективность и необходимость модернизации российской экономики обусловлены требованиями возрастающего уровня конкуренции и темпов технологического развития стран – лидеров мировой экономики. Модернизация экономики, основанная на формировании высокотехнологичных производственных комплексов и современных систем управления ими, позволяет обеспечить необходимые темпы и качество экономического роста.

Нефтеперерабатывающая промышленность является одной из ключевых сфер российской экономики, нуждающейся в модернизации. Целенаправленная модернизация нефтеперерабатывающей промышленности позволит существенным образом улучшить возможности удовлетворения спроса на высококачественные продукты переработки нефти, повысить устойчивость российской экономики за счет увеличения в выпуске доли продукции с высокой добавленной стоимостью, обеспечить необходимый уровень энергетической безопасности и политического авторитета государства в мире.

В период радикальных экономических реформ в России именно в нефтепереработке наиболее резко сократился объем производства. Основные капиталовложения были направлены на разработку новых месторождений нефти и строительство новых высокозатратных нефтепроводов, что обусловило сырьевую ориентацию нефтяного комплекса при накапливающейся технологической отсталости производств по глубокой переработке углеводородного сырья.

Все это обусловило сохраняющуюся недостаточную глубину переработки нефти и низкое качество выпускаемых нефтепродуктов.

В последнее время правительством РФ принят целый ряд мер, кардинально улучшивших ситуацию в нефтеперерабатывающей промышленности и в нефтепромышленном комплексе в целом. Наблюдается качественный рост инвестиций в модернизацию российской нефтепереработки, существенно улучшилась структура выпускаемой продукции, возросли объемы переработки нефти. Вместе с тем, остаются нерешенными многие вопросы, связанные с выбором оптимальных схем и механизмов модернизации предприятий, созданием благоприятных условий для их реализации.

Направленность на выявление и анализ условий и факторов, стимулирующих технологическую модернизацию нефтеперерабатывающей промышленности и обеспечивающих повышение ее эффективности, определила актуальность настоящего диссертационного исследования.

**Степень разработанности проблемы**. Проблеме модернизации экономики в целом, и промышленных предприятий различных секторов в частности, посвящены работы многих зарубежных и отечественных ученых. Наиболее существенный вклад в развитие данного направления внесли такие ученые, как А. Кляйнкнехт, Г. Менш, Д. Норт, А.И. Пригожин, Хэ Чуаньци, Х. Фримен, Й. Шумпетер, Ш. Эйзенштадт и многие другие.

Заметный вклад в теорию и практику организации и управления процессами модернизации содержится в трудах отечественных экономистов: С.Н. Гаврова, В.Г. Захарова, Ю.И. Ефимычева, В.Л. Иноземцева, Г.Б.Клейнера, Я.И. Кузьминова, Б.Н. Кузыка, Ю.И. Любимцева, А.А. Малыгина, Р.Г. Маниловского, П.М. Павлова, Д.М. Палтеровича, А.И. Татаркина, Ю.Н. Царегородцева, В.А. Штанского, Ю.В. Яковца и др.

При наличии значительного количества исследований, посвященных модернизации промышленных предприятий, нет разработок, комплексно изучающих организационно-экономический механизм модернизации предприятий нефтеперерабатывающей промышленности.

*Недостаточная теоретическая проработанность указанных вопросов и их практическая значимость предопределили цель и задачи диссертационного исследования.*

**Целью диссертационной работы** является обоснование методических подходов и разработка практических рекомендаций по совершенствованию организационно-экономического механизма модернизации предприятий нефтеперерабатывающей промышленности.

Цель исследования предопределила **постановку и решение следующих задач**:

1. Уточнить экономическое содержание понятия «модернизация промышленного предприятия» на основе системного подхода и с учетом условий инновационной экономики.
2. Проанализировать текущее состояние и перспективы развития нефтеперерабатывающей промышленности, выявив ее особенности как объекта модернизации.
3. Разработать методические рекомендации, направленные на совершенствование оценки эффективности модернизации нефтеперерабатывающего предприятия.
4. Проанализировать экономические и организационные аспекты модернизации нефтеперерабатывающего предприятия.
5. Обосновать эффективный организационно-экономический механизм модернизации предприятия нефтеперерабатывающей промышленности.

**Объектом исследования** являются процессы модернизации нефтеперерабатывающих предприятий Российской Федерации.

**Предмет исследования** - экономические и организационные отношения, формирующиеся в процессе модернизации промышленных предприятий.

В качестве **информационно-эмпирической базы исследования** использовались законодательные и нормативно-правовые акты Российской Федерации, материалы Федеральной службы государственной статистики РФ, обзорно-аналитические статьи, опубликованные в периодических изданиях, материалы научно-практических конференций, отчетные данные НК «Роснефть» и ОАО «Ачинский НПЗ».

**Теоретическую и методологическую основу исследования** составляют труды российских и зарубежных ученых в области системной модернизации, инновационного развития и конкурентоспособности предприятий. Для решения поставленных задач в диссертационной работе применялись системный подход, финансово-экономический анализ, а также общенаучные методы (сравнительный метод, метод экспертных оценок, методы группировок и классификаций, индексный метод и др.).

**Соответствие содержания диссертационного исследования избранной специальности**. Область исследования соответствует требованиям паспорта номенклатуры специальностей ВАК по научным направлениям: 08.00.05 – Экономика и управление народным хозяйством (1 – экономика, организация и управление предприятиями, отраслями и комплексами – промышленность): 1.1.19. Методологические и методические подходы к решению проблем в области экономики, организации управления отраслями и предприятиями топливно-энергетического комплекса.

**Научная новизна** диссертационной работы заключается в разработке комплекса теоретических положений, методических подходов и практических рекомендаций по совершенствованию организационно-экономического механизма модернизации предприятий нефтеперерабатывающей промышленности.

**Элементы научной новизны содержатся в следующих результатах**:

- предложено авторское определение термина «модернизация предприятия», систематизированы типы модернизационного развития промышленного предприятия, выявлены определяющие их факторы. Главной отличительной особенностью предложенного определения является рассмотрение модернизации предприятия как интеграционного процесса на основе системных инноваций, обеспечивающего качественное повышение эффективности функционирования предприятия;
- обобщены глобальные тенденции изменений российского рынка продукции нефтепереработки, оказывающие ключевое влияние на условия функционирования и развития нефтеперерабатывающих предприятий, выявлены главные причины низкой конкурентоспособности и основные особенности модернизации отечественных нефтеперерабатывающих предприятий, рассмотрены этапы и приоритетные направления модернизации отрасли;
- обоснован набор критериев и показателей эффективности модернизации нефтеперерабатывающего предприятия; предложена методика и алгоритм оценки эффективности модернизации предприятия на основе многокритериального подхода; определены методы расчета показателя интегральной эффективности модернизации;
- выявлены особенности модернизации ОАО «Ачинский НПЗ» в рамках стратегических направлений развития НК «Роснефть», сделана оценка сравнительной эффективности вариантов модернизации производства; систематизированы отличительные характеристики инновационного обеспечения и риски модернизации предприятия; показана противоречивость и значительное влияние рисков на результативность модернизации;
- сформулированы рекомендации по совершенствованию организационного механизма модернизации предприятия нефтеперерабатывающей промышленности на основе построения и использования «дорожных карт».

**Теоретическая и практическая значимость** диссертационной работы определяется актуальностью изучения выбранной проблемы, теоретически значимыми определениями, предложенными методами и алгоритмами системного анализа модернизации производства на промышленном предприятии, прикладным характером исследования и возможностью использования его результатов.

Теоретические результаты диссертации состоят в развитии теории стратегического управления модернизацией промышленного предприятия, они основаны на обобщении имеющихся подходов к предмету исследования и направлены на повышение эффективности нефтеперерабатывающих предприятий. Практическая значимость диссертационного исследования заключается в системном обосновании теоретико-методологических основ организационно-экономического управления модернизацией предприятий нефтеперерабатывающей промышленности, что позволяет предложить хозяйствующим субъектам эффективные инструменты для разработки и реализации стратегий их модернизации и экономического развития. 

Результаты исследования могут быть использованы:

- при выборе проектов модернизации, направленных на повышение конкурентоспособности предприятия;
- для создания на предприятии системы анализа и управления рисками в целях минимизации их негативного влияния на результаты модернизации;
- при оценке результативности и эффективности проектов модернизации с использованием разработанной методики, основанной на оценке конкурентоспособности предприятия.

**Апробация результатов** диссертационного исследования. Разработанные теоретико-методические положения и практические рекомендации прошли апробацию на промышленных предприятиях (ОАО «Ачинский НПЗ») и внедрены в учебный процесс на экономическом факультете Нижегородского государственного университета им. Н.И. Лобачевского.

Теоретические и практические разработки настоящего диссертационного исследования нашли отражение в научных публикациях. По теме диссертации автором опубликовано 10 научных работ, в том числе 2 научные работы в изданиях, входящих в Перечень ведущих рецензируемых научных журналов и изданий, рекомендованных Высшей аттестационной комиссией Минобрнауки России. Общий объем научных работ составляет 3,75 п.л. (в том числе авторский вклад 3,45 п.л.).

Основные теоретические и практические результаты диссертационной работы докладывались на международных и всероссийских научнопрактических конференциях:

- Всероссийской научно-практической конференции «Российский регион: Управление инновационным развитием в условиях мирового финансового кризиса» (г.Волгоград, 2010 г.);
- IV Всероссийской заочной научно-практической конференции «Проблемы реформирования экономики России» (г.Тверь, 2011 г.);
- Международной научно-практической конференции «Инновационное развитие российской экономики: потенциал и перспективы» (г. Нижний Новгород, 2012 г.);
- VII заочной Международной конференции «Актуальные проблемы и перспективы развития экономики в условиях модернизации» (г. Саратов, 2012 г.);
- IX Международной научно-практической конференции «Инновационная экономика XXI века» (г. Нижний Новгород, 2013 г.);
- Научно-практической конференции студентов и аспирантов экономических специальностей СФУ «Проблемы современной экономики» (г. Красноярск, 2011 г.);
- Всероссийской молодежной конференции «Инновации в экономике, менеджменте и подготовке кадров» (г. Нижний Новгород, 2012 г.).

**Объем и структура диссертации**. Диссертационная работа состоит из введения, трех глав, заключения, списка литературы и приложений. Работа изложена на 212 страницах, содержит 36 рисунков, 28 таблиц и 19 приложений. Список литературы включает 110 наименований.

---

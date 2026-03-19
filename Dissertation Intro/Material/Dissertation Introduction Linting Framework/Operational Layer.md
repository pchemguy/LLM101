---
url: https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b7d46f-ae38-8385-9871-d556a66c88dd
---
# Operational Layer: `intro-lint` / `intro-qa`

## Практически применимый tooling stack для QA-пайплайна введений диссертаций

Ниже — уже не просто концепция, а **операциональный слой**, который можно реально использовать как рабочую систему.
Он состоит из четырех уровней:

1. **CLI-инструмент**
2. **Нормализованные артефакты и схемы**
3. **Режим auto-repair / targeted rewrite**
4. **Acceptance gates и workflow версионирования**

---

### 1. Общая архитектура инструмента

Предлагаю мыслить систему как набор команд вокруг одного инструмента:

```text
intro-qa
```

или, если хотите более “линтерное” имя:

```text
intro-lint
```

Я бы развел их по роли:

* `intro-lint` — быстрый структурно-логический анализ
* `intro-qa` — полный аудит, сравнение версий, repair workflow

---

### 2. Основные команды CLI

#### 2.1. `extract`

Извлекает из введения нормализованную исследовательскую спецификацию.

Пример:

```bash
intro-qa extract inputs/intro_v1.md --out reports/extraction_v1.json
```

Что делает:

* выделяет problem context
* knowledge state
* gap
* goal
* tasks
* object
* subject
* methods
* novelty
* defense propositions
* significance
* reliability
* approbation
* publications
* structure

Это базовый шаг. Без него все остальное менее надежно.

---

#### 2.2. `lint`

Быстрый анализ на дефекты и нарушения структуры.

Пример:

```bash
intro-qa lint inputs/intro_v1.md \
  --standard standards/evaluation_standard.md \
  --taxonomy standards/defect_taxonomy.md \
  --out reports/lint_v1.json
```

Что делает:

* проверяет наличие обязательных элементов
* ищет типовые дефекты
* присваивает defect codes
* выдает severity summary

Это быстрый режим, полезный для первой итерации.

---

#### 2.3. `audit`

Полный методологический аудит.

Пример:

```bash
intro-qa audit inputs/intro_v1.md \
  --standard standards/evaluation_standard.md \
  --taxonomy standards/defect_taxonomy.md \
  --prompt prompts/lint_prompt.md \
  --out reports/audit_v1.json \
  --report-md reports/audit_v1.md
```

Что делает:

* выполняет full extraction
* оценивает по критериям
* проставляет scores
* строит defect map
* формирует приоритеты правки
* выдает итоговый diagnostic verdict

Это основной режим для серьезной проверки.

---

#### 2.4. `compare`

Сравнивает две версии введения через их отчеты.

Пример:

```bash
intro-qa compare reports/audit_v1.json reports/audit_v2.json \
  --out comparisons/v1_v2.json \
  --report-md comparisons/v1_v2.md
```

Что делает:

* показывает resolved defects
* remaining defects
* new defects
* score delta
* regression alerts

Это особенно ценно для итеративной переработки.

---

#### 2.5. `gate`

Проверяет, проходит ли введение acceptance gate.

Пример:

```bash
intro-qa gate reports/audit_v2.json --profile strict
```

Профили могут быть такие:

* `draft`
* `supervisor`
* `pre-defense`
* `strict`

Например, `strict` может означать:

* 0 critical defects
* не более 1 major defect
* LC average ≥ 2
* NOV ≥ 2
* GOST mandatory components all present

---

#### 2.6. `repair-plan`

Строит план адресной переработки.

Пример:

```bash
intro-qa repair-plan reports/audit_v1.json \
  --out reports/repair_plan_v1.md
```

Что делает:

* группирует дефекты по разделам
* ранжирует их по severity
* превращает defect map в actionable rewrite agenda

Это мост между диагностикой и редактированием.

---

#### 2.7. `repair`

Режим auto-repair / targeted rewrite.

Пример:

```bash
intro-qa repair inputs/intro_v1.md \
  --audit reports/audit_v1.json \
  --mode targeted \
  --section "Научная новизна" \
  --out outputs/intro_v1_repaired_novelty.md
```

Что делает:

* переписывает только проблемные секции
* использует defect codes как constraints
* сохраняет остальные части нетронутыми

Это намного лучше, чем просить LLM “перепиши все введение”.

---

### 3. Рекомендуемая структура репозитория

```text
/dissertation_intro_qa/

  /inputs/
    intro_v1.md
    intro_v2.md

  /standards/
    evaluation_standard.md
    defect_taxonomy.md
    acceptance_profiles.yaml

  /prompts/
    extract_prompt.md
    lint_prompt.md
    audit_prompt.md
    repair_prompt.md
    compare_prompt.md

  /schemas/
    extraction_schema.json
    audit_report_schema.json
    comparison_schema.json
    gate_schema.json

  /reports/
    extraction_v1.json
    audit_v1.json
    audit_v1.md

  /comparisons/
    compare_v1_v2.json
    compare_v1_v2.md

  /repair/
    repair_plan_v1.md
    intro_v1_repaired_gap.md
    intro_v1_repaired_novelty.md

  /history/
    defect_trends.json
```

---

### 4. Нормализованные JSON-схемы

#### 4.1. Extraction schema

```json
{
  "problem_context": {
    "text": "",
    "status": "explicit"
  },
  "knowledge_state": {
    "text": "",
    "status": "explicit"
  },
  "research_gap": {
    "text": "",
    "status": "implicit"
  },
  "goal": {
    "text": "",
    "status": "explicit"
  },
  "tasks": [],
  "object": {
    "text": "",
    "status": "explicit"
  },
  "subject": {
    "text": "",
    "status": "explicit"
  },
  "methodology": "",
  "methods": [],
  "database": "",
  "scientific_novelty": [],
  "propositions_for_defense": [],
  "theoretical_significance": "",
  "practical_significance": "",
  "reliability": "",
  "approbation": "",
  "publications": "",
  "dissertation_structure": ""
}
```

Поле `status` должно принимать значения:

* `explicit`
* `implicit_but_clear`
* `vague`
* `absent`

Это очень полезно: можно автоматически снижать credit для неявных элементов.

---

#### 4.2. Audit schema

```json
{
  "metadata": {
    "document_id": "intro_v1",
    "language": "ru",
    "audit_mode": "full",
    "date": "2026-03-19"
  },
  "extraction": {},
  "scores": {
    "SC1": 0,
    "SC2": 0,
    "LC1": 0,
    "LC2": 0,
    "LC3": 0,
    "LC4": 0,
    "LC5": 0,
    "LC6": 0,
    "NV": 0,
    "VAL": 0
  },
  "defects": [
    {
      "code": "GAP-02",
      "severity": "major",
      "section": "Степень разработанности / исследовательский пробел",
      "description": "",
      "evidence": "",
      "recommendation": ""
    }
  ],
  "gost_compliance": {
    "relevance": true,
    "degree_of_development": true,
    "goals_tasks": true,
    "novelty": true,
    "significance": true,
    "methods": true,
    "defense_propositions": false,
    "reliability": false,
    "approbation": true
  },
  "summary": {
    "critical_count": 0,
    "major_count": 0,
    "moderate_count": 0,
    "minor_count": 0,
    "logical_integrity_score": 0.0,
    "overall_verdict": ""
  }
}
```

---

### 5. Acceptance profiles

Очень полезно определить профили приемки.

#### 5.1. `draft`

Для раннего черновика:

* допускаются critical defects
* главное — извлечь структуру и увидеть основные слабые места

#### 5.2. `supervisor`

Для рабочей версии у научрука:

* 0 critical defects
* ≤ 5 major defects
* все ГОСТ-элементы должны быть хотя бы слабо представлены

#### 5.3. `pre-defense`

Перед вынесением текста на более серьезное обсуждение:

* 0 critical
* ≤ 2 major
* LC average ≥ 2
* novelty ≥ 2
* reliability present
* defense propositions present

#### 5.4. `strict`

Максимальный режим:

* 0 critical
* ≤ 1 major
* no GOST violations
* no missing mandatory field
* all core logic links at least adequate
* ambiguity in core blocks minimized

Пример `acceptance_profiles.yaml`:

```yaml
profiles:
  draft:
    max_critical: 99
    max_major: 99

  supervisor:
    max_critical: 0
    max_major: 5
    require_gost:
      - relevance
      - degree_of_development
      - goals_tasks
      - novelty
      - methods

  pre_defense:
    max_critical: 0
    max_major: 2
    min_scores:
      LC1: 2
      LC2: 2
      LC3: 2
      NV: 2
      VAL: 1
    require_gost:
      - relevance
      - degree_of_development
      - goals_tasks
      - novelty
      - significance
      - methods
      - defense_propositions
      - reliability
      - approbation

  strict:
    max_critical: 0
    max_major: 1
    min_scores:
      SC1: 3
      LC1: 2
      LC2: 2
      LC3: 2
      LC4: 2
      LC5: 2
      LC6: 2
      NV: 2
      VAL: 2
```

---

### 6. Repair subsystem

Это самый practically useful слой после аудита.

#### 6.1. Почему нужен не “rewrite all”, а targeted repair

Полная перепись введения часто:

* размывает исходную авторскую структуру
* ломает уже хорошие куски
* создает новый набор дефектов
* маскирует старые проблемы вместо исправления

Поэтому лучше ремонтировать **по секциям**, **по кодам дефектов**, **по severity**.

---

#### 6.2. Repair modes

##### Mode A — section repair

Переписать один раздел:

* Актуальность
* Цель
* Научная новизна
* Достоверность

##### Mode B — defect-driven repair

Переписать только то, что связано с определенными кодами:

* `GAP-*`
* `GOAL-*`
* `NOV-*`

##### Mode C — dependency repair

Исправить логическую связку:

* gap → goal
* goal → tasks
* goal → novelty

Это особенно мощно, потому что многие введения страдают не отсутствием элементов, а **разрывом между ними**.

---

#### 6.3. Repair prompt skeleton

```text
Ты выполняешь не полную перепись введения, а адресную методологическую переработку.

Я предоставлю:
1. исходный текст введения
2. аудиторский отчет
3. список defect codes, которые нужно исправить

Твоя задача:
- исправить только те фрагменты, которые необходимы для устранения указанных дефектов
- сохранить общий смысл и структуру текста, если они не противоречат исправлению
- не вносить произвольные улучшения вне поставленной задачи
- писать по-русски
- устранять не только формальные, но и логические дефекты

Для каждого исправления:
- кратко укажи, какой defect code ты устраняешь
- покажи новый вариант фрагмента
- объясни, почему он лучше в методологическом смысле
```

---

### 7. Delta and regression analysis

Система должна не только фиксировать улучшения, но и ловить регрессии.

#### 7.1. Resolved defects

Были в `v1`, исчезли в `v2`.

#### 7.2. Remaining defects

Были и остались.

#### 7.3. New defects

Появились после переработки.

Это очень важно: часто при исправлении цели ломаются задачи, а при усилении новизны внезапно проявляется несоответствие методам.

---

#### 7.4. Comparison report

Пример markdown-отчета:

```text
### Comparison: intro_v1 → intro_v2

#### Resolved defects
- GAP-02
- GOAL-03
- GOST-07

#### Remaining defects
- TASK-04
- METH-03

#### New defects
- LOG-05

#### Score delta
- LC2: +1
- SC1: +1
- NV: +1

#### Regression warning
The novelty section became more specific, but now no longer clearly follows
from the stated goal, creating LOG-05.
```

---

### 8. Metrics layer

Можно ввести набор полезных метрик.

#### 8.1. Defect density

```text
(total defects / total words) * 1000
```

Показывает “плотность проблем”.

#### 8.2. Core logic integrity

Среднее по:

* LC1
* LC2
* LC3
* LC4
* LC5
* LC6

#### 8.3. GOST compliance rate

```text
present_mandatory_components / total_mandatory_components
```

#### 8.4. Scientific contribution robustness

Можно считать по подмножеству:

* NV score
* LOG-05 absence
* DEF alignment
* REL adequacy

---

### 9. VS Code / editor integration concept

Если идти дальше, то можно сделать очень удобный слой поверх CLI.

#### 9.1. Inline diagnostics

Как у линтера:

* подсветка фрагментов
* рядом defect code
* severity badge

Например:

```text
[MAJOR][GAP-02] Исследовательский пробел подразумевается, но не сформулирован явно.
```

#### 9.2. Quick actions

* “Generate repair for this section”
* “Explain why this is a defect”
* “Show linked defects”
* “Re-run audit”

#### 9.3. Section heatmap

Показывать, какие разделы самые проблемные:

* актуальность — moderate
* gap — critical
* novelty — major
* reliability — absent

---

### 10. Semi-automated rewriting protocol

Очень полезный рабочий режим:

#### Pass 1

Только диагностика.

#### Pass 2

Repair critical defects only.

#### Pass 3

Re-audit.

#### Pass 4

Repair major defects.

#### Pass 5

Re-audit.

#### Pass 6

Polish moderate/minor issues if нужно.

Это намного надежнее, чем единичный “сделай хорошо”.

---

### 11. Suggested acceptance gate document

Можно оформить отдельный нормативный артефакт.

#### `INTRO_ACCEPTANCE_GATES.md`

Пример содержимого:

```text
### INTRO_ACCEPTANCE_GATES

#### Gate 0 — Basic extractability
- Core sections can be identified
- No catastrophic structural collapse

#### Gate 1 — Minimum methodological viability
- Goal exists
- Tasks exist
- Novelty exists
- Gap exists or is at least weakly explicit

#### Gate 2 — GOST compliance
- All mandatory GOST components are present

#### Gate 3 — Logical coherence
- No critical logical defects
- LC average >= 2

#### Gate 4 — Scientific contribution credibility
- Novelty score >= 2
- Defense propositions aligned
- Reliability present

#### Gate 5 — Supervisor-ready quality
- 0 critical defects
- <= 2 major defects
```

---

### 12. Human-in-the-loop model

Несмотря на формализацию, человек все равно нужен как final arbiter.

Лучший режим использования:

LLM делает:

* extraction
* linting
* scoring
* defect coding
* repair suggestions

Человек делает:

* проверку содержательной справедливости критики
* доменную оценку научной состоятельности
* принятие решения о финальной редакции

То есть система должна быть **decision-support**, а не “automatic truth machine”.

---

### 13. Most likely practical bottlenecks

#### 13.1. LLM over-charity

Даже при строгом prompt модель может иногда “засчитывать” слишком слабые элементы.

Лечится:

* anti-inference rule
* evidence requirement
* defect code discipline

#### 13.2. LLM over-severity without calibration

Иногда модель может маркировать как defect почти все подряд.

Лечится:

* четкими scoring anchors
* cross-run comparison
* human validation on first few uses

#### 13.3. Mixed sections in real introductions

Во многих введениях элементы не выделены чисто.

Это не проблема, но нужно явно работать со статусами:

* explicit
* implicit_but_clear
* vague
* absent

---

### 14. Minimal viable implementation path

Если делать это практически, я бы шел так:

##### Phase 1 — Manual operational use

* standard
* taxonomy
* audit prompt
* repair prompt
* markdown/json outputs вручную

##### Phase 2 — Lightweight CLI wrapper

* запуск промптов по шаблону
* сохранение audit reports
* compare reports

##### Phase 3 — Structured project

* schemas
* gates
* metrics
* regression tracking

##### Phase 4 — Editor integration

* VS Code tasks
* inline diagnostics
* repair quick actions

---

### 15. Strongest immediate next artifact

Самый полезный следующий артефакт — это не общая теория, а **готовый пакет файлов**, который можно сразу положить в репозиторий.

Я бы сделал следующий набор:

* `evaluation_standard.md`
* `defect_taxonomy.md`
* `audit_prompt.md`
* `lint_prompt.md`
* `repair_prompt.md`
* `acceptance_profiles.yaml`
* `audit_report_schema.json`
* `comparison_schema.json`
* `INTRO_ACCEPTANCE_GATES.md`
* `README.md`

Именно это уже будет полноценным starter kit.

---

### 16. Final synthesis

Теперь вся система выглядит так:

```text
Introduction text
   ↓
Normalized extraction
   ↓
Lint / audit against standard
   ↓
Defect coding via taxonomy
   ↓
Scoring + severity classification
   ↓
Acceptance gate check
   ↓
Repair plan
   ↓
Targeted rewrite
   ↓
Re-audit
   ↓
Version comparison
```

Это уже действительно похоже на **CI/CD для введения диссертации**:
не “написал и надеешься”, а
**проверил → исправил → перепроверил → сравнил версии → прошел gate**.


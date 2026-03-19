---
url: https://chatgpt.com/g/g-p-69b70421d23c819181e1ced20776eb34-dissertation-analysis/c/69b7d46f-ae38-8385-9871-d556a66c88dd
---

# 1. Структура репозитория

```text
dissertation_intro_qa/
├─ README.md
├─ standards/
│  ├─ evaluation_standard.md
│  ├─ defect_taxonomy.md
│  └─ INTRO_ACCEPTANCE_GATES.md
├─ prompts/
│  ├─ audit_prompt.md
│  ├─ lint_prompt.md
│  ├─ repair_prompt.md
│  └─ compare_prompt.md
├─ configs/
│  └─ acceptance_profiles.yaml
├─ schemas/
│  ├─ extraction_schema.json
│  ├─ audit_report_schema.json
│  └─ comparison_schema.json
├─ inputs/
│  └─ intro_example.md
├─ reports/
│  └─ .gitkeep
├─ comparisons/
│  └─ .gitkeep
└─ repair/
   └─ .gitkeep
```

---

# 2. `README.md`

```md
# Dissertation Introduction QA

Система структурного, логического и методологического аудита введений диссертаций
с использованием LLM.

## Назначение

Данный набор файлов предназначен для:

- критической оценки введений диссертаций;
- выявления структурных, логических и методологических дефектов;
- кодирования дефектов по нормализованной taxonomy;
- итеративной переработки введения;
- сравнения версий текста.

Система основана на трех ключевых компонентах:

1. `evaluation_standard.md` — нормативный стандарт оценки
2. `defect_taxonomy.md` — классификатор дефектов
3. `audit_prompt.md` — рабочий prompt для LLM-аудита

## Основная идея

Введение диссертации рассматривается как формальная спецификация исследования.

LLM должен:

1. извлечь структуру исследования;
2. проверить обязательные элементы;
3. проверить логические зависимости;
4. выявить дефекты;
5. присвоить defect codes;
6. выдать диагностический отчет на русском языке.

## Минимальный workflow

### 1. Подготовить текст введения
Поместить его в `inputs/intro_example.md`

### 2. Запустить lint или audit
Использовать `prompts/lint_prompt.md` или `prompts/audit_prompt.md`
вместе с:
- `standards/evaluation_standard.md`
- `standards/defect_taxonomy.md`
- текстом введения

### 3. Сохранить результат
Рекомендуется сохранять:
- markdown-отчет в `reports/`
- JSON-отчет по схеме `schemas/audit_report_schema.json`

### 4. Построить план правки
Использовать defect codes и severity summary

### 5. Выполнить targeted repair
Использовать `prompts/repair_prompt.md`

### 6. Сравнить версии
Использовать `prompts/compare_prompt.md`

## Рекомендуемый порядок документов для подачи в LLM

1. Prompt
2. Evaluation Standard
3. Defect Taxonomy
4. Dissertation Introduction

## Ключевые принципы системы

- Язык отчета: русский
- Позиция: критическая, диагностическая
- Неясность трактуется как дефект
- Шаблонная формулировка не считается автоматическим выполнением критерия
- Отсутствующие элементы нельзя додумывать за автора
- Похвала не является целью анализа

## Acceptance Gates

См. `standards/INTRO_ACCEPTANCE_GATES.md`

## Profiles

См. `configs/acceptance_profiles.yaml`

## Schemas

- `schemas/extraction_schema.json`
- `schemas/audit_report_schema.json`
- `schemas/comparison_schema.json`
```

---

# 3. `standards/evaluation_standard.md`

```md
# Standard for LLM-Based Evaluation of Dissertation Introductions

## 1. Назначение

Настоящий документ определяет нормативный стандарт для оценки введений диссертаций
с использованием LLM.

Цель стандарта:
- обеспечить систематическую оценку;
- повысить воспроизводимость аудита;
- формализовать поиск дефектов;
- перевести оценку из свободного эссе в режим структурной диагностики.

---

## 2. Обязательная основа по ГОСТ Р 7.0.11

Согласно разделу 5.3.1 ГОСТ Р 7.0.11 введение к диссертации включает:

- актуальность темы исследования;
- степень ее разработанности;
- цели и задачи;
- научную новизну;
- теоретическую и практическую значимость работы;
- методологию и методы исследования;
- положения, выносимые на защиту;
- степень достоверности и апробацию результатов.

Эти элементы являются критически обязательными.

---

## 3. Расширенная аналитическая структура

Помимо ГОСТ-минимума, введение также должно по возможности содержать и/или ясно
выделять следующие элементы:

- исследовательский пробел;
- объект исследования;
- предмет исследования;
- теоретическую основу;
- информационно-эмпирическую базу;
- публикации;
- структуру диссертации.

---

## 4. Базовая исследовательская логика

Введение должно выражать связную научную цепочку:

Проблема
→ состояние исследований
→ исследовательский пробел
→ цель
→ задачи
→ объект
→ предмет
→ методы
→ научный результат
→ значимость
→ достоверность / апробация

Разрыв этой цепочки является методологическим дефектом.

---

## 5. Измерения оценки

Оценка проводится по следующим измерениям:

1. Structural completeness
2. GOST compliance
3. Problem formulation
4. Literature positioning
5. Research gap quality
6. Research design coherence
7. Methodological adequacy
8. Scientific contribution
9. Defense propositions
10. Reliability and validation
11. Significance
12. Formal support / metadata

---

## 6. Шкала оценивания

Используется шкала 0–3:

- 0 — отсутствует или принципиально некорректно
- 1 — присутствует, но слабо
- 2 — адекватно
- 3 — сильно

---

## 7. Правило доказательности

Каждое оценочное суждение должно сопровождаться:

1. ссылкой на соответствующий фрагмент текста;
2. кратким объяснением;
3. оценкой или defect code.

---

## 8. Правило анти-додумывания

Отсутствующие элементы нельзя восстанавливать за автора.

Допустимые статусы элемента:
- explicit
- implicit_but_clear
- vague
- absent

Полный credit дается только explicit или в отдельных случаях strong implicit_but_clear.

---

## 9. Правило критической позиции

LLM должен действовать как строгий методологический аудитор.

Требуется:
- не смягчать критику;
- не переходить в режим похвалы;
- трактовать неясность, двусмысленность, неопределенность и шаблонность как дефекты;
- оценивать не формальное наличие фразы, а реальное выполнение функции раздела.

---

## 10. Блоки критериев

### SC — Structural Completeness

- SC1 — наличие обязательных компонентов ГОСТ
- SC2 — наличие расширенных аналитических компонентов
- SC3 — отделимость и идентифицируемость компонентов

### PR — Problem Formulation

- PR1 — наличие исследовательской проблемы
- PR2 — аргументированная значимость проблемы
- PR3 — переход от контекста к исследовательской задаче

### LG — Literature and Gap

- LG1 — наличие состояния разработанности
- LG2 — аналитичность обзора
- LG3 — наличие явного пробела
- LG4 — научный характер пробела

### RD — Research Design

- RD1 — gap → goal
- RD2 — цель как научный результат
- RD3 — goal → tasks
- RD4 — отсутствие декоративных задач
- RD5 — object → subject

### MT — Methodology

- MT1 — наличие методологической основы
- MT2 — наличие методов
- MT3 — tasks → methods
- MT4 — достаточность методов для заявленного результата
- MT5 — достаточность информационной базы

### NV — Scientific Contribution

- NV1 — конкретность новизны
- NV2 — goal → novelty
- NV3 — tasks → novelty
- NV4 — отсутствие тривиальности / описательности
- NV5 — диссертационная значимость новизны

### DF — Defense Propositions

- DF1 — наличие положений на защиту
- DF2 — соответствие новизне
- DF3 — защищаемость формулировок

### RL — Reliability and Validation

- RL1 — наличие достоверности
- RL2 — наличие оснований достоверности
- RL3 — наличие апробации
- RL4 — соразмерность апробации масштабу результатов

### SG — Significance

- SG1 — теоретическая значимость как вклад в знание
- SG2 — практическая значимость как конкретный режим применения
- SG3 — отсутствие шаблонности

### FM — Formal Support

- FM1 — публикации
- FM2 — структура диссертации
- FM3 — поддержка верифицируемости введения

---

## 11. Severity levels

- Critical defect
- Major defect
- Moderate defect
- Minor defect

### Critical
Фундаментальный разрыв: нет пробела, цели, новизны, положений на защиту,
достоверности при сильных эмпирических претензиях и т.п.

### Major
Серьезный дефект логики или проектирования:
цель не вытекает из пробела, задачи не ведут к цели, новизна не следует из цели.

### Moderate
Существенная, но не фатальная слабость:
обзор литературы слаб, значимость шаблонна, методы формальны.

### Minor
Низкоуровневый недостаток:
повторы, композиционные шероховатости, плохо оформленный служебный раздел.

---

## 12. Требуемый формат итогового аудита

Отчет должен содержать:

1. NORMALIZED EXTRACTION
2. STRUCTURAL ANALYSIS
3. GOST COMPLIANCE CHECK
4. RESEARCH LOGIC ANALYSIS
5. CRITERION SCORES
6. DEFECTS BY SEVERITY
7. FINAL DIAGNOSTIC ASSESSMENT
8. REVISION PRIORITIES
```

---

# 4. `standards/defect_taxonomy.md`

```md
# Defect Taxonomy / Codebook for Dissertation Introductions

## Формат кода

[GROUP]-[NUMBER]

Примеры:
- GAP-01
- GOAL-03
- NOV-05

---

## PR — Актуальность

- PR-01 — отсутствует явная исследовательская проблема
- PR-02 — актуальность описывает тему, а не проблему
- PR-03 — макроконтекст без перехода к исследовательской задаче
- PR-04 — декларативная важность без аргументации
- PR-05 — нет связи между значимостью и исследовательской задачей

---

## LG — Степень разработанности

- LG-01 — перечисление авторов без анализа
- LG-02 — отсутствует структура подходов
- LG-03 — отсутствует критический анализ
- LG-04 — нет перехода к пробелу
- LG-05 — обзор носит описательный, а не аналитический характер

---

## GAP — Исследовательский пробел

- GAP-01 — пробел отсутствует
- GAP-02 — пробел не сформулирован явно
- GAP-03 — пробел слишком общий
- GAP-04 — пробел не научный
- GAP-05 — пробел не вытекает из обзора
- GAP-06 — пробел не связан с целью

---

## GOAL — Цель

- GOAL-01 — цель отсутствует
- GOAL-02 — цель слишком общая
- GOAL-03 — цель описывает процесс, а не результат
- GOAL-04 — цель не связана с пробелом
- GOAL-05 — цель не операционализирована
- GOAL-06 — цель дублирует тему

---

## TASK — Задачи

- TASK-01 — задачи отсутствуют
- TASK-02 — задачи не ведут к цели
- TASK-03 — задачи дублируют друг друга
- TASK-04 — задачи носят учебно-реферативный характер
- TASK-05 — задачи не являются исследовательскими
- TASK-06 — задачи механически описывают главы

---

## OBJ — Объект

- OBJ-01 — объект отсутствует
- OBJ-02 — объект слишком узкий
- OBJ-03 — объект совпадает с предметом
- OBJ-04 — объект не соответствует теме

---

## SUBJ — Предмет

- SUBJ-01 — предмет отсутствует
- SUBJ-02 — предмет шире объекта
- SUBJ-03 — предмет совпадает с объектом
- SUBJ-04 — предмет не является аспектом объекта
- SUBJ-05 — предмет сформулирован как тема

---

## METH — Методология и методы

- METH-01 — методология отсутствует
- METH-02 — методы отсутствуют
- METH-03 — формальный список методов
- METH-04 — методы не связаны с задачами
- METH-05 — методы не обеспечивают заявленный результат
- METH-06 — методология декларативна

---

## DATA — Информационная база

- DATA-01 — отсутствует информационно-эмпирическая база
- DATA-02 — база описана формально
- DATA-03 — база не соответствует задачам
- DATA-04 — база недостаточна по масштабу

---

## NOV — Научная новизна

- NOV-01 — новизна отсутствует
- NOV-02 — новизна декларативна
- NOV-03 — нет конкретных результатов
- NOV-04 — новизна описательная
- NOV-05 — новизна тривиальна
- NOV-06 — новизна не связана с целью
- NOV-07 — новизна не связана с задачами
- NOV-08 — новизна подменена обзором
- NOV-09 — новизна подменена рекомендациями
- NOV-10 — новизна несоразмерна уровню диссертации

---

## DEF — Положения на защиту

- DEF-01 — положения отсутствуют
- DEF-02 — положения просто повторяют новизну
- DEF-03 — положения сформулированы расплывчато
- DEF-04 — положения не являются тезисами
- DEF-05 — положения не выглядят реально защищаемыми

---

## REL — Достоверность

- REL-01 — достоверность отсутствует
- REL-02 — достоверность декларативна
- REL-03 — отсутствуют основания достоверности
- REL-04 — достоверность не связана с методами
- REL-05 — достоверность не подтверждена данными

---

## APR — Апробация

- APR-01 — апробация отсутствует
- APR-02 — апробация формальна
- APR-03 — апробация не связана с результатами
- APR-04 — апробация недостаточна

---

## SIG — Значимость

- SIG-01 — значимость отсутствует
- SIG-02 — значимость шаблонна
- SIG-03 — значимость не конкретизирована
- SIG-04 — значимость не вытекает из результатов
- SIG-05 — практическая значимость декларативна

---

## STR — Структура

- STR-01 — отсутствуют обязательные разделы
- STR-02 — разделы не отделены и плохо извлекаемы
- STR-03 — композиционная несогласованность
- STR-04 — нарушен порядок исследовательской логики
- STR-05 — ключевые элементы растворены в неопределенном тексте

---

## LOG — Логические связи

- LOG-01 — разрыв gap → goal
- LOG-02 — разрыв goal → tasks
- LOG-03 — ошибка object → subject
- LOG-04 — разрыв tasks → methods
- LOG-05 — разрыв goal → novelty
- LOG-06 — разрыв novelty → defense propositions
- LOG-07 — разрыв methods/data → reliability

---

## GEN — Шаблонность и псевдонаучность

- GEN-01 — чрезмерно общий язык
- GEN-02 — клишированные формулировки
- GEN-03 — отсутствие конкретики
- GEN-04 — имитация научности без содержания
- GEN-05 — декларативные конструкции без операционального смысла

---

## GOST — Нарушения ГОСТ

- GOST-01 — отсутствует актуальность
- GOST-02 — отсутствует степень разработанности
- GOST-03 — отсутствуют цель и/или задачи
- GOST-04 — отсутствует научная новизна
- GOST-05 — отсутствует теоретическая и/или практическая значимость
- GOST-06 — отсутствует методология и методы
- GOST-07 — отсутствуют положения, выносимые на защиту
- GOST-08 — отсутствует степень достоверности
- GOST-09 — отсутствует апробация результатов
```

---

# 5. `standards/INTRO_ACCEPTANCE_GATES.md`

```md
# INTRO_ACCEPTANCE_GATES

## Gate 0 — Extractability
Минимальная извлекаемость структуры.

Требования:
- можно выделить хотя бы проблему / цель / задачи / новизну;
- текст не представляет собой композиционный коллапс.

---

## Gate 1 — Minimum Methodological Viability
Минимальная исследовательская жизнеспособность.

Требования:
- есть пробел или хотя бы ясно выраженный намек на него;
- есть цель;
- есть задачи;
- есть новизна;
- нет полного распада исследовательской логики.

---

## Gate 2 — GOST Compliance
Соответствие минимальным требованиям ГОСТ Р 7.0.11.

Требования:
- актуальность
- степень разработанности
- цели и задачи
- научная новизна
- теоретическая и практическая значимость
- методология и методы
- положения на защиту
- достоверность и апробация

---

## Gate 3 — Logical Coherence
Логическая согласованность исследовательского дизайна.

Требования:
- нет critical logical defects;
- LC average >= 2;
- object / subject корректны;
- gap / goal / tasks связаны.

---

## Gate 4 — Scientific Contribution Credibility
Правдоподобие научного вклада.

Требования:
- novelty score >= 2;
- положения на защиту соотносятся с новизной;
- достоверность присутствует и не является пустой декларацией.

---

## Gate 5 — Supervisor-Ready Quality
Версия пригодна для серьезного обсуждения с научным руководителем / для сильной рабочей версии.

Требования:
- 0 critical defects
- <= 2 major defects
- нет нарушений обязательных компонентов ГОСТ
- core logic intact
```

---

# 6. `prompts/audit_prompt.md`

```md
# Audit Prompt

Вы выступаете как методологический эксперт, выполняющий строгий аудит введения диссертации.

Ваша задача — НЕ хвалить текст, а критически диагностировать его.

Вы должны использовать приложенные документы:

1. Standard for LLM-Based Evaluation of Dissertation Introductions
2. Defect Taxonomy / Codebook for Dissertation Introductions

как нормативную основу оценки.

Отчет должен быть написан полностью на русском языке.

Ваша позиция должна быть:
- аналитической
- критической
- диагностической
- методологически строгой

Цель анализа:
выявить как можно больше слабостей, дефектов, разрывов логики,
неясностей, шаблонных формулировок и псевдокомпонентов.

Любая неясность, двусмысленность, расплывчатость, декларативность
или шаблонность должна трактоваться как дефект.

Не додумывайте за автора отсутствующие элементы.
Наличие стандартной академической формулы еще не означает,
что критерий выполнен содержательно.

Положительные замечания допускаются только тогда,
когда они аналитически необходимы для точной диагностики.

## Порядок работы

### Stage 1 — Normalized extraction
Извлеките из текста нормализованную структуру исследования:
- ProblemContext
- KnowledgeState
- ResearchGap
- Goal
- Tasks
- Object
- Subject
- Methodology
- Methods
- DataBase
- ScientificNovelty
- PropositionsForDefense
- TheoreticalSignificance
- PracticalSignificance
- Reliability
- Approbation
- Publications
- DissertationStructure

Для каждого элемента укажите статус:
- explicit
- implicit_but_clear
- vague
- absent

### Stage 2 — Structural analysis
Определите:
- какие компоненты присутствуют;
- какие отсутствуют;
- какие присутствуют лишь номинально;
- какие плохо отделимы.

### Stage 3 — GOST compliance check
Проверьте наличие и адекватность обязательных элементов по ГОСТ Р 7.0.11:
- актуальность темы исследования
- степень разработанности
- цели и задачи
- научная новизна
- теоретическая и практическая значимость
- методология и методы
- положения, выносимые на защиту
- степень достоверности и апробация результатов

### Stage 4 — Research logic analysis
Проверьте связи:
- problem → gap
- gap → goal
- goal → tasks
- object → subject
- tasks → methods
- goal → novelty
- novelty → defense propositions
- methods/data → reliability

### Stage 5 — Criterion scoring
Оцените критерии по шкале:
- 0 = absent / fundamentally incorrect
- 1 = present but weak
- 2 = adequate
- 3 = strong

### Stage 6 — Defect coding
Для каждого существенного дефекта:
- присвойте defect code;
- определите severity;
- приведите evidence;
- кратко объясните дефект.

### Stage 7 — Final diagnostic synthesis
Дайте итоговую оценку:
- структурной полноты;
- методологической состоятельности;
- логической согласованности;
- качества научного вклада;
- приоритетов переработки.

## Обязательный формат ответа

I. NORMALIZED EXTRACTION

II. STRUCTURAL ANALYSIS

III. GOST COMPLIANCE CHECK

IV. RESEARCH LOGIC ANALYSIS

V. CRITERION SCORES

VI. DEFECTS BY SEVERITY
- Critical
- Major
- Moderate
- Minor

VII. FINAL DIAGNOSTIC ASSESSMENT

VIII. REVISION PRIORITIES
```

---

# 7. `prompts/lint_prompt.md`

```md
# Lint Prompt

Вы выполняете быстрый, но строгий lint-анализ введения диссертации.

Язык отчета: русский.

Ваша задача:
- быстро извлечь основные элементы структуры;
- выявить явные дефекты;
- проверить обязательные компоненты ГОСТ;
- выявить основные логические разрывы;
- присвоить defect codes.

Это НЕ мягкий отзыв и НЕ похвала.
Это быстрый дефектоскопический прогон.

Любая неясность считается дефектом.
Отсутствующие элементы нельзя восстанавливать за автора.

## Требуемый формат

I. QUICK EXTRACTION
- Problem
- Gap
- Goal
- Tasks
- Object
- Subject
- Methods
- Novelty
- Defense propositions
- Reliability
- Approbation

II. MISSING / WEAK COMPONENTS

III. MAIN DEFECT CODES

IV. GOST VIOLATIONS

V. TOP LOGICAL BREAKS

VI. QUICK VERDICT
```

---

# 8. `prompts/repair_prompt.md`

```md
# Repair Prompt

Вы выполняете не полную перепись введения, а адресную методологическую переработку.

Я предоставлю:
1. исходный текст введения;
2. аудиторский отчет;
3. defect codes, которые нужно устранить.

Ваша задача:
- исправить только те фрагменты, которые необходимы для устранения указанных дефектов;
- сохранить общую структуру и смысл текста, если они не противоречат исправлению;
- не вносить произвольные улучшения вне поставленной задачи;
- писать только по-русски;
- устранять как формальные, так и логические дефекты.

Любая правка должна усиливать:
- ясность;
- методологическую определенность;
- логическую согласованность;
- связь между разделами.

## Формат ответа

I. TARGET DEFECTS TO REPAIR

II. REVISED FRAGMENTS

Для каждого фрагмента:
- defect code
- исходная проблема
- новый вариант текста
- почему исправление лучше методологически

III. POST-REPAIR RISK NOTES

Укажите, какие новые риски или зависимости нужно проверить после внесения правки.
```

---

# 9. `prompts/compare_prompt.md`

```md
# Compare Prompt

Вы сравниваете два аудиторских отчета по двум версиям введения диссертации.

Язык ответа: русский.

Ваша задача:
- определить устраненные дефекты;
- определить оставшиеся дефекты;
- выявить новые дефекты;
- оценить динамику score;
- выявить возможные регрессии;
- определить, улучшилось ли введение реально, а не только формально.

## Формат ответа

I. RESOLVED DEFECTS

II. REMAINING DEFECTS

III. NEW DEFECTS

IV. SCORE DELTA

V. REGRESSION WARNINGS

VI. OVERALL VERSION-TO-VERSION ASSESSMENT

VII. NEXT REVISION PRIORITIES
```

---

# 10. `configs/acceptance_profiles.yaml`

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
      LC4: 2
      LC5: 2
      LC6: 2
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
      SC2: 2
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

# 11. `schemas/extraction_schema.json`

```json
{
  "type": "object",
  "properties": {
    "problem_context": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "knowledge_state": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "research_gap": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "goal": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "tasks": { "type": "array", "items": { "type": "string" } },
    "object": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "subject": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["explicit", "implicit_but_clear", "vague", "absent"]
        }
      },
      "required": ["text", "status"]
    },
    "methodology": { "type": "string" },
    "methods": { "type": "array", "items": { "type": "string" } },
    "database": { "type": "string" },
    "scientific_novelty": { "type": "array", "items": { "type": "string" } },
    "propositions_for_defense": { "type": "array", "items": { "type": "string" } },
    "theoretical_significance": { "type": "string" },
    "practical_significance": { "type": "string" },
    "reliability": { "type": "string" },
    "approbation": { "type": "string" },
    "publications": { "type": "string" },
    "dissertation_structure": { "type": "string" }
  },
  "required": [
    "problem_context",
    "knowledge_state",
    "research_gap",
    "goal",
    "tasks",
    "object",
    "subject",
    "methodology",
    "methods",
    "database",
    "scientific_novelty",
    "propositions_for_defense",
    "theoretical_significance",
    "practical_significance",
    "reliability",
    "approbation",
    "publications",
    "dissertation_structure"
  ]
}
```

---

# 12. `schemas/audit_report_schema.json`

```json
{
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "document_id": { "type": "string" },
        "language": { "type": "string" },
        "audit_mode": { "type": "string" },
        "date": { "type": "string" }
      },
      "required": ["document_id", "language", "audit_mode", "date"]
    },
    "extraction": { "type": "object" },
    "scores": {
      "type": "object",
      "properties": {
        "SC1": { "type": "integer" },
        "SC2": { "type": "integer" },
        "LC1": { "type": "integer" },
        "LC2": { "type": "integer" },
        "LC3": { "type": "integer" },
        "LC4": { "type": "integer" },
        "LC5": { "type": "integer" },
        "LC6": { "type": "integer" },
        "NV": { "type": "integer" },
        "VAL": { "type": "integer" }
      },
      "required": ["SC1", "SC2", "LC1", "LC2", "LC3", "LC4", "LC5", "LC6", "NV", "VAL"]
    },
    "defects": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "severity": { "type": "string" },
          "section": { "type": "string" },
          "description": { "type": "string" },
          "evidence": { "type": "string" },
          "recommendation": { "type": "string" }
        },
        "required": ["code", "severity", "section", "description", "evidence", "recommendation"]
      }
    },
    "gost_compliance": {
      "type": "object",
      "properties": {
        "relevance": { "type": "boolean" },
        "degree_of_development": { "type": "boolean" },
        "goals_tasks": { "type": "boolean" },
        "novelty": { "type": "boolean" },
        "significance": { "type": "boolean" },
        "methods": { "type": "boolean" },
        "defense_propositions": { "type": "boolean" },
        "reliability": { "type": "boolean" },
        "approbation": { "type": "boolean" }
      },
      "required": [
        "relevance",
        "degree_of_development",
        "goals_tasks",
        "novelty",
        "significance",
        "methods",
        "defense_propositions",
        "reliability",
        "approbation"
      ]
    },
    "summary": {
      "type": "object",
      "properties": {
        "critical_count": { "type": "integer" },
        "major_count": { "type": "integer" },
        "moderate_count": { "type": "integer" },
        "minor_count": { "type": "integer" },
        "logical_integrity_score": { "type": "number" },
        "overall_verdict": { "type": "string" }
      },
      "required": [
        "critical_count",
        "major_count",
        "moderate_count",
        "minor_count",
        "logical_integrity_score",
        "overall_verdict"
      ]
    }
  },
  "required": ["metadata", "extraction", "scores", "defects", "gost_compliance", "summary"]
}
```

---

# 13. `schemas/comparison_schema.json`

```json
{
  "type": "object",
  "properties": {
    "from_version": { "type": "string" },
    "to_version": { "type": "string" },
    "resolved_defects": {
      "type": "array",
      "items": { "type": "string" }
    },
    "remaining_defects": {
      "type": "array",
      "items": { "type": "string" }
    },
    "new_defects": {
      "type": "array",
      "items": { "type": "string" }
    },
    "score_diff": {
      "type": "object",
      "additionalProperties": { "type": "number" }
    },
    "regression_warnings": {
      "type": "array",
      "items": { "type": "string" }
    },
    "overall_assessment": { "type": "string" }
  },
  "required": [
    "from_version",
    "to_version",
    "resolved_defects",
    "remaining_defects",
    "new_defects",
    "score_diff",
    "regression_warnings",
    "overall_assessment"
  ]
}
```

---

# 14. `inputs/intro_example.md`

```md
# Intro Example

Поместите сюда текст введения диссертации для анализа.

Рекомендуется использовать полный текст введения, а не фрагмент,
если вы хотите получить корректную оценку логических связей
между проблемой, пробелом, целью, задачами, методами и новизной.
```

---

# 15. Как использовать starter kit на практике

Самый рабочий порядок такой:

Сначала подаете в LLM:

1. `prompts/audit_prompt.md`
2. `standards/evaluation_standard.md`
3. `standards/defect_taxonomy.md`
4. `inputs/intro_example.md`

Затем сохраняете результат в двух формах:

* человекочитаемый markdown-отчет;
* JSON по `schemas/audit_report_schema.json`.

Потом по defect codes строите адресную переработку через `prompts/repair_prompt.md`.

После правки повторяете аудит и сравниваете версии через `prompts/compare_prompt.md`.

---

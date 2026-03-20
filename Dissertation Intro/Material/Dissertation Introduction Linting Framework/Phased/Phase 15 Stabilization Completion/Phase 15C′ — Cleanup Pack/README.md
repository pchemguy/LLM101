**Phase 15C′ (cleanup-only) pack**

👉 [Скачать архив](sandbox:/mnt/data/dissertation_intro_qa_phase15c_prime_pack.zip)

---

## Что это именно (важно)

Это **не новый функциональный слой**, а строго:

* нормализация поведения
* устранение скрытых источников нестабильности
* подготовка к интеграции

---

## Что включено

### 1. Централизация критических констант

* `core/severity.py` → единый `SEVERITY_ORDER`

### 2. Нормализация exit codes

* `core/exit_codes.py`
* каноническая модель:

  * `0` success
  * `1` validation
  * `2` usage
  * `3` runtime

### 3. Детерминированная сортировка

* `core/sort_utils.py`
* единая функция сортировки дефектов

### 4. Strict-mode конфигурация

* `docs/STRICT_MODE_CONFIG.yaml`
* фиксирует production-поведение

### 5. Acceptance criteria (жёсткий gate)

* `docs/PHASE15C_PRIME_ACCEPTANCE.md`

### 6. Минимальный CLI-паттерн (правильный)

* `example_cli.py` — эталон обработки exit codes

### 7. Тест на детерминизм

* `test_sorting.py`

---

## Чего **намеренно нет**

* ❌ новых CLI
* ❌ новых схем
* ❌ расширения функционала
* ❌ интеграции

Это deliberate — иначе ты снова уйдёшь в Phase 15D вместо завершения.

---

## Как использовать этот pack правильно

Не как “установить и забыть”, а как **patch guide**:

### Применить в Phase 15 finalization:

1. Заменить все локальные:

   * `SEVERITY_ORDER` → импорт из `core.severity`
2. Вставить сортировку:

   * `sort_defects()` в:

     * render
     * compare
     * repair-plan
3. Обернуть ВСЕ CLI в exit-code pattern
4. Включить strict-mode как default (или через config)

---

## Критический вывод

После применения этого pack:

```text
Система становится:
- детерминированной
- предсказуемой
- пригодной для пайплайнов
```

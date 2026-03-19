# Synthetic Corpus Generator Spec

## Purpose

Генерировать искусственные введения диссертаций с контролируемыми дефектами
для benchmark и regression testing.

## Controlled dimensions

- наличие / отсутствие исследовательского пробела
- тип формулировки цели
- качество задач
- корректность объекта и предмета
- конкретность методов
- уровень научной новизны
- полнота ГОСТ-компонентов
- степень шаблонности языка

## Generator modes

### Mode A — Single-defect cases
Один доминирующий дефект на кейс.

### Mode B — Compound-defect cases
2–4 логически связанных дефекта.

### Mode C — Near-pass cases
Почти сильные введения с 1–3 умеренными слабостями.

## Output recommendation

Каждый сгенерированный кейс должен сопровождаться:
- case_id
- target defect codes
- expected severity floor
- short rationale

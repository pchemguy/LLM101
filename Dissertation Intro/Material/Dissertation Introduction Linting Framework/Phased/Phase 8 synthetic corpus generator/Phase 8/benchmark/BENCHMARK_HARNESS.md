# Benchmark Harness

## Goal

Использовать стандартные benchmark-cases для сравнения:
- prompt variants
- acceptance profiles
- версии LLM-based audit pipeline

## Minimal evaluation protocol

For each case:
1. Run audit with one prompt variant.
2. Save resulting audit JSON.
3. Compare detected defect codes with expected defect codes.
4. Record misses and extras.
5. Summarize sensitivity and stability.

## Primary benchmark questions

1. Выявляет ли система ожидаемый ключевой дефект?
2. Не пропускает ли критически важные нарушения ГОСТ?
3. Не переоценивает ли weak cases как acceptable?
4. Не становится ли слишком мягкой при vague formulations?

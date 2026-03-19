# Smoke Test Workflow

## Purpose

Проверить end-to-end цикл Phase 7 на демо-данных.

## Steps

1. Сгенерировать markdown-отчеты из двух demo audit JSON.
2. Сравнить две версии введения через `compare`.
3. Построить trends / history index.
4. Построить defect clusters и section analytics.
5. Сгенерировать HTML dashboard.
6. Проверить, что все выходные файлы создаются без ошибок.

## Expected outcomes

- `audit_demo_v1.md` и `audit_demo_v2.md` успешно рендерятся.
- comparison JSON и markdown создаются.
- trends JSON/MD создаются.
- clusters JSON/MD создаются.
- section analytics JSON/MD создаются.
- dashboard HTML создается.

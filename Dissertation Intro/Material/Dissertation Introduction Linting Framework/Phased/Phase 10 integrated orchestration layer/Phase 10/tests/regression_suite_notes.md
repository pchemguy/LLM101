# Regression Suite Notes

## Purpose

Проверять, не ухудшилась ли система после:
- изменения prompt
- изменения evaluation standard
- изменения taxonomy
- изменения acceptance profiles

## Recommended minimal regression set

- case_gap_missing
- case_methods_formal
- case_gost_missing
- case_balanced_strong

## Failure signals

- benchmark case stops triggering expected critical/major defect
- strong case starts producing many false positives
- GOST-missing case passes stricter profile unexpectedly

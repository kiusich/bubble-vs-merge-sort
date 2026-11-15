# Bubble Sort vs Merge Sort

Курсовая работа по дисциплине «Алгоритмы и структуры данных» (ИжГТУ имени М.Т. Калашникова).
Тема: сравнительный анализ алгоритмов сортировки массивов — сортировка пузырьком и сортировка слиянием.

## Состав
- `sorting.py` — реализации `bubble_sort` (с флагом обмена), `bubble_sort_basic` (без флага), `merge_sort` (сверху вниз, внешний буфер)
- `counting.py` — версии со счётчиками сравнений и записей
- `tests.py` — проверка корректности (сравнение с `sorted()`, устойчивость)
- `benchmark.py` — генерация данных и измерения (`time.perf_counter`), результаты в `results/`
- `plot.py` — графики по `results/results.json`
- `results/` — исходные данные измерений (`results.json`, `random_time_ms.csv`) и графики (`*.png`)

## Запуск
```
python3 tests.py            # проверка корректности
python3 benchmark.py        # полный прогон (около 15 минут), либо: python3 benchmark.py quick
python3 plot.py             # графики (нужен matplotlib)
```
Python 3.12; для измерений сторонние библиотеки не нужны, для графиков — `matplotlib`.

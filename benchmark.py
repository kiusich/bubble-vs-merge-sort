"""Экспериментальное сравнение Bubble Sort и Merge Sort. Результаты -> results/*.json, results/*.csv
Запуск: python3 benchmark.py          (полный прогон)
        python3 benchmark.py quick    (быстрая проверка)"""
import csv, gc, json, os, platform, random, statistics, sys, time
from sorting import bubble_sort, bubble_sort_basic, merge_sort
from counting import bubble_sort_count, merge_sort_count

SEED = 20261113
perf = time.perf_counter
OUT = "results"
os.makedirs(OUT, exist_ok=True)
random.seed(SEED)
QUICK = len(sys.argv) > 1 and sys.argv[1] == "quick"

SIZES = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
SETS = {10: 1000, 20: 1000, 50: 1000, 100: 1000, 200: 1000, 500: 1000,
        1000: 500, 2000: 300, 5000: 100, 10000: 100}
SMALL = [4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 50]      # поиск точки пересечения
TYPE_N = 2000
if QUICK:
    SETS = {k: 3 for k in SETS}


def gen(kind, n):
    base = [random.randint(0, 10**6) for _ in range(n)]
    if kind == "random":
        return base
    if kind == "sorted":
        return sorted(base)
    if kind == "reversed":
        return sorted(base, reverse=True)
    if kind == "nearly":                                # 1% случайных перестановок в отсортированном массиве
        a = sorted(base)
        for _ in range(max(1, n // 100)):
            i, j = random.randrange(n), random.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if kind == "few":                                   # всего 10 различных значений
        return [random.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def stat(v):
    return {"mean": statistics.fmean(v) * 1e3, "std": statistics.pstdev(v) * 1e3}   # миллисекунды


def measure(kind, n, sets):
    """Для каждого набора: сначала Bubble, затем Merge, затем встроенная сортировка на тех же данных."""
    tb, tm, ts = [], [], []
    gc.disable()
    for _ in range(sets):
        data = gen(kind, n)
        expected = sorted(data)
        buf = [0] * n                                   # буфер выделяется до замера
        a = data[:]
        t = perf(); bubble_sort(a); tb.append(perf() - t)
        assert a == expected
        a = data[:]
        t = perf(); merge_sort(a, buf); tm.append(perf() - t)
        assert a == expected
        a = data[:]
        t = perf(); a.sort(); ts.append(perf() - t)
        assert a == expected
    gc.enable()
    return {"n": n, "sets": sets, "bubble": stat(tb), "merge": stat(tm), "builtin": stat(ts)}


res = {"meta": {"python": platform.python_version(), "platform": platform.platform(),
                "machine": platform.machine(), "seed": SEED}}

# Эксперимент 1: случайные данные, разные размеры
res["random"] = []
for n in SIZES:
    r = measure("random", n, SETS[n]); res["random"].append(r)
    print("random", n, r["sets"], round(r["bubble"]["mean"], 4), round(r["merge"]["mean"], 4), round(r["builtin"]["mean"], 4), flush=True)

# Эксперимент 1а: малые размеры (точка пересечения)
res["small"] = []
for n in SMALL:
    r = measure("random", n, 2000 if not QUICK else 3); res["small"].append(r)
    print("small", n, round(r["bubble"]["mean"] * 1e3, 2), round(r["merge"]["mean"] * 1e3, 2), flush=True)

# Эксперимент 2: типы данных при n = 2000
res["types"] = {}
for kind in ["random", "sorted", "reversed", "nearly", "few"]:
    r = measure(kind, TYPE_N, 100 if not QUICK else 3); res["types"][kind] = r
    print("type", kind, round(r["bubble"]["mean"], 3), round(r["merge"]["mean"], 3), round(r["builtin"]["mean"], 3), flush=True)

# Эксперимент 3: отсортированные данные - ранний выход пузырька и базовая версия без флага
res["sorted"] = []
gc.disable()
for n in [100, 200, 500, 1000, 2000, 5000]:
    tf, tb, tm = [], [], []
    for _ in range(30 if not QUICK else 3):
        data = gen("sorted", n)
        buf = [0] * n
        a = data[:]; t = perf(); bubble_sort(a); tf.append(perf() - t)
        a = data[:]; t = perf(); bubble_sort_basic(a); tb.append(perf() - t)
        a = data[:]; t = perf(); merge_sort(a, buf); tm.append(perf() - t)
    res["sorted"].append({"n": n, "bubble_flag": statistics.fmean(tf) * 1e3,
                          "bubble_basic": statistics.fmean(tb) * 1e3, "merge": statistics.fmean(tm) * 1e3})
    print("sorted", res["sorted"][-1], flush=True)
gc.enable()

# Эксперимент 4: счётчики операций, случайные данные
res["ops"] = []
for n in SIZES:
    cs = (100 if n <= 2000 else 20) if not QUICK else 3
    bc = bw = mc = mw = 0
    for _ in range(cs):
        data = gen("random", n)
        a = data[:]; c, w = bubble_sort_count(a); bc += c; bw += w
        a = data[:]; c, w = merge_sort_count(a, [0] * n); mc += c; mw += w
    res["ops"].append({"n": n, "sets": cs, "b_cmp": bc / cs, "b_wr": bw / cs, "m_cmp": mc / cs, "m_wr": mw / cs})
    print("ops", res["ops"][-1], flush=True)

json.dump(res, open(f"{OUT}/results.json", "w"), ensure_ascii=False, indent=1)
with open(f"{OUT}/random_time_ms.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n", "sets", "bubble_ms", "merge_ms", "builtin_ms"])
    for r in res["random"]:
        w.writerow([r["n"], r["sets"], r["bubble"]["mean"], r["merge"]["mean"], r["builtin"]["mean"]])
print("OK")

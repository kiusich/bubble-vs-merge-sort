"""Построение графиков по results/results.json -> results/*.png"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.dpi": 100})
R = json.load(open("results/results.json"))
C = {"bubble": "#c0392b", "merge": "#1f5fa8", "builtin": "#2e8b57"}
L = {"bubble": "Сортировка пузырьком", "merge": "Сортировка слиянием", "builtin": "list.sort() (Timsort)"}

# Рис. 1: случайные данные: (а) малые n, линейная шкала; (б) все n, двойная логарифмическая шкала
fig, ax = plt.subplots(1, 2, figsize=(10, 3.9))
ns = [r["n"] for r in R["random"]]
sm = [r for r in R["random"] if r["n"] <= 500]
for k in ("bubble", "merge", "builtin"):
    ax[0].plot([r["n"] for r in sm], [r[k]["mean"] for r in sm], "o-", color=C[k], label=L[k], ms=4)
    ax[1].loglog(ns, [r[k]["mean"] for r in R["random"]], "o-", color=C[k], label=L[k], ms=4)
ax[0].set_title("а) n ≤ 500, линейная шкала"); ax[1].set_title("б) двойная логарифмическая шкала")
for a in ax:
    a.set_xlabel("Размер массива n"); a.set_ylabel("Среднее время, мс")
ax[0].legend(); fig.tight_layout(); fig.savefig("results/fig1_random.png", dpi=200); plt.close(fig)

# Рис. 2: разные типы данных при n = 2000 (логарифмическая ось Y)
kinds = ["random", "sorted", "reversed", "nearly", "few"]
names = ["случайные", "отсортир.", "обратные", "почти отсорт.", "10 знач."]
fig, ax = plt.subplots(figsize=(8, 3.8))
w = 0.26
for i, k in enumerate(("bubble", "merge", "builtin")):
    ax.bar([j + (i - 1) * w for j in range(5)], [R["types"][t][k]["mean"] for t in kinds], w, color=C[k], label=L[k])
ax.set_yscale("log"); ax.set_xticks(range(5)); ax.set_xticklabels(names)
ax.set_ylabel("Среднее время, мс"); ax.set_xlabel("Тип входных данных (n = %d)" % R["types"]["random"]["n"])
ax.set_ylim(top=3e3); ax.legend(ncol=3, loc="upper center"); fig.tight_layout(); fig.savefig("results/fig2_types.png", dpi=200); plt.close(fig)

# Рис. 3: отсортированные данные
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ns = [r["n"] for r in R["sorted"]]
ax.loglog(ns, [r["bubble_basic"] for r in R["sorted"]], "s-", color="#8e44ad", label="Пузырёк без флага обмена", ms=4)
ax.loglog(ns, [r["merge"] for r in R["sorted"]], "o-", color=C["merge"], label=L["merge"], ms=4)
ax.loglog(ns, [r["bubble_flag"] for r in R["sorted"]], "^-", color=C["bubble"], label="Пузырёк с флагом обмена", ms=4)
ax.set_xlabel("Размер массива n"); ax.set_ylabel("Среднее время, мс"); ax.legend()
fig.tight_layout(); fig.savefig("results/fig3_sorted.png", dpi=200); plt.close(fig)
print("графики готовы")

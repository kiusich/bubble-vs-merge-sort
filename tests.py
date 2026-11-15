"""Проверка корректности: сравнение с sorted() на случайных и граничных данных."""
import random
from sorting import bubble_sort, bubble_sort_basic, merge_sort
from counting import bubble_sort_count, merge_sort_count

random.seed(1)
cases = [[], [1], [2, 1], [1, 1, 1, 1], list(range(50)), list(range(50, 0, -1))]
for n in (2, 3, 10, 100, 300):
    for _ in range(200):
        cases.append([random.randint(0, 20) for _ in range(n)])
        cases.append([random.randint(0, 10**6) for _ in range(n)])
for data in cases:
    exp = sorted(data)
    a = data[:]; bubble_sort(a); assert a == exp
    a = data[:]; bubble_sort_basic(a); assert a == exp
    a = data[:]; merge_sort(a, [0] * len(a)); assert a == exp
    a = data[:]; bubble_sort_count(a); assert a == exp
    a = data[:]; merge_sort_count(a, [0] * len(a)); assert a == exp


class K:                                   # проверка устойчивости обеих сортировок
    __slots__ = ("k", "i")
    def __init__(self, k, i): self.k, self.i = k, i
    def __lt__(self, o): return self.k < o.k
    def __gt__(self, o): return self.k > o.k


for sorter in (lambda x: merge_sort(x, [None] * len(x)), bubble_sort):
    objs = [K(random.randint(0, 5), i) for i in range(500)]
    sorter(objs)
    assert all((objs[t].k, objs[t].i) <= (objs[t + 1].k, objs[t + 1].i) for t in range(499))
print("Все тесты пройдены:", len(cases), "наборов")

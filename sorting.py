"""Сортировка пузырьком и сортировка слиянием (чистый Python, без сторонних библиотек)."""


def bubble_sort(a):
    """Сортировка пузырьком с флагом обмена (ранний выход) и сужением неотсортированной части."""
    n = len(a)
    while n > 1:
        swapped = False
        for i in range(1, n):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:                    # обменов не было - массив уже отсортирован
            break
        n -= 1                             # максимум "всплыл" на место a[n-1]


def bubble_sort_basic(a):
    """Базовая версия без флага обмена: всегда выполняет n(n-1)/2 сравнений."""
    n = len(a)
    for k in range(n - 1):
        for i in range(1, n - k):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]


def merge_sort(a, buf):
    """Сортировка слиянием сверху вниз. buf - вспомогательный буфер длины не меньше len(a)."""
    _merge_sort(a, buf, 0, len(a))


def _merge_sort(a, buf, lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) >> 1
    _merge_sort(a, buf, lo, mid)
    _merge_sort(a, buf, mid, hi)
    buf[lo:mid] = a[lo:mid]                # копируем только левую половину
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[j] < buf[i]:                  # строгое <: при равенстве берём левый (устойчивость)
            a[k] = a[j]
            j += 1
        else:
            a[k] = buf[i]
            i += 1
        k += 1
    while i < mid:                         # остаток левой половины; правый уже на месте
        a[k] = buf[i]
        i += 1
        k += 1

"""Версии алгоритмов со счётчиками операций: сравнения элементов и записи элементов в память."""


def bubble_sort_count(a):
    cmp = wr = 0
    n = len(a)
    while n > 1:
        swapped = False
        for i in range(1, n):
            cmp += 1
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                wr += 2
                swapped = True
        if not swapped:
            break
        n -= 1
    return cmp, wr


def merge_sort_count(a, buf):
    c = [0, 0]  # [сравнения, записи]
    _m(a, buf, 0, len(a), c)
    return c[0], c[1]


def _m(a, buf, lo, hi, c):
    if hi - lo < 2:
        return
    mid = (lo + hi) >> 1
    _m(a, buf, lo, mid, c)
    _m(a, buf, mid, hi, c)
    buf[lo:mid] = a[lo:mid]
    c[1] += mid - lo
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        c[0] += 1
        if a[j] < buf[i]:
            a[k] = a[j]
            j += 1
        else:
            a[k] = buf[i]
            i += 1
        k += 1
        c[1] += 1
    while i < mid:
        a[k] = buf[i]
        i += 1
        k += 1
        c[1] += 1

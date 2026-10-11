"""Tasks 6-7 - evaluates C(n) = C(floor(n/2)) + 1, C(1) = 1 and compares it with the code's own counter."""
import math
from common import *
from algo2_binary import binary_search


def C(n):
    return 1 if n <= 1 else C(n // 2) + 1


if __name__ == "__main__":
    banner("TASKS 6-7 - Recurrence C(n) = C(floor(n/2)) + 1 versus floor(log2 n) + 1 versus measured worst case")
    print(f"{'n':>10} {'C(n) recurrence':>16} {'floor(log2 n)+1':>16} {'measured worst':>15}  match")
    ok = True
    for n in (1, 2, 3, 7, 8, 15, 16, 100, 1000, 10_000, 100_000, 1_000_000):
        s = list(range(n))
        worst = max(binary_search(s, k)[1] for k in list(range(-1, n + 1, max(1, n // 4000))) + [n - 1, 0, n])
        f = int(math.log2(n)) + 1
        good = C(n) == f == worst
        ok &= good
        print(f"{n:>10,} {C(n):>16} {f:>16} {worst:>15}  {good}")
    print("-" * 66)
    print("all rows agree" if ok else "MISMATCH")

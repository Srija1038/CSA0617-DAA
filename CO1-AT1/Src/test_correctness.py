"""Task 8 - correctness tests of all three algorithms against an independent oracle."""
import random, sys
from common import *
from algo1_linear import linear_search
from algo2_binary import binary_search, binary_search_iter
from algo3_hash_probing import ProbingTable

checks = fails = 0


def check(cond):
    global checks, fails
    checks += 1
    if not cond: fails += 1


def run_size(n):
    data = make_dataset(n)
    srt = sorted(data)
    oracle = {k: p for p, k in enumerate(data)}      # independent oracle (dictionary)
    ht = ProbingTable(data)
    rng = random.Random(SEED)
    found = [OWN_KEY, data[0], data[-1], srt[0], srt[-1], srt[n // 2]] + rng.sample(data, 20)
    free = next(x for x in range(srt[n // 2] + 1, srt[n // 2] + 100) if x not in oracle)
    absent = [MISSING_KEY, 0, srt[0] - 1, srt[-1] + 1, 999_999_999, free]
    absent = [k for k in absent if k not in oracle]
    nf = nn = 0
    for k in found:
        pl, _ = linear_search(data, k)
        pb, _ = binary_search(srt, k)
        ph, _ = ht.search(k)
        check(pl == oracle[k]); check(srt[pb] == k and pb != -1); check(data[ph] == k)
        check(binary_search_iter(srt, k) == pb); nf += 1
    for k in absent:
        check(linear_search(data, k)[0] == -1); check(binary_search(srt, k)[0] == -1)
        check(ht.search(k)[0] == -1); check(binary_search_iter(srt, k) == -1); nn += 1
    own = linear_search(data, OWN_KEY)[0] != -1 and binary_search(srt, OWN_KEY)[0] != -1 and ht.search(OWN_KEY)[0] != -1
    nxt = linear_search(data, MISSING_KEY)[0] != -1 or binary_search(srt, MISSING_KEY)[0] != -1 or ht.search(MISSING_KEY)[0] != -1
    return nf, nn, own, nxt


if __name__ == "__main__":
    banner("TASK 8 - Correctness tests: Linear | Binary (recursive + iterative check) | Hash (linear probing)")
    check(linear_search([], 5)[0] == -1); check(binary_search([], 5)[0] == -1); check(ProbingTable([]).search(5)[0] == -1)
    check(linear_search([7], 7)[0] == 0); check(binary_search([7], 7)[0] == 0); check(ProbingTable([7]).search(7)[0] == 0)
    check(linear_search([7], 8)[0] == -1); check(binary_search([7], 8)[0] == -1); check(ProbingTable([7]).search(8)[0] == -1)
    print(f"edge cases (empty list, single record)           -> {'ALL PASS' if fails == 0 else 'FAIL'}")
    for n in (1_000, 10_000, 100_000, 1_000_000):
        before, f0 = checks, fails
        nf, nn, own, nxt = run_size(n)
        print(f"n = {n:>9,} | found keys {nf}, not-found keys {nn} | own reg no found: {own} | reg no+1 found: {nxt}"
              f" | checks {checks - before:>3} -> {'ALL PASS' if fails == f0 else 'FAIL'}")
    print("=" * 78)
    print(f"TOTAL checks: {checks} | passed: {checks - fails} | failed: {fails}")
    print("RESULT: ALL ALGORITHMS CORRECT" if fails == 0 else "RESULT: FAILURES FOUND")
    sys.exit(1 if fails else 0)

"""Task 9 - experimental performance of the three algorithms (python benchmark.py --n 1000)."""
import argparse, json, os, random, tracemalloc, gc
from common import *
from algo1_linear import linear_search
from algo2_binary import binary_search
from algo3_hash_probing import ProbingTable

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")


def measure(fn, keys):
    """Average time (microseconds) and average comparisons per query, plus worst comparisons."""
    t0 = timer(); tot = worst = 0
    for k in keys:
        _, c = fn(k)
        tot += c
        if c > worst: worst = c
    dt = timer() - t0
    return dt / len(keys) * 1e6, tot / len(keys), worst


def run(n):
    data = make_dataset(n)
    rng = random.Random(SEED + 1)
    present = set(data)
    nq = 1000 if n <= 10_000 else (300 if n <= 100_000 else 100)
    def strat(m):                      # stratified random sample: one random record from each of m equal blocks
        return [data[rng.randrange(j * n // m, (j + 1) * n // m)] for j in range(m)]
    found = [OWN_KEY] + strat(999)
    lin_found = [OWN_KEY] + strat(nq - 1)
    missing = [MISSING_KEY]
    while len(missing) < 1000:
        x = rng.randrange(100_000_000, 1_000_000_000)
        if x not in present: missing.append(x)
    out = {"n": n}

    # --- preprocessing (sort / hash build) -------------------------------------------------
    gc.collect(); reps = 3 if n <= 10_000 else 1
    best = 1e9
    for _ in range(reps):
        t0 = timer(); srt = sorted(data); best = min(best, timer() - t0)
    out["sort_ms"] = best * 1e3
    best = 1e9
    for _ in range(reps):
        t0 = timer(); ht = ProbingTable(data); best = min(best, timer() - t0)
    out["hash_build_ms"] = best * 1e3
    out["hash_m"], out["hash_load"], out["hash_longest_probe"] = ht.m, ht.load, ht.longest_probe

    # --- extra memory (peak of the structure itself) ---------------------------------------
    tracemalloc.start(); s2 = sorted(data); out["sort_mem_mb"] = tracemalloc.get_traced_memory()[0] / 1e6
    tracemalloc.stop(); del s2
    tracemalloc.start(); h2 = ProbingTable(data); out["hash_mem_mb"] = tracemalloc.get_traced_memory()[0] / 1e6
    tracemalloc.stop(); del h2

    # --- search -----------------------------------------------------------------------------
    r = {}
    r["linear"] = (measure(lambda k: linear_search(data, k), lin_found) +
                   measure(lambda k: linear_search(data, k), missing[:nq]))
    r["binary"] = (measure(lambda k: binary_search(srt, k), found) +
                   measure(lambda k: binary_search(srt, k), missing))
    r["hash"] = (measure(ht.search, found) + measure(ht.search, missing))
    keys = ("t_found", "c_found", "w_found", "t_miss", "c_miss", "w_miss")
    for alg, v in r.items():
        out[alg] = dict(zip(keys, v))
    # exact average over EVERY stored key (comparison counts only, no timing)
    out["binary"]["exact_c_found"] = sum(binary_search(srt, k)[1] for k in data) / n
    out["hash"]["exact_c_found"] = sum(ht.search(k)[1] for k in data) / n
    # exact best cases
    out["linear"]["best"] = linear_search(data, data[0])[1]
    out["binary"]["best"] = binary_search(srt, srt[(len(srt) - 1) // 2])[1]
    out["hash"]["best"] = 1
    out["queries"] = {"linear": nq, "binary": 1000, "hash": 1000}
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, required=True)
    n = ap.parse_args().n
    banner(f"TASK 9 - Benchmark: Linear (iterative) | Binary (recursive) | Hash (linear probing)  n = {n:,}")
    o = run(n)
    print(f"Dataset size n = {n:,}  (seed {SEED}; own reg no {OWN_KEY} = found, {MISSING_KEY} = not found)")
    print(f"{'Algorithm':<26}{'prep(ms)':>10}{'us/found':>11}{'us/miss':>11}{'cmp(found)':>13}{'cmp(miss)':>13}{'best':>6}{'worst':>11}")
    prep = {"linear": 0.0, "binary": o["sort_ms"], "hash": o["hash_build_ms"]}
    names = {"linear": "Linear search", "binary": "Binary search (recursive)", "hash": "Hash (linear probing)"}
    for a in ("linear", "binary", "hash"):
        d = o[a]; worst = max(d["w_found"], d["w_miss"], o["hash_longest_probe"] if a == "hash" else 0)
        print(f"{names[a]:<26}{prep[a]:>10.2f}{d['t_found']:>11.2f}{d['t_miss']:>11.2f}{d['c_found']:>13,.2f}{d['c_miss']:>13,.2f}{d['best']:>6}{worst:>11,}")
    print(f"(hash table: m = {o['hash_m']:,} slots, load factor = {o['hash_load']:.3f}, longest probe sequence = {o['hash_longest_probe']};")
    print(f" timings = mean per query; queries: linear {o['queries']['linear']}, binary/hash 1000)")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(o, open(os.path.join(RESULTS, f"bench_{n}.json"), "w"), indent=1)
    print(f"\nresults saved to results/bench_{n}.json")

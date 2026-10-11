"""Task 12 - Day-4 design challenge: 50,000 searches per hour on 1,000,000 records, daily updates."""
import heapq, json, os, random
from common import *
from algo1_linear import linear_search
from algo2_binary import binary_search
from algo3_hash_probing import ProbingTable

N, Q, K_NEW = 1_000_000, 50_000, 5_000
RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")

if __name__ == "__main__":
    banner(f"TASK 12 - Design challenge benchmark: {Q:,} searches on {N:,} records, new records once per day")
    data = make_dataset(N); present = set(data)
    rng = random.Random(SEED + 12)
    nf = int(Q * 0.9)
    found = [OWN_KEY] + rng.sample(data, nf - 1)
    missing = [MISSING_KEY]
    while len(missing) < Q - nf:
        x = rng.randrange(100_000_000, 1_000_000_000)
        if x not in present: missing.append(x)
    queries = found + missing; rng.shuffle(queries)

    t0 = timer(); srt = sorted(data); sort_s = timer() - t0
    t0 = timer(); ht = ProbingTable(data); build_s = timer() - t0
    t0 = timer(); [binary_search(srt, k) for k in queries]; bin_s = timer() - t0
    t0 = timer(); [ht.search(k) for k in queries]; hash_s = timer() - t0
    lin_q = [found[j * len(found) // 90] for j in range(90)] + missing[:10]      # 90 stratified found + 10 missing
    t0 = timer(); [linear_search(data, k) for k in lin_q]; lin_per = (timer() - t0) / len(lin_q)
    lin_s = lin_per * Q                                    # projected from 100 measured searches

    # daily update: k new records arrive once per day
    new = []
    while len(new) < K_NEW:
        x = rng.randrange(100_000_000, 1_000_000_000)
        if x not in present: present.add(x); new.append(x)
    t0 = timer(); sorted(data + new); resort_s = timer() - t0                 # re-sort everything from scratch
    t0 = timer(); nsorted = sorted(new); merged_py = list(heapq.merge(srt, nsorted)); heap_s = timer() - t0
    t0 = timer(); merged_ts = srt + nsorted; merged_ts.sort(); runs_s = timer() - t0   # two sorted runs -> one linear merge
    ok = merged_py == merged_ts == sorted(data + new)
    t0 = timer(); ProbingTable(data + new); rebuild_s = timer() - t0

    day = 24
    res = dict(N=N, Q=Q, K=K_NEW, sort_s=sort_s, build_s=build_s, bin_s=bin_s, hash_s=hash_s, lin_per_us=lin_per * 1e6,
               lin_s=lin_s, resort_s=resort_s, heap_merge_s=heap_s, runs_merge_s=runs_s, rebuild_s=rebuild_s, merge_ok=ok,
               bin_per_us=bin_s / Q * 1e6, hash_per_us=hash_s / Q * 1e6,
               bin_rate=Q / bin_s, hash_rate=Q / hash_s, lin_rate=1 / lin_per,
               day_lin=lin_s * day, day_bin=sort_s + bin_s * day, day_hash=build_s + hash_s * day)
    json.dump(res, open(os.path.join(RESULTS, "task12.json"), "w"), indent=1)
    print(f"{'Design':<28}{'prep(s)':>9}{f'{Q:,} searches(s)':>20}{'per search(us)':>16}{'searches/s':>13}{'one day(s)':>12}")
    print(f"{'Linear (projected, 100 meas.)':<28}{0:>9.2f}{lin_s:>20.2f}{lin_per*1e6:>16.2f}{1/lin_per:>13,.0f}{res['day_lin']:>12,.0f}")
    print(f"{'Binary search (original)':<28}{sort_s:>9.2f}{bin_s:>20.2f}{res['bin_per_us']:>16.2f}{res['bin_rate']:>13,.0f}{res['day_bin']:>12.2f}")
    print(f"{'Hash (linear probing)':<28}{build_s:>9.2f}{hash_s:>20.2f}{res['hash_per_us']:>16.2f}{res['hash_rate']:>13,.0f}{res['day_hash']:>12.2f}")
    print()
    print(f"daily update with k = {K_NEW:,} new records (merged result identical to full sort: {ok})")
    print(f"  full re-sort of {N+K_NEW:,} records            : {resort_s:.3f} s")
    print(f"  sort new batch + heapq.merge (pure Python)    : {heap_s:.3f} s")
    print(f"  old run + new run concatenated, then .sort()  : {runs_s:.3f} s   (Timsort merges the two runs in linear time)")
    print(f"  rebuild of the hash table                     : {rebuild_s:.3f} s")

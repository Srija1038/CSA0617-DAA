"""Shared helpers: student identity banner, dataset generator, timing."""
import random, time
from datetime import datetime

NAME, REG, SEED = "T. Srija", 192525223, 5223      # seed = last four digits of the reg. no.
OWN_KEY, MISSING_KEY = REG, REG + 1                # found-test key and not-found-test key


def banner(title):
    print(f"Reg No: {REG} | Name: {NAME} | Seed: {SEED} | {datetime.now():%d-%m-%Y %H:%M:%S}")
    print(title)
    print("=" * 78)


def make_dataset(n, seed=SEED):
    """n unique 9-digit registration numbers in random order.
    Always contains OWN_KEY and never contains MISSING_KEY."""
    rng = random.Random(seed + n)
    pool = set(rng.sample(range(100_000_000, 1_000_000_000), n))
    pool.discard(MISSING_KEY)
    pool.discard(OWN_KEY)
    data = list(pool)
    while len(data) < n - 1:
        x = rng.randrange(100_000_000, 1_000_000_000)
        if x not in (OWN_KEY, MISSING_KEY) and x not in pool:
            pool.add(x); data.append(x)
    data = data[:n - 1]
    rng.shuffle(data)
    data.insert(rng.randrange(len(data) + 1), OWN_KEY)
    return data


def timer():
    return time.perf_counter()

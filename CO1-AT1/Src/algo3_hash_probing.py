"""Algorithm 3 - hash table with open addressing (linear probing), static (build once, then search)."""


def next_prime(x):
    def is_prime(v):
        if v < 2: return False
        if v % 2 == 0: return v == 2
        d = 3
        while d * d <= v:
            if v % d == 0: return False
            d += 2
        return True
    while not is_prime(x):
        x += 1
    return x


class ProbingTable:
    EMPTY = -1

    def __init__(self, records, max_load=0.5):
        self.records = records                       # raw list; the table stores positions only
        self.m = next_prime(int(len(records) / max_load) + 1)
        self.slots = [self.EMPTY] * self.m
        self.longest_probe = 0
        m, slots = self.m, self.slots
        for p, k in enumerate(records):
            i, steps = k % m, 1
            while slots[i] != -1:                    # collision: step to the next slot
                i += 1
                if i == m: i = 0
                steps += 1
            slots[i] = p
            if steps > self.longest_probe: self.longest_probe = steps
        self.load = len(records) / m

    def search(self, key):
        """Return (position or -1, number of key comparisons)."""
        m, slots, rec = self.m, self.slots, self.records
        i, comps = key % m, 0
        while True:
            p = slots[i]
            if p == -1:                              # empty slot: key is absent
                return -1, comps
            comps += 1
            if rec[p] == key:                        # basic operation: key comparison
                return p, comps
            i += 1
            if i == m: i = 0

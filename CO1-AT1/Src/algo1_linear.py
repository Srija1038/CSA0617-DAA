"""Algorithm 1 - linear (sequential) search, iterative."""


def linear_search(a, key):
    """Return (position or -1, number of key comparisons)."""
    comps = 0
    for i in range(len(a)):
        comps += 1
        if a[i] == key:                # basic operation: key comparison
            return i, comps
    return -1, comps

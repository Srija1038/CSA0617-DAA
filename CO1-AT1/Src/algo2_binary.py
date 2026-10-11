"""Algorithm 2 - binary search, recursive (the iterative twin is used only as a cross-check)."""


def binary_search(s, key, low=0, high=None, comps=0):
    """s must be sorted.  Return (position or -1, number of key comparisons)."""
    if high is None:
        high = len(s) - 1
    if low > high:                     # base case: empty range
        return -1, comps
    mid = (low + high) // 2
    comps += 1
    if s[mid] == key:                  # basic operation: key comparison
        return mid, comps
    if s[mid] < key:
        return binary_search(s, key, mid + 1, high, comps)
    return binary_search(s, key, low, mid - 1, comps)


def binary_search_iter(s, key):
    low, high = 0, len(s) - 1
    while low <= high:
        mid = (low + high) // 2
        if s[mid] == key:
            return mid
        if s[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1

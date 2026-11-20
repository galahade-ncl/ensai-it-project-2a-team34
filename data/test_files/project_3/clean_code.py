import hashlib

# ---------------------------------------------------------------------------
# F3: clean code (should get a good score)
# ---------------------------------------------------------------------------


def sum_squares_efficient(n):
    """Closed-form formula: O(1)."""
    return n * (n + 1) * (2 * n + 1) // 6


def binary_search(sorted_items, target):
    """Binary search: O(log n)."""
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        if sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def sha256_of(text):
    return hashlib.sha256(text.encode()).hexdigest()

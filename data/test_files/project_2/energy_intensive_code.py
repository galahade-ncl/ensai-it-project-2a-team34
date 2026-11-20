"""
Sample project for testing CleanOps.
"""

import os

# ---------------------------------------------------------------------------
# F3: Energy-Intensive Anti-Patterns
# ---------------------------------------------------------------------------


def fib_recursive(n):
    """Recursive Fibonacci: exponential complexity O(2^n)."""
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def factorial_recursive(n):
    """Simple recursion: O(n)."""
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def find_duplicates_quadratic(items):
    """Two nested loops: O(n^2)."""
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates


def matrix_multiply_cubic(a, b):
    """Three nested loops: O(n^3)."""
    size = len(a)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += a[i][k] * b[k][j]
    return result


def build_string_slow(n):
    """Concatenation in a loop (repeated reallocations)."""
    text = ""
    for i in range(n):
        text = text + str(i) + ","
    return text


def busy_wait(flag_file):
    """Active waiting without sleep: wastes CPU resources."""
    while not os.path.exists(flag_file):
        pass

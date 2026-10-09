r"""
QUICKSORT -- with the Lomuto partition and a random pivot
CLRS 3rd ed., chapter 7 (pp. 171-180).

Notes: [[Quicksort — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Quicksort — Code Notes.md

What is in this file:
    1. partition              CLRS 7.1 (Lomuto)
    2. randomized_partition   CLRS 7.3
    3. quicksort              plain and randomized, chosen by a parameter
    4. comparison counts      sorted input: plain is n(n-1)/2, random is not
    5. tests

Run with:
    python3 Quicksort.py
"""

import random
import sys

# Section 4 sorts 1000 already-sorted elements with the plain pivot, which
# recurses 1000 levels deep. Python's default limit is 1000 frames.
sys.setrecursionlimit(5000)

# Counts every "A[j] <= x" comparison inside partition.
stats = {"comparisons": 0}


# =====================================================================
# 1. PARTITION [CLRS 7.1, p. 171]
# =====================================================================
#     PARTITION(A, p, r)
#     1 x = A[r]
#     2 i = p - 1
#     3 for j = p to r - 1
#     4     if A[j] <= x
#     5         i = i + 1
#     6         exchange A[i] with A[j]
#     7 exchange A[i + 1] with A[r]
#     8 return i + 1
#
# Notes: [[Quicksort — Code Notes#1. Partition]] (variables, loop invariant)

def partition(values, low, high):
    pivot = values[high]
    small_end = low - 1
    for scan in range(low, high):
        stats["comparisons"] += 1
        if values[scan] <= pivot:
            small_end += 1  # grow the "<= pivot" region by one
            values[small_end], values[scan] = values[scan], values[small_end]
    values[small_end + 1], values[high] = values[high], values[small_end + 1]
    return small_end + 1


# =====================================================================
# 2. RANDOM PIVOT [CLRS 7.3, p. 179]
# =====================================================================
#     RANDOMIZED-PARTITION(A, p, r)
#     1 i = RANDOM(p, r)
#     2 exchange A[r] with A[i]
#     3 return PARTITION(A, p, r)
#
# chosen: a random position in low..high; its value becomes the pivot

def randomized_partition(values, low, high):
    chosen = random.randint(low, high)
    values[high], values[chosen] = values[chosen], values[high]
    return partition(values, low, high)


# =====================================================================
# 3. QUICKSORT [CLRS 7.1, p. 171 and 7.3, p. 179]
# =====================================================================
# Notes: [[Quicksort — Code Notes#3. Quicksort]] (variables, base case)

def quicksort(values, low, high, split_pivot=randomized_partition):
    if low < high:
        pivot_position = split_pivot(values, low, high)
        quicksort(values, low, pivot_position - 1, split_pivot)
        quicksort(values, pivot_position + 1, high, split_pivot)


def quicksorted(values, split_pivot=randomized_partition):
    # returns a sorted copy, leaving the caller's list alone
    working_copy = list(values)
    quicksort(working_copy, 0, len(working_copy) - 1, split_pivot)
    return working_copy


# =====================================================================
# 4. THE WORST CASE, COUNTED
# =====================================================================
# Notes: [[Quicksort — Code Notes#4. The worst case, counted]]

def count_comparisons(values, split_pivot):
    stats["comparisons"] = 0
    quicksorted(values, split_pivot)
    return stats["comparisons"]


def show_worst_case():
    print("\nComparisons on ALREADY SORTED input (CLRS 7.4.1)")
    print(f"  {'n':>5}  {'plain pivot':>11}  {'n(n-1)/2':>9}  {'random pivot':>12}"
          f"  {'expected':>9}")
    random.seed(1)
    for size in [10, 100, 250, 500, 1000]:
        already_sorted = list(range(size))
        plain_count = count_comparisons(already_sorted, partition)
        random_count = count_comparisons(already_sorted, randomized_partition)
        harmonic = sum(1 / term for term in range(1, size + 1))
        expected = 2 * (size + 1) * harmonic - 4 * size
        print(f"  {size:>5}  {plain_count:>11}  {size * (size - 1) // 2:>9}"
              f"  {random_count:>12}  {expected:>9.0f}")


# =====================================================================
# 5. TESTS -- checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([42], "one element"),
        ([3, 1, 3, 2, 3, 1], "duplicates"),
        ([7, 7, 7, 7, 7], "all equal"),
        ([1, 2, 3, 4, 5, 6], "already sorted"),
        ([6, 5, 4, 3, 2, 1], "reversed"),
        ([2, 8, 7, 1, 3, 5, 6, 4], "CLRS figure 7.1"),
        ([-5, 0, 12, -3, 8], "negatives"),
    ]

    for values, description in test_cases:
        check(f"random pivot {values} ({description})", quicksorted(values), sorted(values))
        check(f"plain pivot  {values} ({description})",
              quicksorted(values, partition), sorted(values))

    # CLRS figure 7.1: one PARTITION call around the last element, 4
    figure_values = [2, 8, 7, 1, 3, 5, 6, 4]
    figure_pivot_position = partition(figure_values, 0, 7)
    check("CLRS figure 7.1 after one partition", figure_values, [2, 1, 3, 4, 7, 5, 6, 8])
    check("  pivot 4 lands at position", figure_pivot_position, 3)

    original = [9, 4, 7, 1]
    quicksorted(original)
    check("caller's list untouched", original, [9, 4, 7, 1])

    for split_pivot, name in [(randomized_partition, "random"), (partition, "plain")]:
        random_failures = 0
        for trial in range(300):
            length = random.randint(0, 80)
            values = [random.randint(-30, 30) for position in range(length)]
            if quicksorted(values, split_pivot) != sorted(values):
                random_failures += 1
        check(f"300 random lists, {name} pivot: mismatches", random_failures, 0)

    show_worst_case()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

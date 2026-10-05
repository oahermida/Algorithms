r"""
QUICKSORT -- with the Lomuto partition and a random pivot
=========================================================

Advanced Algorithms: quicksort is listed but not re-taught. Lecture 1, slide 11
puts it under Programming Fundamentals with "O(n^2) w.c. / O(n log n) ave.c.".
Lecture 2, slide 36 lists it as a divide-and-conquer algorithm. Lecture 6-7,
slides 6 and 14 come back to it through QuickSelect and median of medians.
The pseudocode here is CLRS 3rd ed., chapter 7: QUICKSORT and PARTITION
(section 7.1, p. 171), RANDOMIZED-QUICKSORT (section 7.3, p. 179), worst case
(section 7.4.1, p. 180).

The partition procedure is the same one ../../Order_Statistics/QuickSelect/
QuickSelect.py uses for slide 7's "split" step. Quicksort recurses into BOTH
sides of the split; QuickSelect recurses into one.

    QUICKSORT(A, p, r)                       [CLRS p. 171]
    1 if p < r
    2     q = PARTITION(A, p, r)
    3     QUICKSORT(A, p, q - 1)
    4     QUICKSORT(A, q + 1, r)

Divide and conquer, but backwards from merge sort:
    merge sort:  split blindly in the middle,   do the real work when merging
    quicksort:   do the real work when splitting, combining needs nothing
After PARTITION the pivot is in its final place, everything left of it is <= it
and everything right of it is > it. Sort the two sides and the whole piece is
sorted. There is no merge step.


WHERE THE PIVOT LANDS DECIDES EVERYTHING
----------------------------------------
    balanced split every time:  T(n) = 2T(n/2) + Theta(n)  =  Theta(n log n)
    1 : n-1 split every time:   T(n) = T(n-1) + Theta(n)   =  Theta(n^2)

The second line is what happens to the plain version on SORTED input. The pivot
is always the last element, which is always the maximum of its piece. The split
leaves n-1 elements on the left and nothing on the right. Each level removes
only the pivot, so the comparisons add up to
    (n-1) + (n-2) + ... + 1  =  n(n-1)/2.
Reversed input does the same, with the pivot always the minimum. Section 4
counts it.

THE RANDOM PIVOT (CLRS 7.3) swaps a random element into the last spot before
partitioning. Now no fixed input is bad: sorted, reversed or anything else gets
expected O(n log n) comparisons (about 1.39 n log2 n for large n; CLRS 7.4.2
proves O(n lg n)). The worst case is still n^2, but only through bad luck, not
through a bad input.

Lecture 6-7, slide 14 mentions the third option: pick the exact median as the
pivot with median of medians. That guarantees O(n log n) in the worst case,
"however, generally there is no need to do this on practice."


STABILITY AND DUPLICATES
------------------------
Quicksort is NOT stable: the long-distance swaps in partition can reorder equal
keys. (Compare ../Counting_Sort/Counting_Sort.py, which is.)
With the Lomuto partition, an array of identical values is ALSO a worst case:
every element is <= the pivot, so the split is n-1 : 0 again. CLRS problem 7-2
fixes that with a three-way partition; that is beyond the course.


WHAT IS IN THIS FILE
--------------------
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
# values: the list, rearranged in place
# low, high: the piece being split, both ends included (CLRS p, r)
# pivot: the value everything is compared with; always values[high] (CLRS x)
# small_end: last position of the "<= pivot" region (CLRS i)
# scan: the position being looked at (CLRS j)
#
# The loop invariant (CLRS p. 171) -- at the start of every pass:
#   low .. small_end          all <= pivot
#   small_end+1 .. scan-1     all >  pivot
#   high                      the pivot
# A value <= pivot found at scan is swapped to the front of the "> pivot"
# region, and that region shifts one step right. At the end the pivot swaps into
# small_end + 1, its final sorted position.

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
# values: the list, sorted in place
# low, high: the piece to sort, both ends included (CLRS p, r)
# split_pivot: which partition to use -- randomized_partition (default) or the
#              plain partition, which always picks the last element
# pivot_position: where the pivot ended up (CLRS q); it never moves again
#
# A piece with 0 or 1 elements (low >= high) is already sorted, which is the
# base case. The pivot itself is left out of both recursive calls.

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
# Sorted input, both pivots. For the plain pivot the count matches n(n-1)/2
# exactly. For the random pivot one run is shown next to the exact average
# for distinct keys, 2(n+1)H(n) - 4n, where H(n) = 1 + 1/2 + ... + 1/n.
# That average grows like 1.39 n log2 n.
#
# harmonic: H(n)
# expected: the average number of comparisons over all random pivot choices

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

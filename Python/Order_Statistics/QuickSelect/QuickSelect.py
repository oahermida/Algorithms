r"""
QUICKSELECT -- the k-th smallest element in expected O(n)
Lecture 6-7, slides 3-9; CLRS 3rd ed., section 9.2 (p. 216).

Notes: [[QuickSelect — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/QuickSelect — Code Notes.md

What is in this file:
    1. partition             CLRS 7.1 (Lomuto), the "split" step
    2. randomized_partition  CLRS 7.3, random pivot then partition
    3. quick_select          the slide 7 algorithm, typo fixed
    4. kth_smallest          a wrapper that copies the input and uses ranks 1..n
    5. comparison counts     expected linear vs. the forced quadratic case
    6. slide 3's shop        the median minimises the total distance
    7. tests

Run with:
    python3 QuickSelect.py
"""

import random

# Counts every "A[j] <= x" comparison inside partition, so section 5 can show
# the running time instead of just claiming it.
stats = {"comparisons": 0}


# =====================================================================
# 1. PARTITION -- the "split" step [CLRS 7.1, p. 171]
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
# Notes: [[QuickSelect — Code Notes#1. Partition — the "split" step]] (variables, the four regions)

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
# 2. RANDOM PIVOT [slide 7 line 4; CLRS 7.3, p. 179]
# =====================================================================
#     RANDOMIZED-PARTITION(A, p, r)
#     1 i = RANDOM(p, r)
#     2 exchange A[r] with A[i]
#     3 return PARTITION(A, p, r)
#
# Notes: [[QuickSelect — Code Notes#2. Random pivot]] (variables)

def randomized_partition(values, low, high):
    chosen = random.randint(low, high)
    values[high], values[chosen] = values[chosen], values[high]
    return partition(values, low, high)


# =====================================================================
# 3. QUICKSELECT [slide 7; CLRS RANDOMIZED-SELECT, p. 216]
# =====================================================================
# Notes: [[QuickSelect — Code Notes#3. Quickselect]] (variables, the three outcomes)

def quick_select(values, low, high, wanted_rank, split_pivot=randomized_partition):
    if low == high:  # one element left: it must be the answer
        return values[low]
    pivot_position = split_pivot(values, low, high)
    pivot_rank = pivot_position - low + 1
    if wanted_rank == pivot_rank:
        return values[pivot_position]  # the slide writes A[l] here; it means A[j]
    if wanted_rank < pivot_rank:
        return quick_select(values, low, pivot_position - 1, wanted_rank, split_pivot)
    return quick_select(values, pivot_position + 1, high,
                        wanted_rank - pivot_rank, split_pivot)


# =====================================================================
# 4. A FRIENDLY WRAPPER
# =====================================================================
# quick_select scrambles its list. This copies first, so the caller's list is
# left alone, and checks the rank is in range. Rank 1 is the minimum, rank
# len(values) the maximum.

def kth_smallest(values, wanted_rank, split_pivot=randomized_partition):
    if not 1 <= wanted_rank <= len(values):
        raise ValueError("wanted_rank must be between 1 and len(values)")
    working_copy = list(values)
    return quick_select(working_copy, 0, len(working_copy) - 1, wanted_rank, split_pivot)


def median(values):
    # the lower median, rank ceil(n/2), the same convention CLRS uses
    return kth_smallest(values, (len(values) + 1) // 2)


# =====================================================================
# 5. HOW MUCH WORK -- slide 8 and slide 9, measured
# =====================================================================
# Notes: [[QuickSelect — Code Notes#5. How much work — slide 8 and slide 9, measured]]

def count_comparisons(values, wanted_rank, split_pivot):
    stats["comparisons"] = 0
    kth_smallest(values, wanted_rank, split_pivot)
    return stats["comparisons"]


def show_work():
    print("\nComparisons made (slide 8: expected O(n); slide 9: worst case O(n^2))")
    print(f"  {'n':>6}  {'random pivot, median':>22}  {'per element':>11}"
          f"  {'last pivot, sorted, min':>24}  {'n(n-1)/2':>9}")
    random.seed(7)
    for size in [100, 200, 400, 800]:
        shuffled = random.sample(range(size), size)
        random_count = count_comparisons(shuffled, (size + 1) // 2, randomized_partition)
        worst_count = count_comparisons(list(range(size)), 1, partition)
        print(f"  {size:>6}  {random_count:>22}  {random_count / size:>11.2f}"
              f"  {worst_count:>24}  {size * (size - 1) // 2:>9}")


# =====================================================================
# 6. SLIDE 3: WHERE TO OPEN THE SHOP
# =====================================================================
# Notes: [[QuickSelect — Code Notes#6. Slide 3 — where to open the shop]] (problem statement, why the median)

def total_distance(shop, houses):
    return sum(abs(shop - house) for house in houses)


def show_shop():
    houses = [1, 2, 6, 7, 30]
    best = median(houses)
    average = sum(houses) / len(houses)
    print("\nSlide 3: houses at", houses)
    print(f"  shop at the median  {best}:    total distance {total_distance(best, houses)}")
    print(f"  shop at the average {average}:  total distance {total_distance(average, houses):g}")


# =====================================================================
# 7. TESTS -- every rank checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


def all_ranks(values, split_pivot=randomized_partition):
    # the k-th smallest for every k, which should rebuild sorted(values)
    return [kth_smallest(values, rank, split_pivot) for rank in range(1, len(values) + 1)]


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([42], "one element"),
        ([3, 1, 3, 2, 3, 1], "duplicates"),
        ([7, 7, 7, 7], "all equal"),
        ([1, 2, 3, 4, 5, 6], "already sorted"),
        ([6, 5, 4, 3, 2, 1], "reversed"),
        ([2, 8, 7, 1, 3, 5, 6, 4], "CLRS figure 7.1"),
        ([-5, 0, 12, -3, 8], "negatives"),
    ]

    for values, description in test_cases:
        check(f"all ranks of {values} ({description})", all_ranks(values), sorted(values))
        check(f"  same, last-element pivot", all_ranks(values, partition), sorted(values))

    check("median([5, 1, 4, 2, 3])", median([5, 1, 4, 2, 3]), 3)
    check("median([4, 1, 3, 2]) (lower median)", median([4, 1, 3, 2]), 2)

    original = [9, 4, 7, 1]
    kth_smallest(original, 2)
    check("caller's list untouched", original, [9, 4, 7, 1])

    # randomized: 300 lists, random lengths, many repeated values
    random_failures = 0
    for trial in range(300):
        length = random.randint(1, 60)
        values = [random.randint(-20, 20) for position in range(length)]
        wanted_rank = random.randint(1, length)
        if kth_smallest(values, wanted_rank) != sorted(values)[wanted_rank - 1]:
            random_failures += 1
    check("300 random lists, random rank: mismatches", random_failures, 0)

    show_work()
    show_shop()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

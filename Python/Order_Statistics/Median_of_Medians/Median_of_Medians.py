r"""
MEDIAN OF MEDIANS -- the k-th smallest element in WORST-CASE O(n)
Lecture 6-7, slides 9-14; CLRS 3rd ed., section 9.3 (pp. 220-222).

Notes: [[Median of Medians — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Median of Medians — Code Notes.md

What is in this file:
    1. insertion_sort_group  sort one group of at most 5 (CLRS step 2)
    2. partition_around      partition with a GIVEN pivot value (CLRS step 4)
    3. select                the slide 10-11 algorithm
    4. kth_smallest          a wrapper that copies the input and uses ranks 1..n
    5. group sizes           3, 5 and 7: worst-case recurrence and real runs
    6. tests

Run with:
    python3 Median_of_Medians.py
"""

import random

# Counts every comparison between two elements, for section 5.
stats = {"comparisons": 0}


# =====================================================================
# 1. SORT ONE SMALL GROUP [CLRS 9.3 step 2]
# =====================================================================
# Notes: [[Median of Medians — Code Notes#1. Sort one small group]] (variables, why O(n) over all groups)

def insertion_sort_group(group):
    for position in range(1, len(group)):
        current = group[position]
        slot = position - 1
        while slot >= 0:
            stats["comparisons"] += 1
            if group[slot] <= current:
                break
            group[slot + 1] = group[slot]  # shift the bigger value right
            slot -= 1
        group[slot + 1] = current


# =====================================================================
# 2. PARTITION AROUND A GIVEN VALUE [slide 11 "find position of x"; CLRS 9.3 step 4]
# =====================================================================
# Notes: [[Median of Medians — Code Notes#2. Partition around a given value]] (variables)

def partition_around(values, low, high, pivot_value):
    pivot_spot = values.index(pivot_value, low, high + 1)
    values[pivot_spot], values[high] = values[high], values[pivot_spot]
    small_end = low - 1
    for scan in range(low, high):
        stats["comparisons"] += 1
        if values[scan] <= pivot_value:
            small_end += 1
            values[small_end], values[scan] = values[scan], values[small_end]
    values[small_end + 1], values[high] = values[high], values[small_end + 1]
    return small_end + 1


# =====================================================================
# 3. SELECT -- the k-th smallest, worst-case O(n) [slides 10-11; CLRS 9.3]
# =====================================================================
# Notes: [[Median of Medians — Code Notes#3. Select — the k-th smallest, worst-case O(n)]] (variables, base case)

def select(values, low, high, wanted_rank, group_size=5):
    size = high - low + 1
    if size <= group_size:
        piece = values[low:high + 1]
        insertion_sort_group(piece)
        values[low:high + 1] = piece
        return values[low + wanted_rank - 1]

    # steps 1-2: split into groups and take each group's median
    medians = []
    for group_start in range(low, high + 1, group_size):
        group = values[group_start:min(group_start + group_size, high + 1)]
        insertion_sort_group(group)
        medians.append(group[(len(group) - 1) // 2])  # lower median of the group

    # step 3: first recursive call -- the median of the medians
    pivot_value = select(medians, 0, len(medians) - 1, (len(medians) + 1) // 2, group_size)

    # step 4: split the piece around x
    pivot_position = partition_around(values, low, high, pivot_value)
    pivot_rank = pivot_position - low + 1

    # step 5: second recursive call -- only on the side holding the answer
    if wanted_rank == pivot_rank:
        return values[pivot_position]
    if wanted_rank < pivot_rank:
        return select(values, low, pivot_position - 1, wanted_rank, group_size)
    return select(values, pivot_position + 1, high, wanted_rank - pivot_rank, group_size)


# =====================================================================
# 4. A FRIENDLY WRAPPER
# =====================================================================
# Copies first so the caller's list is left alone. Rank 1 is the minimum.

def kth_smallest(values, wanted_rank, group_size=5):
    if not 1 <= wanted_rank <= len(values):
        raise ValueError("wanted_rank must be between 1 and len(values)")
    working_copy = list(values)
    return select(working_copy, 0, len(working_copy) - 1, wanted_rank, group_size)


def median(values):
    return kth_smallest(values, (len(values) + 1) // 2)


# =====================================================================
# 5. WHY 5 -- groups of 3, 5 and 7 compared
# =====================================================================
# Notes: [[Median of Medians — Code Notes#5. Why 5 — groups of 3, 5 and 7 compared]] (the two tables, variables)

def worst_case_work(size, group_size, memo):
    if size <= group_size:
        return size
    if (size, group_size) not in memo:
        group_count = -(-size // group_size)  # ceiling division
        thrown_away = (group_size + 1) // 2 * (-(-group_count // 2))
        memo[(size, group_size)] = (size + worst_case_work(group_count, group_size, memo)
                                    + worst_case_work(size - thrown_away, group_size, memo))
    return memo[(size, group_size)]


def show_group_sizes():
    memo = {}
    print("\nWorst case from the recurrence: work per element (slides 12-13)")
    print(f"  {'n':>9}  {'groups of 3':>11}  {'groups of 5':>11}  {'groups of 7':>11}")
    for size in [10 ** exponent for exponent in range(2, 8)]:
        row = [worst_case_work(size, group_size, memo) / size for group_size in [3, 5, 7]]
        print(f"  {size:>9}  {row[0]:>11.2f}  {row[1]:>11.2f}  {row[2]:>11.2f}")

    print("\nReal runs on shuffled input: comparisons per element, finding the median")
    print(f"  {'n':>9}  {'groups of 3':>11}  {'groups of 5':>11}  {'groups of 7':>11}")
    random.seed(5)
    for size in [500, 2500, 12500, 62500]:
        shuffled = random.sample(range(size), size)
        row = []
        for group_size in [3, 5, 7]:
            stats["comparisons"] = 0
            kth_smallest(shuffled, (size + 1) // 2, group_size)
            row.append(stats["comparisons"] / size)
        print(f"  {size:>9}  {row[0]:>11.2f}  {row[1]:>11.2f}  {row[2]:>11.2f}")


# =====================================================================
# 6. TESTS -- every rank checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


def all_ranks(values, group_size=5):
    return [kth_smallest(values, rank, group_size) for rank in range(1, len(values) + 1)]


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([42], "one element"),
        ([3, 1, 3, 2, 3, 1, 2, 2, 3, 1, 1, 3], "duplicates"),
        ([7] * 13, "all equal"),
        (list(range(1, 18)), "already sorted"),
        (list(range(17, 0, -1)), "reversed"),
        ([3, 2, 9, 0, 7, 5, 4, 8, 6, 1], "CLRS exercise 9.2-4"),
        ([-5, 0, 12, -3, 8, 22, -9], "negatives"),
    ]

    for values, description in test_cases:
        check(f"all ranks of {values} ({description})", all_ranks(values), sorted(values))

    check("median of 0..24 shuffled", median(random.sample(range(25), 25)), 12)

    original = [9, 4, 7, 1, 8, 2, 6]
    kth_smallest(original, 3)
    check("caller's list untouched", original, [9, 4, 7, 1, 8, 2, 6])

    # randomized: lengths up to 200 so the recursion goes several levels deep
    for group_size in [3, 5, 7]:
        random_failures = 0
        for trial in range(200):
            length = random.randint(1, 200)
            values = [random.randint(-50, 50) for position in range(length)]
            wanted_rank = random.randint(1, length)
            if kth_smallest(values, wanted_rank, group_size) != sorted(values)[wanted_rank - 1]:
                random_failures += 1
        check(f"200 random lists, groups of {group_size}: mismatches", random_failures, 0)

    show_group_sizes()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

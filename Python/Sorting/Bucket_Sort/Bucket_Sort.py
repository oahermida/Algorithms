r"""
BUCKET SORT -- numbers in [0, 1), average O(n) when they are spread evenly
Lecture 6-7 (Ivan Bliznets), slides 45-48; CLRS 3rd ed., section 8.4 (p. 201).

Notes: [[Bucket Sort — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Bucket Sort — Code Notes.md

What is in this file:
    1. insertion_sort     the per-bucket sort, with a comparison counter
    2. bucket_sort        slide 46 / CLRS p. 201
    3. slide 47's table   printed from the code
    4. average vs worst   even spread vs everything in one bucket
    5. tests

Run with:
    python3 Bucket_Sort.py
"""

import random

# Counts comparisons inside insertion sort, for section 4.
stats = {"comparisons": 0}


# =====================================================================
# 1. INSERTION SORT FOR ONE BUCKET [CLRS 2.1]
# =====================================================================
# Notes: [[Bucket Sort — Code Notes#1. Insertion sort for one bucket]] (variables, stability)

def insertion_sort(bucket):
    for position in range(1, len(bucket)):
        current = bucket[position]
        slot = position - 1
        while slot >= 0:
            stats["comparisons"] += 1
            if bucket[slot] <= current:
                break
            bucket[slot + 1] = bucket[slot]  # shift the bigger value right
            slot -= 1
        bucket[slot + 1] = current


# =====================================================================
# 2. BUCKET SORT [slide 46; CLRS 8.4, p. 201]
# =====================================================================
#     BUCKET-SORT(A)
#     1 let B[0 .. n-1] be a new array
#     2 n = A.length
#     3 for i = 0 to n-1
#     4     make B[i] an empty list
#     5 for i = 1 to n
#     6     insert A[i] into list B[floor(n A[i])]
#     7 for i = 0 to n-1
#     8     sort list B[i] with insertion sort
#     9 concatenate the lists B[0], B[1], ..., B[n-1] together in order
#
# Notes: [[Bucket Sort — Code Notes#2. Bucket sort]] (variables)

def bucket_sort(values):
    for value in values:
        if not 0 <= value < 1:
            raise ValueError("bucket sort here needs values in [0, 1)")
    bucket_count = len(values)
    buckets = [[] for bucket_number in range(bucket_count)]

    for value in values:
        bucket_index = int(bucket_count * value)  # floor, since value >= 0
        buckets[bucket_index].append(value)

    for bucket in buckets:
        insertion_sort(bucket)

    result = []
    for bucket in buckets:
        result.extend(bucket)  # concatenate in bucket order
    return result


def fill_buckets(values):
    # only the distribution step, so section 3 can show B before sorting
    buckets = [[] for bucket_number in range(len(values))]
    for value in values:
        buckets[int(len(values) * value)].append(value)
    return buckets


# =====================================================================
# 3. SLIDE 47, FROM THE CODE
# =====================================================================

SLIDE_VALUES = [0.55, 0.26, 0.71, 0.99, 0.77, 0.52, 0.51, 0.81, 0.32, 0.44]


def show_slide_47():
    buckets = fill_buckets(SLIDE_VALUES)
    sorted_buckets = [sorted(bucket) for bucket in buckets]
    result = bucket_sort(SLIDE_VALUES)
    print("\nSlide 47")
    print(f"  {'':>2}  {'A':>5}  {'B':<18}  {'Sorted(B)':<18}  {'Sorted(A)':>9}")
    for row in range(len(SLIDE_VALUES)):
        unsorted_text = ", ".join(str(value) for value in buckets[row]) or "-"
        sorted_text = ", ".join(str(value) for value in sorted_buckets[row]) or "-"
        print(f"  {row:>2}  {SLIDE_VALUES[row]:>5}  {unsorted_text:<18}  {sorted_text:<18}"
              f"  {result[row]:>9}")


# =====================================================================
# 4. AVERAGE CASE vs WORST CASE [slide 48]
# =====================================================================
# Two inputs of the same size:
#   spread evenly      random values over [0, 1): buckets hold about 1 each
#   all in one bucket  every value in [0, 1/n): bucket 0 holds all n, and the
#                      values are in DESCENDING order, insertion sort's worst
# Comparisons per element stay flat for the first and grow with n for the
# second: n(n-1)/2 in total, so (n-1)/2 per element.

def count_comparisons(values):
    stats["comparisons"] = 0
    bucket_sort(values)
    return stats["comparisons"]


def show_average_vs_worst():
    print("\nInsertion-sort comparisons per element (slide 48)")
    print(f"  {'n':>6}  {'spread evenly':>13}  {'all in one bucket':>17}")
    random.seed(48)
    for size in [100, 400, 1600]:
        spread = [random.random() for position in range(size)]
        crowded = [(size - position) / (size * size + 1) for position in range(size)]
        print(f"  {size:>6}  {count_comparisons(spread) / size:>13.2f}"
              f"  {count_comparisons(crowded) / size:>17.2f}")


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
        ([0.5], "one element"),
        ([0.3, 0.1, 0.3, 0.7, 0.1], "duplicates"),
        ([0.25, 0.25, 0.25], "all equal"),
        ([0.0, 0.1, 0.2, 0.9], "already sorted"),
        ([0.9, 0.6, 0.3, 0.0], "reversed"),
        (SLIDE_VALUES, "slide 47"),
        ([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68], "CLRS figure 8.4"),
        ([0.01, 0.02, 0.03, 0.04], "all in bucket 0"),
    ]

    for values, description in test_cases:
        check(f"bucket_sort {values} ({description})", bucket_sort(values), sorted(values))

    check("slide 47 bucket 5 before sorting", fill_buckets(SLIDE_VALUES)[5], [0.55, 0.52, 0.51])

    original = [0.3, 0.1, 0.2]
    bucket_sort(original)
    check("caller's list untouched", original, [0.3, 0.1, 0.2])

    random_failures = 0
    for trial in range(300):
        length = random.randint(0, 100)
        values = [random.random() for position in range(length)]
        if bucket_sort(values) != sorted(values):
            random_failures += 1
    check("300 random lists, uniform: mismatches", random_failures, 0)

    random_failures = 0
    for trial in range(300):
        length = random.randint(0, 60)
        values = [random.randint(0, 9) / 10 for position in range(length)]  # many repeats
        if bucket_sort(values) != sorted(values):
            random_failures += 1
    check("300 random lists, one decimal place: mismatches", random_failures, 0)

    show_slide_47()
    show_average_vs_worst()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

"""
SELECTION SORT
==============

Advanced Algorithms, Lecture 2 (Ivan Bliznets), slides 3-7. Also CLRS (3rd
ed.) exercise 2.2-2, p. 29 -- CLRS only sets it as an exercise.

    Problem: sort given array of numbers                        [slide 3]

    Basic Idea: Divides the list into a sorted and an unsorted region,
    repeatedly selecting the smallest (or largest) element from the unsorted
    region and moving it to the sorted region.                  [slide 3]

    We can think of Selection Sort as recursive algorithm: find minimum, put
    on the first place, run recursively on the array of one size smaller.
    Running time: T(n) <= T(n - 1) + c * n                      [slide 3]

    Step-by-Step Process                                        [slide 4]
      1. Find the minimum element in the array.
      2. Place the minimum element just before unsorted part.
      3. Move the boundary between sorted and unsorted arrays one element to
         the right.
      4. Repeat until the entire array is sorted.

    Python Code                                                 [slide 5]
    for i from 0 to n-1:
        min_idx = i
        for j from i+1 to n:
            if arr[j] < arr[min_idx]:
                min_idx = j
        swap(arr[i], arr[min_idx])


THE PICTURE
-----------
The array is split by a boundary. Left of it: sorted, and final. Right of it:
not sorted yet.

    [ 1  2  3 | 9  5  7 ]       sorted | unsorted
                ^
    find the smallest on the right (5), swap it to the boundary:
    [ 1  2  3  5 | 9  7 ]
    the boundary moves one step right.

Every value left of the boundary is smaller than or equal to every value right
of it. So once a value crosses the boundary, it never moves again.


RUNNING TIME
------------
Unrolling T(n) <= T(n - 1) + c * n from slide 3:

    T(n) <= c*n + c*(n-1) + ... + c*1 = c * n(n+1)/2 = O(n^2)

It does that much work on EVERY input, even an already sorted one. Slide 7
calls this "not adaptive". Insertion sort, by contrast, is O(n) on sorted
input.


PROS AND CONS [slides 6-7]
--------------------------
    + O(n) swaps: at most one swap per position. Useful when writing is
      expensive.
    + In place: no extra memory.
    - O(n^2) comparisons, always.
    - Not stable: equal values may come out in a different order than they
      went in. Section 4 shows an example.


WHAT IS IN THIS FILE
--------------------
    1. selection_sort              slide 5's loop, in place
    2. selection_sort_recursive    slide 3's recursive description
    3. the swap count              slide 6's "O(n) swaps"
    4. why it is not stable        slide 7
    5. tests: hand cases and random cases, checked against Python's sorted()

Run with:
    python3 Selection_Sort.py
"""

import random


# =====================================================================
# 1. SELECTION SORT -- the loop [slide 5]
# =====================================================================
# boundary: i on the slide. Everything left of it is sorted and final.
# smallest_index: min_idx on the slide. Where the smallest value of the
#                 unsorted part is, as far as the scan has seen.
# scan_index: j on the slide. Walks over the unsorted part, looking for
#             anything smaller.
#
# The slide's "for j from i+1 to n" means up to n, not including n.
# Python's range(boundary + 1, len(values)) does exactly that.
#
# Sorts the list in place, and also returns it for convenience.

def selection_sort(values):
    for boundary in range(len(values)):
        smallest_index = boundary  # guess: the first unsorted value is smallest
        for scan_index in range(boundary + 1, len(values)):
            if values[scan_index] < values[smallest_index]:
                smallest_index = scan_index  # found something smaller
        values[boundary], values[smallest_index] = values[smallest_index], values[boundary]
    return values


# =====================================================================
# 2. SELECTION SORT -- recursive [slide 3]
# =====================================================================
# "find minimum, put on the first place, run recursively on the array of one
#  size smaller."
#
# start: where the unsorted part begins. The recursion moves it one step right
#        each call, which is "the array of one size smaller".
# smallest_index: where the minimum of values[start:] is
#
# Each call does c * n work (finding the minimum), then one recursive call on
# n - 1 values. That is exactly T(n) <= T(n - 1) + c * n.
#
# Note: Python's default recursion limit is about 1000. So this version is
# only for small lists. The loop above is the one to use.

def selection_sort_recursive(values, start=0):
    if start >= len(values) - 1:  # zero or one value left: already sorted
        return values
    smallest_index = start
    for scan_index in range(start + 1, len(values)):
        if values[scan_index] < values[smallest_index]:
            smallest_index = scan_index
    values[start], values[smallest_index] = values[smallest_index], values[start]
    return selection_sort_recursive(values, start + 1)


# =====================================================================
# 3. COUNTING THE WORK [slide 6]
# =====================================================================
# The same loop, but it counts comparisons and real swaps instead of only
# sorting.
#
# comparison_count: how many times two values were compared
# swap_count: how many swaps actually moved something. A "swap" of a value
#             with itself (smallest_index == boundary) is not counted.

def selection_sort_counted(values):
    comparison_count = 0
    swap_count = 0
    for boundary in range(len(values)):
        smallest_index = boundary
        for scan_index in range(boundary + 1, len(values)):
            comparison_count += 1
            if values[scan_index] < values[smallest_index]:
                smallest_index = scan_index
        if smallest_index != boundary:
            values[boundary], values[smallest_index] = values[smallest_index], values[boundary]
            swap_count += 1
    return comparison_count, swap_count


# =====================================================================
# 4. NOT STABLE [slide 7]
# =====================================================================
# Sort cards by their number only. Two cards have the number 5: "5 red" comes
# before "5 blue" in the input. A stable sort keeps that order. Selection sort
# does not, because the long-distance swap jumps one 5 over the other.
#
# cards: (number, colour) pairs. Same loop as section 1, but it compares
#        only the number.

def selection_sort_by_number(cards):
    for boundary in range(len(cards)):
        smallest_index = boundary
        for scan_index in range(boundary + 1, len(cards)):
            if cards[scan_index][0] < cards[smallest_index][0]:
                smallest_index = scan_index
        cards[boundary], cards[smallest_index] = cards[smallest_index], cards[boundary]
    return cards


print("=" * 72)
print("SELECTION SORT   -- Lecture 2, slides 3-7;  CLRS exercise 2.2-2")
print("=" * 72)

example = [64, 25, 12, 22, 11]
print(f"\ninput:  {example}")
working_copy = list(example)
for boundary in range(len(working_copy)):
    smallest_index = boundary
    for scan_index in range(boundary + 1, len(working_copy)):
        if working_copy[scan_index] < working_copy[smallest_index]:
            smallest_index = scan_index
    working_copy[boundary], working_copy[smallest_index] = (
        working_copy[smallest_index], working_copy[boundary])
    sorted_part = " ".join(str(value) for value in working_copy[:boundary + 1])
    unsorted_part = " ".join(str(value) for value in working_copy[boundary + 1:])
    print(f"  pass {boundary}: [ {sorted_part} | {unsorted_part} ]")

print("\nComparisons and swaps for n = 100:")
for label, values in (("already sorted", list(range(100))),
                      ("reversed", list(range(100, 0, -1))),
                      ("random", random.Random(5).sample(range(1000), 100))):
    comparison_count, swap_count = selection_sort_counted(values)
    print(f"  {label:<16}{comparison_count} comparisons, {swap_count} swaps")
print("  comparisons are n(n-1)/2 = 4950 every time: not adaptive.")
print("  swaps never go above n - 1 = 99: the O(n) swaps from slide 6.")

cards = [(5, "red"), (3, "green"), (5, "blue"), (1, "black")]
print(f"\nNot stable: {cards}")
print(f"  sorted by number -> {selection_sort_by_number(list(cards))}")
print("  '5 red' was before '5 blue' going in, and is after it coming out.")
print("  The first swap moved (5, red) to where (1, black) was, past (5, blue).")


# =====================================================================
# 5. TESTS
# =====================================================================

# Each case: (input list, expected sorted list)
test_cases = [
    ([64, 25, 12, 22, 11], [11, 12, 22, 25, 64]),  # a typical small list
    ([], []),  # empty
    ([7], [7]),  # one value
    ([2, 1], [1, 2]),  # two values, wrong order
    ([1, 2, 3, 4], [1, 2, 3, 4]),  # already sorted
    ([4, 3, 2, 1], [1, 2, 3, 4]),  # reversed
    ([3, 1, 3, 1, 3], [1, 1, 3, 3, 3]),  # repeats
    ([0, -5, 8, -2], [-5, -2, 0, 8]),  # negatives
    ([2.5, 1.5, 2.0], [1.5, 2.0, 2.5]),  # floats
]

print("\n" + "=" * 72)
print("TESTS")
print("=" * 72 + "\n")

pass_count = 0
fail_count = 0

for values, expected in test_cases:
    for method_name, method in (("selection_sort", selection_sort),
                                ("selection_sort_recursive", selection_sort_recursive)):
        result = method(list(values))  # a copy, so each method gets fresh input
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{status}  {method_name}({values}) = {result}, expected {expected}")
    print()

# Random check against Python's own sorted(). Fixed seed, so every run uses
# the same cases.
random.seed(2)
trial_count = 2000
random_failures = 0
swap_limit_failures = 0

for _ in range(trial_count):
    values = [random.randint(-50, 50) for _ in range(random.randint(0, 30))]
    expected = sorted(values)
    if (selection_sort(list(values)) != expected
            or selection_sort_recursive(list(values)) != expected):
        random_failures += 1
    _, swap_count = selection_sort_counted(list(values))
    if swap_count > max(len(values) - 1, 0):
        swap_limit_failures += 1

for status_failures, description in (
        (random_failures, "both versions match sorted()"),
        (swap_limit_failures, "never more than n - 1 swaps")):
    status = "PASS" if status_failures == 0 else "FAIL"
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1
    print(f"{status}  {trial_count} random lists: {description} "
          f"({status_failures} failures)")

print(f"\n{pass_count} PASS, {fail_count} FAIL")

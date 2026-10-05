"""
3-SUM
=====

Advanced Algorithms, Lecture 1 (Ivan Bliznets), slides 18-22. It builds
directly on 2-SUM (slides 16-17), which lives next door in ../2_SUM/2_Sum.py.

    3-SUM PROBLEM [slide 18]
        Input:     Three arrays of numbers A, B, C of length n, number s.
        Question:  Are there i, j, k such that A[i] + B[j] + C[k] = s?

        Example:   A = [1, 2, 15, 18, -10, 7]
                   B = [54, 12, 23, 11, -21, 0]
                   C = [11, -100, 15, 19, 6]
                   s = 20     ->  'Yes' as 20 = 2 + 12 + 6
                   s = 1000   ->  'No'                         [slide 19]

Like 2-SUM on these slides, it is the THREE-ARRAY version. One value comes
from each array. So there is no "don't reuse the same element" rule.


THE THREE ALGORITHMS
--------------------
    "Trivial algorithm: O(n^3)."                                [slide 19]

    "For each i in 0, 1, ..., n-1 solve 2-SUM PROBLEM with arrays B, C and
     target sum s - A[i].  Running time O(n^2 log n)."          [slide 20]

    "Can we do better?  Sort arrays B, C.  Now we need to solve 2-SUM PROBLEM
     for ordered arrays!"                                       [slide 20]
    "We presented algorithm with running time O(n^2)."          [slide 22]

The idea in one line: fix the value from A. What is left is a 2-SUM problem
on B and C, with target s - A[i]. Then use the best 2-SUM you know.

    2-SUM by binary search costs  O(n log n)  ->  n times that = O(n^2 log n)
    2-SUM by two pointers costs   O(n)        ->  n times that = O(n^2)

The trick for O(n^2) is to sort B and C ONCE, before the loop over A.
Sorting inside the loop would put the log n straight back.


THE SLIDE 21 PSEUDOCODE HAS TYPOS
---------------------------------
Slide 21, verbatim:

    j <- 0, k <- n - 1
    while i = 0, ..., n - 2 do
        if |B[j] + C[k]| == s : then
            return 'Yes'
        end if
        if |B[j] + C[k]| < s : then
            j++
        end if
        if |B[j] + C[k]| == s : then
            k--
        end if
    end while
    return 'No'

Four things to fix before it works:

    1. "while i = 0, ..., n-2" mixes up a for-loop and a while-loop. What is
       meant is: keep going while j < n and k >= 0.
    2. The |...| bars are not absolute values. Taken literally, -5 would match
       s = 5. They should just be B[j] + C[k].
    3. The third test says "== s". It must be "> s": too big, so step k down.
    4. The three ifs should be if / elif / else. Otherwise j++ happens and the
       next test reads the NEW j in the same round.

Section 3 below is the corrected version.


HOW THIS DIFFERS FROM CLRS
--------------------------
CLRS (3rd ed.) has no 3-SUM section. The closest is exercise 2.3-7 (p. 39):
"given a set S of n integers and another integer x, determine whether or not
there exist two elements in S whose sum is exactly x", in O(n lg n). That is
the ONE-array 2-SUM. The lecture's three-array version is the course's own.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_three_sum      every triple, O(n^3)              [slide 19]
    2. three_sum_binary_search    fix A and B, binary search C,
                                  O(n^2 log n)                      [slide 20]
    3. three_sum_two_pointers     fix A, walk B and C inward, O(n^2)
                                                                    [slides 20-22]
    4. the slide's examples
    5. agreement checks: hand cases and random cases

Run with:
    python3 3_Sum.py
"""

import random

# The example from slides 18-19.
SLIDE_FIRST = [1, 2, 15, 18, -10, 7]
SLIDE_SECOND = [54, 12, 23, 11, -21, 0]
SLIDE_THIRD = [11, -100, 15, 19, 6]


# =====================================================================
# 1. BRUTE FORCE -- every triple [slide 19]
# =====================================================================
# Three nested loops, one per array. Try every combination.
#
# first_value: the value taken from A
# second_value: the value taken from B
# third_value: the value taken from C
#
# n * n * n triples, constant work each: O(n^3).
# Slow, but obviously correct, so it is the reference the others are checked
# against.

def brute_force_three_sum(first_array, second_array, third_array, target):
    for first_value in first_array:
        for second_value in second_array:
            for third_value in third_array:
                if first_value + second_value + third_value == target:
                    return (first_value, second_value, third_value)
    return None


# =====================================================================
# 2. BINARY SEARCH VERSION -- O(n^2 log n) [slide 20, using slide 17]
# =====================================================================
# Slide 20 says "for each A[i], solve 2-SUM on B and C with target s - A[i]".
# Slide 17's 2-SUM is: sort one array, then binary search for the missing
# value. So:
#
#     sort C once
#     for each value in A:
#         for each value in B:
#             binary search C for  target - first_value - second_value
#
# third_sorted: C, sorted once, so binary search works on it
# first_value: the value fixed from A
# second_value: the value fixed from B
# needed_value: what C would have to contain to finish the sum
#
# n * n pairs, and each binary search costs log n: O(n^2 log n).
# (The sort is O(n log n), which is smaller, so it does not change the total.)

def binary_search(sorted_values, wanted_value):
    low_index = 0
    high_index = len(sorted_values) - 1
    while low_index <= high_index:
        middle_index = (low_index + high_index) // 2
        if sorted_values[middle_index] == wanted_value:
            return True
        if sorted_values[middle_index] < wanted_value:
            low_index = middle_index + 1  # the wanted value is to the right
        else:
            high_index = middle_index - 1  # the wanted value is to the left
    return False


def three_sum_binary_search(first_array, second_array, third_array, target):
    third_sorted = sorted(third_array)

    for first_value in first_array:
        for second_value in second_array:
            needed_value = target - first_value - second_value
            if binary_search(third_sorted, needed_value):
                return (first_value, second_value, needed_value)
    return None


# =====================================================================
# 3. TWO POINTERS VERSION -- O(n^2) [slides 20-22]
# =====================================================================
# Sort B and C once. Then, for each value in A, run the sorted 2-SUM walk
# from slide 21 (with its typos fixed -- see the docstring).
#
# second_sorted: B, sorted once, smallest first
# third_sorted: C, sorted once, smallest first
# first_value: the value fixed from A for this round
# remaining_target: s - A[i], what B and C must add up to
# second_index: j on the slide; starts at the SMALLEST value of B, only goes up
# third_index: k on the slide; starts at the LARGEST value of C, only goes down
#
# Why throwing a value away is safe (same argument as 2-SUM):
#     Sum too small: B[second_index] is paired with the BIGGEST C value left.
#     If even that is too small, no C value can save it. Drop it: step up.
#     Sum too big: C[third_index] is paired with the SMALLEST B value left.
#     If even that is too big, no B value can save it. Drop it: step down.
#
# Each walk moves one index per step, so it ends after at most 2n steps: O(n).
# n walks of O(n) each: O(n^2).

def three_sum_two_pointers(first_array, second_array, third_array, target):
    second_sorted = sorted(second_array)  # sorted ONCE, outside the loop
    third_sorted = sorted(third_array)

    for first_value in first_array:
        remaining_target = target - first_value
        second_index = 0
        third_index = len(third_sorted) - 1

        while second_index < len(second_sorted) and third_index >= 0:
            pair_total = second_sorted[second_index] + third_sorted[third_index]
            if pair_total == remaining_target:
                return (first_value, second_sorted[second_index],
                        third_sorted[third_index])
            elif pair_total < remaining_target:
                second_index += 1  # too small: need a bigger B value
            else:
                third_index -= 1  # too big: need a smaller C value

    return None


# =====================================================================
# 4. RUN THE SLIDE'S EXAMPLES [slides 18-19]
# =====================================================================

print("=" * 72)
print("3-SUM   -- Lecture 1, slides 18-22")
print("=" * 72)
print(f"\nA = {SLIDE_FIRST}")
print(f"B = {SLIDE_SECOND}")
print(f"C = {SLIDE_THIRD}\n")

for slide_target in (20, 1000):
    print(f"s = {slide_target}:")
    for method_name, method in (("brute force", brute_force_three_sum),
                                ("binary search", three_sum_binary_search),
                                ("two pointers", three_sum_two_pointers)):
        found = method(SLIDE_FIRST, SLIDE_SECOND, SLIDE_THIRD, slide_target)
        if found:
            print(f"  {method_name:<14}Yes   {found[0]} + {found[1]} + {found[2]}")
        else:
            print(f"  {method_name:<14}No")
    print()

print("The slide's answer for s = 20 is 2 + 12 + 6. The methods may find a")
print("different triple. Any triple that adds up to s is a correct 'Yes'.")


# =====================================================================
# 5. TESTS
# =====================================================================
# Only the YES/NO is compared between methods. Different methods may find
# different triples when several work. So each found triple is also checked:
# its values must really come from A, B and C, and really add up to s.

def is_valid_triple(triple, first_array, second_array, third_array, target):
    if triple is None:
        return True
    return (triple[0] in first_array and triple[1] in second_array
            and triple[2] in third_array and sum(triple) == target)


# Each case: (A, B, C, s, expected yes/no)
test_cases = [
    (SLIDE_FIRST, SLIDE_SECOND, SLIDE_THIRD, 20, True),  # slide 18
    (SLIDE_FIRST, SLIDE_SECOND, SLIDE_THIRD, 1000, False),  # slide 19
    ([1], [2], [3], 6, True),  # one element each
    ([1], [2], [3], 7, False),  # one element each, no match
    ([], [1, 2], [3, 4], 5, False),  # an empty array: nothing to pick
    ([0, 0], [0, 0], [0, 0], 0, True),  # all zeros
    ([-5, -1], [-7, -2], [-3, -8], -20, True),  # all negative: -5 + -7 + -8
    ([5, 5, 5], [5, 5], [5], 15, True),  # repeats
    ([1, 2, 3], [10, 20, 30], [100, 200, 300], 333, True),  # largest of each
    ([1, 2, 3], [10, 20, 30], [100, 200, 300], 111, True),  # smallest of each
    ([1, 2, 3], [10, 20, 30], [100, 200, 300], 110, False),  # just below
]

print("\n" + "=" * 72)
print("TESTS")
print("=" * 72 + "\n")

pass_count = 0
fail_count = 0

for first_array, second_array, third_array, target, expected in test_cases:
    for method_name, method in (("brute_force_three_sum", brute_force_three_sum),
                                ("three_sum_binary_search", three_sum_binary_search),
                                ("three_sum_two_pointers", three_sum_two_pointers)):
        result = method(first_array, second_array, third_array, target)
        found = result is not None
        valid = is_valid_triple(result, first_array, second_array, third_array, target)
        status = "PASS" if found == expected and valid else "FAIL"
        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{status}  {method_name}(s={target}) = {result}, expected "
              f"{'Yes' if expected else 'No'}")
    print()

# Random check: fixed seed, so every run uses the same cases.
random.seed(3)
trial_count = 3000
random_failures = 0

for _ in range(trial_count):
    array_length = random.randint(1, 7)
    first_array = [random.randint(-15, 15) for _ in range(array_length)]
    second_array = [random.randint(-15, 15) for _ in range(array_length)]
    third_array = [random.randint(-15, 15) for _ in range(array_length)]
    target = random.randint(-30, 30)

    brute_found = brute_force_three_sum(first_array, second_array, third_array,
                                        target) is not None
    for method in (three_sum_binary_search, three_sum_two_pointers):
        result = method(first_array, second_array, third_array, target)
        if ((result is not None) != brute_found
                or not is_valid_triple(result, first_array, second_array,
                                       third_array, target)):
            random_failures += 1

status = "PASS" if random_failures == 0 else "FAIL"
if status == "PASS":
    pass_count += 1
else:
    fail_count += 1
print(f"{status}  {trial_count} random cases: binary search and two pointers "
      f"agree with brute force ({random_failures} disagreements)")

print(f"\n{pass_count} PASS, {fail_count} FAIL")

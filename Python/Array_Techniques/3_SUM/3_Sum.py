"""
3-SUM
Advanced Algorithms, Lecture 1 (Ivan Bliznets), slides 18-22.

Notes: [[3-SUM — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/3-SUM — Code Notes.md

What is in this file:
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
# Notes: [[3-SUM — Code Notes#1. Brute force — every triple]] (variables)

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
# Notes: [[3-SUM — Code Notes#2. Binary search version]] (outline, variables)

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
# Notes: [[3-SUM — Code Notes#3. Two pointers version]] (variables, why throwing a value away is safe)

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

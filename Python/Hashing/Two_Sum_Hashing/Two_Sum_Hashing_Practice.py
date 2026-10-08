r"""
2-SUM VIA HASHING -- PRACTICE
=============================

Write it yourself here. Two_Sum_Hashing.py, next to this file, is the answer
to compare with afterwards.

THE PROBLEM [Lecture 9, slide 5]
    Input:   two arrays of positive integers, left_array and right_array,
             and a number target.
    Output:  a pair (left_value, right_value) with
             left_value + right_value == target, or None if there is none.

THE RULES
    - Build your own hash table with chaining: a list of lists. No Python
      set or dict, or the exercise is one line.
    - Run this file. Every test prints PASS, FAIL or NOT WRITTEN YET.
      Brute force is the reference.

Run with:
    python3 Two_Sum_Hashing_Practice.py
"""

import random


# =====================================================================
# YOUR PLAN
# =====================================================================
# Write the steps in prose first, then the code under them.
#
#


# =====================================================================
# YOUR CODE
# =====================================================================

def two_sum_hashing(left_array, right_array, target):
    raise NotImplementedError


# =====================================================================
# TESTS -- no need to edit below this line
# =====================================================================

def brute_force_two_sum(left_array, right_array, target):
    for left_value in left_array:
        for right_value in right_array:
            if left_value + right_value == target:
                return (left_value, right_value)
    return None


def is_valid_pair(pair, left_array, right_array, target):
    if not (isinstance(pair, tuple) and len(pair) == 2):
        return False
    left_value, right_value = pair
    return left_value in left_array and right_value in right_array and left_value + right_value == target


def run_case(description, left_array, right_array, target):
    expected_found = brute_force_two_sum(left_array, right_array, target) is not None
    try:
        pair = two_sum_hashing(list(left_array), list(right_array), target)
    except NotImplementedError:
        print(f"NOT WRITTEN YET  {description}")
        return None
    except Exception as error:
        print(f"FAIL  {description}: crashed with {type(error).__name__}: {error}")
        return False
    if expected_found:
        passed = is_valid_pair(pair, left_array, right_array, target)
        want = "a valid pair"
    else:
        passed = pair is None
        want = "None"
    print(f"{'PASS' if passed else 'FAIL'}  {description}: got {pair}, want {want}")
    return passed


SLIDE_RIGHT_ARRAY = [11, 24, 34, 6, 29, 8, 17]

cases = [
    ("slide 10, Example 1 (no collisions under x mod 7)",
     [4, 16, 10, 26, 21, 34], SLIDE_RIGHT_ARRAY, 33),
    ("slide 11, Example 2 (16,9 and 4,18 collide under x mod 7)",
     [4, 16, 9, 26, 18, 34], SLIDE_RIGHT_ARRAY, 33),
    ("no pair at all", [2, 7, 11, 15], [9, 1, 6, 3], 100),
    ("collision must not lose 16: 16 + 17", [16, 9], [17], 33),
    ("occupied cell is not a match: 16 + 24 = 40", [16], [24], 33),
    ("right value bigger than target (wanted < 0)", [5], [40, 28], 33),
    ("right value equal to target (wanted = 0)", [5], [33], 33),
    ("one element each, a pair", [10], [23], 33),
    ("duplicates in both arrays", [7, 7, 7], [26, 26], 33),
    ("arrays of different lengths", [1, 2], [30, 31, 32, 99, 100], 33),
    ("empty right array", [4, 16], [], 33),
    ("big values, n = 2", [3, 1000000], [5, 1000000], 1000003),
]

print("=" * 70)
print("FIXED CASES")
print("=" * 70)
results = [run_case(*case) for case in cases]

if None not in results:
    print("\n" + "=" * 70)
    print("RANDOM CASES AGAINST BRUTE FORCE")
    print("=" * 70)
    random_generator = random.Random(52)
    trial_count = 5000
    failures = 0
    for _ in range(trial_count):
        random_left = [random_generator.randint(1, 40) for _ in range(random_generator.randint(1, 8))]
        random_right = [random_generator.randint(1, 40) for _ in range(random_generator.randint(1, 8))]
        random_target = random_generator.randint(2, 80)
        expected_found = brute_force_two_sum(random_left, random_right, random_target) is not None
        try:
            pair = two_sum_hashing(list(random_left), list(random_right), random_target)
            correct = (is_valid_pair(pair, random_left, random_right, random_target)
                       if expected_found else pair is None)
        except Exception:
            correct = False
        if not correct:
            failures += 1
            if failures == 1:
                print(f"first failure: left={random_left} right={random_right} target={random_target}")
    print(f"{'PASS' if failures == 0 else 'FAIL'}  {trial_count - failures}/{trial_count} agree with brute force")
    results.append(failures == 0)

print()
if None in results:
    print("Write two_sum_hashing, then run again.")
elif all(results):
    print("ALL PASS")
else:
    print(f"{results.count(False)} FAILED")

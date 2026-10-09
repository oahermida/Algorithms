"""
2-SUM
Advanced Algorithms, Lecture 1.

Notes: [[2-SUM — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/2-SUM — Code Notes.md

Run with:
    python3 2_Sum.py
"""

left_array  = [2, 7, 11, 15]
right_array = [9, 1, 6, 3]
target      = 20


# =====================================================================
# 1. BRUTE FORCE -- the slow version, kept as the reference answer
# =====================================================================
# Every value in the left array against every value in the right array.
# n choices times n choices = n^2 pairs. Correct, and fine for small n.

def brute_force(left_array, right_array, target):
    for left_value in left_array:
        for right_value in right_array:
            if left_value + right_value == target:
                return (left_value, right_value)
    return None


# =====================================================================
# 2. TWO POINTERS -- the fast version
# =====================================================================
# Notes: [[2-SUM — Code Notes#2. Two pointers — the fast version]] (why throwing a value away is safe)

def two_pointers(left_array, right_array, target):
    left_sorted  = sorted(left_array)
    right_sorted = sorted(right_array)

    left_low_index   = 0                       # climbs UP   from the smallest left value
    right_high_index = len(right_sorted) - 1   # walks DOWN  from the largest right value

    while left_low_index < len(left_sorted) and right_high_index >= 0:
        left_value  = left_sorted[left_low_index]
        right_value = right_sorted[right_high_index]
        pair_total  = left_value + right_value

        if pair_total == target:
            return (left_value, right_value)

        if pair_total < target:
            left_low_index += 1            # need a bigger left value
        else:
            right_high_index -= 1           # need a smaller right value

    # One of the indices walked off its end, which means every pair has been
    # ruled out. No answer exists.
    return None


# =====================================================================
# 3. RUN BOTH
# =====================================================================

print(f"left_array  = {left_array}   -> sorted {sorted(left_array)}")
print(f"right_array = {right_array}   -> sorted {sorted(right_array)}")
print(f"target      = {target}\n")

found_pair = two_pointers(left_array, right_array, target)
print(f"result: {found_pair if found_pair else 'no pair'}")
print(f"brute force agrees: {brute_force(left_array, right_array, target) is not None} "
      f"(it found {brute_force(left_array, right_array, target)})")

# A target that is impossible, so the "ran off the end" path gets run too.
print(f"\nsame arrays, target = 100:")
impossible_result = two_pointers(left_array, right_array, 100)
print(f"result: {impossible_result if impossible_result else 'no pair'}")


# =====================================================================
# 4. CHECK IT PROPERLY -- don't trust one example
# =====================================================================
# Two examples passing proves nothing. Run both versions against each other on
# random data and confirm they never disagree.

import random

random.seed(1)
disagreement_count = 0
trial_count = 20000

for _ in range(trial_count):
    array_length = random.randint(1, 8)
    random_left_array   = [random.randint(0, 20) for _ in range(array_length)]
    random_right_array  = [random.randint(0, 20) for _ in range(array_length)]
    random_target = random.randint(0, 40)

    # Only compare YES/NO. The two methods can legitimately find DIFFERENT pairs
    # when several pairs work, so comparing the pairs themselves would report
    # false failures.
    brute_force_found  = brute_force(random_left_array, random_right_array, random_target) is not None
    two_pointers_found = two_pointers(random_left_array, random_right_array, random_target) is not None

    if brute_force_found != two_pointers_found:
        disagreement_count += 1

print(f"\nrandom check: {trial_count - disagreement_count}/{trial_count} agree with brute force")

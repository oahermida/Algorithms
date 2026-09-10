"""
2-SUM
=====

The question:
    Given two arrays and a target number, is there one value from the FIRST array
    and one value from the SECOND array that add up to the target?

    left_array  = [2, 7, 11, 15]
    right_array = [1, 3, 6, 9]
    target      = 20                 ->  11 + 9 = 20   ->  Yes

Note this is the TWO-ARRAY version, which is the one from Lecture 1 of Advanced
Algorithms. You take one value from each array, so there is no "don't use the same
element twice" rule to worry about. The one-array version (find two entries of a
single array that add to the target) needs that extra check.

Three ways to do it:

    brute force      O(n^2)        check every pair
    binary search    O(n log n)    sort one array, then look up target - value
    two pointers     O(n log n)    sort both, walk inward from opposite ends
                                   (the sort is the expensive part -- the walk
                                    itself is only O(n))

Two pointers is the one to reach for when memory is tight, because it needs two
integer indices and nothing else. There is also a hash-set version that is O(n)
time, but it costs O(n) extra memory, which a small memory limit will not allow.

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
# Both arrays get sorted first. Then put one index at the LOW end of the left
# array and one at the HIGH end of the right array, and walk them toward
# each other.
#
# At every step there are only three possibilities:
#
#     sum == target   ->  found it, stop
#     sum <  target   ->  too small, so move to a BIGGER left value
#     sum >  target   ->  too big,   so move to a SMALLER right value
#
# WHY THROWING A VALUE AWAY IS SAFE (this is the part that matters):
#
#     Say the sum is too small, and right_high_index is sitting on the LARGEST
#     remaining right value. That is the biggest partner this left value will
#     ever be offered. If even that is not enough to reach the target, then no
#     smaller right value will be either -- so this left value cannot be part
#     of any answer at all, and dropping it loses nothing.
#
#     Same logic mirrored for "too big": the left value is the smallest one
#     left, so if the sum overshoots, this right value is too big for every
#     left value still available. Drop it.
#
# That is why the walk is O(n) and not O(n^2): each step eliminates a whole
# ROW or COLUMN of the n x n grid of pairs, not a single pair.
#
# left_low_index only ever goes up and right_high_index only ever goes down --
# neither turns around, so between them they take at most 2n steps before one
# runs off its end.

def two_pointers(left_array, right_array, target, show_steps=False):
    left_sorted  = sorted(left_array)
    right_sorted = sorted(right_array)

    left_low_index   = 0                       # climbs UP   from the smallest left value
    right_high_index = len(right_sorted) - 1   # walks DOWN  from the largest right value

    while left_low_index < len(left_sorted) and right_high_index >= 0:
        left_value  = left_sorted[left_low_index]
        right_value = right_sorted[right_high_index]
        pair_total  = left_value + right_value

        if show_steps:
            print(f"    left_low_index={left_low_index} right_high_index={right_high_index}   "
                  f"{left_value:>2} + {right_value:>2} = {pair_total:>2}", end="   ")

        if pair_total == target:
            if show_steps:
                print("equal -> found it")
            return (left_value, right_value)

        if pair_total < target:
            if show_steps:
                print("too small -> left_low_index += 1")
            left_low_index += 1            # need a bigger left value
        else:
            if show_steps:
                print("too big   -> right_high_index -= 1")
            right_high_index -= 1           # need a smaller right value

    # One of the indices walked off its end, which means every pair has been
    # ruled out. No answer exists.
    if show_steps:
        print("    an index ran off the end -> no pair exists")
    return None


# =====================================================================
# 3. RUN BOTH AND SHOW THE WALK
# =====================================================================

print(f"left_array  = {left_array}   -> sorted {sorted(left_array)}")
print(f"right_array = {right_array}   -> sorted {sorted(right_array)}")
print(f"target      = {target}\n")

print("two-pointer walk:")
found_pair = two_pointers(left_array, right_array, target, show_steps=True)
print(f"\nresult: {found_pair if found_pair else 'no pair'}")
print(f"brute force agrees: {brute_force(left_array, right_array, target) is not None} "
      f"(it found {brute_force(left_array, right_array, target)})")

# A target that is impossible, so the "ran off the end" path gets shown too.
print(f"\nsame arrays, target = 100:")
impossible_result = two_pointers(left_array, right_array, 100, show_steps=True)
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

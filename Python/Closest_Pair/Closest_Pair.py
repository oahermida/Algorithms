r"""
CLOSEST PAIR
============

Advanced Algorithms, Lecture 1 (Ivan Bliznets), slides 12-14, under the heading
"Importance of sorting".

    CLOSEST PAIR [slide 12]
        Input:     array of numbers A
        Question:  what is the minimum value of |A[i] - A[j]| for i != j?

        Example:   A = [1, 23, 12, 53, -2, 100, 75, 14, 101]
                   Answer: 1 = 101 - 100, when i = 5, j = 8.

This is the ONE-DIMENSIONAL problem: numbers on a line, not points in a plane.
The famous O(n log n) divide-and-conquer closest-pair algorithm is the 2-D
geometric one, and it is not what this lecture covers -- see the note at the
bottom of this docstring, because the names collide and the confusion is easy.


THE NAIVE ALGORITHM [slide 13]
------------------------------
        n <- len(A), val <- +infinity
        for i = 0, ..., n-1 do
            for j = i+1, ..., n do
                if |A[i] - A[j]| < val then
                    val = |A[i] - A[j]|
        return val

Every pair against every other pair: n(n-1)/2 comparisons, so O(n^2).


THE SORTING ALGORITHM [slide 14]
--------------------------------
        n <- len(A), val <- +infinity
        Sort(A)
        for i = 0, ..., n-2 do
            if |A[i] - A[i+1]| < val then
                val = |A[i] - A[i+1]|
        return val

        "Running time O(n log n)!"

Sort first, then look only at NEIGHBOURS. The sort costs O(n log n), the scan
costs O(n), so the sort dominates and the whole thing is O(n log n).


WHY LOOKING AT NEIGHBOURS IS ENOUGH
-----------------------------------
This is the step the slide leaves to the reader, and it is the entire reason the
algorithm is correct rather than merely fast. The claim:

    after sorting, the closest pair is always ADJACENT in the sorted order.

Proof. Take any three values in sorted order, x <= y <= z. Then

        z - x = (z - y) + (y - x)

and both bracketed terms are >= 0, so z - x is at least as large as each of
them. In words: any pair that has another element BETWEEN it is at least as far
apart as one of the two smaller gaps it is made of. So a non-adjacent pair can
never be strictly closer than every adjacent pair, and checking the n-1 adjacent
gaps is enough.

    A = [1, 23, 12, 53, -2, 100, 75, 14, 101]

    sorted:   -2     1    12    14    23    53    75   100   101
    gaps:         3    11     2     9    30    22    25     1
                                                            ^
                                                   the smallest gap, = 1

The pair (100, 101) is the answer, and it is a neighbour pair -- as it must be.
Section 4 checks this claim empirically rather than only asserting it.


WHAT THE LECTURE IS ACTUALLY TEACHING HERE
------------------------------------------
Slide 12-14 sits inside "Importance of sorting", and the lesson is not the
algorithm. It is that sorting is rarely the goal -- it is the step that makes
the real question easy. The array is not wanted in order for its own sake; it is
wanted in order so that "closest" becomes "adjacent", which turns a quadratic
search into a linear scan.

The same lecture makes the same point with 2-SUM (see ../2_SUM/2_Sum.py), where
sorting turns "find a pair summing to the target" into a single two-pointer
walk. Two different problems, one technique: pay O(n log n) once to buy
structure, then exploit the structure in O(n).


NOT TO BE CONFUSED WITH THE 2-D CLOSEST PAIR
--------------------------------------------
"Closest pair" usually names the geometric problem: given n points in the plane,
find the two with the smallest Euclidean distance. That one genuinely needs
divide and conquer -- sorting alone does not solve it, because two points can be
close in the plane while being far apart in x-order. It is CLRS 33.4 and it is
NOT in this course's covered-material list. The one-dimensional problem on this
slide is strictly easier, and sorting really is the whole solution.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_closest_pair   the naive O(n^2) version  [slide 13]
    2. sort_then_scan             the O(n log n) version    [slide 14]
    3. the slide's worked example, with the gaps shown
    4. a check that the closest pair really is always adjacent after sorting
    5. timing, and agreement checks

Both return (distance, first_index, second_index) with indices into the ORIGINAL
array, not the sorted one -- which is the one real implementation subtlety, see
section 2.

Run with:
    python3 Closest_Pair.py
"""

import random
import time

# The example from slide 12. The answer is 1, from 101 - 100 at original
# indices 5 and 8.
SLIDE_VALUES = [1, 23, 12, 53, -2, 100, 75, 14, 101]


# =====================================================================
# 1. NAIVE -- every pair [slide 13]
# =====================================================================
# best_distance  - the smallest |A[i] - A[j]| seen so far
# best_pair      - the indices where that happened
#
# The inner loop starts at first_index + 1 so each unordered pair is considered
# once and no element is ever compared with itself -- that is what the i != j in
# the problem statement demands.
#
# n(n-1)/2 comparisons: O(n^2).

def brute_force_closest_pair(values):
    best_distance = float("inf")
    best_pair = (0, 1)

    for first_index in range(len(values)):
        for second_index in range(first_index + 1, len(values)):
            distance = abs(values[first_index] - values[second_index])
            if distance < best_distance:
                best_distance = distance
                best_pair = (first_index, second_index)

    return best_distance, best_pair[0], best_pair[1]


# =====================================================================
# 2. SORT, THEN SCAN NEIGHBOURS [slide 14]
# =====================================================================
# labelled_values - (value, original_index) pairs, sorted by value
# position        - which neighbouring pair the scan is looking at
#
# THE SUBTLETY: sorting destroys the original positions, and the slide's own
# answer is phrased in them ("when i = 5, j = 8"). So the values are carried
# with their original indices attached, and the scan reports those rather than
# the sorted positions. Sorting the raw values and then trying to look the
# answer up with .index() would also break on duplicates.
#
# Sorting (value, index) pairs also makes the sort deterministic when values
# tie, so repeated runs report the same pair.
#
# The scan itself never looks further than one step ahead, because of the
# adjacency argument in the docstring.

def sort_then_scan(values):
    labelled_values = sorted((value, index) for index, value in enumerate(values))

    best_distance = float("inf")
    best_pair = (labelled_values[0][1], labelled_values[1][1])

    for position in range(len(labelled_values) - 1):
        lower_value, lower_index = labelled_values[position]
        higher_value, higher_index = labelled_values[position + 1]
        distance = higher_value - lower_value          # already ordered, so no abs needed

        if distance < best_distance:
            best_distance = distance
            best_pair = (lower_index, higher_index)

    first_index, second_index = sorted(best_pair)
    return best_distance, first_index, second_index


# =====================================================================
# 3. RUN THE SLIDE'S EXAMPLE
# =====================================================================

print("=" * 78)
print("CLOSEST PAIR   -- Lecture 1, slides 12-14  ('Importance of sorting')")
print("=" * 78)

print(f"\nA = {SLIDE_VALUES}   [slide 12]")

distance, first_index, second_index = sort_then_scan(SLIDE_VALUES)
brute_distance, brute_first, brute_second = brute_force_closest_pair(SLIDE_VALUES)

labelled = sorted((value, index) for index, value in enumerate(SLIDE_VALUES))
sorted_values = [value for value, _ in labelled]
gaps = [sorted_values[position + 1] - sorted_values[position]
        for position in range(len(sorted_values) - 1)]

print(f"\n  sorted: " + "".join(f"{value:>6}" for value in sorted_values))
print(f"  gaps:     " + "".join(f"{gap:>6}" for gap in gaps))
smallest_gap_position = gaps.index(min(gaps))
print(f"            " + " " * (6 * smallest_gap_position) + f"{'^':>6}")
print(f"            " + " " * (6 * smallest_gap_position)
      + f"{'':>6}the smallest gap")

print(f"\n  answer: {distance}, between A[{first_index}] = {SLIDE_VALUES[first_index]} "
      f"and A[{second_index}] = {SLIDE_VALUES[second_index]}")
print(f"  the slide says: 'Answer: 1 = 101 - 100, when i = 5, j = 8'  -- matches")
print(f"\n  naive O(n^2) agrees: {brute_distance}, at indices "
      f"({brute_first}, {brute_second})")
print(f"\n  note how far apart those two values are in the ORIGINAL array "
      f"(positions {first_index} and {second_index}),")
print(f"  and how adjacent they are once sorted (positions "
      f"{smallest_gap_position} and {smallest_gap_position + 1}) -- that is the")
print(f"  whole trick: sorting moves the answer next to itself")


# =====================================================================
# 4. IS THE CLOSEST PAIR ALWAYS ADJACENT AFTER SORTING?
# =====================================================================
# The correctness argument, tested rather than only stated. For each random
# array, find the closest pair by brute force and check that the two values sit
# next to each other in sorted order.
#
# This is the claim the O(n log n) algorithm rests on: if it ever failed, the
# scan would be looking in the wrong places and the speed would be worthless.

print("\n" + "=" * 78)
print("THE CLAIM THE ALGORITHM RESTS ON")
print("=" * 78)

random.seed(2)
trial_count = 5000
not_adjacent_count = 0

for _ in range(trial_count):
    length = random.randint(2, 12)
    sample = [random.randint(-40, 40) for _ in range(length)]

    _, brute_first, brute_second = brute_force_closest_pair(sample)
    ordered = sorted((value, index) for index, value in enumerate(sample))
    positions = {index: position for position, (_, index) in enumerate(ordered)}

    if abs(positions[brute_first] - positions[brute_second]) != 1:
        not_adjacent_count += 1

print(f"\n  {trial_count} random arrays: in "
      f"{trial_count - not_adjacent_count}/{trial_count} of them the closest pair")
print(f"  found by brute force is ADJACENT in sorted order\n")
print(f"  proof, for x <= y <= z:   z - x = (z - y) + (y - x)")
print(f"  both terms are non-negative, so z - x is at least as big as each of them.")
print(f"  a pair with something between it can never beat both of its own halves,")
print(f"  so the minimum is always between neighbours.")

# The same fact from the other side: count how often a NON-adjacent pair even
# ties the best distance, to show adjacency is about the minimum, not uniqueness.
tie_count = 0
for _ in range(trial_count):
    sample = [random.randint(-10, 10) for _ in range(random.randint(3, 10))]
    best_distance, _, _ = brute_force_closest_pair(sample)
    ordered = sorted(sample)
    for first_position in range(len(ordered)):
        for second_position in range(first_position + 2, len(ordered)):
            if ordered[second_position] - ordered[first_position] == best_distance:
                tie_count += 1
                break
        else:
            continue
        break

print(f"\n  ({tie_count} of those arrays also have a NON-adjacent pair at the same")
print(f"   minimum distance -- usually duplicates, where the distance is 0. adjacency")
print(f"   guarantees the minimum is FOUND, not that it is achieved only once)")


# =====================================================================
# 5. TIMING -- O(n^2) against O(n log n)
# =====================================================================

print("\n" + "=" * 78)
print("TIMING")
print("=" * 78)
print(f"\n{'n':>8}{'naive O(n^2)':>17}{'sort+scan O(n log n)':>24}{'speedup':>11}")
print("-" * 78)

random.seed(13)
for size in (250, 500, 1000, 2000, 4000):
    sample = [random.randint(-10 ** 6, 10 ** 6) for _ in range(size)]

    start_time = time.perf_counter()
    brute_force_closest_pair(sample)
    brute_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    sort_then_scan(sample)
    sorted_seconds = time.perf_counter() - start_time

    print(f"{size:>8}{brute_seconds:>17.6f}{sorted_seconds:>24.6f}"
          f"{brute_seconds / sorted_seconds:>10.0f}x")

print("\n  doubling n quadruples the naive column and slightly more than doubles")
print("  the sorted one -- and the speedup column grows without bound, because")
print("  the two are not the same shape of curve")


# =====================================================================
# 6. AGREEMENT CHECK
# =====================================================================
# The two must agree on the DISTANCE. They need not return the same PAIR: ties
# are common, especially with duplicates, and the two methods break them
# differently. So the distance is compared directly, and each returned pair is
# checked to be two distinct indices actually that far apart.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(10)
trial_count = 5000
distance_disagreements = 0
pair_disagreements = 0

for _ in range(trial_count):
    length = random.randint(2, 14)
    # narrow ranges force duplicates, which is where an implementation that
    # looks values up by .index() would fall over
    spread = random.choice((3, 20, 1000))
    sample = [random.randint(-spread, spread) for _ in range(length)]

    brute_result = brute_force_closest_pair(sample)
    sorted_result = sort_then_scan(sample)

    if brute_result[0] != sorted_result[0]:
        distance_disagreements += 1

    for result in (brute_result, sorted_result):
        reported_distance, index_one, index_two = result
        if (index_one == index_two
                or abs(sample[index_one] - sample[index_two]) != reported_distance):
            pair_disagreements += 1

print(f"\n{trial_count} random arrays, lengths 2-14, value spreads 3 / 20 / 1000")
print(f"  (the narrow spreads force duplicates, where the distance is 0)\n")
print(f"  both methods agree on the distance   {trial_count - distance_disagreements}/{trial_count}")
print(f"  every returned pair is real          {2 * trial_count - pair_disagreements}/{2 * trial_count}")


# === How it Runs ===
#
# --- brute_force_closest_pair ---
# two nested loops; the inner one starts one past the outer, so every unordered
# pair is seen exactly once and nothing is compared with itself
# best_distance starts at infinity so the first real pair always replaces it
# n(n-1)/2 comparisons -- for n = 9 that is 36
#
# --- sort_then_scan ---
# first the values are labelled with their original positions and sorted:
#
#   A          = [1, 23, 12, 53, -2, 100, 75, 14, 101]
#   labelled   = [(1,0), (23,1), (12,2), (53,3), (-2,4), (100,5), (75,6), (14,7), (101,8)]
#   sorted     = [(-2,4), (1,0), (12,2), (14,7), (23,1), (53,3), (75,6), (100,5), (101,8)]
#
# the index travels WITH the value, which is what lets the answer be reported in
# the original array's terms -- the slide's "i = 5, j = 8" rather than "positions
# 7 and 8 of the sorted array"
#
# then one pass over neighbours, subtracting each from the next:
#   position 0:  1 - (-2)   =  3      best = 3,  pair (4, 0)
#   position 1:  12 - 1     = 11
#   position 2:  14 - 12    =  2      best = 2,  pair (2, 7)
#   position 3:  23 - 14    =  9
#   position 4:  53 - 23    = 30
#   position 5:  75 - 53    = 22
#   position 6:  100 - 75   = 25
#   position 7:  101 - 100  =  1      best = 1,  pair (5, 8)   <- the answer
#   return 1, indices 5 and 8
#
# the subtraction needs no abs() because the pairs come out of a sorted list --
# the later value is never smaller. that is a small thing, but it is the kind of
# check the sort has already paid for
#
# 8 subtractions instead of 36 comparisons, and the gap widens as n^2 pulls away
# from n
#
# --- why the sort is the whole algorithm ---
# the scan is O(n) and trivial; the sort is O(n log n) and does all the work
# the lecture's heading is "Importance of sorting", and this is the cleanest
# possible example of it: nobody wants the array sorted. they want "closest" to
# become "adjacent", and sorting is what makes that true

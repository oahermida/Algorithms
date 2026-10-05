r"""
SET COVER -- DYNAMIC PROGRAMMING OVER SUBSETS OF THE UNIVERSE
=============================================================

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 53-54, the last
problem of the deck. The same table is the standard exact algorithm for set
cover in Fomin & Kratsch, *Exact Exponential Algorithms*, chapter 3 (not
checked against the book here -- the slides are the source). No CLRS section
gives this algorithm; CLRS 35.3 covers set cover only by a greedy
approximation.

    THE MOVIE STORY [slide 53]
        A group of friends planning a trip to remote area without internet.
        They are planning to download some movies to watch in the road.
        However, they have different tastes. They made a list of films and for
        each film it is known a subset of friends that would like to watch
        this movie. Your goal is to pick the smallest number of movies such
        that for each person there is at least one film that she/he would like
        to watch.

    SET COVER [slide 53]
        Input:     A set U and a list of subsets C1, C2, ..., Cm
        Question:  What is the smallest number k such that there are
                   i1, i2, ..., ik such that Ci1 u Ci2 u ... u Cik = U.

So U is the friends, and each Cj is the friends who like movie j.

    Example [slide 54]:
        U = {1, 2, ..., 6},
        C1 = {1, 2, 6}, C2 = {1, 3, 6}, C3 = {4, 5}, C4 = {4, 5, 6},
        C5 = {3}, C6 = {2, 5}
        Solution: k = 3, C1 u C3 u C5 = U.


THE TABLE [slide 54]
--------------------
    For S (subset of U) and j in {1, 2, ..., m} we denote by OPT(S, j) the
    smallest number of sets from C1, C2, ..., Cj which union covers S.
    Answer to our problem is OPT(U, m).

One row per j (how many sets are on offer), one column per SUBSET S of U.
There are 2^n subsets, so the table is 2^n x m. This is the "exponential" in
the title: the DP is exponential in n = |U|, but only linear in m.

The recurrence is the same take-or-skip choice as subset sum:

    OPT(S, j+1) = min{ OPT(S, j),  1 + OPT(S \ C(j+1), j) }
                         |               |
                         |               '-- TAKE set j+1: it covers its part
                         |                   of S for the cost of one set; the
                         |                   rest, S \ C(j+1), must be covered
                         |                   by the first j sets
                         '-- SKIP set j+1: cover S with the first j sets

    base:  OPT(empty set, 0) = 0           nothing to cover, no sets needed
           OPT(S, 0) = infinity, S not empty   no sets cannot cover anything

Running time [slide 54]: O(n m 2^n). "Size of the table 2^n x m.
Computation of S \ C(j+1) takes O(n) time."


SUBSETS AS BITMASKS
-------------------
Store each subset of U as an integer. Bit number k is 1 when element k+1 is in
the set:

    U  = {1, 2, 3, 4, 5, 6}  ->  0b111111  = 63
    C1 = {1, 2, 6}           ->  0b100011  = 35
                                   ^   ^^
                                   6   21

Then the set operations are single machine instructions:

    S \ C      ->  S & ~C
    S u C      ->  S | C
    every S    ->  for subset_mask in range(2 ** len(universe))

So S \ C costs O(1), not the slide's O(n), and the total is O(m 2^n).


TYPOS IN THE SLIDES
-------------------
    - Slide 54 writes "OPT(S, j+1) = min{OPT(S, j), OPT(S \ Cj+1)}". Two
      things are missing: the "1 +" for taking the set, and the second index
      ", j". Without the "1 +" every answer would be 0.
    - Slide 54 defines OPT only for j in {1, ..., m}, but the recurrence needs
      a starting row. The base row j = 0 is added above.
    - Slide 53 spells "SET COVEr". No effect.


WHY NOT JUST BRUTE FORCE?
-------------------------
Brute force tries families of sets: up to 2^m of them. The DP costs about
m * 2^n. Which wins depends on which number is small:

    few friends, many movies  (n small, m big)    -> the DP wins
    many friends, few movies  (n big, m small)    -> brute force wins

Section 6 prints both counts for a few sizes.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_set_cover   every family of sets, smallest first
    2. set_cover_table         the lecture's table OPT(S, j)       [slide 54]
    3. restore_cover           WHICH sets, walking back on the table
    4. set_cover_rolling       one row of 2^n instead of the table
    5. the slide's example
    6. the 2^n vs 2^m comparison
    7. tests: hand cases, then random cases against brute force

Run with:
    python3 Set_Cover.py
"""

import random
from itertools import combinations

INFINITY = float("inf")

# The example from slide 54.
SLIDE_UNIVERSE = [1, 2, 3, 4, 5, 6]
SLIDE_SETS = [{1, 2, 6}, {1, 3, 6}, {4, 5}, {4, 5, 6}, {3}, {2, 5}]  # C1 .. C6


def to_mask(subset, universe):
    # bit k is set when universe[k] is in the subset
    mask = 0
    for position, element in enumerate(universe):
        if element in subset:
            mask |= 1 << position
    return mask


def from_mask(mask, universe):
    return {element for position, element in enumerate(universe) if mask >> position & 1}


# =====================================================================
# 1. BRUTE FORCE -- every family of sets, smallest first
# =====================================================================
# family_size: k, how many sets this round picks
# family: the indices of one particular choice of k sets
#
# Up to 2^m families, each checked in O(m n). Only for testing.
# Returns (k, indices), or (infinity, None) when U cannot be covered.

def brute_force_set_cover(universe, sets):
    full = set(universe)
    for family_size in range(len(sets) + 1):
        for family in combinations(range(len(sets)), family_size):
            covered = set()
            for index in family:
                covered |= sets[index]
            if covered >= full:
                return family_size, list(family)
    return INFINITY, None


# =====================================================================
# 2. THE LECTURE'S TABLE [slide 54]
# =====================================================================
# universe: U, as a list (its order fixes the bit numbers)
# sets: C1 .. Cm
# set_masks: each Cj as a bitmask
# table: table[set_count][subset_mask] = OPT(S, j), the fewest sets among the
#        first `set_count` that cover the subset S
# set_count: j, how many sets are on offer, 0 .. m
# subset_mask: S, one subset of U, 0 .. 2^n - 1
#
# O(m 2^n) time and space.

def set_cover_table(universe, sets):
    subset_total = 2 ** len(universe)
    set_masks = [to_mask(chosen_set, universe) for chosen_set in sets]

    table = [[INFINITY] * subset_total]  # row j = 0: nothing can be covered...
    table[0][0] = 0  # ...except the empty set, with 0 sets

    for set_count in range(1, len(sets) + 1):
        new_set = set_masks[set_count - 1]
        previous = table[set_count - 1]
        row = []
        for subset_mask in range(subset_total):
            skip = previous[subset_mask]
            take = 1 + previous[subset_mask & ~new_set]  # S \ C(j)
            row.append(min(skip, take))
        table.append(row)

    full_mask = subset_total - 1
    return table[len(sets)][full_mask], table


# =====================================================================
# 3. RESTORE THE COVER -- walking back on the table
# =====================================================================
# Stand on OPT(U, m). Ask which branch of the min made it:
#
#   OPT(S, j) == OPT(S, j-1)  -> set j was SKIPPED; go up a row
#   otherwise                 -> set j was TAKEN; remove its elements from S
#
# set_count / remaining: where the walk stands (the row, and the subset S)
# chosen: the indices of the sets taken (0-based: index 0 is C1)
#
# Preferring the skip means it walks up to the first row j where U can be
# covered at the optimal size, so it prefers the EARLIEST sets in the list.

def restore_cover(universe, sets, table):
    remaining = 2 ** len(universe) - 1
    if table[len(sets)][remaining] == INFINITY:
        return None

    chosen = []
    for set_count in range(len(sets), 0, -1):
        if table[set_count][remaining] == table[set_count - 1][remaining]:
            continue  # skipped
        chosen.append(set_count - 1)  # taken
        remaining &= ~to_mask(sets[set_count - 1], universe)

    chosen.reverse()
    return chosen


# =====================================================================
# 4. ONE ROW INSTEAD OF THE TABLE
# =====================================================================
# Each row reads only the row before it, so keep one row of 2^n values.
#
# best: best[S] = fewest sets so far that cover S
#
# In subset sum the one-row version had to run DOWNWARD, or an element got
# used twice. Here the direction does not matter. Reading a value that
# already took set C this round is harmless: taking C twice covers nothing
# new, because (S \ C) \ C = S \ C. So that value is never better than the
# old one. The tests check this against the full table.
#
# O(2^n) space. As always, it gives up the restore.

def set_cover_rolling(universe, sets):
    best = [INFINITY] * (2 ** len(universe))
    best[0] = 0
    for chosen_set in sets:
        new_set = to_mask(chosen_set, universe)
        for subset_mask in range(len(best)):
            best[subset_mask] = min(best[subset_mask], 1 + best[subset_mask & ~new_set])
    return best[len(best) - 1]


def format_set(chosen_set):
    return "{" + ", ".join(str(element) for element in sorted(chosen_set)) + "}"


# =====================================================================
# 5. RUN THE SLIDE'S EXAMPLE [slide 54]
# =====================================================================

print("=" * 78)
print("SET COVER   -- Lecture 4-5, slides 53-54")
print("=" * 78)

print(f"\nU = {format_set(SLIDE_UNIVERSE)}")
for index, chosen_set in enumerate(SLIDE_SETS, start=1):
    print(f"  C{index} = {format_set(chosen_set):<11} bitmask {to_mask(chosen_set, SLIDE_UNIVERSE):06b}")

answer, slide_table = set_cover_table(SLIDE_UNIVERSE, SLIDE_SETS)
cover = restore_cover(SLIDE_UNIVERSE, SLIDE_SETS, slide_table)
print(f"\n  OPT(U, 6) = {answer}")
print(f"  restored: {' u '.join(f'C{index + 1}' for index in cover)}"
      f" = {' u '.join(format_set(SLIDE_SETS[index]) for index in cover)}")
print("  the slide's answer is C1 u C3 u C5 -- also 3 sets. Both are optimal.")

print("\n  the row OPT(S, j) for S = U, as more sets come on offer:")
full_mask = 2 ** len(SLIDE_UNIVERSE) - 1
for set_count in range(len(SLIDE_SETS) + 1):
    value = slide_table[set_count][full_mask]
    print(f"    j = {set_count}:  {'inf' if value == INFINITY else value}")


# =====================================================================
# 6. 2^n AGAINST 2^m
# =====================================================================

print("\n" + "=" * 78)
print("TABLE CELLS (m * 2^n) AGAINST FAMILIES TRIED BY BRUTE FORCE (2^m)")
print("=" * 78)
print(f"\n{'friends n':>10}{'movies m':>10}{'DP cells':>14}{'families':>14}{'smaller':>14}")
for friend_count, movie_count in ((6, 6), (10, 40), (20, 100), (40, 20)):
    cells = movie_count * 2 ** friend_count
    families = 2 ** movie_count
    print(f"{friend_count:>10}{movie_count:>10}{cells:>14.3g}{families:>14.3g}"
          f"{('the DP' if cells < families else 'brute force'):>14}")
print("\n  the DP pays for every SUBSET OF FRIENDS, brute force for every SET OF MOVIES.")


# =====================================================================
# 7. TESTS
# =====================================================================

print("\n" + "=" * 78)
print("TESTS")
print("=" * 78 + "\n")

all_passed = True


def report(passed, message):
    global all_passed
    all_passed = all_passed and passed
    print(f"{'PASS' if passed else 'FAIL'}  {message}")


def check_all_versions(universe, sets):
    # returns the answer, and whether the rolling version and the restore agree
    answer, table = set_cover_table(universe, sets)
    cover = restore_cover(universe, sets, table)
    if answer == INFINITY:
        restored_ok = cover is None
    else:
        covered = set()
        for index in cover:
            covered |= sets[index]
        restored_ok = len(cover) == answer and covered >= set(universe)
    return answer, set_cover_rolling(universe, sets) == answer and restored_ok


hand_cases = [
    (SLIDE_UNIVERSE, SLIDE_SETS, 3),  # slide 54
    ([], [], 0),  # nothing to cover
    ([1, 2], [{1, 2}], 1),  # one set covers all
    ([1, 2, 3], [{1}, {2}], INFINITY),  # 3 is in no set: impossible
    ([1, 2, 3, 4], [{1, 2}, {3, 4}, {1, 2, 3}], 2),  # the big set is a trap
    ([1, 2, 3, 4, 5], [{1, 2, 3}, {3, 4, 5}, {1, 4}, {2, 5}], 2),  # greedy would also find 2 here
]
for universe, sets, expected in hand_cases:
    answer, agree = check_all_versions(universe, sets)
    report(answer == expected and agree,
           f"U={format_set(universe)} sets={[format_set(chosen_set) for chosen_set in sets]}"
           f" -> {answer}, expected {expected}")

# Random cases against brute force.
random.seed(53)
trial_count = 1500
failures = 0
for _ in range(trial_count):
    universe = list(range(1, random.randint(1, 7) + 1))
    sets = [set(random.sample(universe, random.randint(1, len(universe))))
            for _ in range(random.randint(0, 8))]
    answer, agree = check_all_versions(universe, sets)
    if answer != brute_force_set_cover(universe, sets)[0] or not agree:
        failures += 1
report(failures == 0, f"{trial_count} random cases (|U| 1-7, 0-8 sets) agree with brute force"
       f" ({trial_count - failures}/{trial_count})")

print(f"\n{'ALL PASS' if all_passed else 'SOME TESTS FAILED'}")

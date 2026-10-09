r"""
SET COVER -- DYNAMIC PROGRAMMING OVER SUBSETS OF THE UNIVERSE
Lecture 4-5, slides 53-54 (no CLRS section gives this algorithm).

Notes: [[Set Cover — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Set Cover — Code Notes.md

What is in this file:
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
# Notes: [[Set Cover — Code Notes#2. The lecture's table]] (variables)

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
# Notes: [[Set Cover — Code Notes#3. Restore the cover — walking back on the table]] (walk-back rule, variables)

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
# Notes: [[Set Cover — Code Notes#4. One row instead of the table]] (why the direction does not matter)

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

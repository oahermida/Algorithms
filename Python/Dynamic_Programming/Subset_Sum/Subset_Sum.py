r"""
SUBSET SUM
Lecture 4-5, slides 30-38; Erickson, Algorithms, section 3.8.

Notes: [[Subset Sum — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Subset Sum — Code Notes.md

What is in this file:
    1. brute_force_subset_sum   every subset, O(n * 2^n)      [slide 31]
    2. subset_sum_table         the lecture's algorithm       [slide 37]
    3. restore_subset           WHICH subset, not just yes/no
    4. subset_sum_rolling       one row instead of the grid, O(s) space
    5. subset_sum_bitset        the same recurrence in one integer, beyond the
                                slides -- included because it makes section 7
                                runnable at interesting sizes
    6. the slide's examples, with the grid printed as the lecture draws it
    7. the pseudopolynomial demonstration
    8. agreement checks

Run with:
    python3 Subset_Sum.py
"""

import random
import time
from itertools import combinations

# The two examples from the slides.
SLIDE_SET = [2, 12, 4, 26, 14, 100, 6]      # slide 30, targets 58 (yes) and 59 (no)
GRID_SET = [1, 3, 2, 5]                      # slide 32, target 7


# =====================================================================
# 1. BRUTE FORCE -- every subset [slide 31]
# =====================================================================
# Notes: [[Subset Sum — Code Notes#1. Brute force — every subset]] (variables)

def brute_force_subset_sum(values, target):
    for subset_size in range(len(values) + 1):
        for chosen in combinations(range(len(values)), subset_size):
            if sum(values[index] for index in chosen) == target:
                return [values[index] for index in chosen]
    return None


# =====================================================================
# 2. THE LECTURE'S ALGORITHM [slide 37]
# =====================================================================
# Notes: [[Subset Sum — Code Notes#2. The lecture's algorithm]] (variables, orientation, bounds guard)

def subset_sum_table(values, target):
    table = [[False] * (target + 1) for _ in range(len(values) + 1)]
    table[0][0] = True                              # the empty subset sums to 0

    for element_count in range(1, len(values) + 1):
        element_value = values[element_count - 1]
        for current_sum in range(target + 1):
            # SKIP this element: was the sum already reachable without it?
            reachable = table[element_count - 1][current_sum]
            # USE this element: was the remainder reachable without it?
            if not reachable and current_sum >= element_value:
                reachable = table[element_count - 1][current_sum - element_value]
            table[element_count][current_sum] = reachable

    return table[len(values)][target], table


# =====================================================================
# 3. WHICH SUBSET -- reading the answer back out
# =====================================================================
# Notes: [[Subset Sum — Code Notes#3. Which subset — reading the answer back out]] (walk-back rule)

def restore_subset(values, table, target):
    if not table[len(values)][target]:
        return None

    chosen = []
    element_count = len(values)
    remaining = target

    while element_count > 0:
        element_value = values[element_count - 1]
        if table[element_count - 1][remaining]:
            element_count -= 1                      # skipped
        else:
            chosen.append(element_value)            # used
            remaining -= element_value
            element_count -= 1

    chosen.reverse()
    return chosen


# =====================================================================
# 4. ONE ROW INSTEAD OF THE GRID
# =====================================================================
# Notes: [[Subset Sum — Code Notes#4. One row instead of the grid]] (why the loop runs downward)

def subset_sum_rolling(values, target):
    reachable = [False] * (target + 1)
    reachable[0] = True

    for element_value in values:
        for current_sum in range(target, element_value - 1, -1):     # DOWNWARD
            if reachable[current_sum - element_value]:
                reachable[current_sum] = True

    return reachable[target]


# =====================================================================
# 5. THE SAME RECURRENCE IN ONE INTEGER -- beyond the slides
# =====================================================================
# Notes: [[Subset Sum — Code Notes#5. The same recurrence in one integer — beyond the slides]]

def subset_sum_bitset(values, target):
    mask = (1 << (target + 1)) - 1
    reachable = 1                                    # only bit 0: the empty sum

    for element_value in values:
        reachable |= (reachable << element_value) & mask

    return bool(reachable >> target & 1)


# =====================================================================
# 6. RUN THE SLIDE'S EXAMPLES
# =====================================================================

print("=" * 78)
print("SUBSET SUM   -- Lecture 4-5, slides 30-38;  Erickson 3.8")
print("=" * 78)

print(f"\nX = {{{', '.join(str(value) for value in SLIDE_SET)}}}   [slide 30]\n")

for target in (58, 59):
    found, table = subset_sum_table(SLIDE_SET, target)
    subset = restore_subset(SLIDE_SET, table, target)
    print(f"  s = {target}:  {'YES' if found else 'NO'}", end="")
    if subset:
        print(f"   {' + '.join(str(value) for value in subset)} = {sum(subset)}")
    else:
        print()

print(f"\n  the slide's own answer for 58 is 6 + 12 + 14 + 26; this finds")
print(f"  {' + '.join(str(v) for v in restore_subset(SLIDE_SET, subset_sum_table(SLIDE_SET, 58)[1], 58))}"
      f" -- a different subset, equally correct")
print(f"\n  and for 59, the slide's reasoning is 'all numbers in the set are even,")
print(f"  so no odd sum is reachable'. the DP does not know that argument -- it")
print(f"  fills all {(59 + 1) * (len(SLIDE_SET) + 1)} cells to find out, and every odd row comes out 0.")

odd_rows_all_false = all(
    not subset_sum_table(SLIDE_SET, 59)[1][len(SLIDE_SET)][odd_sum]
    for odd_sum in range(1, 60, 2))
print(f"  every odd target from 1 to 59 is unreachable: {odd_rows_all_false}")


# =====================================================================
# 7. THE GRID, AS THE LECTURE DRAWS IT [slide 32]
# =====================================================================
# Printed in the SLIDE's orientation -- sums down the side, elements across the
# top -- even though the table is stored the other way round. That is the
# transposition described in the docstring, made concrete.

print("\n" + "=" * 78)
print("THE GRID FOR X = {1, 3, 2, 5}, s = 7   [slide 32]")
print("=" * 78)

grid_found, grid_table = subset_sum_table(GRID_SET, 7)
grid_subset = restore_subset(GRID_SET, grid_table, 7)

column_labels = ["{}"] + [f"x{index}={value}"
                          for index, value in enumerate(GRID_SET, start=1)]
print("\n      " + "".join(f"{label:>8}" for label in column_labels))
print("      " + "-" * (8 * (len(GRID_SET) + 1)))
for current_sum in range(8):
    cells = "".join(f"{1 if grid_table[element_count][current_sum] else 0:>8}"
                    for element_count in range(len(GRID_SET) + 1))
    print(f"{current_sum:>4} |" + cells)

print(f"\n  read a column as 'which sums can I make with the elements up to here'")
print(f"  the first column is the empty set: only 0 is reachable")
print(f"  each later column copies the one before it, then ORs in a copy of it")
print(f"  shifted down by that element's value")
print(f"\n  answer A[n][s] = A[4][7] = {1 if grid_found else 0}"
      f"   ->  {' + '.join(str(value) for value in grid_subset)} = {sum(grid_subset)}")
print(f"  (the slide's pseudocode says 'return A[s, n]'; in the loops' own")
print(f"   convention that is A[n, s] -- see the index note in the docstring)")

print(f"\n  every reachable total for this set, read off the last column:")
reachable_totals = [current_sum for current_sum in range(8)
                    if grid_table[len(GRID_SET)][current_sum]]
print(f"    {reachable_totals}")
print(f"  all eight targets from 0 to 7 are reachable, which is why the last")
print(f"  column is solid 1s. the set totals {sum(GRID_SET)}, so targets 8 to "
      f"{sum(GRID_SET)} would be")
print(f"  reachable too, and anything above {sum(GRID_SET)} never could be.")


# =====================================================================
# 8. PSEUDOPOLYNOMIAL -- WHERE O(sn) LOSES TO O(n * 2^n)
# =====================================================================
# The slide says "note that potentially s can be bigger than 2^n". This is that
# sentence, run.

print("\n" + "=" * 78)
print("WHY O(sn) IS NOT A POLYNOMIAL ALGORITHM   [slide 31]")
print("=" * 78)

print(f"\n{'n':>4}{'s':>14}{'subsets 2^n':>16}{'cells s*n':>16}{'which is smaller':>19}")
print("-" * 78)
for element_count, target in ((20, 10), (20, 500), (16, 60000), (12, 4000000), (10, 100000000)):
    subsets = 2 ** element_count
    cells = target * element_count
    print(f"{element_count:>4}{target:>14,}{subsets:>16,}{cells:>16,}"
          f"{('brute force' if subsets < cells else 'the DP table'):>19}")

print("\n  the DP wins on the first rows and loses badly on the last. nothing about")
print("  the SET changed -- only the size of the number s, which costs about")
print("  log2(s) bits to write down. an algorithm taking s steps takes 2^(those")
print("  bits) steps, which is exponential in the length of its own input.")

# The honest measurement is what happens to the DP as s grows while the SET
# stays the same size. Each row below multiplies s by 10 -- which lengthens the
# written-down input by a single digit -- and the work goes up by 10 with it.

print("\n  the same 12-element set, with s multiplied by 10 each time:")
print(f"\n{'s':>12}{'digits in s':>14}{'table cells':>16}{'dp secs':>12}"
      f"{'brute secs':>13}")
print("-" * 78)

random.seed(21)
fixed_values = [random.randint(1, 60) for _ in range(12)]

for target in (200, 2000, 20000, 200000):
    start_time = time.perf_counter()
    subset_sum_table(fixed_values, target)
    dp_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    brute_force_subset_sum(fixed_values, target)
    brute_seconds = time.perf_counter() - start_time

    print(f"{target:>12,}{len(str(target)):>14}{target * len(fixed_values):>16,}"
          f"{dp_seconds:>12.4f}{brute_seconds:>13.4f}")

print("\n  the brute-force column does not move at all -- it depends only on n,")
print("  and n never changed. the DP column grows by a factor of 10 per row,")
print("  while the input grew by ONE CHARACTER. that is the whole distinction:")
print("  the DP is linear in the VALUE of s and exponential in its LENGTH.")
print("\n  by the last row the DP is already the slower of the two, on an input a")
print("  human would describe as tiny.")

print("\n  THE POINT: subset sum is NP-complete, and appears on this course's")
print("  NP-complete list in Part II. The O(sn) algorithm does not contradict")
print("  that, because it never was polynomial in the input size. 'Pseudo-")
print("  polynomial' means polynomial in the VALUE of a number, exponential in")
print("  its LENGTH.")


# =====================================================================
# 9. AGREEMENT CHECK
# =====================================================================
# All four versions must agree on the yes/no, and every subset that comes back
# must actually consist of distinct elements of X summing to the target -- the
# "at most once" rule from slide 30 is exactly what a careless rolling
# implementation breaks, so it is checked explicitly.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(9)
trial_count = 3000
decision_disagreements = 0
subset_disagreements = 0
reuse_violations = 0

for _ in range(trial_count):
    element_count = random.randint(1, 10)
    values = [random.randint(1, 25) for _ in range(element_count)]
    target = random.randint(0, 40)

    table_answer, table_grid = subset_sum_table(values, target)
    brute_subset = brute_force_subset_sum(values, target)

    if (table_answer != (brute_subset is not None)
            or subset_sum_rolling(values, target) != table_answer
            or subset_sum_bitset(values, target) != table_answer):
        decision_disagreements += 1

    restored = restore_subset(values, table_grid, target)
    if table_answer:
        if restored is None or sum(restored) != target:
            subset_disagreements += 1
        else:
            # every element of the restored subset must come from X, counted
            # with multiplicity -- no element used twice
            remaining_pool = list(values)
            for value in restored:
                if value in remaining_pool:
                    remaining_pool.remove(value)
                else:
                    reuse_violations += 1
    elif restored is not None:
        subset_disagreements += 1

print(f"\n{trial_count} random sets, up to 10 elements of 1-25, targets 0-40\n")
print(f"  table / rolling / bitset / brute force agree  "
      f"{trial_count - decision_disagreements}/{trial_count}")
print(f"  restored subsets sum to the target             "
      f"{trial_count - subset_disagreements}/{trial_count}")
print(f"  no element used more than once                 "
      f"{trial_count - reuse_violations}/{trial_count}")
print("\n  (the last check is slide 30's '6 + 6 + 6 + 14 + 26 is not allowed'. it is")
print("   the rule a rolling implementation breaks by scanning upward instead of")
print("   downward -- the element gets reused within its own pass)")

# And the specific bug that check exists to catch, demonstrated.
def subset_sum_rolling_wrong(values, target):
    """The rolling version with the loop scanning UPWARD -- allows reuse."""
    reachable = [False] * (target + 1)
    reachable[0] = True
    for element_value in values:
        for current_sum in range(element_value, target + 1):          # UPWARD
            if reachable[current_sum - element_value]:
                reachable[current_sum] = True
    return reachable[target]

print(f"\n  the wrong direction, on X = {{3}}, s = 9:")
print(f"    correct (downward): {subset_sum_rolling([3], 9)}"
      f"   -- one 3 cannot make 9")
print(f"    buggy   (upward):   {subset_sum_rolling_wrong([3], 9)}"
      f"   -- it used the 3 three times, which is coin change, not subset sum")


# Notes: [[Subset Sum — Code Notes#How it runs]] (traced example on X = {1, 3, 2, 5}, s = 7)

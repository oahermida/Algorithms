r"""
SUBSET SUM
==========

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 30-38 -- the same deck
as the two bunnies. Also Erickson, *Algorithms*, section 3.8. It is the deck's
worked example for the plan item "Pseudopolynomial algorithms via dynamic
programming", which is the real subject of this file.

    SUBSET SUM [slide 30]
        Input:     a set X of positive integers x1, x2, ..., xn and integer s
        Question:  is there a subset S of X such that the sum of all elements
                   in S is s?

        Example:   X = {2, 12, 4, 26, 14, 100, 6},  s = 58
                   6 + 12 + 14 + 26 = 58.
                   6 + 6 + 6 + 14 + 26 = 58 is NOT allowed, as we can only use
                   each number at most once.

                   What if s = 59?
                   We cannot obtain 59 as a sum, as all numbers in the set are
                   even.

Two things that statement fixes, and both matter:

    EACH NUMBER AT MOST ONCE. This is what separates subset sum from coin
    change (see the coin-change example in the vault's DecodingIntuition note,
    where a coin may be reused). It is why the recurrence below moves to i-1
    after taking an element and never back to i.

    THE ANSWER IS YES OR NO. The slide's algorithm is a DECISION procedure: it
    fills a table of 1s and 0s and returns one bit. It does not say WHICH
    subset -- section 4 adds that, because in practice the subset is what you
    want.

The s = 59 case is worth keeping, because it is a reminder that a "no" can
sometimes be proved instantly by an argument the algorithm knows nothing about:
every element is even, so every subset sum is even, so no odd target is
reachable. The DP still fills the whole table to discover that.


WHY IT IS HARD [slide 31]
-------------------------
    - Consider all subsets and compute their sum. The running time is O(n*2^n).
    - In general it is a very hard problem and the best known algorithm for
      this problem for the general case is exponential.
    - However, we can do better if s is small.
    - We present an algorithm with O(sn) running time.
    - Note that potentially s can be bigger than 2^n.

That last line is the whole point of the section, and it is easy to read past.
See PSEUDOPOLYNOMIAL below.


THE TABLE [slides 32-37]
------------------------
    Consider an arbitrary order of elements from X. Let it be x1, x2, ..., xn.
    Construct a table A of size (s+1) x (n+1).
    A[i, j] = 1 if i can be obtained as sum of elements from the set
    {x1, x2, ..., xj}.

So one axis is every target from 0 to s, the other is "how many of the elements
am I allowed to use". The recurrence is a two-way choice per element:

        A[i][j] = A[i-1][j]  OR  A[i-1][j - xi]
                     \                \
                      \                '-- USE element i: then the remaining
                       \                   j - xi must be reachable without it
                        '-- SKIP element i: j was already reachable without it

    base case:  A[0][0] = 1        the empty subset sums to 0
                A[0][j] = 0 for j > 0

Drawn for one cell, with x = 3:

        target j-3  ---- take the 3 ------.
        (using items 1..i-1)              |
                                          v
                                     target j
        target j    ---- skip the 3 ------^
        (using items 1..i-1)

"Reachable" only ever flows forward, from fewer elements to more, which is why
a single pass fills the table.

    X = {1, 3, 2, 5},  s = 7   [slide 32]

The lecture builds that 8 x 5 grid one column at a time; section 5 prints the
finished version in the same orientation.


THE PROOF [slide 38]
--------------------
    We want to prove that A[i, j] = 1 if and only if there is Si subset of
    {x1, ..., xi} such that the sum of elements in Si equals j.

    Proof by induction.
    At the very beginning, step 0, the statement is true: only A[0, 0] equals 1.
    Now we prove the induction step from i to i+1.
    Clearly, if A[i, j] = 1 then A[i+1, j] should be one.
    Similarly, if A[i, j - x(i+1)] = 1 then A[i+1, j] should be one.

The two "clearly" lines are the two halves of the OR, and they are the only two
ways a sum can become reachable when one more element is offered: it was already
reachable, or it becomes reachable by adding exactly that element. Nothing else
changes, which is what makes the induction step airtight rather than plausible.


AN INDEX MIX-UP ACROSS SLIDES 32, 37 AND 38
-------------------------------------------
Slide 32 defines A[i, j] with i the SUM and j the element count. Slide 38's
proof uses A[i, j] with i the element count and j the SUM -- transposed. The
slide 37 pseudocode follows slide 38's order in its loops:

        for i in {1, .., n} do           <- i is the element index
            for j in {0, .., s} do       <- j is the sum
                A[i, j] = A[i-1, j] OR A[i-1, j - xi]
        return A[s, n]                   <- but this is slide 32's order

so the loops fill A[element][sum] and the return statement reads A[sum][element].
Taken literally it returns the wrong cell unless s and n happen to be equal.
What is meant is A[n, s] in the loops' own convention: all n elements, target s.

The pseudocode also indexes A[i-1, j - xi] without checking j - xi >= 0, which
the rod cutting and knight slides both flag as a caution elsewhere. Section 3
guards it.

None of this is an objection to the method -- the method is clearly right and
the proof on slide 38 is correct. It is flagged so that transcribing the
pseudocode straight into code does not silently produce nonsense. This file
uses the loops' convention throughout: table[element_count][target].


PSEUDOPOLYNOMIAL -- THE ACTUAL LESSON
-------------------------------------
O(sn) looks polynomial. It is not polynomial in the SIZE OF THE INPUT, and the
distinction is the reason this problem is in the lecture at all.

An input of n numbers with target s is written down in roughly

        n * (digits per number) + log2(s)  bits

because a number is written in binary, not in tally marks. The target s takes
about log2(s) BITS to write, so an algorithm that takes s steps is taking
2^(bits of s) steps -- exponential in the length of its own input.

    "Note that potentially s can be bigger than 2^n."  [slide 31]

If s = 2^n then O(sn) = O(n * 2^n), which is exactly the brute force the slide
started by rejecting. The DP is a genuine improvement only while s stays small,
and section 7 shows a case where it is thousands of times SLOWER than trying
every subset.

That is what "pseudopolynomial" means: polynomial in the VALUE of a number in
the input, exponential in its LENGTH. Subset sum is NP-complete (it is on the
lecture's NP-complete list in Part II), and this algorithm does not contradict
that -- it never was polynomial.


WHAT IS IN THIS FILE
--------------------
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
# Follows the statement literally: look at all 2^n subsets, add each one up.
# Returns the subset itself rather than a bit, so the table version has
# something independent to be checked against.
#
# subset_size   - how many elements this round is choosing
# chosen        - one particular combination of that many elements
#
# O(n * 2^n): 2^n subsets, and adding one up costs O(n).

def brute_force_subset_sum(values, target):
    for subset_size in range(len(values) + 1):
        for chosen in combinations(range(len(values)), subset_size):
            if sum(values[index] for index in chosen) == target:
                return [values[index] for index in chosen]
    return None


# =====================================================================
# 2. THE LECTURE'S ALGORITHM [slide 37]
# =====================================================================
# values        - X, the set, in an arbitrary but fixed order
# target        - s, the sum being asked about
# table         - A; table[element_count][sum] is True when `sum` can be made
#                 from the first `element_count` elements of X
# element_count - how many elements are on offer in this row; 0 .. n
# current_sum   - the target this cell is about; 0 .. s
#
# The orientation is the one the slide's LOOPS use: element count first, sum
# second. See the index note in the docstring.
#
# Row 0 is the base case: with no elements the only reachable sum is 0. Every
# later row is computed from the row directly above it, which is why the rolling
# version in section 5 works.
#
# The `current_sum >= element_value` guard is the bounds check the slide's
# pseudocode leaves out: you cannot use an element bigger than the target you
# are trying to hit.
#
# O(sn) cells, constant work each.

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
# The slide's algorithm returns one bit. The table holds more than that, and the
# subset can be recovered by the same walk-back used in ../Bunny_DP/ and
# ../Knight_Rewards/: stand on the answer cell and ask which of the two OR
# branches made it True.
#
# element_count / remaining - where the walk currently stands
#
#   table[element_count-1][remaining] is True  ->  this element was SKIPPED,
#                                                  the sum was already reachable
#   otherwise                                  ->  this element was USED, so
#                                                  subtract it and carry on
#
# Preferring the skip makes the result deterministic; when several subsets work,
# this returns the one using the latest elements.

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
# Every row of the table reads only the row above it, so the whole grid is never
# needed at once -- exactly the observation that shrinks the bunny to two
# variables and Fibonacci to two.
#
# reachable - one row: reachable[sum] is True when `sum` can be made from the
#             elements seen so far
#
# THE SUBTLETY: the row must be updated from HIGH sums DOWNWARD. Going upward
# would let a cell that has already been updated with this element be read again
# by a later cell in the same pass -- which would silently allow the element to
# be used twice, turning this into the coin-change problem. The descending range
# is doing real work, not cosmetics; section 8 checks it against the grid.
#
# O(s) space instead of O(sn). Like every other space optimisation in this
# collection, it gives up the ability to restore the subset.

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
# Not examinable, and included for one reason: it makes section 7 runnable at
# sizes where the point about s becomes visible.
#
# reachable - a single Python integer used as a bit set. Bit k is 1 exactly when
#             the sum k is reachable. It starts as 1, i.e. only bit 0 set, which
#             is "only the empty sum is reachable" -- the same base case.
#
# Offering one more element x shifts the whole set of reachable sums up by x and
# ORs it back in:
#
#     reachable |= reachable << element_value
#
# That one line IS A[i][j] = A[i-1][j] OR A[i-1][j-xi], done for every j at once.
# The mask keeps the integer from growing past s.
#
# Same O(sn) bit operations, but the machine does 64 of them per word, so the
# constant factor is dramatically smaller. The asymptotics are unchanged -- and
# so is the pseudopolynomial problem.

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


# === How it Runs ===
#
# --- subset_sum_table ---
# table is (n+1) rows by (s+1) columns of False, with one cell written directly:
# table[0][0] = True, the empty subset summing to 0. that is the base case and
# the only value the recurrence cannot produce
# each row corresponds to ONE MORE ELEMENT being offered, and is computed
# entirely from the row above it -- nothing ever reads its own row, which is
# what makes the whole thing a single forward pass
# each cell does constant work: one lookup for SKIP, and if that failed, one
# bounds check and one lookup for USE
#
# filling the grid for X = {1, 3, 2, 5}, s = 7, row by row:
#
#   row 0 (no elements):     sums reachable = {0}
#     1 0 0 0 0 0 0 0
#
#   row 1 (offer x1 = 1):    copy row 0, then OR in row 0 shifted down by 1
#     1 1 0 0 0 0 0 0        reachable = {0, 1}
#
#   row 2 (offer x2 = 3):    copy row 1, then OR in row 1 shifted down by 3
#     1 1 0 1 1 0 0 0        reachable = {0, 1, 3, 4}
#                            3 = the 3 alone,  4 = 1 + 3
#
#   row 3 (offer x3 = 2):    copy row 2, then OR in row 2 shifted down by 2
#     1 1 1 1 1 1 1 0        reachable = {0, 1, 2, 3, 4, 5, 6}
#                            5 = 3 + 2,  6 = 1 + 3 + 2
#
#   row 4 (offer x4 = 5):    copy row 3, then OR in row 3 shifted down by 5
#     1 1 1 1 1 1 1 1        reachable = {0..7},  7 = 2 + 5  (or 1 + 3 + ... )
#
#   return table[4][7] = True
#
# "copy the row above, then OR in a shifted copy of it" IS the recurrence --
# the copy is the SKIP branch and the shift is the USE branch. seeing it as a
# shift is also what makes the one-integer version in section 5 obvious
#
# --- restore_subset ---
# the table says yes; the walk-back says which elements
#   at element_count=4, remaining=7:  table[3][7] = False
#       -> row 3 could NOT make 7, so x4 = 5 must have been used
#       -> take 5, remaining becomes 2
#   at element_count=3, remaining=2:  table[2][2] = False
#       -> row 2 could not make 2, so x3 = 2 was used
#       -> take 2, remaining becomes 0
#   at element_count=2, remaining=0:  table[1][0] = True
#       -> 0 was already reachable without x2, so x2 = 3 was SKIPPED
#   at element_count=1, remaining=0:  table[0][0] = True  -> x1 skipped
#   chosen = [2, 5], reversed into set order, summing to 7
#
# the test is always "could the row above already do it?" -- if yes the element
# was not needed, if no it was the only thing that can have made the difference
#
# --- subset_sum_rolling, and why the loop runs downward ---
# one row, updated in place. going DOWNWARD, every cell it reads
# (current_sum - element_value) is below the cells already written this pass, so
# every read sees the PREVIOUS row's value -- which is what the recurrence asks
# for
# going upward, a cell written earlier in this same pass gets read again later
# in the same pass, so the element can be applied twice:
#   X = {3}, s = 9, scanning upward
#     reachable[3] set from reachable[0]      <- uses the 3 once
#     reachable[6] set from reachable[3]      <- uses it AGAIN
#     reachable[9] set from reachable[6]      <- and again
#   answer True, which is wrong: one 3 cannot make 9
# that upward version is a correct algorithm for a DIFFERENT problem -- coin
# change with unlimited coins. one loop direction is the entire difference
# between the two

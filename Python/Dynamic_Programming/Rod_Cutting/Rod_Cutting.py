r"""
ROD CUTTING
===========

Advanced Algorithms, Lecture 3 (Ivan Bliznets), slides 10-12, cited to CLRS 15.1
(3rd edition -- it moves to 14.1 in the 4th).

    ROD CUTTING [slide 10]
        You are given a rod of length n. You can cut it into several pieces and
        then sell all pieces. Price of a piece depends on its length according
        to a table:

            Length   1   2   3   4    5   ...
            Price    1   5   8   10   17  ...

        "It is clear that the longer is your rod the more money you can get. As
         a piece of length 1 already provides money."

        Goal: choose the cuts that maximise the total price of the pieces.

The cuts are free and only whole-number lengths exist, so a rod of length n has
n-1 possible cut positions and every one of them is independently cut or not:

    a rod of length 8 -- the 7 places a cut could go:

            +---+---+---+---+---+---+---+---+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
            +---+---+---+---+---+---+---+---+
                ^   ^   ^   ^   ^   ^   ^
                each cut or not cut, independently  ->  2^7 = 128 ways

which is the slide's "brute force solution 2^(n-1), too slow" [slide 11].


THE RECURRENCE [slide 11]
-------------------------
The lecture's argument, which is worth reading as a proof rather than a rule:

    Consider an optimal solution of cuts. Let the left-most part (place of the
    first cut) have a length l. Then R[n] = P[l] + R[n-l], P[l] being the price
    of a rod of length l. So your first cut of length l should be the one that
    maximises P[l] + R[n-l]. Hence, in order to compute the answer for n, it is
    helpful to find an answer for all smaller values.

Drawn:

        +---------+-------------------------------+
        |    l    |          the rest: n - l      |
        +---------+-------------------------------+
           P[l]     +          R[n - l]
          sold as              cut optimally, whatever that turns out to be
          one piece            -- and that is a SMALLER instance of this
                                  same problem

    R[n] = max over l in 1..n of ( P[l] + R[n-l] )

    base case:  R[0] = 0        a rod of length 0 is worth nothing
    answer:     R[n]

WHY THE ARGUMENT IS VALID. It never asks where the LAST cut is, or how many cuts
there are -- only how long the leftmost piece is. Every possible set of cuts has
exactly one leftmost piece, of some length l between 1 and n, so the n cases are
exhaustive and do not overlap. And the l = n case is "no cut at all", the whole
rod sold in one piece, which is why the max runs all the way to n.

This is optimal substructure in its cleanest form: once the first piece is
fixed, the rest of the rod is an independent, smaller copy of the problem, and
how the first piece was chosen cannot change what the rest is worth.

    O(n^2) time -- n values of R, each a max over up to n options  [slide 12]
    "incredibly faster compared to 2^n"


A TYPO ON SLIDE 12
------------------
The slide's pseudocode reads:

        R[0] = 0
        for i in {1, .., n} do  R[i] = -inf  end for
        for i in {1, .., n} do
            for j in {i, ..1} do
                R[n] = max{R[n], P[i] + R[n - i]}        <- R[n], every time
            end for
        end for
        return R[n]

The inner assignment writes R[n] on every pass, so R[1] .. R[n-1] are never
filled and stay -infinity. Since R[n-i] is then -infinity except when i = n,
the whole thing collapses to R[n] = P[n]: the uncut rod, which is only
accidentally right when no cut is profitable. The loop variable j is also never
used in the body.

What is meant is R[j] = max{R[j], P[i] + R[j - i]} with j the rod length being
filled and i the first piece, which is what section 2 implements. The slides for
the knight problem have a companion slip -- "return R[n]" for a 2-D table; see
../Knight_Rewards/Knight_Rewards.py.

Mentioned because reading the slide literally and getting P[n] is a plausible
way to lose marks, not because the lecture is unclear about the method.


TWO PRICE TABLES
----------------
The slide's table (lengths 1-5) is 1, 5, 8, 10, 17. CLRS figure 15.1's table
(lengths 1-10) is 1, 5, 8, 9, 10, 17, 17, 20, 24, 30 -- the same opening, then
they diverge: the slide's price for length 4 is 10 where CLRS has 9, and the
slide's length 5 is 17 where CLRS has 10. Both are run below. Nothing in the
method depends on which is used, but the ANSWERS differ, so it is worth knowing
which table a given exam question is handing you.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_rod         every subset of cut positions, 2^(n-1) of them
    2. rod_cutting             the bottom-up O(n^2) version  [slide 12, fixed]
    3. rod_cutting_memoised    the same recurrence top-down, for the comparison
                               made in ../Fibonacci_DP/Fibonacci_DP.py
    4. restore_cuts            which pieces to actually cut, not just the value
    5. both price tables, worked
    6. agreement checks

Run with:
    python3 Rod_Cutting.py
"""

import random
import time
from itertools import combinations

NEGATIVE_INFINITY = float("-inf")

# prices[length] is the price of a piece of that length; index 0 is unused
# padding so that the list index IS the length, matching P[l] on the slide.
SLIDE_PRICES = [0, 1, 5, 8, 10, 17]
CLRS_PRICES = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


# =====================================================================
# 1. BRUTE FORCE -- every subset of cut positions
# =====================================================================
# Follows the problem statement literally: a rod of length n has n-1 interior
# positions, and a set of cuts is any subset of them. 2^(n-1) subsets.
#
# cut_positions - the chosen subset, as distances from the left end
# pieces        - the lengths those cuts produce
#
# Returns the best total and the piece lengths that achieve it, so the
# reconstruction in section 4 has something independent to be checked against.

def brute_force_rod(prices, length):
    if length == 0:
        return 0, []

    best_total = NEGATIVE_INFINITY
    best_pieces = []

    for cut_count in range(length):                        # 0 .. length-1 cuts
        for cut_positions in combinations(range(1, length), cut_count):
            boundaries = (0,) + cut_positions + (length,)
            pieces = [boundaries[index + 1] - boundaries[index]
                      for index in range(len(boundaries) - 1)]
            total = sum(prices[piece] for piece in pieces)
            if total > best_total:
                best_total = total
                best_pieces = pieces

    return best_total, best_pieces


# =====================================================================
# 2. BOTTOM-UP -- the lecture's algorithm [slide 12, with the typo fixed]
# =====================================================================
# prices             - P, indexed by piece length
# length             - n, the rod to be cut
# best_for_length    - R; best_for_length[rod] is the best revenue obtainable
#                      from a rod of exactly that length
# rod                - the length being filled on this pass; runs 1, 2, ..., n
# first_piece        - the candidate length of the LEFTMOST piece
# first_piece_of     - for the reconstruction: which first_piece won, per rod
#
# The outer loop fills R left to right, so R[rod - first_piece] is always
# already final when it is read -- the same "loop order is a topological order"
# guarantee as every other bottom-up DP in this collection.
#
# first_piece runs all the way to rod, and that last case is "do not cut at
# all": P[rod] + R[0] = P[rod] + 0.

def rod_cutting(prices, length):
    best_for_length = [0] * (length + 1)                   # R[0] = 0, the base case
    first_piece_of = [0] * (length + 1)

    for rod in range(1, length + 1):
        best_revenue = NEGATIVE_INFINITY
        best_first_piece = 0

        for first_piece in range(1, min(rod, len(prices) - 1) + 1):
            candidate = prices[first_piece] + best_for_length[rod - first_piece]
            if candidate > best_revenue:
                best_revenue = candidate
                best_first_piece = first_piece

        best_for_length[rod] = best_revenue
        first_piece_of[rod] = best_first_piece

    return best_for_length[length], best_for_length, first_piece_of


# =====================================================================
# 3. TOP-DOWN WITH MEMOISATION -- the same recurrence, other direction
# =====================================================================
# Included for the comparison made in ../Fibonacci_DP/Fibonacci_DP.py: this is
# a depth-first search over the same subproblem DAG, with a cache that stops it
# re-entering a length it has already solved. The bottom-up version walks the
# same DAG in topological order instead.
#
# Identical answers, and the same O(n^2) work -- the cache turns the 2^(n-1)
# tree into n distinct subproblems, each doing up to n work.

def rod_cutting_memoised(prices, length, memo=None):
    if memo is None:
        memo = {0: 0}

    if length in memo:
        return memo[length]

    best_revenue = NEGATIVE_INFINITY
    for first_piece in range(1, min(length, len(prices) - 1) + 1):
        best_revenue = max(best_revenue,
                           prices[first_piece]
                           + rod_cutting_memoised(prices, length - first_piece, memo))

    memo[length] = best_revenue
    return best_revenue


# =====================================================================
# 4. RESTORING THE CUTS
# =====================================================================
# R tells you what the rod is worth, not what to do with the saw. The fix is the
# same one slide 16 of the knight lecture describes: record the winning choice
# while the max is being taken, then read it back.
#
# Here the recorded choice is the length of the leftmost piece. Peel it off,
# then ask the same question of what remains -- which is exactly the structure
# the recurrence claimed, now run forwards.

def restore_cuts(first_piece_of, length):
    pieces = []
    remaining = length
    while remaining > 0:
        piece = first_piece_of[remaining]
        pieces.append(piece)
        remaining -= piece
    return pieces


# =====================================================================
# 5. RUN IT
# =====================================================================

def show_table(prices, length, label):
    total, table, first_piece_of = rod_cutting(prices, length)
    pieces = restore_cuts(first_piece_of, length)

    print(f"\n  {label}")
    print("    length " + "".join(f"{rod:>5}" for rod in range(length + 1)))
    print("    P[l]   " + "".join(
        f"{(prices[rod] if rod < len(prices) else 0):>5}" for rod in range(length + 1)))
    print("    R[l]   " + "".join(f"{value:>5}" for value in table))
    print("    cut    " + "".join(f"{first_piece_of[rod]:>5}" for rod in range(length + 1)))
    print(f"    ('cut' is the leftmost piece to take off a rod of that length; 0 means none)")
    return total, pieces


print("=" * 78)
print("ROD CUTTING   -- Lecture 3, slides 10-12;  CLRS 15.1")
print("=" * 78)

print("\nTHE SLIDE'S PRICE TABLE  (lengths 1-5: 1, 5, 8, 10, 17)")
slide_total, slide_pieces = show_table(SLIDE_PRICES, 5, "rod of length 5")
print(f"\n    best revenue = {slide_total}")
print(f"    cut into     = {slide_pieces}  "
      f"({' + '.join(f'P[{piece}]={SLIDE_PRICES[piece]}' for piece in slide_pieces)})")
brute_total, brute_pieces = brute_force_rod(SLIDE_PRICES, 5)
print(f"    brute force over all 2^4 = 16 cut sets agrees: {brute_total} via {brute_pieces}")
print(f"\n    with this table a length-5 rod is best left UNCUT, because P[5] = 17")
print(f"    beats every way of splitting it -- e.g. 2 + 3 gives 5 + 8 = 13")

print("\n" + "-" * 78)
print("\nCLRS FIGURE 15.1'S TABLE  (lengths 1-10: 1, 5, 8, 9, 10, 17, 17, 20, 24, 30)")
clrs_total, clrs_pieces = show_table(CLRS_PRICES, 10, "rod of length 10")
print(f"\n    best revenue = {clrs_total}")
print(f"    cut into     = {clrs_pieces}  "
      f"({' + '.join(f'P[{piece}]={CLRS_PRICES[piece]}' for piece in clrs_pieces)})")

print(f"\n    the interesting entries in that R row:")
_, clrs_table, clrs_first = rod_cutting(CLRS_PRICES, 10)
for rod in (4, 5, 7, 8, 10):
    pieces = restore_cuts(clrs_first, rod)
    uncut = CLRS_PRICES[rod]
    print(f"      R[{rod:>2}] = {clrs_table[rod]:>2}  by cutting {str(pieces):<10}"
          f" vs {uncut:>2} for the uncut rod"
          f"{'   <- cutting wins' if clrs_table[rod] > uncut else '   <- leave it whole'}")

print(f"\n    R[10] = 30 is the uncut rod: P[10] = 30 is high enough that no split")
print(f"    beats it. R[8] = 22 is not: 2 + 6 pays 5 + 17 against P[8] = 20.")


# =====================================================================
# 6. WHY THE BRUTE FORCE IS HOPELESS
# =====================================================================

print("\n" + "=" * 78)
print("2^(n-1) VERSUS O(n^2)   [slide 11]")
print("=" * 78)

extended_prices = CLRS_PRICES + [random.Random(2).randint(25, 40) for _ in range(12)]

print(f"\n{'n':>5}{'cut sets':>14}{'brute secs':>14}{'dp secs':>12}{'both agree':>13}")
print("-" * 78)
for length in (4, 8, 12, 16, 18):
    start_time = time.perf_counter()
    brute_value, _ = brute_force_rod(extended_prices, length)
    brute_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    dp_value, _, _ = rod_cutting(extended_prices, length)
    dp_seconds = time.perf_counter() - start_time

    print(f"{length:>5}{2 ** (length - 1):>14,}{brute_seconds:>14.6f}"
          f"{dp_seconds:>12.6f}{str(brute_value == dp_value):>13}")

print("\n  the cut-set column doubles with every +1 of n, which is the slide's")
print("  2^(n-1) made visible; the dp column is quadratic and barely moves")


# =====================================================================
# 7. AGREEMENT CHECK
# =====================================================================
# Random price tables, including ones where cutting never pays and ones where
# it always does. The restored piece list is checked by actually adding it up --
# the value can be right while the reconstruction is wrong.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(4)
trial_count = 600
value_disagreements = 0
memo_disagreements = 0
piece_disagreements = 0

for _ in range(trial_count):
    max_length = random.randint(1, 11)
    # three shapes of price table: random, strongly convex (never cut), and
    # strongly concave (always cut into 1s)
    shape = random.choice(("random", "never cut", "always cut"))
    if shape == "random":
        prices = [0] + [random.randint(0, 30) for _ in range(max_length)]
    elif shape == "never cut":
        prices = [0] + [length ** 2 for length in range(1, max_length + 1)]
    else:
        prices = [0] + [10 for _ in range(max_length)]

    dp_total, _, first_piece_of = rod_cutting(prices, max_length)
    brute_total, _ = brute_force_rod(prices, max_length)

    if dp_total != brute_total:
        value_disagreements += 1
    if rod_cutting_memoised(prices, max_length) != dp_total:
        memo_disagreements += 1

    pieces = restore_cuts(first_piece_of, max_length)
    if sum(pieces) != max_length or sum(prices[piece] for piece in pieces) != dp_total:
        piece_disagreements += 1

print(f"\n{trial_count} random price tables, rods up to length 11")
print(f"  (three shapes: random prices, convex 'never cut', flat 'always cut')\n")
print(f"  bottom-up vs brute force          {trial_count - value_disagreements}/{trial_count}")
print(f"  top-down memoised vs bottom-up    {trial_count - memo_disagreements}/{trial_count}")
print(f"  restored pieces sum to n and to R {trial_count - piece_disagreements}/{trial_count}")


# === How it Runs ===
#
# --- rod_cutting ---
# best_for_length is R, one slot per rod length from 0 to n, filled left to right
# slot 0 is written directly as 0 -- the base case, and the only value the
# recurrence cannot produce (a rod of length 0 is worth nothing)
# each pass fills ONE slot by trying every possible leftmost piece:
#   for a rod of length `rod`, try first_piece = 1, 2, ..., rod
#   each option is worth P[first_piece] + R[rod - first_piece]
#   keep the best, and remember WHICH first_piece won
# R[rod - first_piece] is always already final, because rod - first_piece < rod
# and the loop only moves right. no recursion needed
#
# filling R for the CLRS table P = [_, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]:
#
#   R[0] = 0                                                     base case
#   R[1] = P[1] + R[0] = 1 + 0                        = 1        only one option
#   R[2] = max( P[1]+R[1] = 1+1 = 2,
#               P[2]+R[0] = 5+0 = 5 )                 = 5        uncut wins
#   R[3] = max( 1+5 = 6,  5+1 = 6,  8+0 = 8 )         = 8        uncut wins
#   R[4] = max( 1+8 = 9,  5+5 = 10, 8+1 = 9, 9+0 = 9) = 10       <- 2 + 2 WINS
#   R[5] = max( 1+10=11,  5+8 =13,  8+5 =13,
#               9+1 =10,  10+0=10 )                   = 13       <- 2 + 3
#   R[6] = max( 1+13=14,  5+10=15,  8+8 =16,
#               9+5 =14,  10+1=11,  17+0=17 )         = 17       uncut wins
#   R[7] = max( 1+17=18,  5+13=18,  8+10=18,
#               9+8 =17,  10+5=15,  17+1=18, 17+0=17) = 18       <- several ties
#   R[8] = max( 1+18=19,  5+17=22,  8+13=21,
#               9+10=19,  10+8=18,  17+5=22,
#               17+1=18,  20+0=20 )                   = 22       <- 2 + 6
#   R[9]  = 25   (3 + 6)
#   R[10] = 30   (uncut: P[10] = 30 beats every split)
#
# R[4] is the first slot where cutting beats not cutting, and it is worth
# stopping on: P[4] = 9 for the whole rod, but two pieces of length 2 pay 5 each.
# the table prices are not proportional to length, which is the only reason this
# problem exists at all
#
# R[7] shows several options tying at 18. any of them is a correct answer; the
# > in the loop keeps the FIRST one found, so the reconstruction is deterministic
# even though the problem is not
#
# --- restore_cuts ---
# first_piece_of[rod] recorded the winning first piece while the max was taken
# for the CLRS table at length 8:
#   first_piece_of[8] = 2   ->  cut off a 2, leaving 6
#   first_piece_of[6] = 6   ->  the remaining 6 is sold whole
#   remaining = 0, stop
#   pieces = [2, 6], worth P[2] + P[6] = 5 + 17 = 22, matching R[8] exactly
# the walk is forwards, not backwards, because the recurrence peels off the LEFT
# end -- unlike the bunny and knight tracebacks, which walk from the finish
#
# --- why the brute force is 2^(n-1) ---
# a rod of length n has n-1 interior positions, and a set of cuts is any subset
# of them, so the count is 2^(n-1): n=8 gives 128, n=18 gives 131,072, and each
# one has to be built and priced
# the dp does n(n+1)/2 additions instead -- for n=18 that is 171

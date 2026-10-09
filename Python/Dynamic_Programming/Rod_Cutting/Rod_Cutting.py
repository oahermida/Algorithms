r"""
ROD CUTTING
Lecture 3, slides 10-12; CLRS 3rd ed., section 15.1 (14.1 in the 4th).

Notes: [[Rod Cutting — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Rod Cutting — Code Notes.md

What is in this file:
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
# Notes: [[Rod Cutting — Code Notes#1. Brute force — every subset of cut positions]] (variables)

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
# Notes: [[Rod Cutting — Code Notes#2. Bottom-up — the lecture's algorithm]] (variables, loop order)

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
# Notes: [[Rod Cutting — Code Notes#3. Top-down with memoisation — the same recurrence, other direction]]

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
# Notes: [[Rod Cutting — Code Notes#4. Restoring the cuts]]

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


# Notes: [[Rod Cutting — Code Notes#How it runs]] (traced example on the CLRS table)

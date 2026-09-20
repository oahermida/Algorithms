r"""
THE MAXIMUM-SUBARRAY PROBLEM
============================

Advanced Algorithms, Lecture 2 (Ivan Bliznets), slides 15-19, which closes with
"More details in Chapter 4.1, CLRS book."

The lecture introduces it as TWO problems and then shows they are the same one.

    PROPHET AND TRADER [slide 15]
        Input:     array of numbers A
        Question:  what is the maximum value of A[i] - A[j] such that i >= j?

        A prophet predicts the price of a stock, 100% accurately. You may buy
        one share and then sell it. Maximise your profit.

    MAXIMUM SUBARRAY [slide 16]
        Input:     array of numbers B
        Question:  find a CONTIGUOUS subarray of B with the largest sum, i.e.
                   find i, j such that B[i] + B[i+1] + ... + B[j] is maximal.

    How are the two related?   Take B[i] = A[i+1] - A[i].   [slide 16]

That one line is the whole reduction, and it is worth slowing down on. Buying on
day j and selling on day i earns A[i] - A[j]. Write that as a telescoping sum of
the DAILY CHANGES:

    A[i] - A[j] = (A[j+1] - A[j]) + (A[j+2] - A[j+1]) + ... + (A[i] - A[i-1])
                =      B[j]       +      B[j+1]       + ... +     B[i-1]

Every intermediate price cancels. So a buy/sell pair is exactly a contiguous
block of B, and its profit is exactly that block's sum. Maximising one maximises
the other. Section 4 below does the conversion and prints both answers.


THE DIVIDE-AND-CONQUER SOLUTION [slides 17-19]
----------------------------------------------
Split the array in half. The best subarray must be in exactly one of three
places, and the slide enumerates them:

     0                      middle | middle+1                     n-1
     +----------------------------+-----------------------------+
     |         left half          |         right half          |
     +----------------------------+-----------------------------+

  case 1     [~~~~~~~~]                                  entirely LEFT
  case 2                               [~~~~~~~~]        entirely RIGHT
  case 3                  [~~~~~~~|~~~~~~~~]             CROSSES the middle

Cases 1 and 2 are the same problem on half the input, so recurse. Case 3 is the
one that needs an idea, and it is the reason this works:

    a crossing subarray MUST contain both middle and middle+1

so it splits into a piece ending exactly at middle and a piece starting exactly
at middle+1, and those two pieces can be chosen INDEPENDENTLY. Find the best of
each by walking outward from the centre -- the slide spells the sums out:

    B[middle], B[middle] + B[middle-1], ... , B[middle] + ... + B[0]
    B[middle+1], B[middle+1] + B[middle+2], ... , B[middle+1] + ... + B[n-1]

"Take the sum of two largest values. This takes O(n) time." [slide 18]

    T(n) <= 2T(n/2) + O(n)      ->      O(n log n)      [slide 19]

which is merge sort's recurrence exactly -- see ../Merge_Sort/Merge_Sort.py.
Same shape, same master-theorem case, for the same reason: two halves plus a
linear combining step.


KADANE'S ALGORITHM -- O(n), NOT ON THE SLIDES
---------------------------------------------
Flagged clearly because it is NOT what Lecture 2 asks for: the examinable
solution is the divide-and-conquer one above. But the same problem has a linear
DP solution, and seeing why is worth more than the algorithm itself.

Use the arrival-based framing from ../Bunny_DP/Bunny_DP.py -- stand at position
i and ask "what is the best subarray ENDING exactly here?" There are only two
answers:

    best_ending_at[i] = max( B[i] ,  best_ending_at[i-1] + B[i] )
                            \             \
                             \             '-- extend the block that ended at i-1
                              '-- start a fresh block right here

Extend, or start over. The answer is then the largest of those n values.

WHY THIS BEATS DIVIDE AND CONQUER, in the terms of the Fibonacci file: merge
sort and the D&C version above have optimal substructure but NOT overlapping
subproblems -- their halves are disjoint, so nothing is ever recomputed and
O(n log n) is the honest price. Maximum subarray DOES have overlap: the best
block ending at i reuses the best block ending at i-1. Exploiting that overlap
is what removes the log n.

    divide and conquer   O(n log n)   disjoint halves, nothing reused
    Kadane (DP)          O(n)         each position reuses its predecessor


WHAT IS IN THIS FILE
--------------------
    1. brute_force_max_subarray   every (i, j) pair, O(n^2), for checking
    2. divide_and_conquer         the lecture's algorithm [slides 17-19]
    3. kadane                     the O(n) DP version, beyond the slides
    4. prophet_and_trader         the stock problem, via B[i] = A[i+1] - A[i]
    5. the CLRS 4.1 worked example, timings, and agreement checks

All three return (total, start_index, end_index) with the range INCLUSIVE, so a
returned answer can always be checked by summing that slice.

Run with:
    python3 Max_Subarray.py
"""

import random
import time

# The stock prices from CLRS figure 4.1, which is the example the slide's
# citation points at. Days 0..16.
CLRS_PRICES = [100, 113, 110, 85, 105, 102, 86, 63, 81, 101, 94, 106, 101, 79, 94, 90, 97]


# =====================================================================
# 1. BRUTE FORCE -- every contiguous block
# =====================================================================
# start_index  - where the candidate block begins
# end_index    - where it ends (inclusive)
# running_sum  - the sum of values[start_index .. end_index], extended one step
#                at a time so no block is ever re-added from scratch
#
# There are n(n+1)/2 contiguous blocks, so this is O(n^2). It exists to disagree
# with the other two if they are wrong, and it follows the problem statement
# literally rather than any recurrence.

def brute_force_max_subarray(values):
    best_total = None
    best_range = (0, 0)

    for start_index in range(len(values)):
        running_sum = 0
        for end_index in range(start_index, len(values)):
            running_sum += values[end_index]
            if best_total is None or running_sum > best_total:
                best_total = running_sum
                best_range = (start_index, end_index)

    return best_total, best_range[0], best_range[1]


# =====================================================================
# 2. DIVIDE AND CONQUER -- the lecture's algorithm [slides 17-19]
# =====================================================================
# best_crossing_subarray is case 3: the best block that contains BOTH middle and
# middle+1.
#
# left_sum      - running total walking LEFT from middle, one cell at a time
# best_left_sum - the largest such total seen, and left_start where it happened
# right_sum     - the mirror image, walking RIGHT from middle+1
#
# The two walks are independent because the block must cross: whatever the left
# piece is, it ends at middle, and whatever the right piece is, it starts at
# middle+1, so any left choice fits with any right choice. That independence is
# what lets the best crossing block be found in one O(n) pass instead of by
# trying every pair.
#
# Both walks start from a single cell and never consider "nothing", because a
# crossing block is non-empty on both sides by definition.

def best_crossing_subarray(values, low, middle, high):
    left_sum = 0
    best_left_sum = None
    left_start = middle
    for index in range(middle, low - 1, -1):          # middle, middle-1, ..., low
        left_sum += values[index]
        if best_left_sum is None or left_sum > best_left_sum:
            best_left_sum = left_sum
            left_start = index

    right_sum = 0
    best_right_sum = None
    right_end = middle + 1
    for index in range(middle + 1, high + 1):         # middle+1, ..., high
        right_sum += values[index]
        if best_right_sum is None or right_sum > best_right_sum:
            best_right_sum = right_sum
            right_end = index

    return best_left_sum + best_right_sum, left_start, right_end


# low, high  - the slice of `values` this call is responsible for, inclusive
# middle     - the split point; the left half ends here, the right half starts
#              at middle+1
#
# The base case is a single cell: with one element there is exactly one
# non-empty subarray, itself.

def divide_and_conquer(values, low=None, high=None):
    if low is None:
        low, high = 0, len(values) - 1

    if low == high:                                   # base case: one element
        return values[low], low, high

    middle = (low + high) // 2

    left_best = divide_and_conquer(values, low, middle)
    right_best = divide_and_conquer(values, middle + 1, high)
    crossing_best = best_crossing_subarray(values, low, middle, high)

    # max on tuples would compare the indices too when totals tie, so compare
    # the totals explicitly and keep the first winner.
    best = left_best
    for candidate in (right_best, crossing_best):
        if candidate[0] > best[0]:
            best = candidate
    return best


# =====================================================================
# 3. KADANE -- O(n), beyond the slides
# =====================================================================
# best_ending_here  - the best sum of a block ENDING exactly at this position
# current_start     - where that block begins
# best_total        - the best value of best_ending_here seen anywhere so far
#
# One decision per position: extend the previous block, or throw it away and
# start fresh here. Throwing it away is right exactly when the previous block's
# total was negative -- a negative prefix can only drag down whatever follows,
# so no block that would contain it can be optimal.
#
# Nothing is ever reconsidered, which is why it is one pass.

def kadane(values):
    best_ending_here = values[0]
    current_start = 0
    best_total = values[0]
    best_range = (0, 0)

    for index in range(1, len(values)):
        value = values[index]
        if best_ending_here + value >= value:
            best_ending_here = best_ending_here + value    # extend
        else:
            best_ending_here = value                       # start fresh
            current_start = index

        if best_ending_here > best_total:
            best_total = best_ending_here
            best_range = (current_start, index)

    return best_total, best_range[0], best_range[1]


# =====================================================================
# 4. PROPHET AND TRADER -- the reduction [slides 15-16]
# =====================================================================
# prices          - A, the price on each day
# daily_changes   - B, where daily_changes[i] = prices[i+1] - prices[i]
#
# A maximal block of B running from index i to index j corresponds to buying on
# day i and selling on day j+1: the block's sum telescopes to
# prices[j+1] - prices[i].
#
# The off-by-one is the whole subtlety. B has one FEWER entry than A, because
# there are n-1 gaps between n prices, and the sell day is one past the block's
# last index.

def prophet_and_trader(prices):
    daily_changes = [prices[day + 1] - prices[day] for day in range(len(prices) - 1)]

    profit, first_change, last_change = kadane(daily_changes)

    buy_day = first_change
    sell_day = last_change + 1
    return profit, buy_day, sell_day, daily_changes


# =====================================================================
# 5. RUN IT
# =====================================================================

def describe(values, result, label):
    total, start, end = result
    block = values[start:end + 1]
    print(f"  {label:<22} total {total:>5}   indices [{start}..{end}]   {block}")


print("=" * 78)
print("MAXIMUM SUBARRAY   -- Lecture 2, slides 15-19;  CLRS 4.1")
print("=" * 78)

profit, buy_day, sell_day, daily_changes = prophet_and_trader(CLRS_PRICES)

print(f"\nPROPHET AND TRADER  [slide 15]")
print(f"  prices A = {CLRS_PRICES}")
print(f"\n  the reduction B[i] = A[i+1] - A[i]  [slide 16]:")
print(f"  changes B = {daily_changes}")
print(f"           ({len(CLRS_PRICES)} prices -> {len(daily_changes)} changes: "
      f"n prices have n-1 gaps between them)")

print(f"\nMAXIMUM SUBARRAY on B:")
brute_result = brute_force_max_subarray(daily_changes)
dc_result = divide_and_conquer(daily_changes)
kadane_result = kadane(daily_changes)
describe(daily_changes, brute_result, "brute force O(n^2)")
describe(daily_changes, dc_result, "divide & conquer")
describe(daily_changes, kadane_result, "Kadane O(n)")

print(f"\nREADING IT BACK AS THE TRADE:")
print(f"  buy on day {buy_day} at price {CLRS_PRICES[buy_day]}")
print(f"  sell on day {sell_day} at price {CLRS_PRICES[sell_day]}")
print(f"  profit = {CLRS_PRICES[sell_day]} - {CLRS_PRICES[buy_day]} = "
      f"{CLRS_PRICES[sell_day] - CLRS_PRICES[buy_day]}")
block_parts = [str(change) if change >= 0 else f"({change})"
               for change in daily_changes[buy_day:sell_day]]
print(f"  the block sum agrees: {' + '.join(block_parts)}"
      f" = {sum(daily_changes[buy_day:sell_day])}")

# This array is itself the counterexample to "buy at the minimum, sell at the
# maximum" -- a rule that sounds obviously right and is not even legal here.
lowest_day = CLRS_PRICES.index(min(CLRS_PRICES))
highest_day = CLRS_PRICES.index(max(CLRS_PRICES))
print(f"\n  WHY THE OBVIOUS RULE FAILS ON THIS VERY ARRAY:")
print(f"    lowest price  {min(CLRS_PRICES)} on day {lowest_day}")
print(f"    highest price {max(CLRS_PRICES)} on day {highest_day}")
print(f"    the highest price comes {lowest_day - highest_day} days BEFORE the lowest,")
print(f"    so 'buy at the minimum, sell at the maximum' is not a legal trade at all.")
print(f"    the real answer buys at the minimum ({CLRS_PRICES[buy_day]}, day {buy_day}) and sells at "
      f"{CLRS_PRICES[sell_day]} (day {sell_day}) --")
print(f"    the best price that occurs AFTER it, not the best price overall.")


# =====================================================================
# 6. THE THREE CASES, ON THE TOP-LEVEL SPLIT
# =====================================================================
# What the very first call of divide_and_conquer compares, before any recursion
# resolves. This is the slide-17 picture with the real numbers in it.

print("\n" + "=" * 78)
print("THE THREE CASES AT THE TOP-LEVEL SPLIT  [slide 17]")
print("=" * 78)

low, high = 0, len(daily_changes) - 1
middle = (low + high) // 2

left_case = divide_and_conquer(daily_changes, low, middle)
right_case = divide_and_conquer(daily_changes, middle + 1, high)
crossing_case = best_crossing_subarray(daily_changes, low, middle, high)

print(f"\n  B has {len(daily_changes)} entries, indices {low}..{high}, "
      f"middle = {middle}")
print(f"  left half  = B[{low}..{middle}]   = {daily_changes[low:middle + 1]}")
print(f"  right half = B[{middle + 1}..{high}] = {daily_changes[middle + 1:high + 1]}\n")
describe(daily_changes, left_case, "case 1: entirely left")
describe(daily_changes, right_case, "case 2: entirely right")
describe(daily_changes, crossing_case, "case 3: crossing")
winner = max((left_case, right_case, crossing_case), key=lambda option: option[0])
print(f"\n  the winner is case "
      f"{1 if winner is left_case else 2 if winner is right_case else 3}, "
      f"with total {winner[0]}")
print(f"  (the crossing case is the only one that needs work -- the other two are")
print(f"   just the same problem again, on half the input)")


# =====================================================================
# 7. AN ARRAY WHERE THE OBVIOUS ANSWER IS WRONG
# =====================================================================
# Two traps in one array: the global minimum comes AFTER the global maximum, so
# "buy low, sell high" is illegal; and every single day is a loss, so the best
# trade is the least bad one. CLRS makes this point too -- the answer can be
# negative when the array is all negative, and an algorithm that quietly returns
# 0 for "buy nothing" is answering a different question.

print("\n" + "=" * 78)
print("WHEN 'BUY LOW, SELL HIGH' IS ILLEGAL")
print("=" * 78)

falling_prices = [50, 45, 40, 38, 30, 29]
falling_profit, falling_buy, falling_sell, falling_changes = prophet_and_trader(falling_prices)

print(f"\n  prices  = {falling_prices}   (the maximum is on day 0, before every minimum)")
print(f"  changes = {falling_changes}   (every day is a loss)")
print(f"  best trade: buy day {falling_buy} at {falling_prices[falling_buy]}, "
      f"sell day {falling_sell} at {falling_prices[falling_sell]}, profit {falling_profit}")
print(f"  the answer is NEGATIVE, and that is correct: the trader must buy and")
print(f"  must sell, so the best available outcome is the smallest loss.")
print(f"  an implementation that returned 0 here would be solving 'may I decline")
print(f"  to trade?', which is a different problem.")

all_negative = [-8, -3, -6, -2, -5, -4]
print(f"\n  same point on the subarray side: B = {all_negative}")
describe(all_negative, brute_force_max_subarray(all_negative), "brute force")
describe(all_negative, divide_and_conquer(all_negative), "divide & conquer")
describe(all_negative, kadane(all_negative), "Kadane")
print(f"  all three pick the single least-negative element, not the empty block")


# =====================================================================
# 8. TIMING -- O(n^2) vs O(n log n) vs O(n)
# =====================================================================

print("\n" + "=" * 78)
print("TIMING")
print("=" * 78)
print(f"\n{'n':>8}{'brute O(n^2)':>16}{'D&C O(n log n)':>18}{'Kadane O(n)':>15}")
print("-" * 78)

random.seed(7)
for size in (200, 400, 800, 1600, 3200):
    sample = [random.randint(-50, 50) for _ in range(size)]

    start_time = time.perf_counter()
    brute_force_max_subarray(sample)
    brute_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    divide_and_conquer(sample)
    dc_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    kadane(sample)
    kadane_seconds = time.perf_counter() - start_time

    print(f"{size:>8}{brute_seconds:>16.6f}{dc_seconds:>18.6f}{kadane_seconds:>15.6f}")

print("\n  doubling n roughly QUADRUPLES the brute force column, a bit more than")
print("  DOUBLES the divide-and-conquer one, and exactly doubles Kadane's --")
print("  which is what n^2, n log n and n look like when you can watch them.")


# =====================================================================
# 9. AGREEMENT CHECK
# =====================================================================
# The three must agree on the VALUE. They need not agree on WHICH block achieves
# it -- ties are common and each algorithm breaks them differently -- so the
# check verifies the value, and separately that each returned range really does
# sum to the value it claims. That second part is the one that catches an
# off-by-one in the indices while the total happens to be right.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(3)
trial_count = 4000
value_disagreements = 0
range_disagreements = 0

for _ in range(trial_count):
    length = random.randint(1, 14)
    # include all-negative and all-positive arrays, not just mixed ones
    low_bound, high_bound = random.choice([(-20, 20), (-20, -1), (1, 20)])
    sample = [random.randint(low_bound, high_bound) for _ in range(length)]

    results = (brute_force_max_subarray(sample),
               divide_and_conquer(sample),
               kadane(sample))

    if not (results[0][0] == results[1][0] == results[2][0]):
        value_disagreements += 1

    for total, start, end in results:
        if sum(sample[start:end + 1]) != total or not (0 <= start <= end < length):
            range_disagreements += 1

print(f"\n{trial_count} random arrays, lengths 1-14, all-negative and all-positive included\n")
print(f"  all three agree on the total          {trial_count - value_disagreements}/{trial_count}")
print(f"  every returned range sums to its total {3 * trial_count - range_disagreements}/{3 * trial_count}")

# The reduction itself deserves its own check: solving PROPHET AND TRADER by
# brute force over every legal (buy, sell) pair must match the answer that came
# out of MAXIMUM SUBARRAY on the differences.
reduction_disagreements = 0
for _ in range(trial_count):
    prices = [random.randint(1, 200) for _ in range(random.randint(2, 14))]

    best_direct = max(prices[sell] - prices[buy]
                      for buy in range(len(prices))
                      for sell in range(buy + 1, len(prices)))
    best_via_subarray, _, _, _ = prophet_and_trader(prices)

    if best_direct != best_via_subarray:
        reduction_disagreements += 1

print(f"  B[i] = A[i+1] - A[i] reduction is exact {trial_count - reduction_disagreements}/{trial_count}")
print("\n  (the last one checks the SLIDE's claim, not my code: that the stock")
print("   problem and the subarray problem really are the same question)")


# === How it Runs ===
#
# --- divide_and_conquer ---
# called with a slice [low..high]; if low == high there is exactly one non-empty
# subarray, the single cell, SO THIS CALL RETURNS IMMEDIATELY (no split, no scan)
# otherwise it computes middle, then makes TWO recursive calls and ONE O(n) scan
# single threaded and sequential: the left call and its entire subtree finish
# before the right call starts, and best_crossing_subarray runs only after both
# the three candidates are compared on total alone, and the best is returned upward
#
# --- best_crossing_subarray, which is the only real work ---
# a crossing block must contain both middle and middle+1, so it is
#   (some block ending AT middle) + (some block starting AT middle+1)
# the two walks are independent, so each is a simple running maximum:
#
# for B = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
# at the top-level call, low=0, high=15, middle=7:
#
#   walking LEFT from index 7, accumulating:
#     index 7   sum = 18                      <- best so far, left_start = 7
#     index 6   sum = 18 + (-23) = -5
#     index 5   sum = -5 + (-16) = -21
#     index 4   sum = -21 + (-3) = -24
#     index 3   sum = -24 + 20   = -4
#     index 2   sum = -4 + (-25) = -29
#     index 1   sum = -29 + (-3) = -32
#     index 0   sum = -32 + 13   = -19
#     best left piece = 18, starting at index 7
#
#   walking RIGHT from index 8, accumulating:
#     index 8   sum = 20                      <- best so far, right_end = 8
#     index 9   sum = 20 + (-7) = 13
#     index 10  sum = 13 + 12   = 25          <- new best, right_end = 10
#     index 11  sum = 25 + (-5) = 20
#     index 12  sum = 20 + (-22) = -2
#     index 13  sum = -2 + 15   = 13
#     index 14  sum = 13 + (-4) = 9
#     index 15  sum = 9 + 7     = 16
#     best right piece = 25, ending at index 10
#
#   crossing total = 18 + 25 = 43, indices [7..10]
#
# each walk is one pass with one running total, so the scan is O(n), and the
# whole algorithm is T(n) <= 2T(n/2) + O(n) = O(n log n)
#
# --- kadane ---
# one variable, one decision per position: extend or restart
# best_ending_here is the best block ENDING at the current index, never a block
# ending anywhere else, which is what makes the decision a two-way choice
#
# same B, walking once left to right:
#   i= 0  best_ending_here = 13                              best = 13   [0..0]
#   i= 1  13 + (-3) = 10  >= -3   -> extend       = 10
#   i= 2  10 + (-25) = -15 >= -25 -> extend       = -15
#   i= 3  -15 + 20 = 5  <  20     -> RESTART      = 20       best = 20   [3..3]
#   i= 4  20 + (-3) = 17 >= -3    -> extend       = 17
#   i= 5  17 + (-16) = 1 >= -16   -> extend       = 1
#   i= 6  1 + (-23) = -22 >= -23  -> extend       = -22
#   i= 7  -22 + 18 = -4 <  18     -> RESTART      = 18
#   i= 8  18 + 20 = 38 >= 20      -> extend       = 38       best = 38   [7..8]
#   i= 9  38 + (-7) = 31 >= -7    -> extend       = 31
#   i=10  31 + 12 = 43 >= 12      -> extend       = 43       best = 43   [7..10]
#   i=11  43 + (-5) = 38 >= -5    -> extend       = 38
#   i=12  38 + (-22) = 16 >= -22  -> extend       = 16
#   i=13  16 + 15 = 31 >= 15      -> extend       = 31
#   i=14  31 + (-4) = 27 >= -4    -> extend       = 27
#   i=15  27 + 7 = 34 >= 7        -> extend       = 34
#   answer 43, indices [7..10] -- the same block the O(n log n) version found
#
# the two RESTARTs are the interesting steps. at i=3 the running block was worth
# -15; carrying it forward would cost 15 points, so it is dropped. a block is
# abandoned exactly when its total has gone negative, because a negative prefix
# can only reduce whatever comes after it
#
# --- prophet_and_trader ---
# converts A (17 prices) into B (16 changes), runs kadane, converts back
# block [7..10] of B  ->  buy on day 7, sell on day 10 + 1 = 11
# the +1 is not an adjustment, it is the definition: B[10] is the change from
# day 10 to day 11, so using B[10] means still holding the share on day 11
# prices[11] - prices[7] = 106 - 63 = 43, matching the block sum exactly

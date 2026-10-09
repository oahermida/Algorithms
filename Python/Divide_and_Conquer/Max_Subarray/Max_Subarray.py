r"""
THE MAXIMUM-SUBARRAY PROBLEM
Advanced Algorithms, Lecture 2, slides 15-19; CLRS 3rd ed., section 4.1.

Notes: [[Max Subarray — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Max Subarray — Code Notes.md

What is in this file:
    1. brute_force_max_subarray   every (i, j) pair, O(n^2), for checking
    2. divide_and_conquer         the lecture's algorithm [slides 17-19]
    3. kadane                     the O(n) DP version, beyond the slides
    4. prophet_and_trader         the stock problem, via B[i] = A[i+1] - A[i]
    5. the CLRS 4.1 worked example, timings, and agreement checks

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
# Notes: [[Max Subarray — Code Notes#1. Brute force — every contiguous block]] (variables)

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
# Notes: [[Max Subarray — Code Notes#2. Divide and conquer — the lecture's algorithm]] (variables, why the walks are independent)

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
# Notes: [[Max Subarray — Code Notes#3. Kadane — O(n), beyond the slides]] (variables, extend or restart)

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
# Notes: [[Max Subarray — Code Notes#4. Prophet and trader — the reduction]] (variables, the off-by-one)

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


# Notes: [[Max Subarray — Code Notes#How it runs]]

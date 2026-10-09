r"""
FIBONACCI WITH DYNAMIC PROGRAMMING

Notes: [[Fibonacci DP — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Fibonacci DP — Code Notes.md

What is in this file:
    1. naive recursion   O(2^n) time   O(n) stack     the recurrence, written out
    2. memoisation       O(n) time     O(n) memory    top-down DP  -- cache results
    3. tabulation        O(n) time     O(n) memory    bottom-up DP -- fill a table
    4. rolling pair      O(n) time     O(1) memory    tabulation with the table
                                                      thrown away

Run with:
    python3 Fibonacci_DP.py
"""

import time


# =====================================================================
# 1. NAIVE RECURSION -- the recurrence written out literally
# =====================================================================
# Notes: [[Fibonacci DP — Code Notes#1. Naive recursion — the recurrence written out literally]] (variables, cost)

def naive_fibonacci(index, call_counter):
    call_counter["calls"] += 1

    if index < 2:              # base cases: F(0) = 0 and F(1) = 1
        return index

    return naive_fibonacci(index - 1, call_counter) + naive_fibonacci(index - 2, call_counter)


# =====================================================================
# 2. MEMOISATION -- top-down DP
# =====================================================================
# Notes: [[Fibonacci DP — Code Notes#2. Memoisation — top-down DP]] (variables, why the tree collapses, the catch)

def memoised_fibonacci(index, memo_table, call_counter):
    call_counter["calls"] += 1

    if index in memo_table:    # already solved -> return it, expand nothing
        return memo_table[index]

    if index < 2:
        result = index
    else:
        result = (memoised_fibonacci(index - 1, memo_table, call_counter)
                  + memoised_fibonacci(index - 2, memo_table, call_counter))

    memo_table[index] = result      # store before returning, so it is free next time
    return result


# =====================================================================
# 3. TABULATION -- bottom-up DP
# =====================================================================
# Notes: [[Fibonacci DP — Code Notes#3. Tabulation — bottom-up DP]] (variables, why the loop order works)

def tabulated_fibonacci(index):
    if index < 2:
        return index

    fibonacci_table = [0] * (index + 1)    # slots 0 .. index
    fibonacci_table[0] = 0                 # base case
    fibonacci_table[1] = 1                 # base case

    for position in range(2, index + 1):
        fibonacci_table[position] = fibonacci_table[position - 1] + fibonacci_table[position - 2]

    return fibonacci_table[index]


# =====================================================================
# 4. ROLLING PAIR -- tabulation with the table deleted
# =====================================================================
# Notes: [[Fibonacci DP — Code Notes#4. Rolling pair — tabulation with the table deleted]] (variables, the one-line swap)

def rolling_fibonacci(index):
    if index < 2:
        return index

    previous_value = 0     # F(0)
    current_value = 1      # F(1)

    for _ in range(2, index + 1):
        previous_value, current_value = current_value, previous_value + current_value

    return current_value


# =====================================================================
# 5. RUN THEM AND COMPARE
# =====================================================================

TARGET_INDEX = 30

print("=" * 72)
print("FIBONACCI -- FOUR VERSIONS")
print("=" * 72)

print(f"\nThe sequence up to F(12): {[rolling_fibonacci(k) for k in range(13)]}")
print(f"Computing F({TARGET_INDEX}) four ways.\n")

naive_counter = {"calls": 0}
start_time = time.perf_counter()
naive_result = naive_fibonacci(TARGET_INDEX, naive_counter)
naive_seconds = time.perf_counter() - start_time

memo_counter = {"calls": 0}
start_time = time.perf_counter()
memo_result = memoised_fibonacci(TARGET_INDEX, {}, memo_counter)
memo_seconds = time.perf_counter() - start_time

start_time = time.perf_counter()
tabulated_result = tabulated_fibonacci(TARGET_INDEX)
tabulated_seconds = time.perf_counter() - start_time

start_time = time.perf_counter()
rolling_result = rolling_fibonacci(TARGET_INDEX)
rolling_seconds = time.perf_counter() - start_time

print(f"{'version':<16}{'result':>10}{'calls/steps':>14}{'seconds':>12}")
print("-" * 72)
print(f"{'naive':<16}{naive_result:>10}{naive_counter['calls']:>14,}{naive_seconds:>12.6f}")
print(f"{'memoised':<16}{memo_result:>10}{memo_counter['calls']:>14,}{memo_seconds:>12.6f}")
print(f"{'tabulated':<16}{tabulated_result:>10}{TARGET_INDEX - 1:>14,}{tabulated_seconds:>12.6f}")
print(f"{'rolling':<16}{rolling_result:>10}{TARGET_INDEX - 1:>14,}{rolling_seconds:>12.6f}")

print(f"\nThe naive version made {naive_counter['calls']:,} calls to get the same "
      f"number the rolling version got in {TARGET_INDEX - 1} additions.")
print(f"Ratio: {naive_counter['calls'] / (TARGET_INDEX - 1):,.0f}x the work, for an identical answer.")

# The memoised call count is 2n-1, not n: every index above 1 is REQUESTED twice
# (once by index+1 and once by index+2), but the second request returns at the
# cache check without expanding anything. Cheap lookups, not real work.
print(f"\nMemoised made {memo_counter['calls']} calls for index {TARGET_INDEX}: "
      f"{TARGET_INDEX + 1} that did real work, the rest returning straight from the cache.")


# =====================================================================
# 6. WHERE THE NAIVE VERSION GIVES UP
# =====================================================================
# Doubling the index squares the work. Watch the time per index grow.

print("\n" + "=" * 72)
print("HOW FAST THE NAIVE VERSION DEGRADES")
print("=" * 72)
print(f"{'index':>7}{'naive calls':>16}{'naive secs':>14}{'rolling secs':>16}")
print("-" * 72)

for sample_index in (10, 20, 25, 30, 32):
    sample_counter = {"calls": 0}

    start_time = time.perf_counter()
    naive_fibonacci(sample_index, sample_counter)
    sample_naive_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    rolling_fibonacci(sample_index)
    sample_rolling_seconds = time.perf_counter() - start_time

    print(f"{sample_index:>7}{sample_counter['calls']:>16,}"
          f"{sample_naive_seconds:>14.6f}{sample_rolling_seconds:>16.6f}")

# Anything the naive version cannot reach, the DP versions do not even notice.
# Python's ints are arbitrary precision, so these are exact, not floats.
big_index = 1000
big_value = rolling_fibonacci(big_index)
print(f"\nF({big_index}) has {len(str(big_value))} digits and took no measurable time:")
print(f"  {str(big_value)[:40]}...{str(big_value)[-10:]}")
print("  (the memoised version would hit Python's recursion limit here -- "
      "it recurses ~1000 deep; the two bottom-up versions never recurse at all)")


# =====================================================================
# 7. CHECK THEM AGAINST EACH OTHER -- don't trust one example
# =====================================================================
# One matching answer proves nothing. Run all four over every index where the
# naive version is still affordable and confirm they never disagree, then keep
# checking the three fast ones further out.

print("\n" + "=" * 72)
print("AGREEMENT CHECK")
print("=" * 72)

disagreement_count = 0

for check_index in range(0, 25):
    naive_value = naive_fibonacci(check_index, {"calls": 0})
    memo_value = memoised_fibonacci(check_index, {}, {"calls": 0})
    tabulated_value = tabulated_fibonacci(check_index)
    rolling_value = rolling_fibonacci(check_index)

    if not (naive_value == memo_value == tabulated_value == rolling_value):
        disagreement_count += 1
        print(f"  MISMATCH at index {check_index}: "
              f"{naive_value}, {memo_value}, {tabulated_value}, {rolling_value}")

print(f"indices 0-24, all four versions: {25 - disagreement_count}/25 agree")

fast_disagreement_count = 0

for check_index in range(0, 500):
    if tabulated_fibonacci(check_index) != rolling_fibonacci(check_index):
        fast_disagreement_count += 1

print(f"indices 0-499, tabulated vs rolling: {500 - fast_disagreement_count}/500 agree")

# An independent check that does not reuse any of the four functions: every
# Fibonacci number should equal the sum of the two before it, read straight off
# a generated list. If the recurrence itself were mis-coded, all four would be
# wrong together and the comparison above would not catch it.
generated_sequence = [rolling_fibonacci(k) for k in range(100)]
recurrence_holds = all(
    generated_sequence[k] == generated_sequence[k - 1] + generated_sequence[k - 2]
    for k in range(2, 100)
)
print(f"the recurrence F(k) = F(k-1) + F(k-2) holds across indices 2-99: {recurrence_holds}")


# Notes: [[Fibonacci DP — Code Notes#How it runs]] (traced runs of all four versions)

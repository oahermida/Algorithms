r"""
FIBONACCI WITH DYNAMIC PROGRAMMING
==================================

The problem:
    The Fibonacci numbers are defined by a recurrence -- a rule that defines each
    value in terms of earlier values:

        F(0) = 0
        F(1) = 1
        F(n) = F(n - 1) + F(n - 2)      for n >= 2

    So the sequence runs 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
    Given an index n, compute F(n).

Writing that recurrence straight out as a recursive function is correct and takes
about O(2^n) time, which is unusable past roughly n = 40. Dynamic programming
fixes it and brings it down to O(n), without changing the recurrence at all.

WHAT DYNAMIC PROGRAMMING ACTUALLY IS
------------------------------------
DP applies when a problem has two properties. Fibonacci has both, which is why it
is the standard first example:

    1. OPTIMAL SUBSTRUCTURE
       The answer for n is built out of the answers for smaller inputs and
       nothing else. F(n) needs only F(n-1) and F(n-2) -- not the route taken to
       reach them.

    2. OVERLAPPING SUBPROBLEMS
       The same smaller input gets asked for over and over.

    Two pictures of that same recurrence. They are NOT alternative drawings of
    the same thing -- they are the before and after of applying DP:

       RECURSION TREE                              SUBPROBLEM GRAPH (the DAG)
       what recursion executes                     what the recurrence says
       15 nodes                                    6 nodes

                            F(5)                           F(5)
                      /            \                      /    \
                   F(4)            F(3)               v          v
                 /     \          /    \             F(4) ---> F(3)
              F(3)     F(2)    F(2)    F(1)           |       /    \
             /   \     /  \    /  \                   |      v        v
          F(2)  F(1) F(1) F(0) F(1) F(0)              +---> F(2) --> F(1)
          /  \                                               |
       F(1)  F(0)                                            v
                                                           F(0)

       every CALL drawn, however many              every SUBPROBLEM drawn once,
       times the same one is made                  with several arrows INTO it

    Read the difference off the two pictures:

        repeated subproblem     tree: redrawn each call   DAG: one node, arrows in
        F(3)                    appears 2x                appears 1x
        F(2)                    appears 3x                appears 1x
        F(1)                    appears 5x                appears 1x
        nodes to reach F(5)     15                        6
        growth                  ~doubles per +1 of n      linear in n

       In the tree, F(3) is expanded from scratch twice and F(2) three times --
       each repeat rebuilding its own entire subtree. That duplicated work is
       the whole of the exponential blow-up. Collapsing the duplicates into one
       node each IS dynamic programming; the collapsed picture is the DAG.

    Property 2 alone is what DP exploits: compute each distinct subproblem ONCE,
    store the answer, and look it up every time after. Property 1 is what makes
    that safe -- a stored answer can never need revising later, because nothing
    about the larger problem can change what F(3) is.

    THE DAG IS WHAT THE FOUR VERSIONS BELOW ARE ALL DOING
    -----------------------------------------------------
    Nodes are STATES (here just an index), arrows are TRANSITIONS (the
    dependencies the recurrence declares). Solving the problem means evaluating
    every node in an order where each node's dependencies are already done.
    There are exactly two ways to get such an order, and they are versions 2
    and 3:

        memoisation (top-down)  = depth-first search over this DAG, starting at
                                  F(5), with the cache stopping the search from
                                  ever re-entering a node it has already solved
        tabulation (bottom-up)  = walking the DAG in topological order, so every
                                  node is reached only after everything it
                                  points to is already computed

    The arrows are acyclic -- they only ever point to smaller indices -- which is
    what guarantees such an order exists at all. A cycle would mean a subproblem
    depending on itself, and no amount of caching would rescue that.

    Merge sort, by contrast, has property 1 but NOT property 2: its two halves are
    disjoint, so no subproblem is ever asked for twice. That is why merge sort is
    divide-and-conquer and gets no benefit from a cache.

THE FOUR VERSIONS IN THIS FILE
------------------------------
    1. naive recursion   O(2^n) time   O(n) stack     the recurrence, written out
    2. memoisation       O(n) time     O(n) memory    top-down DP  -- cache results
    3. tabulation        O(n) time     O(n) memory    bottom-up DP -- fill a table
    4. rolling pair      O(n) time     O(1) memory    tabulation with the table
                                                      thrown away

    2 and 3 are the same idea in opposite directions. 4 is the observation that
    once you fill forward, all but the last two table slots are dead.

Run with:
    python3 Fibonacci_DP.py

The step-by-step narrated version of these same functions is in
fibonacci_traced.py in this directory.
"""

import time


# =====================================================================
# 1. NAIVE RECURSION -- the recurrence written out literally
# =====================================================================
# index         - the n in F(n); the value being asked for right now
# call_counter  - a dict used as a counter, so the recursive calls can all add
#                 to the same box (a plain int would be rebound locally instead)
#
# This is correct. It is also a disaster, because the two recursive calls below
# never find out about each other's work -- the left call computes F(3) and
# throws it away, then the right call computes F(3) again from nothing.
#
# Cost: the call count roughly DOUBLES for every +1 on index, which is the
# definition of exponential. n = 30 is about 2.7 million calls; n = 50 would be
# around 40 billion and would not finish today.

def naive_fibonacci(index, call_counter):
    call_counter["calls"] += 1

    if index < 2:              # base cases: F(0) = 0 and F(1) = 1
        return index

    return naive_fibonacci(index - 1, call_counter) + naive_fibonacci(index - 2, call_counter)


# =====================================================================
# 2. MEMOISATION -- top-down DP
# =====================================================================
# Exactly the function above with three lines added: before computing, check the
# cache; after computing, write to the cache.
#
# index          - the n in F(n), same as before
# memo_table     - dict mapping an index to its already-computed F(index)
# call_counter   - same counter, so the two versions can be compared directly
#
# WHY THIS COLLAPSES THE TREE:
#     The first time F(3) is asked for, it does the full work and stores 2.
#     Every later request for F(3) returns at the cache check, so the entire
#     subtree underneath it is never re-expanded. Each distinct index does real
#     work exactly once, so there are only n distinct pieces of work -- the
#     exponential tree flattens into a line.
#
# "Top-down" means it still starts at the goal (index) and works downward to the
# base cases, exactly like the naive version. The only change is that it
# remembers.
#
# THE CATCH: it is still recursion, so it uses a call stack n deep. Python's
# default recursion limit is 1000, so this version raises RecursionError at
# roughly index 1000 even though the maths is fine. Version 3 has no such limit.

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
# Same recurrence, read the other way round. Instead of starting at index and
# recursing down to the base cases, start AT the base cases and walk up.
#
# fibonacci_table - a list where slot k holds F(k), filled left to right
# position        - the slot being filled on this pass; runs 2, 3, ..., index
#
# The loop can only fill slot `position` once slots position-1 and position-2
# already hold their final values -- and because the loop goes strictly left to
# right, they always do. That ordering is the whole trick: every value is read
# only after it has been written, so nothing ever needs recomputing and no
# recursion is needed to go and fetch it.
#
# No recursion means no call stack and no recursion limit, so this handles
# index = 100000 happily where version 2 would blow up.

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
# Look at the loop above: on the pass filling slot `position`, it reads only
# slots position-1 and position-2. Slot position-3 and everything left of it is
# never touched again. So the list is storing index+1 values to make use of two.
#
# previous_value - F(position - 2), the older of the two
# current_value  - F(position - 1), the newer of the two
#
# Each pass computes the next value, then shifts the window one step right. The
# two names are reassigned together on one line so the right-hand side is fully
# evaluated before either is overwritten -- writing it as two separate statements
# would clobber current_value before previous_value could read it.
#
# Same O(n) time, but O(1) memory: two integers regardless of how big index is.
# This is a common last step in a DP problem -- solve it with the full table
# first, then look at which slots the loop actually reads and shrink to those.

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


# === How it Runs ===
#
# --- naive_fibonacci ---
# called with an index; adds 1 to the shared counter and checks index < 2
# if so this one call returns index immediately (F(0) = 0, F(1) = 1) -- no further calls
# otherwise it makes TWO calls to itself and adds the results
# single threaded and sequential: the LEFT call and its entire subtree finish completely
# before the right call is even started
# nothing is shared between the two calls, so any index reached by both is computed twice
# from scratch -- the whole subtree under it is rebuilt every time
#
# the call tree for F(5), in the order the calls actually happen:
#   F(5) -> F(4) -> F(3) -> F(2) -> F(1) = 1        <- deepest-left path first
#                                 -> F(0) = 0       -> F(2) = 1
#                        -> F(1) = 1                -> F(3) = 2
#               -> F(2) -> F(1) = 1
#                       -> F(0) = 0                 -> F(2) = 1   <- SECOND time F(2) is built
#                                                   -> F(4) = 3
#        -> F(3) -> F(2) -> F(1) = 1
#                        -> F(0) = 0                -> F(2) = 1   <- THIRD time
#                -> F(1) = 1                        -> F(3) = 2   <- SECOND time F(3) is built
#                                                   -> F(5) = 5
#   15 calls for an answer that needs 4 additions. F(3) built twice, F(2) three times,
#   F(1) reached five times. Every one of those repeats is pure waste.
#
# --- memoised_fibonacci ---
# identical control flow, with a cache check at the top and a cache write at the bottom
# the SECOND time F(3) is asked for, the check at the top hits and returns 2 instantly
# -- the six calls that built it the first time do not happen again
# so the tree is walked once down the left spine, and every right-hand call returns
# from the cache the moment it is made
# F(5) memoised: 9 calls instead of 15. F(30): 59 instead of 2,692,537
# the count is 2n-1 because each index is REQUESTED twice but COMPUTED once
#
# --- tabulated_fibonacci ---
# no recursion at all. fibonacci_table is a list of index+1 zeros, slot k for F(k)
# slots 0 and 1 are written directly -- those are the base cases, the only two
# values the recurrence cannot produce
# position runs 2, 3, ..., index; each pass writes ONE slot and never revisits it
#
# filling the table for index = 10, slot by slot:
#   start                [0, 1, 0, 0, 0, 0, 0,  0,  0,  0,  0]
#   position=2  0+1 = 1  [0, 1, 1, 0, 0, 0, 0,  0,  0,  0,  0]
#   position=3  1+1 = 2  [0, 1, 1, 2, 0, 0, 0,  0,  0,  0,  0]
#   position=4  1+2 = 3  [0, 1, 1, 2, 3, 0, 0,  0,  0,  0,  0]
#   position=5  2+3 = 5  [0, 1, 1, 2, 3, 5, 0,  0,  0,  0,  0]
#   position=6  3+5 = 8  [0, 1, 1, 2, 3, 5, 8,  0,  0,  0,  0]
#   position=7  5+8 = 13 [0, 1, 1, 2, 3, 5, 8, 13,  0,  0,  0]
#   position=8  8+13= 21 [0, 1, 1, 2, 3, 5, 8, 13, 21,  0,  0]
#   position=9 13+21= 34 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34,  0]
#   position=10 21+34=55 [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
#   return fibonacci_table[10] = 55
#
# every slot read on a pass was written on an earlier pass, because the loop only
# ever moves right. that is the guarantee memoisation gets from the cache check --
# here it comes free from the loop order
#
# --- rolling_fibonacci ---
# read the table trace above and notice what each pass actually touches: position=10
# reads slots 9 and 8 only. slots 0-7 are dead weight, kept for nothing
# so keep two variables instead: previous_value = F(position-2), current_value = F(position-1)
#
# the same run for index = 10, one pass per line:
#   start        previous=0  current=1                     (F(0), F(1))
#   pass 1       previous=1  current=1     0+1 = 1         (F(1), F(2))
#   pass 2       previous=1  current=2     1+1 = 2         (F(2), F(3))
#   pass 3       previous=2  current=3     1+2 = 3         (F(3), F(4))
#   pass 4       previous=3  current=5     2+3 = 5         (F(4), F(5))
#   pass 5       previous=5  current=8     3+5 = 8         (F(5), F(6))
#   pass 6       previous=8  current=13    5+8 = 13        (F(6), F(7))
#   pass 7       previous=13 current=21    8+13 = 21       (F(7), F(8))
#   pass 8       previous=21 current=34    13+21 = 34      (F(8), F(9))
#   pass 9       previous=34 current=55    21+34 = 55      (F(9), F(10))
#   return current_value = 55
#
# the loop body is ONE line because both names are rebound at once: the whole
# right-hand side (current_value, previous_value + current_value) is evaluated into a
# tuple FIRST, then unpacked. splitting it into two statements would overwrite
# previous_value before the addition could read its old value, and the sequence
# would come out wrong (2, 4, 8, ... instead of 1, 2, 3, 5)
#
# the loop variable is _ because nothing in the body uses it -- only the number of
# passes matters, not which pass it is

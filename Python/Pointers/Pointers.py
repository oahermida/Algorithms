"""
Standard pointer patterns — one pointer and two pointers.

A "pointer" here is just an integer index into a list. What makes it a pointer
pattern is the discipline: it only ever moves FORWARD (or, in pattern 3, the two
only ever move TOWARD each other) and it is never reset. That is what turns work
that looks nested into a single pass.

The while-loop contract — check all three every time you write one:
    1. INITIALISE   every pointer has a starting value before the loop
    2. CONDITION    the test is about a variable the body actually changes
    3. PROGRESS     every path through the body moves at least one pointer
A loop that hangs has almost always broken rule 3.
"""


# ============================================================================
# PATTERN 1 — ONE POINTER, two sequences, the cursor never rewinds
# ============================================================================

def count_below(sorted_values, sorted_queries):
    """For each query, how many values are strictly less than it.

    Both lists must be sorted ascending. Because the queries only ever grow,
    the answer for a later query can never be smaller than for an earlier one,
    so the cursor never needs to go back to the start.
    """
    # The variables
    #   value_cursor  how many values are known to be < the query being handled
    #                 (also the index of the first value NOT yet counted)
    #   counts        one answer per query, in query order
    value_cursor = 0
    counts = []

    for query in sorted_queries:
        while value_cursor < len(sorted_values) and sorted_values[value_cursor] < query:
            value_cursor += 1
        counts.append(value_cursor)

    return counts


# ============================================================================
# PATTERN 2 — TWO POINTERS, two sorted sequences, one step each turn
# ============================================================================

def merge_sorted(left, right):
    """Merge two ascending lists into one ascending list.

    The merge step of merge sort. Exactly one pointer advances per iteration,
    so the total work is len(left) + len(right), never their product.
    """
    # The variables
    #   left_index   next item not yet taken from left
    #   right_index  next item not yet taken from right
    #   merged       the output, built in order
    left_index = 0
    right_index = 0
    merged = []

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:      # <= keeps equal items in left's order (stable)
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # one side is now exhausted; the other is already sorted and all of it is larger
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


# ============================================================================
# PATTERN 3 — TWO POINTERS, one sorted sequence, converging from both ends
# ============================================================================

def find_pair_with_sum(sorted_values, target):
    """Return the indices of two values that add to target, or None.

    Works because the list is sorted: if the current pair is too big, the only
    way to shrink it is to lower the high end; if too small, raise the low end.
    Each step eliminates one candidate permanently.
    """
    # The variables
    #   low_index   index of the smallest value still in play
    #   high_index  index of the largest value still in play
    low_index = 0
    high_index = len(sorted_values) - 1

    while low_index < high_index:
        total = sorted_values[low_index] + sorted_values[high_index]
        if total == target:
            return (low_index, high_index)
        elif total < target:
            low_index += 1          # need a bigger sum
        else:
            high_index -= 1         # need a smaller sum

    return None


# === How it Runs ===
# --- count_below (one pointer) ---
# the for loop walks the queries; value_cursor walks the values and NEVER resets between queries
# the while advances value_cursor past every value smaller than the current query, then stops
# whatever value_cursor is at that moment IS the answer, because it counts exactly the values already passed
# the two guards in the while matter in this order: bounds first, then the comparison,
#   because Python stops at the first false test and would otherwise index off the end
#
# trace on sorted_values = [10, 20, 30, 40], sorted_queries = [15, 25, 100]:
#   query 15 : cursor 0 -> 10 < 15 so cursor 1 -> 20 < 15 is false, stop.  counts [1]
#   query 25 : cursor 1 -> 20 < 25 so cursor 2 -> 30 < 25 is false, stop.  counts [1, 2]
#   query 100: cursor 2 -> 30 < 100 so 3 -> 40 < 100 so 4 -> out of range. counts [1, 2, 4]
#   cursor moved 0 -> 4 in total across all three queries, not 4 times over
#
# --- merge_sorted (two pointers, two lists) ---
# both pointers start at 0 and the loop runs while BOTH lists still have items left
# compare the two front items, take the smaller, advance only that side
# when either side runs out the loop ends and the remainder of the other is appended whole - no comparisons needed
#
# trace on left = [2, 4, 5], right = [1, 3, 6]:
#   left[0]=2 vs right[0]=1 -> take 1, right_index 1     merged [1]
#   left[0]=2 vs right[1]=3 -> take 2, left_index  1     merged [1, 2]
#   left[1]=4 vs right[1]=3 -> take 3, right_index 2     merged [1, 2, 3]
#   left[1]=4 vs right[2]=6 -> take 4, left_index  2     merged [1, 2, 3, 4]
#   left[2]=5 vs right[2]=6 -> take 5, left_index  3     merged [1, 2, 3, 4, 5]
#   left_index 3 == len(left), loop ends, extend with right[2:] = [6]
#                                                        merged [1, 2, 3, 4, 5, 6]
#
# --- find_pair_with_sum (two pointers, one list, converging) ---
# low_index starts at the smallest value, high_index at the largest
# each comparison rules out one value forever, so the gap only ever narrows - that is the progress guarantee
# the loop ends when they meet, which is at most len(sorted_values) steps
#
# trace on sorted_values = [1, 3, 4, 6, 8, 11], target = 10:
#   low 0 (1)  + high 5 (11) = 12 > 10 -> high 4
#   low 0 (1)  + high 4 (8)  =  9 < 10 -> low  1
#   low 1 (3)  + high 4 (8)  = 11 > 10 -> high 3
#   low 1 (3)  + high 3 (6)  =  9 < 10 -> low  2
#   low 2 (4)  + high 3 (6)  = 10 == 10 -> return (2, 3)


print(count_below([10, 20, 30, 40], [15, 25, 100]))  # [1, 2, 4] — cursor ends at 4, having moved forward only
print(count_below([10, 20, 30, 40], [5]))  # [0] — every value is bigger, cursor never moves
print(count_below([], [1, 2]))  # [0, 0] — no values at all, the bounds guard stops the while immediately
print(count_below([10, 20], [20, 20]))  # [1, 1] — strictly less, so 20 does not count itself

print(merge_sorted([2, 4, 5], [1, 3, 6]))  # [1, 2, 3, 4, 5, 6] — the classic interleave
print(merge_sorted([], [1, 2]))  # [1, 2] — empty side, loop never runs, extend does the work
print(merge_sorted([1, 2], []))  # [1, 2] — same in mirror
print(merge_sorted([1, 1], [1]))  # [1, 1, 1] — ties all kept, left first

print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 10))  # (2, 3) — 4 + 6
print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 12))  # (0, 5) — 1 + 11, found on the first step
print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 100))  # None — pointers meet without a hit
print(find_pair_with_sum([5], 10))  # None — one element, low_index < high_index is false immediately

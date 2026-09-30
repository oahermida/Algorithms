# Fibonacci, dynamic programming - instrumented copy.
#
# Generated from Fibonacci_DP.py in this directory. That file is the clean set of
# algorithms and the one to edit; this one is the same code with print statements
# added around it, and nothing else changed.
#
# It narrates the two DP versions side by side on the same index, so the point
# that they are one recurrence read in two directions is visible rather than
# asserted:
#
#   memoisation (top-down)  - starts at index, recurses DOWN to the base cases,
#                             and writes each answer into the cache on the way
#                             back UP. The cache starts empty and fills in
#                             descending order of index.
#   tabulation (bottom-up)  - starts AT the base cases and fills a table
#                             forward. Nothing recurses; slot k is written once
#                             and only after slots k-1 and k-2 already hold
#                             their final values.
#
# index          - the n in F(n), the value being asked for
# memo_table     - dict mapping index -> F(index), for the top-down version
# depth          - how deep the recursion currently is, used only for indenting
# fibonacci_table- list where slot k holds F(k), for the bottom-up version
# position       - the slot being filled on this pass of the bottom-up loop
# previous_value - F(position - 2) in the rolling version
# current_value  - F(position - 1) in the rolling version
#
# Each trace line is tagged [Ln] with the line of the algorithm it is reporting
# on. The numbers are looked up from this file at startup, so they stay correct
# even if the code moves around.

import pathlib

SOURCE = pathlib.Path(__file__).read_text().splitlines()


def line_of(statement):
    """Return the 1-based line number where `statement` appears in this file."""
    for number, text in enumerate(SOURCE, start=1):
        if text.strip() == statement:
            return number
    raise ValueError(f"statement not found in source: {statement!r}")


def tag(number=None):
    """A fixed-width [Ln] label, or blank padding for lines with no code line."""
    return f"[L{number:>3}] " if number else "        "


THICK = "=" * 78
THIN = "-" * 78

TRACE_INDEX = 8


# =====================================================================
# 1. NAIVE RECURSION - counted, not narrated
# =====================================================================
# Printing every naive call would be unreadable (67 lines for index 8 alone,
# 2.7 million for index 30), so this one is only counted. The repeats it makes
# are what the two versions below exist to remove.

def naive_fibonacci(index, call_counter, rebuild_counter):
    call_counter["calls"] += 1
    rebuild_counter[index] = rebuild_counter.get(index, 0) + 1

    if index < 2:
        return index

    return (naive_fibonacci(index - 1, call_counter, rebuild_counter)
            + naive_fibonacci(index - 2, call_counter, rebuild_counter))


# =====================================================================
# 2. MEMOISATION - narrated
# =====================================================================

L_CHECK = line_of("if index in memo_table:")
L_BASE = line_of("result = index")
L_RECURSE = line_of("left_value = traced_memoised(index - 1, memo_table, depth + 1)")
L_STORE = line_of("memo_table[index] = result")


def traced_memoised(index, memo_table, depth=0):
    pad = "  " * depth

    print(f"{tag(L_CHECK)}{pad}F({index})?  cache holds {sorted(memo_table) if memo_table else 'nothing yet'}")

    if index in memo_table:
        print(f"{tag(L_CHECK)}{pad}  HIT  -> {memo_table[index]} returned without expanding anything")
        return memo_table[index]

    if index < 2:
        result = index
        print(f"{tag(L_BASE)}{pad}  base case -> F({index}) = {result}")
    else:
        print(f"{tag(L_RECURSE)}{pad}  MISS -> must compute F({index - 1}) + F({index - 2})")
        left_value = traced_memoised(index - 1, memo_table, depth + 1)
        right_value = traced_memoised(index - 2, memo_table, depth + 1)
        result = left_value + right_value
        print(f"{tag(L_RECURSE)}{pad}  F({index - 1}) + F({index - 2}) = {left_value} + {right_value} = {result}")

    memo_table[index] = result
    print(f"{tag(L_STORE)}{pad}  STORE F({index}) = {result}   cache now {dict(sorted(memo_table.items()))}")
    return result


# =====================================================================
# 3. TABULATION - narrated
# =====================================================================

L_INIT = line_of("fibonacci_table = [0] * (index + 1)")
L_BASE0 = line_of("fibonacci_table[0] = 0")
L_BASE1 = line_of("fibonacci_table[1] = 1")
L_LOOP = line_of("for position in range(2, index + 1):")
L_FILL = line_of("fibonacci_table[position] = (fibonacci_table[position - 1]")


def traced_tabulated(index):
    if index < 2:
        print(f"{tag()}index {index} is a base case, no table needed -> {index}")
        return index

    fibonacci_table = [0] * (index + 1)
    print(f"{tag(L_INIT)}table of {index + 1} slots, one per index 0..{index}")
    print(f"{tag(L_INIT)}  {fibonacci_table}")

    fibonacci_table[0] = 0
    print(f"{tag(L_BASE0)}slot 0 = 0   (base case - the recurrence cannot produce this one)")
    fibonacci_table[1] = 1
    print(f"{tag(L_BASE1)}slot 1 = 1   (base case)")
    print(f"{tag()}  {fibonacci_table}")
    print(f"{tag(L_LOOP)}filling forward, one slot per pass:")

    for position in range(2, index + 1):
        left_source = fibonacci_table[position - 1]
        right_source = fibonacci_table[position - 2]
        fibonacci_table[position] = (fibonacci_table[position - 1]
                                     + fibonacci_table[position - 2])
        print(f"{tag(L_FILL)}  position = {position:<2} reads slot {position - 1} ({left_source}) "
              f"+ slot {position - 2} ({right_source}) = {fibonacci_table[position]}")
        print(f"{tag()}     {fibonacci_table}")
        print(f"{tag()}     slots 0..{max(position - 2, 0) - 1 if position >= 3 else -1} "
              f"are now dead - nothing reads them again"
              if position >= 3 else f"{tag()}     nothing dead yet")

    print(f"{tag()}return slot {index} = {fibonacci_table[index]}")
    return fibonacci_table[index]


# =====================================================================
# 4. ROLLING PAIR - narrated
# =====================================================================

L_ROLL_INIT = line_of("previous_value, current_value = 0, 1")
L_ROLL = line_of("previous_value, current_value = current_value, previous_value + current_value")


def traced_rolling(index):
    if index < 2:
        print(f"{tag()}index {index} is a base case -> {index}")
        return index

    previous_value, current_value = 0, 1
    print(f"{tag(L_ROLL_INIT)}previous_value = 0  (F(0)),  current_value = 1  (F(1))")
    print(f"{tag()}the window starts on F(0), F(1) and slides right one step per pass")

    for pass_number in range(2, index + 1):
        old_previous, old_current = previous_value, current_value
        previous_value, current_value = current_value, previous_value + current_value
        print(f"{tag(L_ROLL)}  pass for F({pass_number}): "
              f"({old_previous}, {old_current}) -> ({previous_value}, {current_value})"
              f"    {old_previous} + {old_current} = {current_value}")
        print(f"{tag()}     window is now (F({pass_number - 1}), F({pass_number}))")

    print(f"{tag()}return current_value = {current_value}")
    return current_value


# =====================================================================
# 5. RUN ALL THREE ON THE SAME INDEX
# =====================================================================

print(THICK)
print(f"FIBONACCI - TRACED AT index = {TRACE_INDEX}")
print(THICK)

print()
print(THIN)
print("WHAT THE NAIVE VERSION WASTES")
print(THIN)

naive_counter = {"calls": 0}
rebuild_counter = {}
naive_result = naive_fibonacci(TRACE_INDEX, naive_counter, rebuild_counter)

print(f"{tag()}F({TRACE_INDEX}) = {naive_result}, reached in {naive_counter['calls']} calls")
print(f"{tag()}how many times each index was rebuilt from scratch:")
for rebuilt_index in sorted(rebuild_counter, reverse=True):
    times = rebuild_counter[rebuilt_index]
    bar = "#" * times
    print(f"{tag()}  F({rebuilt_index}) built {times:>2}x  {bar}")
print(f"{tag()}only {len(rebuild_counter)} distinct values exist, "
      f"but {naive_counter['calls']} calls were made to get them")

print()
print(THIN)
print("2. MEMOISATION (top-down) - indentation is recursion depth")
print(THIN)
memo_table = {}
memo_result = traced_memoised(TRACE_INDEX, memo_table)
print(f"{tag()}result {memo_result}, cache ended up holding "
      f"{len(memo_table)} entries: {dict(sorted(memo_table.items()))}")
print(f"{tag()}note the ORDER of the STORE lines: {sorted(memo_table)} - "
      f"it fills from the bottom up, even though the calls went top-down")

print()
print(THIN)
print("3. TABULATION (bottom-up) - no recursion, no indentation")
print(THIN)
tabulated_result = traced_tabulated(TRACE_INDEX)

print()
print(THIN)
print("4. ROLLING PAIR (bottom-up, two variables)")
print(THIN)
rolling_result = traced_rolling(TRACE_INDEX)

print()
print(THICK)
print("DONE")
print(f"naive      {naive_result:>6}   {naive_counter['calls']:>6} calls")
print(f"memoised   {memo_result:>6}   {len(memo_table):>6} cache entries")
print(f"tabulated  {tabulated_result:>6}   {TRACE_INDEX - 1:>6} additions, {TRACE_INDEX + 1} slots")
print(f"rolling    {rolling_result:>6}   {TRACE_INDEX - 1:>6} additions, 2 variables")
print(f"all four agree: "
      f"{naive_result == memo_result == tabulated_result == rolling_result}")
print(THICK)

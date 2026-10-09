r"""
MAGIC BUNNY AND REAL BUNNY
Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 3-14.

Notes: [[Bunny DP — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Bunny DP — Code Notes.md

What is in this file:
    1. magic_bunny            the lecturer's pseudocode [slide 6], as Python
    2. magic_bunny_rolling    same answer, O(1) space  [slide 15's question]
    3. restore_magic_path     which cells the bunny actually landed on
    4. real_bunny             the two-state version    [slide 12]
    5. restore_real_path      path restoring with the state bit carried along
    6. real_bunny_wrong       the dp3[i-3] bug, run to show what it breaks
    7. brute force checks     every legal path enumerated, for verification

Run with:
    python3 Bunny_DP.py
"""

import random

NEGATIVE_INFINITY = float("-inf")

# The two arrays from the slides, kept as named constants so every section can
# be checked against the numbers the lecturer put on screen.
MAGIC_SLIDE_AWARDS = [2, -5, -5, 4, -1, 3, 7]        # slide 7,  answer 15
REAL_SLIDE_AWARDS = [1, -10, -10, 5, -10, -10, 6]    # slide 13, answer -8


# =====================================================================
# 1. MAGIC BUNNY -- the lecturer's pseudocode [slide 6]
# =====================================================================
# Notes: [[Bunny DP — Code Notes#1. Magic Bunny — the lecturer's pseudocode]] (variables, loop order)

def magic_bunny(awards):
    last_cell = len(awards) - 1
    best_to_cell = [NEGATIVE_INFINITY] * len(awards)

    best_to_cell[0] = awards[0]                    # base case: dp[0] = a[0]

    for cell in range(1, len(awards)):
        best_arrival = best_to_cell[cell - 1]      # a +1 hop is always possible
        if cell - 3 >= 0:                          # a +3 jump only exists from cell 3 on
            best_arrival = max(best_arrival, best_to_cell[cell - 3])
        best_to_cell[cell] = awards[cell] + best_arrival

    return best_to_cell[last_cell], best_to_cell


# =====================================================================
# 2. MAGIC BUNNY, O(1) SPACE [slide 15 asks "how to save a bit of space?"]
# =====================================================================
# Notes: [[Bunny DP — Code Notes#2. Magic Bunny, O(1) space]] (variables, the trade-off)

def magic_bunny_rolling(awards):
    value_three_back = NEGATIVE_INFINITY           # dp[-2], does not exist
    value_two_back = NEGATIVE_INFINITY             # dp[-1], does not exist
    value_one_back = awards[0]                     # dp[0], the base case

    for cell in range(1, len(awards)):
        best_arrival = value_one_back
        if cell - 3 >= 0:
            best_arrival = max(best_arrival, value_three_back)
        current_value = awards[cell] + best_arrival

        value_three_back, value_two_back, value_one_back = (
            value_two_back, value_one_back, current_value)

    return value_one_back


# =====================================================================
# 3. PATH RESTORING [slide 15, "can we restore an optimal path?"]
# =====================================================================
# Notes: [[Bunny DP — Code Notes#3. Path restoring]] (variables, tie-breaking)

def restore_magic_path(awards, best_to_cell):
    path = []
    cell = len(awards) - 1

    while cell > 0:
        path.append(cell)
        if cell - 3 >= 0 and best_to_cell[cell - 3] >= best_to_cell[cell - 1]:
            cell -= 3                              # the +3 jump was the better arrival
        else:
            cell -= 1                              # the +1 hop was

    path.append(0)
    path.reverse()
    return path


# =====================================================================
# 4. REAL BUNNY -- two states [slide 12]
# =====================================================================
# Notes: [[Bunny DP — Code Notes#4. Real Bunny — two states]] (variables, the asymmetry)

def real_bunny(awards):
    last_cell = len(awards) - 1
    arrived_by_hop = [NEGATIVE_INFINITY] * len(awards)
    arrived_by_jump = [NEGATIVE_INFINITY] * len(awards)

    arrived_by_hop[0] = awards[0]                  # starts rested, collects cell 0
    arrived_by_jump[0] = NEGATIVE_INFINITY         # cannot have arrived by jumping

    for cell in range(1, len(awards)):
        # +1 hop: legal from a rested OR a tired bunny, and it leaves it rested
        arrived_by_hop[cell] = awards[cell] + max(arrived_by_hop[cell - 1],
                                                  arrived_by_jump[cell - 1])
        # +3 jump: legal only from a RESTED bunny -- note arrived_by_hop, not _jump
        if cell - 3 >= 0:
            arrived_by_jump[cell] = awards[cell] + arrived_by_hop[cell - 3]
        else:
            arrived_by_jump[cell] = NEGATIVE_INFINITY

    best_total = max(arrived_by_hop[last_cell], arrived_by_jump[last_cell])
    return best_total, arrived_by_hop, arrived_by_jump


# =====================================================================
# 5. PATH RESTORING WITH A STATE BIT
# =====================================================================
# Notes: [[Bunny DP — Code Notes#5. Path restoring with a state bit]] (variables)

def restore_real_path(awards, arrived_by_hop, arrived_by_jump):
    last_cell = len(awards) - 1
    cell = last_cell
    current_state = 1 if arrived_by_hop[last_cell] >= arrived_by_jump[last_cell] else 3

    path = []
    while cell > 0:
        path.append(cell)
        if current_state == 3:
            cell -= 3                              # the only legal predecessor
            current_state = 1                      # and it must have been rested
        else:
            previous_cell = cell - 1
            current_state = (1 if arrived_by_hop[previous_cell]
                             >= arrived_by_jump[previous_cell] else 3)
            cell = previous_cell

    path.append(0)
    path.reverse()
    return path


# =====================================================================
# 6. THE BUG THE SLIDE WARNS ABOUT -- "# NOT dp3[i-3] !"
# =====================================================================
# Identical to real_bunny except the +3 line also allows a tired predecessor.
# It looks harmless, and it silently deletes the entire rule: if a +3 jump may
# follow a +3 jump, the bunny never has to rest, and the answer collapses back
# to the Magic Bunny's. Kept here and run below so the failure is visible
# rather than described.

def real_bunny_wrong(awards):
    last_cell = len(awards) - 1
    arrived_by_hop = [NEGATIVE_INFINITY] * len(awards)
    arrived_by_jump = [NEGATIVE_INFINITY] * len(awards)

    arrived_by_hop[0] = awards[0]
    arrived_by_jump[0] = NEGATIVE_INFINITY

    for cell in range(1, len(awards)):
        arrived_by_hop[cell] = awards[cell] + max(arrived_by_hop[cell - 1],
                                                  arrived_by_jump[cell - 1])
        if cell - 3 >= 0:
            # THE BUG: a tired bunny is allowed to jump again
            arrived_by_jump[cell] = awards[cell] + max(arrived_by_hop[cell - 3],
                                                       arrived_by_jump[cell - 3])
        else:
            arrived_by_jump[cell] = NEGATIVE_INFINITY

    return max(arrived_by_hop[last_cell], arrived_by_jump[last_cell])


# =====================================================================
# 7. BRUTE FORCE -- every legal path, for checking only
# =====================================================================
# Exponential, and that is fine: it exists to disagree with the DP versions if
# they are wrong. It follows the problem statement literally rather than any
# recurrence, so a mistake in the recurrence cannot hide in it too.
#
# A jump landing past cell n is not a move -- the bunny must reach n exactly.

def brute_force_magic(awards):
    last_cell = len(awards) - 1

    def best_from(cell):
        if cell == last_cell:
            return awards[cell]
        options = [best_from(cell + 1)]
        if cell + 3 <= last_cell:
            options.append(best_from(cell + 3))
        return awards[cell] + max(options)

    return best_from(0)


def brute_force_real(awards):
    last_cell = len(awards) - 1

    def best_from(cell, last_jump_length):
        if cell == last_cell:
            return awards[cell]
        options = [best_from(cell + 1, 1)]
        if cell + 3 <= last_cell and last_jump_length != 3:
            options.append(best_from(cell + 3, 3))
        return awards[cell] + max(options)

    return best_from(0, 1)                         # starts rested


# =====================================================================
# 8. HELPERS FOR PRINTING THE TABLES THE WAY THE SLIDES DO
# =====================================================================

def format_value(value):
    return "-inf" if value == NEGATIVE_INFINITY else str(value)


def format_sum(awards, path):
    """The landed-on values as a sum, negatives in brackets so it reads cleanly."""
    parts = [str(awards[cell]) if awards[cell] >= 0 else f"({awards[cell]})"
             for cell in path]
    return f"{' + '.join(parts)} = {sum(awards[cell] for cell in path)}"


def print_table(awards, rows, path=None):
    """Print the cell / a[i] / dp rows as a slide-style table."""
    columns = len(awards)
    width = 6

    print("      " + "".join(f"{cell:>{width}}" for cell in range(columns)))
    print("      " + "-" * (width * columns))
    print("a[i] |" + "".join(f"{value:>{width}}" for value in awards))
    for label, values in rows:
        print(f"{label:<5}|" + "".join(f"{format_value(value):>{width}}" for value in values))

    if path is not None:
        marks = ["*" if cell in path else "." for cell in range(columns)]
        print("land |" + "".join(f"{mark:>{width}}" for mark in marks))


# =====================================================================
# 9. RUN THE SLIDE EXAMPLES
# =====================================================================

print("=" * 78)
print("MAGIC BUNNY   -- Lecture 4-5, slides 3-8")
print("=" * 78)

magic_total, magic_table = magic_bunny(MAGIC_SLIDE_AWARDS)
magic_path = restore_magic_path(MAGIC_SLIDE_AWARDS, magic_table)

print(f"\na = {MAGIC_SLIDE_AWARDS},  n = {len(MAGIC_SLIDE_AWARDS) - 1}   [slide 7]\n")
print_table(MAGIC_SLIDE_AWARDS, [("dp", magic_table)], magic_path)

print(f"\nanswer dp[n] = {magic_total}")
print(f"optimal path = {' -> '.join(str(cell) for cell in magic_path)}")
print(f"check        = {format_sum(MAGIC_SLIDE_AWARDS, magic_path)}")

# The single most important cell on the slide: the one where the +3 jump wins.
print(f"\nthe cell that shows why the +3 jump exists [slide 7]:")
print(f"  dp[3] = a[3] + max(dp[2], dp[0]) = {MAGIC_SLIDE_AWARDS[3]} + "
      f"max({magic_table[2]}, {magic_table[0]}) = {magic_table[3]}")
print(f"  it comes from dp[0], NOT dp[2] -- the +3 jump flies over both -5 cells")
print(f"  hopping all the way would have given 2 + (-5) + (-5) + 4 = "
      f"{sum(MAGIC_SLIDE_AWARDS[:4])} instead of {magic_table[3]}")

print(f"\nrolling O(1)-space version agrees: {magic_bunny_rolling(MAGIC_SLIDE_AWARDS)}")
print(f"brute force over every legal path agrees: {brute_force_magic(MAGIC_SLIDE_AWARDS)}")


print("\n" + "=" * 78)
print("REAL BUNNY   -- Lecture 4-5, slides 9-14")
print("=" * 78)

real_total, hop_table, jump_table = real_bunny(REAL_SLIDE_AWARDS)
real_path = restore_real_path(REAL_SLIDE_AWARDS, hop_table, jump_table)

print(f"\na = {REAL_SLIDE_AWARDS},  n = {len(REAL_SLIDE_AWARDS) - 1}   [slide 13]\n")
print_table(REAL_SLIDE_AWARDS,
            [("dp1", hop_table), ("dp3", jump_table)],
            real_path)
print("\n  dp1 = last jump was +1 (bunny is rested)")
print("  dp3 = last jump was +3 (bunny is tired)")

last_cell = len(REAL_SLIDE_AWARDS) - 1
print(f"\nanswer max(dp1[n], dp3[n]) = max({format_value(hop_table[last_cell])}, "
      f"{format_value(jump_table[last_cell])}) = {real_total}")
print(f"optimal path = {' -> '.join(str(cell) for cell in real_path)}")
print(f"check        = {format_sum(REAL_SLIDE_AWARDS, real_path)}")

# What the rest rule actually costs, on the same array.
magic_on_real_total, magic_on_real_table = magic_bunny(REAL_SLIDE_AWARDS)
magic_on_real_path = restore_magic_path(REAL_SLIDE_AWARDS, magic_on_real_table)
print(f"\nwhat the rest rule costs, on this same array [slide 13]:")
print(f"  magic bunny (no rest rule): {magic_on_real_total} "
      f"via {' -> '.join(str(cell) for cell in magic_on_real_path)}  -- two +3 jumps")
print(f"  real bunny  (rest rule):    {real_total} "
      f"via {' -> '.join(str(cell) for cell in real_path)}  -- +3, then forced rests")
print(f"  the rule costs {magic_on_real_total - real_total} points here: the bunny is "
      f"forced to land on both -10 cells it wanted to skip")

print(f"\nbrute force over every legal path agrees: {brute_force_real(REAL_SLIDE_AWARDS)}")

# The two endings tie at -8, which is worth noticing: there are two different
# optimal paths, one ending in a hop and one ending in a jump.
if hop_table[last_cell] == jump_table[last_cell]:
    print(f"\nboth endings tie at {real_total}: dp1[{last_cell}] is the path "
          f"{' -> '.join(str(cell) for cell in real_path)} (ends with a hop),")
    print(f"  and dp3[{last_cell}] is 0 -> 1 -> 2 -> 3 -> 6 (ends with a jump) -- "
          f"{format_sum(REAL_SLIDE_AWARDS, (0, 1, 2, 3, 6))}")
    print("  two genuinely different optimal answers; the max just reports the value")


print("\n" + "=" * 78)
print("THE BUG THE SLIDE WARNS ABOUT:  dp3[i] = a[i] + dp1[i-3]   NOT dp3[i-3]")
print("=" * 78)

wrong_total = real_bunny_wrong(REAL_SLIDE_AWARDS)
print(f"\ncorrect version:  {real_total}")
print(f"buggy version:    {wrong_total}")
print(f"magic bunny:      {magic_on_real_total}   <- the buggy version reproduces this")
print("\nreading a tired predecessor lets a +3 follow a +3, so the rest rule stops")
print("existing at all and the Real Bunny quietly becomes the Magic Bunny again.")
print("It does not crash and it does not look wrong -- it just answers a different")
print("question. That is why the lecturer put the warning in the pseudocode itself.")


# =====================================================================
# 10. CHECK THEM PROPERLY -- don't trust two slide examples
# =====================================================================
# Both slide examples passing proves very little. Run every version against the
# brute force on random arrays, including the shapes most likely to break an
# off-by-one: arrays too short for any +3 jump to exist at all.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(1)
trial_count = 3000
magic_disagreements = 0
real_disagreements = 0
rolling_disagreements = 0
path_disagreements = 0

for _ in range(trial_count):
    cell_count = random.randint(1, 12)             # 1 cell means n = 0: start IS finish
    random_awards = [random.randint(-10, 10) for _ in range(cell_count)]

    magic_value, magic_values = magic_bunny(random_awards)
    real_value, hop_values, jump_values = real_bunny(random_awards)

    if magic_value != brute_force_magic(random_awards):
        magic_disagreements += 1
    if real_value != brute_force_real(random_awards):
        real_disagreements += 1
    if magic_bunny_rolling(random_awards) != magic_value:
        rolling_disagreements += 1

    # A restored path must be legal AND worth exactly what the table claims.
    # This is the stronger check: the value can be right while the traceback is
    # wrong, and only walking the path catches that.
    for restored_path, allow_repeat_jumps, claimed_total in (
            (restore_magic_path(random_awards, magic_values), True, magic_value),
            (restore_real_path(random_awards, hop_values, jump_values), False, real_value)):

        legal = restored_path[0] == 0 and restored_path[-1] == cell_count - 1
        previous_jump = 1
        for step in range(1, len(restored_path)):
            jump_length = restored_path[step] - restored_path[step - 1]
            if jump_length not in (1, 3):
                legal = False
            if jump_length == 3 and previous_jump == 3 and not allow_repeat_jumps:
                legal = False                      # two +3 in a row, real bunny only
            previous_jump = jump_length
        if sum(random_awards[cell] for cell in restored_path) != claimed_total:
            legal = False
        if not legal:
            path_disagreements += 1

print(f"\n{trial_count} random arrays, lengths 1-12, values -10..10\n")
print(f"  magic_bunny vs brute force        {trial_count - magic_disagreements}/{trial_count} agree")
print(f"  real_bunny vs brute force         {trial_count - real_disagreements}/{trial_count} agree")
print(f"  rolling vs full table             {trial_count - rolling_disagreements}/{trial_count} agree")
print(f"  restored paths legal and exact    {2 * trial_count - path_disagreements}/{2 * trial_count} pass")

# One more, aimed at the rest rule specifically: on arrays where the magic bunny
# wants two +3 jumps in a row, the real bunny must score strictly less.
rule_bites_count = 0
for _ in range(trial_count):
    random_awards = [random.randint(-10, 10) for _ in range(random.randint(7, 12))]
    magic_value, _ = magic_bunny(random_awards)
    real_value, _, _ = real_bunny(random_awards)
    if real_value > magic_value:
        rule_bites_count += 1

print(f"  real bunny never beats magic       {trial_count - rule_bites_count}/{trial_count} hold")
print("\n  (the last one is a sanity property, not a coincidence: every legal real-bunny")
print("   path is also a legal magic-bunny path, so the real bunny can never score more)")


# Notes: [[Bunny DP — Code Notes#How it runs]] (both slide examples, traced)

r"""
MAGIC BUNNY AND REAL BUNNY
==========================

Both problems come from Advanced Algorithms, Lecture 4-5 (Ivan Bliznets):
Magic Bunny on slides 3-8, Real Bunny on slides 9-14. Neither has a textbook
citation -- the lecture is the only source, so the statements below are the
lecturer's own, kept word for word where it matters.

    MAGIC BUNNY [slide 3]
        - An array a[0 . . . n] of awards and penalties (values can be negative).
        - A bunny starts at cell 0 and must reach cell n.
        - From cell i the bunny may jump to cell i + 1 (a short hop) or
          cell i + 3 (a long jump).
        - Every cell the bunny LANDS ON (including start and finish)
          contributes its value to the total.
        - Goal: choose a sequence of jumps from 0 to n maximising the total.

The one thing to hold on to before anything else: ONLY THE CELLS YOU LAND ON
COUNT. A +3 jump does not collect the two cells it flies over -- it skips them.
That is the whole reason the problem is interesting, because it makes a long
jump the bunny's way of DODGING a run of penalties.

    a = [ 2, -5, -5, 4, -1, 3, 7 ]

      cell     0     1     2     3     4     5     6
      a[i]     2    -5    -5     4    -1     3     7
                \________________/
                 one +3 jump flies straight over both -5 cells


WHY THIS IS A DP PROBLEM [slide 4]
----------------------------------
The same two properties as Fibonacci (see ../Fibonacci_DP/Fibonacci_DP.py):

    OPTIMAL SUBSTRUCTURE   the best path to cell i is built from the best path
                           to i-1 or to i-3, whichever was worth more. You never
                           need to know HOW those were reached, only their value.

    OVERLAPPING SUBPROBLEMS   the best value at a cell is reused later by both
                              i+1 and i+3, so a plain recursion recomputes the
                              same cell many times over.


THE STATE AND THE RECURRENCE [slide 5]
--------------------------------------
    dp[i] = the maximum total value collectible on ANY valid path from cell 0
            to cell i.

The framing that makes the recurrence fall out is ARRIVAL-BASED: stand on cell i
and ask "what is the best way I could have arrived here?" There are only two
answers.

        cell i-3 ------------- +3 jump -------------.
                    (flies OVER i-2 and i-1,        |
                     collecting NEITHER)            v
                                                 cell i
        cell i-1 ------------- +1 hop --------------^

Take whichever arrival was better, then add the cell you are standing on:

        dp[i] = a[i] + max( dp[i-1], dp[i-3] )

        base case:  dp[0] = a[0]          the bunny starts on cell 0 and
                                          collects it
        answer:     dp[n]

THE -infinity CONVENTION [slide 5].  Any dp[j] with j < 0 counts as -infinity,
meaning "that jump simply isn't available this near the start". Using 0 instead
would be a bug: 0 claims "there is a legal path here worth nothing", whereas
-infinity says "there is no legal path here AT ALL". Anything built on top of
-infinity stays -infinity, so an impossible route can never win a max. The same
trick comes back in the Real Bunny.


REAL BUNNY -- THE NEW RULE [slide 9]
------------------------------------
Same array, same start, same goal, one extra restriction:

    The bunny is magic but TIRES OUT -- it cannot perform two jumps of length 3
    in a row. After a length-3 jump it must take a length-1 jump (a rest) before
    it is allowed to jump length 3 again.

WHAT BREAKS [slide 10].  Before, dp[i] only needed the best value of reaching
cell i; it did not matter how the bunny got there. Now it matters -- whether a
+3 jump is legal from cell i depends on whether the LAST jump was already a +3.
One number per cell is no longer enough information. The fix is to extend the
state with one extra bit: was the last jump length 1 or length 3?

That bit turns the problem into a two-state machine:

                    +1 hop (still rested)
                     .--------------.
                     |              |
                     v              |
                [ STATE 1 ] --------'
                last jump was +1
                    |        ^
          +3 jump   |        |   +1 hop -- the forced rest
                    v        |
                [ STATE 3 ] -'
                last jump was +3
                    |
                    X   a +3 jump from here is ILLEGAL


THE STATE AND THE RECURRENCE [slide 11]
---------------------------------------
    dp[i][1] = max value reaching i where the last jump had length 1 (or i = 0)
    dp[i][3] = max value reaching i where the last jump had length 3

    base cases:  dp[0][1] = a[0]          the bunny starts RESTED
                 dp[0][3] = -infinity     it cannot have arrived by a +3 jump

    the two ways into            dp1[i-1] --.
    dp1[i] -- a +1 hop                       \  +1 hop
    is legal from either                      v
    state                        dp3[i-1] -->  dp1[i]

        dp[i][1] = a[i] + max( dp[i-1][1], dp[i-1][3] )

    the ONE way into             dp1[i-3] ---- +3 jump ---->  dp3[i]
    dp3[i] -- the bunny
    had to be rested             dp3[i-3] --X  ILLEGAL: that would be
                                               two +3 jumps in a row

        dp[i][3] = a[i] + dp[i-3][1]          NOT dp[i-3][3]  [slide 12]

    answer:  max( dp[n][1], dp[n][3] )        either ending is acceptable

The slide writes "# NOT dp3[i-3] !" in the pseudocode itself, which is a strong
hint that it is the mistake people make. Section 6 below implements the wrong
version on purpose and shows exactly what it costs.


COMPLEXITY [slides 8 and 14]
----------------------------
    Magic bunny   time O(n)   space O(n), or O(1) with a rolling window
    Real bunny    time O(n)   space O(n) for both arrays, or O(1) rolling

Real Bunny is still O(n): each cell now does a constant amount of EXTRA work --
two states instead of one -- and a constant times O(n) is still O(n).

THE GENERAL PATTERN [slide 14], which is the part worth carrying to the exam:
whenever a constraint depends on the HISTORY of recent choices ("can't repeat X
twice in a row", "must alternate", "cooldown after an action"), augment the DP
state with just enough memory to capture that history. Here a single bit was
enough. A "no +3 jump within the last k moves" rule would need a state tracking
how many steps since the last +3, i.e. dp[i][0 . . . k].

Slide 8 makes the matching point for the Magic Bunny: the arrival-based
recurrence generalises immediately to more jump options (i+1, i+3, i+5) by
adding more terms inside the max.


WHAT IS IN THIS FILE
--------------------
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
# awards         - the array a[0 . . . n]; awards[i] is what cell i pays out
# best_to_cell   - the dp table; best_to_cell[i] is dp[i], the best total
#                  collectible on any legal path from cell 0 to cell i
# cell           - the i being filled on this pass; runs 1, 2, ..., n
# best_arrival   - the better of the two predecessors, before adding a[cell]
#
# The loop fills strictly left to right, so when cell is reached, both cell-1
# and cell-3 already hold their final values. That ordering is the entire
# reason no recursion is needed.
#
# The table is returned alongside the answer because the worked example, the
# path restoring and the agreement checks all want to look at it.

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
# Look at what the loop above actually reads on the pass for cell i: slots i-1
# and i-3, and nothing else. Everything left of i-3 is dead. So keep a window of
# the last three values instead of the whole table.
#
# value_one_back   - dp[cell - 1]
# value_two_back   - dp[cell - 2]   (never read; carried only so the window can shift)
# value_three_back - dp[cell - 3]
#
# The three names are reassigned together on one line, for the same reason the
# Fibonacci rolling version does it: the right-hand side is evaluated in full
# before anything is overwritten.
#
# The trade is real -- this version CANNOT restore the path, because restoring
# needs the whole table to walk back through. That is the actual answer to the
# lecturer's pairing of the two questions on slide 15: you can have O(1) space
# OR the path, not both, unless you re-run the computation.

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
# The table holds only values, not routes -- but the route can be recovered by
# reading the table BACKWARDS. Stand on the last cell and ask the same arrival
# question the recurrence asked: which predecessor did this value come from?
#
# cell    - where the walk-back currently stands, starting at n
# path    - the cells landed on, collected last-to-first and reversed at the end
#
# Whichever of dp[cell-3] and dp[cell-1] was larger is the one the max picked,
# so that is the cell jumped from. The >= makes ties prefer the +3 jump; either
# choice is a genuinely optimal path, they just differ in which one gets printed.

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
# The slides call the two tables dp[i][1] and dp[i][3]. Named here after what
# the bit actually means, since "1" and "3" as array indices are easy to misread:
#
# arrived_by_hop   - dp[i][1]: best value reaching cell i with the last jump
#                    length 1 (or i = 0, because the bunny starts rested)
# arrived_by_jump  - dp[i][3]: best value reaching cell i with the last jump
#                    length 3, which means the bunny is now TIRED
#
# The asymmetry between the two lines below is the whole problem:
#
#   a +1 hop is legal from either state, so arrived_by_hop takes the max of both
#   a +3 jump needs a rested bunny, so arrived_by_jump reads arrived_by_hop ONLY
#
# arrived_by_jump[cell] stays -infinity while cell < 3, because no +3 jump can
# have landed there yet -- there is no such cell to have jumped from.

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
# Same walk-back as the magic bunny, except the state has to be carried along:
# where you came from depends on which table you are currently standing in.
#
# current_state  - 1 if the walk-back is sitting in arrived_by_hop, 3 if in
#                  arrived_by_jump
#
#   in state 3 at cell i  ->  there is only one way in: a +3 from i-3, and the
#                             bunny was rested there, so move to i-3, state 1
#   in state 1 at cell i  ->  came by +1 from i-1, in whichever state held the
#                             larger value there
#
# Starting state is whichever of the two tables won the final max.

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


# === How it Runs ===
#
# --- magic_bunny ---
# best_to_cell is the dp table, one slot per cell, filled strictly left to right
# slot 0 is written directly from awards[0] -- the base case, the only value the
# recurrence cannot produce
# each pass computes ONE slot and never revisits it: look back 1, look back 3 if
# that cell exists, take the better arrival, add the cell you are standing on
# no recursion, because the loop order already guarantees both predecessors are final
#
# filling the table for a = [2, -5, -5, 4, -1, 3, 7]:
#   dp[0] = a[0]                                    = 2      base case
#   dp[1] = -5 + dp[0]                 = -5 +  2    = -3     cell-3 < 0, only the hop exists
#   dp[2] = -5 + dp[1]                 = -5 + -3    = -8     same
#   dp[3] =  4 + max(dp[2], dp[0]) =  4 + max(-8, 2) = 6     <- the +3 jump WINS
#   dp[4] = -1 + max(dp[3], dp[1]) = -1 + max( 6,-3) = 5     hop from 3
#   dp[5] =  3 + max(dp[4], dp[2]) =  3 + max( 5,-8) = 8     hop from 4
#   dp[6] =  7 + max(dp[5], dp[3]) =  7 + max( 8, 6) = 15    hop from 5
#   return dp[6] = 15
#
# dp[3] is the cell the whole example is built around. Arriving by hops means
# landing on both -5 cells (2 - 5 - 5 + 4 = -4); arriving by a +3 jump from cell 0
# skips them entirely (2 + 4 = 6). The jump collects NOTHING in mid-air, which is
# exactly why it wins here
#
# --- restore_magic_path ---
# the table says WHAT the best value is, not HOW it was reached; the walk-back
# recovers the route by asking the arrival question again, in reverse
# start at cell 6, compare dp[3]=6 against dp[5]=8 -> 8 is bigger, so the last
# jump was a +1 hop from cell 5. step to 5 and repeat
#   at 6: max(dp[5]=8,  dp[3]=6)  -> from 5, a hop
#   at 5: max(dp[4]=5,  dp[2]=-8) -> from 4, a hop
#   at 4: max(dp[3]=6,  dp[1]=-3) -> from 3, a hop
#   at 3: max(dp[2]=-8, dp[0]=2)  -> from 0, a JUMP
#   at 0: stop, the start
#   collected backwards as [6,5,4,3,0], reversed to 0 -> 3 -> 4 -> 5 -> 6
# exactly the path on slide 7, and 2 + 4 + (-1) + 3 + 7 = 15 confirms it
#
# --- real_bunny ---
# two tables now, because one number per cell can no longer answer "may I jump?"
#   arrived_by_hop[i]  = dp[i][1], best value reaching i with the last jump = 1
#   arrived_by_jump[i] = dp[i][3], best value reaching i with the last jump = 3
# both are filled on the same pass, left to right, same as before
# arrived_by_hop reads BOTH tables at i-1, because a hop is legal whatever the
# bunny just did; arrived_by_jump reads only arrived_by_hop at i-3, because a
# jump needs a rested bunny. that asymmetry IS the rest rule
#
# filling both tables for a = [1, -10, -10, 5, -10, -10, 6]:
#   i=0  dp1 =   1                                          base: starts rested
#        dp3 =  -inf                                        cannot have jumped in
#   i=1  dp1 = -10 + max(  1, -inf)               =  -9
#        dp3 =  -inf                                        i-3 < 0, no such jump
#   i=2  dp1 = -10 + max( -9, -inf)               = -19
#        dp3 =  -inf                                        i-3 < 0
#   i=3  dp1 =   5 + max(-19, -inf)               = -14     hopped in from 2
#        dp3 =   5 + dp1[0] = 5 + 1               =   6     <- jumped in from 0
#   i=4  dp1 = -10 + max(-14,    6)               =  -4     <- the forced rest, off dp3[3]
#        dp3 = -10 + dp1[1] = -10 + -9            = -19     NOT dp3[1], which is -inf anyway
#   i=5  dp1 = -10 + max( -4,  -19)               = -14
#        dp3 = -10 + dp1[2] = -10 + -19           = -29
#   i=6  dp1 =   6 + max(-14,  -29)               =  -8
#        dp3 =   6 + dp1[3] = 6 + -14             =  -8
#   return max(dp1[6], dp3[6]) = max(-8, -8) = -8
#
# the interesting slot is dp1[4] = -4. it reads dp3[3] = 6, the tired bunny that
# just jumped in from cell 0 -- and that hop is precisely the REST the rule demands.
# the rule is never checked anywhere; it is enforced entirely by which table each
# line is allowed to read
#
# without the rule the bunny would go 0 -> 3 -> 6 for 1 + 5 + 6 = 12. that needs two
# +3 jumps back to back, so it is now illegal, and the best legal answer is -8
#
# --- restore_real_path ---
# same walk-back, but the state bit decides which question to ask
#   dp1[6] = -8 and dp3[6] = -8 tie, so start in state 1 (the >= prefers the hop)
#   at 6 state 1: dp1[5]=-14 vs dp3[5]=-29 -> from 5, state 1
#   at 5 state 1: dp1[4]= -4 vs dp3[4]=-19 -> from 4, state 1
#   at 4 state 1: dp1[3]=-14 vs dp3[3]=  6 -> from 3, state 3   <- arrived TIRED
#   at 3 state 3: only one way in, a +3 from cell 0, which was rested
#   at 0: stop
#   0 -> 3 -> 4 -> 5 -> 6, the path on slide 13, worth 1 + 5 - 10 - 10 + 6 = -8
# in state 3 there is no comparison to make at all, which is the traceback seeing
# the same asymmetry the forward pass had

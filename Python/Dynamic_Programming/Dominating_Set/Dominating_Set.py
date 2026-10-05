r"""
MINIMUM-COST DOMINATING SET -- IN A PATH, AND IN A 2 x n GRID
=============================================================

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets): the path on slides 24-28,
the 2 x n grid on slide 29. Lecture 6-7 ends with the 2 x n grid again
(slide 49/49). Slides 28 and 29, and Lecture 6-7 slide 49, have a title and
nothing else -- the lecturer worked them on the board. So the path DP below
is the slides' own; the 2 x n grid DP is built here by the same idea, and is
not quoted from any slide. No CLRS section covers this problem.

    DOMINATING SET IN A PATH [slide 24]
        Input:   A path P with a specified positive cost for each vertex.
        Output:  Choose a subset of vertices S with a minimum cost such that
                 for each v in P: either v in S or there is u such that u in S
                 and u, v are neighbours.

        Example: 7 -- 2 -- 1 -- 3 -- 5 -- 10 -- 6 -- 17 -- 9 -- 4
                 Solution: S = {2, 3, 6, 4}.

The numbers in the example are the COSTS, and the solution lists the costs of
the chosen vertices: 2 + 3 + 6 + 4 = 15.

    7 -- 2 -- 1 -- 3 -- 5 -- 10 -- 6 -- 17 -- 9 -- 4
        [2]       [3]           [6]            [4]
    each [chosen] vertex covers itself and its two neighbours


FIRST TRY: TWO STATES [slides 25-26]
------------------------------------
    A[i] - cost of the cheapest set Si (subset of Pi) that dominates all
           vertices in Pi.                        (Pi = the first i vertices)
    Is it a good subproblem?

No: it forgets whether vi is in S, and the next vertex needs to know. So the
slide adds one bit:

    A[i, 0] equals to the cost of the cheapest Si that dominates Pi and vi not in Si,
    A[i, 1] equals to the cost of the cheapest Si that dominates Pi and vi in Si?
    Is it true that: A[i+1, 1] = c[i+1] + min{A[i, 0], A[i, 1]}?

Still no. Both states demand that vi is ALREADY dominated inside Pi. But vi can
also be dominated by v(i+1), from the right. That case has no state, so it is
lost. Slide 26 shows it on the path 3 -- 10 -- 2 -- 1: the best set is {3, 1}
(cost 4), where the vertex costing 2 is covered by its RIGHT neighbour.
Section 3 runs the two-state version on it: it answers 5.


THE FIX: THREE STATES [slide 27]
--------------------------------
    A[i, 0]  = cheapest Si that dominates Pi    and vi not in Si
    A[i, 0^] = cheapest Si that dominates Pi-1  and vi not in Si
    A[i, 1]  = cheapest Si that dominates Pi    and vi in Si

The new state 0^ ("zero hat") is "vi is not chosen and may still be
uncovered -- v(i+1) must cover it". Per vertex:

        1    chosen
        0    not chosen, already covered from the left
        0^   not chosen, waiting to be covered from the right

    A[i+1, 0]  = A[i, 1]                         v(i+1) is covered only if vi is chosen
    A[i+1, 0^] = min{ A[i, 1], A[i, 0] }         vi must be fine on its own, not 0^
    A[i+1, 1]  = c[i+1] + min{ A[i, 1], A[i, 0], A[i, 0^] }
                                                 choosing v(i+1) covers vi too,
                                                 so all three states are allowed

    "We have a linear time algorithm."  [slide 27]

Drawn as arrows from column i to column i+1:

        A[i, 1]  ----------.----------.--------> A[i+1, 0]
                            \          \
        A[i, 0]  ------------+----------+------> A[i+1, 0^]
                              \          \
        A[i, 0^] --------------+----------+----> A[i+1, 1]  (+ c[i+1])

        0^ can only go to 1: a waiting vertex MUST be covered by the next one.

The slide does not write the start or the answer. They are:

    base:    A[1, 0] = infinity   (v1 alone cannot be covered without choosing it)
             A[1, 0^] = 0
             A[1, 1] = c[1]
    answer:  min{ A[n, 0], A[n, 1] }    (0^ is not allowed at the end: no v(n+1))


TYPOS IN THE SLIDES
-------------------
    - Slide 27 writes "A[i+1, 1] = c[i] + min{...}". It must be c[i+1]: the
      vertex being chosen is v(i+1).
    - Slide 27 drops commas: "min{A[i, 1]A[i, 0]}" means min{A[i, 1], A[i, 0]}.
    - Slide 26 says "A[2, 1] = 4, A[2, 0] = 10, however the final answer is 3".
      With the slide's own two-state definitions on 3 -- 10 -- 2 -- 1 the
      values are A[2, 1] = 13, A[2, 0] = 3, and the true answer is 4. I could not find a
      reading that gives the slide's numbers. Section 3 prints the real ones.
      The point of the slide still stands: two states give the wrong answer.


THE 2 x n GRID [slide 29 -- board only]
---------------------------------------
Two rows, n columns. Each cell is a vertex with a cost. Neighbours are up,
down, left and right.

        column:   1    2    3    4
        top     [ ] - [ ] - [ ] - [ ]
                 |     |     |     |
        bottom  [ ] - [ ] - [ ] - [ ]

The same idea, one COLUMN at a time instead of one vertex. Each of the two
cells in the current column gets one of the path's three states:

        1    chosen
        0    not chosen, covered (by its column partner or by the left)
        0^   not chosen, still waiting -- the cell to its RIGHT must be chosen

A column state is a pair (top state, bottom state): 3 x 3 = 9 states.

    T[k, (top, bottom)] = cheapest choice in columns 1..k that covers every
                          cell in columns 1..k-1, and leaves column k in
                          exactly the states (top, bottom)

Going from column k to column k+1, try all 4 ways to choose cells in column
k+1 (none, top, bottom, both):

    - a 0^ cell in column k needs the cell to its right chosen, else skip
    - a new cell is 1 if chosen; 0 if its partner is chosen or its left
      neighbour is 1; otherwise 0^
    - cost = T[k, old state] + costs of the newly chosen cells

    answer: min of T[n, state] over states with no 0^

9 states x 4 choices per column: O(n) time. The path is the 1 x n case of
the same scheme.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_dominating_set   every subset of vertices, any graph
    2. path_two_states              the broken first try       [slides 25-26]
    3. path_dominating_table        the lecture's three states [slide 27]
    4. restore_path                 WHICH vertices, walking back on the table
    5. path_rolling                 three variables instead of the table
    6. grid_dominating_table        the 2 x n grid             [slide 29]
    7. restore_grid                 WHICH cells
    8. the slides' examples
    9. tests: hand cases, then random cases against brute force

Run with:
    python3 Dominating_Set.py
"""

import random
from itertools import combinations

INFINITY = float("inf")

# The examples from the slides.
SLIDE_PATH = [7, 2, 1, 3, 5, 10, 6, 17, 9, 4]  # slide 24, answer 2 + 3 + 6 + 4 = 15
COUNTER_PATH = [3, 10, 2, 1]  # slide 26, breaks the two-state version

# State names for one vertex, as in slide 27.
COVERED = "0"  # not chosen, already dominated
WAITING = "0^"  # not chosen, the next vertex must dominate it
CHOSEN = "1"  # in the set
PATH_STATES = (COVERED, WAITING, CHOSEN)


# =====================================================================
# 1. BRUTE FORCE -- every subset of vertices
# =====================================================================
# Works on any graph, so both the path and the grid are checked by it.
#
# costs: cost of each vertex, vertex numbers 0 .. count-1
# neighbours: neighbours[vertex] is the list of vertices next to it
# subset_size: how many vertices this round chooses
# chosen: one particular choice of that many vertices
#
# O(2^n * n): only for testing.

def is_dominating(chosen, neighbours):
    chosen_set = set(chosen)
    return all(vertex in chosen_set or any(other in chosen_set for other in neighbours[vertex])
               for vertex in range(len(neighbours)))


def brute_force_dominating_set(costs, neighbours):
    best_cost = INFINITY
    best_set = None
    for subset_size in range(len(costs) + 1):
        for chosen in combinations(range(len(costs)), subset_size):
            total = sum(costs[vertex] for vertex in chosen)
            if total < best_cost and is_dominating(chosen, neighbours):
                best_cost = total
                best_set = list(chosen)
    return best_cost, best_set


def path_neighbours(vertex_count):
    return [[other for other in (vertex - 1, vertex + 1) if 0 <= other < vertex_count]
            for vertex in range(vertex_count)]


# =====================================================================
# 2. THE FIRST TRY -- two states [slides 25-26]
# =====================================================================
# Kept on purpose, to show what goes wrong. It has no WAITING state, so it can
# never use "this vertex is covered by the one after it".
#
# covered_cost: A[i, 0] for the current vertex
# chosen_cost: A[i, 1] for the current vertex

def path_two_states(costs):
    covered_cost = INFINITY
    chosen_cost = costs[0]
    for vertex_cost in costs[1:]:
        covered_cost, chosen_cost = chosen_cost, vertex_cost + min(covered_cost, chosen_cost)
    return min(covered_cost, chosen_cost)


# =====================================================================
# 3. THE LECTURE'S ALGORITHM -- three states [slide 27]
# =====================================================================
# costs: c[1..n], stored from index 0
# table: A; table[position][state] for state in 0, 0^, 1
# position: the vertex being filled, 0 .. n-1 (vertex v(position+1))
# previous: the row of the vertex before it
#
# Uses c[i+1], not the slide's c[i] (see the typo note).
# O(n) time and space.

def path_dominating_table(costs):
    table = [{COVERED: INFINITY, WAITING: 0, CHOSEN: costs[0]}]  # base case, v1

    for position in range(1, len(costs)):
        previous = table[position - 1]
        table.append({
            COVERED: previous[CHOSEN],
            WAITING: min(previous[CHOSEN], previous[COVERED]),
            CHOSEN: costs[position] + min(previous[CHOSEN], previous[COVERED], previous[WAITING]),
        })

    last = table[len(costs) - 1]
    return min(last[COVERED], last[CHOSEN]), table


# =====================================================================
# 4. RESTORE THE CHOSEN VERTICES -- walking back on the table
# =====================================================================
# Start at the last vertex, in the state that gave the answer. At each step,
# ask which state of the vertex before could have produced this cell:
#
#   COVERED  came from CHOSEN only
#   WAITING  came from CHOSEN or COVERED
#   CHOSEN   came from any of the three, plus this vertex's cost
#
# Pick a predecessor whose value matches. Every vertex in state CHOSEN goes in
# the set.
#
# state: the state of the vertex at `position` on the optimal route
# allowed_before: which states of the vertex before could lead to `state`

def restore_path(costs, table):
    last = table[len(costs) - 1]
    state = COVERED if last[COVERED] <= last[CHOSEN] else CHOSEN
    chosen = []

    for position in range(len(costs) - 1, -1, -1):
        if state == CHOSEN:
            chosen.append(position)
        if position == 0:
            break
        previous = table[position - 1]
        if state == COVERED:
            allowed_before = (CHOSEN,)
            needed = table[position][state]
        elif state == WAITING:
            allowed_before = (CHOSEN, COVERED)
            needed = table[position][state]
        else:
            allowed_before = (CHOSEN, COVERED, WAITING)
            needed = table[position][state] - costs[position]
        state = next(before for before in allowed_before if previous[before] == needed)

    chosen.reverse()
    return chosen


# =====================================================================
# 5. THREE VARIABLES INSTEAD OF THE TABLE
# =====================================================================
# Each row reads only the row before it, so keep one row. O(1) space.
# As always, the rolling version cannot restore the set.

def path_rolling(costs):
    covered_cost, waiting_cost, chosen_cost = INFINITY, 0, costs[0]
    for vertex_cost in costs[1:]:
        covered_cost, waiting_cost, chosen_cost = (
            chosen_cost,
            min(chosen_cost, covered_cost),
            vertex_cost + min(chosen_cost, covered_cost, waiting_cost),
        )
    return min(covered_cost, chosen_cost)


# =====================================================================
# 6. THE 2 x n GRID [slide 29, board only]
# =====================================================================
# grid_costs: grid_costs[row][column], row 0 = top, row 1 = bottom
# table: table[column][(top_state, bottom_state)] = cheapest cost, see the
#        docstring; missing state = impossible
# choice: which cells of the new column are chosen, as (top?, bottom?)
# old_states / new_states: the column states before and after the step
#
# column_states_after works out the new pair of states from the choice and the
# states of the column to the left (None for the first column).

CHOICES = ((False, False), (True, False), (False, True), (True, True))


def column_states_after(choice, left_states):
    new_states = []
    for row in (0, 1):
        partner = 1 - row
        if choice[row]:
            new_states.append(CHOSEN)
        elif choice[partner] or (left_states is not None and left_states[row] == CHOSEN):
            new_states.append(COVERED)
        else:
            new_states.append(WAITING)
    return tuple(new_states)


def choice_is_allowed(choice, left_states):
    # a WAITING cell on the left must have the cell to its right chosen
    return all(choice[row] for row in (0, 1) if left_states[row] == WAITING)


def choice_cost(grid_costs, column, choice):
    return sum(grid_costs[row][column] for row in (0, 1) if choice[row])


def grid_dominating_table(grid_costs):
    column_count = len(grid_costs[0])
    first_column = {}
    for choice in CHOICES:
        states = column_states_after(choice, None)
        cost = choice_cost(grid_costs, 0, choice)
        first_column[states] = min(first_column.get(states, INFINITY), cost)
    table = [first_column]

    for column in range(1, column_count):
        new_column = {}
        for old_states, old_cost in table[column - 1].items():
            for choice in CHOICES:
                if not choice_is_allowed(choice, old_states):
                    continue
                new_states = column_states_after(choice, old_states)
                cost = old_cost + choice_cost(grid_costs, column, choice)
                if cost < new_column.get(new_states, INFINITY):
                    new_column[new_states] = cost
        table.append(new_column)

    finished = [cost for states, cost in table[column_count - 1].items() if WAITING not in states]
    return min(finished), table


# =====================================================================
# 7. RESTORE THE CHOSEN CELLS IN THE GRID
# =====================================================================
# Same walk-back as the path. A column state already says which cells are
# chosen (the ones in state CHOSEN), so only the state of the column to the
# left has to be found: any old state that allows this choice, leads to this
# state, and has the matching cost.
#
# states: the state pair of the current column on the optimal route
# chosen_cells: the answer, as (row, column) pairs

def restore_grid(grid_costs, table):
    column_count = len(grid_costs[0])
    last_column = table[column_count - 1]
    states = min((states for states in last_column if WAITING not in states),
                 key=lambda states: last_column[states])
    chosen_cells = []

    for column in range(column_count - 1, -1, -1):
        choice = tuple(state == CHOSEN for state in states)
        chosen_cells.extend((row, column) for row in (0, 1) if choice[row])
        if column == 0:
            break
        needed = table[column][states] - choice_cost(grid_costs, column, choice)
        states = next(old_states for old_states, old_cost in table[column - 1].items()
                      if old_cost == needed
                      and choice_is_allowed(choice, old_states)
                      and column_states_after(choice, old_states) == states)

    chosen_cells.sort(key=lambda cell: (cell[1], cell[0]))
    return chosen_cells


def grid_as_graph(grid_costs):
    # vertex number for (row, column) is row * column_count + column
    column_count = len(grid_costs[0])
    costs = grid_costs[0] + grid_costs[1]
    neighbours = []
    for row in (0, 1):
        for column in range(column_count):
            near = [(1 - row) * column_count + column]
            if column > 0:
                near.append(row * column_count + column - 1)
            if column < column_count - 1:
                near.append(row * column_count + column + 1)
            neighbours.append(near)
    return costs, neighbours


def print_grid(grid_costs, chosen_cells):
    chosen_set = set(chosen_cells)
    for row, name in ((0, "top   "), (1, "bottom")):
        cells = []
        for column, cost in enumerate(grid_costs[row]):
            cells.append(f"[{cost:>2}]" if (row, column) in chosen_set else f" {cost:>2} ")
        print(f"    {name}  " + " ".join(cells))


# =====================================================================
# 8. RUN THE SLIDES' EXAMPLES
# =====================================================================

print("=" * 78)
print("DOMINATING SET IN A PATH AND IN A 2 x n GRID   -- Lecture 4-5, slides 24-29")
print("=" * 78)

answer, table = path_dominating_table(SLIDE_PATH)
chosen = restore_path(SLIDE_PATH, table)
print(f"\nPath {' -- '.join(str(cost) for cost in SLIDE_PATH)}   [slide 24]")
print(f"  cheapest cost {answer}, chosen costs {[SLIDE_PATH[vertex] for vertex in chosen]}"
      f"   (slide: S = {{2, 3, 6, 4}})")

print("\n  the table, one column per vertex [slide 27]:")
print("    vertex cost " + "".join(f"{cost:>5}" for cost in SLIDE_PATH))
for state in PATH_STATES:
    print(f"    A[i, {state:<2}]   " + "".join(
        f"{'inf' if row[state] == INFINITY else row[state]:>5}" for row in table))

answer, table = path_dominating_table(COUNTER_PATH)
chosen = restore_path(COUNTER_PATH, table)
print(f"\nPath {' -- '.join(str(cost) for cost in COUNTER_PATH)}   [slide 26]")
print(f"  three states (slide 27): {answer}, chosen costs {[COUNTER_PATH[vertex] for vertex in chosen]}")
print(f"  two states (slide 25):   {path_two_states(COUNTER_PATH)}   <- wrong: it cannot let"
      f" the 2 be covered by the 1 to its right")
two_state_covered = COUNTER_PATH[0]  # A[2, 0] = A[1, 1]
two_state_chosen = COUNTER_PATH[1] + min(INFINITY, COUNTER_PATH[0])  # A[2, 1] = c[2] + min{A[1, 0], A[1, 1]}
print(f"  two-state A[2, 1] = {two_state_chosen}, A[2, 0] = {two_state_covered}"
      f"   (the slide prints 4 and 10; see the typo note)")

example_grid = [[3, 1, 4, 1, 5, 9],
                [2, 6, 5, 3, 5, 8]]
answer, table = grid_dominating_table(example_grid)
chosen_cells = restore_grid(example_grid, table)
print(f"\n2 x 6 grid, chosen cells in [brackets]   [slide 29]")
print_grid(example_grid, chosen_cells)
print(f"  cheapest cost {answer}")


# =====================================================================
# 9. TESTS
# =====================================================================
# Each case checks: the table's answer, the rolling answer (path only), and
# that the restored set really dominates and costs exactly the answer.

print("\n" + "=" * 78)
print("TESTS")
print("=" * 78 + "\n")

all_passed = True


def report(passed, message):
    global all_passed
    all_passed = all_passed and passed
    print(f"{'PASS' if passed else 'FAIL'}  {message}")


def check_path(costs):
    answer, table = path_dominating_table(costs)
    chosen = restore_path(costs, table)
    restored_ok = (is_dominating(chosen, path_neighbours(len(costs)))
                   and sum(costs[vertex] for vertex in chosen) == answer)
    return answer, path_rolling(costs) == answer and restored_ok


def check_grid(grid_costs):
    answer, table = grid_dominating_table(grid_costs)
    chosen_cells = restore_grid(grid_costs, table)
    costs, neighbours = grid_as_graph(grid_costs)
    column_count = len(grid_costs[0])
    chosen = [row * column_count + column for row, column in chosen_cells]
    restored_ok = is_dominating(chosen, neighbours) and sum(costs[vertex] for vertex in chosen) == answer
    return answer, restored_ok


path_cases = [
    (SLIDE_PATH, 15),  # slide 24: 2 + 3 + 6 + 4
    (COUNTER_PATH, 4),  # slide 26: {3, 1}
    ([5], 5),  # one vertex must choose itself
    ([5, 1], 1),  # either end covers both
    ([1, 9, 1], 2),  # both ends beat the middle
    ([9, 1, 9], 1),  # the middle covers all three
    ([1, 1, 1, 1, 1, 1], 2),  # unit costs: ceil(6 / 3) = 2
]
for costs, expected in path_cases:
    answer, internal_ok = check_path(costs)
    report(answer == expected and internal_ok, f"path {costs} = {answer}, expected {expected}")

report(path_two_states(COUNTER_PATH) == 5, "the two-state version gives 5 on slide 26's path (the bug)")

grid_cases = [
    ([[1], [1]], 1),  # one column: either cell covers both
    ([[1, 1], [1, 1]], 2),  # 2 x 2: one cell misses the opposite corner
    ([[1, 1, 1], [1, 1, 1]], 2),  # 2 x 3: top-left and bottom-right
    ([[1, 9, 1], [9, 1, 9]], 3),  # cheap cells in a zig-zag
]
for grid_costs, expected in grid_cases:
    answer, internal_ok = check_grid(grid_costs)
    report(answer == expected and internal_ok, f"grid {grid_costs} = {answer}, expected {expected}")

# Unit costs on a 2 x n grid: the known closed form is floor((n + 2) / 2).
formula_ok = all(grid_dominating_table([[1] * column_count, [1] * column_count])[0]
                 == (column_count + 2) // 2 for column_count in range(1, 41))
report(formula_ok, "unit-cost 2 x n grid matches floor((n + 2) / 2) for n = 1 .. 40")

# Random cases against brute force.
random.seed(5)
trial_count = 1500
failures = 0
for _ in range(trial_count):
    costs = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    answer, internal_ok = check_path(costs)
    if answer != brute_force_dominating_set(costs, path_neighbours(len(costs)))[0] or not internal_ok:
        failures += 1
report(failures == 0, f"{trial_count} random paths (1-12 vertices, costs 1-20) agree with brute force"
       f" ({trial_count - failures}/{trial_count})")

trial_count = 400
failures = 0
for _ in range(trial_count):
    column_count = random.randint(1, 7)
    grid_costs = [[random.randint(1, 20) for _ in range(column_count)] for _ in range(2)]
    answer, internal_ok = check_grid(grid_costs)
    if answer != brute_force_dominating_set(*grid_as_graph(grid_costs))[0] or not internal_ok:
        failures += 1
report(failures == 0, f"{trial_count} random 2 x n grids (n = 1-7, costs 1-20) agree with brute force"
       f" ({trial_count - failures}/{trial_count})")

print(f"\n{'ALL PASS' if all_passed else 'SOME TESTS FAILED'}")

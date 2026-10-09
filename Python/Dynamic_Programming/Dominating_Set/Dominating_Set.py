r"""
MINIMUM-COST DOMINATING SET -- IN A PATH, AND IN A 2 x n GRID
Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 24-29.

Notes: [[Dominating Set — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Dominating Set — Code Notes.md

What is in this file:
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
# Notes: [[Dominating Set — Code Notes#1. Brute force — every subset of vertices]] (variables)

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
# Notes: [[Dominating Set — Code Notes#3. The lecture's algorithm — three states]] (variables)

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
# Notes: [[Dominating Set — Code Notes#4. Restore the chosen vertices — walking back on the table]] (variables, predecessor states)

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
# Notes: [[Dominating Set — Code Notes#6. The 2 x n grid]] (variables)

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
# Notes: [[Dominating Set — Code Notes#7. Restore the chosen cells in the grid]] (variables)

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

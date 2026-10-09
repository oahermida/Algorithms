r"""
CHESS-KNIGHT COLLECTING REWARDS
Lecture 3, slides 13-17 (no textbook covers this problem).

Notes: [[Knight Rewards — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Knight Rewards — Code Notes.md

What is in this file:
    1. brute_force_knight       every legal move sequence, for checking
    2. knight_rewards           the lecture's algorithm  [slide 15]
    3. restore_path_by_parents  slide 16's first suggestion: a parent matrix
    4. restore_path_by_walkback slide 16's second: re-derive the predecessor
    5. reachable_cells          which cells any journey can touch at all
    6. worked examples, including a board with no journey
    7. agreement checks against brute force, and the two restorers against
       each other

Run with:
    python3 Knight_Rewards.py
"""

import random

NEGATIVE_INFINITY = float("-inf")

# The two moves, as (row_step, column_step). Named once so no section can
# disagree with another about what a knight move is.
KNIGHT_MOVES = ((1, 2), (2, 1))

# A small board where both possible journeys exist, used for the worked example
# and the How it Runs trace at the bottom.
SMALL_BOARD = [
    [5, 1, 9, 2],
    [3, 4, 7, 6],
    [8, 2, 1, 3],
    [0, 5, 4, 10],
]


# =====================================================================
# 1. BRUTE FORCE -- every legal sequence of moves
# =====================================================================
# Exponential, and deliberately written from the problem statement rather than
# from the recurrence, so that a mistake in the recurrence cannot also hide here.
#
# Returns NEGATIVE_INFINITY when no sequence of moves reaches the far corner,
# which is the honest answer for an unreachable target.

def brute_force_knight(board):
    row_count = len(board)
    column_count = len(board[0])
    target = (row_count - 1, column_count - 1)

    def best_from(row, column):
        if (row, column) == target:
            return board[row][column]

        best_rest = NEGATIVE_INFINITY
        for row_step, column_step in KNIGHT_MOVES:
            next_row, next_column = row + row_step, column + column_step
            if next_row < row_count and next_column < column_count:
                best_rest = max(best_rest, best_from(next_row, next_column))

        if best_rest == NEGATIVE_INFINITY:
            return NEGATIVE_INFINITY            # dead end, not a journey
        return board[row][column] + best_rest

    return best_from(0, 0)


# =====================================================================
# 2. THE LECTURE'S ALGORITHM [slide 15]
# =====================================================================
# Notes: [[Knight Rewards — Code Notes#2. The lecture's algorithm]] (variables, bounds checks, -infinity)

def knight_rewards(board):
    row_count = len(board)
    column_count = len(board[0])

    best_to_cell = [[NEGATIVE_INFINITY] * column_count for _ in range(row_count)]
    best_to_cell[0][0] = board[0][0]                     # base case

    for row in range(row_count):
        for column in range(column_count):
            if row == 0 and column == 0:
                continue                                  # already the base case

            best_arrival = NEGATIVE_INFINITY
            if row - 1 >= 0 and column - 2 >= 0:          # arrived by a (+1, +2) move
                best_arrival = max(best_arrival, best_to_cell[row - 1][column - 2])
            if row - 2 >= 0 and column - 1 >= 0:          # arrived by a (+2, +1) move
                best_arrival = max(best_arrival, best_to_cell[row - 2][column - 1])

            best_to_cell[row][column] = board[row][column] + best_arrival

    return best_to_cell[row_count - 1][column_count - 1], best_to_cell


# =====================================================================
# 3. PATH RESTORING, WAY ONE [slide 16: "pointers to previous cell"]
# =====================================================================
# Records the winning predecessor at the moment the max is taken, while the
# information is free. parent_of[(row, column)] is the cell the knight came
# from, or None for the start.
#
# Cost: a second table of the same size. Benefit: the walk-back is then trivial
# and cannot be fooled by two different predecessors happening to tie.

def knight_rewards_with_parents(board):
    row_count = len(board)
    column_count = len(board[0])

    best_to_cell = [[NEGATIVE_INFINITY] * column_count for _ in range(row_count)]
    parent_of = {}
    best_to_cell[0][0] = board[0][0]
    parent_of[(0, 0)] = None

    for row in range(row_count):
        for column in range(column_count):
            if row == 0 and column == 0:
                continue

            best_arrival = NEGATIVE_INFINITY
            best_parent = None
            for row_step, column_step in KNIGHT_MOVES:
                previous_row, previous_column = row - row_step, column - column_step
                if previous_row >= 0 and previous_column >= 0:
                    candidate = best_to_cell[previous_row][previous_column]
                    if candidate > best_arrival:
                        best_arrival = candidate
                        best_parent = (previous_row, previous_column)

            best_to_cell[row][column] = board[row][column] + best_arrival
            parent_of[(row, column)] = best_parent

    target = (row_count - 1, column_count - 1)
    total = best_to_cell[target[0]][target[1]]

    if total == NEGATIVE_INFINITY:
        return total, best_to_cell, None                 # no journey exists

    path = []
    cell = target
    while cell is not None:
        path.append(cell)
        cell = parent_of[cell]
    path.reverse()
    return total, best_to_cell, path


# =====================================================================
# 4. PATH RESTORING, WAY TWO [slide 16: "move back looking at values
#    where exactly equality occurs"]
# =====================================================================
# Notes: [[Knight Rewards — Code Notes#4. Path restoring, way two]] (the equality test, ties)

def restore_path_by_walkback(board, best_to_cell):
    row_count = len(board)
    column_count = len(board[0])
    target = (row_count - 1, column_count - 1)

    if best_to_cell[target[0]][target[1]] == NEGATIVE_INFINITY:
        return None

    path = []
    cell = target
    while cell != (0, 0):
        path.append(cell)
        row, column = cell
        required = best_to_cell[row][column] - board[row][column]

        for row_step, column_step in KNIGHT_MOVES:
            previous_row, previous_column = row - row_step, column - column_step
            if (previous_row >= 0 and previous_column >= 0
                    and best_to_cell[previous_row][previous_column] == required):
                cell = (previous_row, previous_column)
                break
        else:
            return None                                   # should be unreachable

    path.append((0, 0))
    path.reverse()
    return path


# =====================================================================
# 5. WHICH CELLS CAN BE VISITED AT ALL
# =====================================================================
# Forward flood from (0,0) using the same two moves. Used only for the display
# and for the reachability discussion -- the DP does not need it, since
# -infinity already encodes exactly this.

def reachable_cells(row_count, column_count):
    reached = {(0, 0)}
    frontier = [(0, 0)]
    while frontier:
        row, column = frontier.pop()
        for row_step, column_step in KNIGHT_MOVES:
            next_cell = (row + row_step, column + column_step)
            if (next_cell[0] < row_count and next_cell[1] < column_count
                    and next_cell not in reached):
                reached.add(next_cell)
                frontier.append(next_cell)
    return reached


# =====================================================================
# 6. DISPLAY HELPERS
# =====================================================================

def format_cell(value):
    return "  -inf" if value == NEGATIVE_INFINITY else f"{value:>6}"


def format_path_sum(board, path):
    """The collected rewards as a sum, negatives bracketed so it reads cleanly."""
    parts = [str(board[r][c]) if board[r][c] >= 0 else f"({board[r][c]})"
             for r, c in path]
    return f"{' + '.join(parts)} = {sum(board[r][c] for r, c in path)}"


def print_grid(title, grid, path=None):
    print(f"  {title}")
    column_count = len(grid[0])
    header = "        " + "".join(f"{column:>6}" for column in range(column_count))
    print(header)
    for row_index, row_values in enumerate(grid):
        marks = ""
        if path is not None:
            marks = "   <- " + " ".join(f"({r},{c})" for r, c in path if r == row_index)
            if marks.strip() == "<-":
                marks = ""
        print(f"    {row_index:>2}  " + "".join(format_cell(value) for value in row_values) + marks)


# =====================================================================
# 7. RUN IT
# =====================================================================

print("=" * 78)
print("KNIGHT COLLECTING REWARDS   -- Lecture 3, slides 13-17")
print("=" * 78)

total, table, path = knight_rewards_with_parents(SMALL_BOARD)

print(f"\na 4 x 4 board:\n")
print_grid("A -- rewards", SMALL_BOARD)
print()
print_grid("R -- best total reaching each cell", table)

print(f"\n  answer R[n-1][m-1] = {total}")
print(f"  path  = {' -> '.join(f'({r},{c})' for r, c in path)}")
print(f"  check = {format_path_sum(SMALL_BOARD, path)}")

walkback_path = restore_path_by_walkback(SMALL_BOARD, table)
print(f"\n  slide 16 offers two ways to recover that path:")
print(f"    parent matrix : {' -> '.join(f'({r},{c})' for r, c in path)}")
print(f"    walk-back     : {' -> '.join(f'({r},{c})' for r, c in walkback_path)}")

reached = reachable_cells(len(SMALL_BOARD), len(SMALL_BOARD[0]))
print(f"\n  only {len(reached)} of the {len(SMALL_BOARD) * len(SMALL_BOARD[0])} cells are "
      f"reachable at all: {sorted(reached)}")
print(f"  every other cell keeps its -inf, which is why the R table above is mostly -inf")
print(f"  (each move adds 3 to row+column, so only cells summing to 0, 3, 6, ... exist")
print(f"   for the knight -- and of those, only the ones the L-shapes can actually reach)")

print(f"\n  the other journey, for comparison:")
print(f"    (0,0) -> (2,1) -> (3,3) = 5 + 2 + 10 = 17   -- worse by "
      f"{total - 17}, because cell (2,1) pays 2 where (1,2) pays 7")


# A larger board with penalties, where the choice is less obvious.
print("\n" + "=" * 78)
print("A BIGGER BOARD, WITH PENALTIES")
print("=" * 78)

# 7 x 7, not 8 x 8: the target must satisfy the divisibility rule above, and
# (7-1) + (7-1) = 12 is a multiple of 3 while (8-1) + (8-1) = 14 is not. On an
# 8 x 8 board the knight simply cannot finish, whatever the rewards are.
random.seed(11)
big_board = [[random.randint(-9, 9) for _ in range(7)] for _ in range(7)]
big_total, big_table, big_path = knight_rewards_with_parents(big_board)
assert big_path is not None, "picked a board shape the knight cannot finish on"

print()
print_grid("A -- rewards", big_board)
print()
print_grid("R -- best total reaching each cell", big_table, big_path)
print(f"\n  answer = {big_total}")
print(f"  path   = {' -> '.join(f'({r},{c})' for r, c in big_path)}")
print(f"  check  = {format_path_sum(big_board, big_path)}")
print(f"  brute force over every legal move sequence agrees: {brute_force_knight(big_board)}")


# =====================================================================
# 8. A BOARD WHERE NO JOURNEY EXISTS
# =====================================================================

print("\n" + "=" * 78)
print("WHEN THE KNIGHT CANNOT FINISH AT ALL")
print("=" * 78)

impossible_board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
impossible_total, impossible_table, impossible_path = knight_rewards_with_parents(impossible_board)

print()
print_grid("A -- rewards", impossible_board)
print()
print_grid("R -- best total reaching each cell", impossible_table)
print(f"\n  target is (2,2), and 2 + 2 = 4, which is not a multiple of 3")
print(f"  every move adds exactly 3 to row+column, so the knight lands only on")
print(f"  cells summing to 0, 3, 6, ... -- cell (2,2) is not one of them")
print(f"\n  answer = {impossible_total}   (not 0 -- there is no journey to collect 0 on)")
print(f"  path   = {impossible_path}")
print(f"  brute force agrees: {brute_force_knight(impossible_board)}")
print(f"\n  reachable cells: {sorted(reachable_cells(3, 3))}")


# =====================================================================
# 9. AGREEMENT CHECK
# =====================================================================
# Random boards, including shapes where the target is unreachable, which is the
# case most likely to be got wrong. Every restored path is walked to confirm it
# is a legal knight journey worth exactly what the table claims -- a value can
# be right while the traceback is wrong, and only walking catches that.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(5)
trial_count = 1500
value_disagreements = 0
path_disagreements = 0
restorer_disagreements = 0
unreachable_count = 0

for _ in range(trial_count):
    row_count = random.randint(1, 7)
    column_count = random.randint(1, 7)
    board = [[random.randint(-9, 9) for _ in range(column_count)] for _ in range(row_count)]

    dp_total, dp_table = knight_rewards(board)
    parent_total, _, parent_path = knight_rewards_with_parents(board)
    walkback_path = restore_path_by_walkback(board, dp_table)

    if dp_total != brute_force_knight(board) or dp_total != parent_total:
        value_disagreements += 1

    if dp_total == NEGATIVE_INFINITY:
        unreachable_count += 1
        if parent_path is not None or walkback_path is not None:
            path_disagreements += 1
        continue

    # both restorers must give legal journeys worth exactly dp_total
    for restored in (parent_path, walkback_path):
        legal = (restored is not None
                 and restored[0] == (0, 0)
                 and restored[-1] == (row_count - 1, column_count - 1))
        if legal:
            for step in range(1, len(restored)):
                move = (restored[step][0] - restored[step - 1][0],
                        restored[step][1] - restored[step - 1][1])
                if move not in KNIGHT_MOVES:
                    legal = False
            if sum(board[r][c] for r, c in restored) != dp_total:
                legal = False
        if not legal:
            path_disagreements += 1

    if (sum(board[r][c] for r, c in parent_path)
            != sum(board[r][c] for r, c in walkback_path)):
        restorer_disagreements += 1

print(f"\n{trial_count} random boards, up to 7 x 7, rewards -9..9")
print(f"  ({unreachable_count} of them have no legal journey at all)\n")
print(f"  dp vs brute force                     {trial_count - value_disagreements}/{trial_count}")
print(f"  restored journeys legal and exact     "
      f"{2 * (trial_count - unreachable_count) - path_disagreements}"
      f"/{2 * (trial_count - unreachable_count)}")
print(f"  slide 16's two restorers tie in value {trial_count - unreachable_count - restorer_disagreements}"
      f"/{trial_count - unreachable_count}")
print("\n  (the last line is the point of section 3 vs section 4: the two methods the")
print("   slide offers can pick DIFFERENT paths when values tie, but never paths of")
print("   different value)")


# Notes: [[Knight Rewards — Code Notes#How it runs]] (traced example on the 4 x 4 board)

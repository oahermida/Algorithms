r"""
THE FARMER PROBLEM  (maximal square of good land)
=================================================

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slide 23.

    A PROVENANCE NOTE, because this file is different from its neighbours.
    Every other problem in this collection quotes the lecture deck directly.
    Slide 23 has no text at all -- it is a title and the words "Link to google
    mock interview", pointing at:

        https://www.youtube.com/watch?v=Ti5vfu9arXQ
        "How to solve a Google coding interview question", Life at Google

    So the statement below is transcribed from the interviewer's screen in that
    video, not from the deck. It is the only statement of the problem that
    exists for this course. The candidate's working solution, whiteboarded
    later in the same video, is discussed in THE VIDEO'S OWN SOLUTION below --
    it reaches the same recurrence, and its way of handling the grid edges is
    the one this file uses.

    THE FARMER PROBLEM [from the video]
        A farmer wants to farm their land with the maximum area where good land
        is present. The "land" is represented as a matrix with 1s and 0s, where
        1s mean good land and 0s mean bad land. The farmer only want to farm in
        a square of good land with the maximum area. Please help the farmer to
        find the maximum area of the land they can farm in good land.

        Example:
            0 1 1 0 1
            1 1 0 1 0
            0 1 1 1 0
            1 1 1 1 0
            1 1 1 1 1
            0 0 0 0 0

TWO WORDS DO ALL THE WORK, and both are easy to read past:

    SQUARE.  Not a rectangle. Every side the same length. This is the entire
             reason the problem has a clean O(nm) solution -- see THE SQUARE
             CONSTRAINT IS THE ALGORITHM below.

    AREA.    The answer is a number of cells, not a side length. A 3 x 3 square
             is the answer "9", not "3". The DP naturally computes the side, so
             the last step squares it -- an easy mark to drop.


THE STATE
---------
The framing that makes this fall out is the same arrival-based one as the
bunnies and the knight, adapted to two dimensions. Do NOT ask "where is the
biggest square?" -- ask a question every cell can answer about itself:

    side[i][j] = the side length of the LARGEST SQUARE OF GOOD LAND whose
                 BOTTOM-RIGHT CORNER is the cell (i, j)

Fixing the corner is what turns a search over all squares into one value per
cell. Every square has exactly one bottom-right corner, so the n*m answers
cover every possible square exactly once, and the biggest square overall is
just the largest entry in the table.

    if the land at (i, j) is bad:   side[i][j] = 0    no square can end here
    otherwise:                      side[i][j] = 1 + min( three neighbours )


THE RECURRENCE, AND WHY IT IS A MIN OF THREE
--------------------------------------------
                j-1    j
              +------+------+
        i-1   |  a   |  b   |      a = side[i-1][j-1]   diagonally up-left
              +------+------+      b = side[i-1][j]     directly above
         i    |  c   |  X   |      c = side[i][j-1]     directly left
              +------+------+      X = side[i][j]

    side[i][j] = 1 + min( a, b, c )        when land[i][j] is good

WHY. Suppose a square of side k sits with its bottom-right corner at X. Strip
off X's own row and column and what remains is a square of side k-1 -- and that
same k-1 square is simultaneously covered by all three neighbours' squares:

    it ends at (i-1, j-1), so a >= k-1
    it fits inside the square ending above,   so b >= k-1
    it fits inside the square ending left,    so c >= k-1

So k-1 <= min(a, b, c). The converse holds too: if all three are at least k-1
then the whole k x k block is good land, so the square exists. Hence k is
exactly 1 + min(a, b, c). The MIN is the bottleneck -- one blocked direction
caps the square, no matter how much room the other two have.

ALL THREE TERMS ARE NECESSARY. Dropping the diagonal looks harmless and is not;
section 5 runs a grid where "1 + min(above, left)" claims a 3 x 3 square that
contains a 0. The diagonal is the only term that sees the interior.


THE SQUARE CONSTRAINT IS THE ALGORITHM
--------------------------------------
This recurrence works because a square is described by ONE number. Ask the same
question about the largest RECTANGLE of good land and the state collapses: a
rectangle ending at (i, j) needs both a width and a height, the two trade off
against each other, and no single value per cell can capture it. The maximal
rectangle problem is genuinely harder and needs a different technique (a stack
over histogram heights, which is not a DP at all).

So "the farmer only want to farm in a square" is not flavour text. It is the
hypothesis that makes one number per cell sufficient.


THE VIDEO'S OWN SOLUTION
------------------------
The candidate writes this, live, about 24 minutes in:

        def largest_square(bin_array: list[list[int]]) -> int:
            n = len(bin_array)
            m = len(bin_array[0])
            dp = ...
            for i in range(n):
                for j in range(m):
                    if bin_array[i][j] == 0:
                        continue
                    left = right = diag = 0
                    if i > 0: left = dp[i-1][j]
                    if j > 0: right = dp[i][j-1]
                    if (i > 0 and j > 0): diag = dp[i-1][j-1]

                    dp[i][j] = min([left, right, diag]) + 1

            rowwise_max = [max(row) for row in dp]
            return max(rowwise_max)

It is a mock interview, so this is work in progress rather than finished code --
the point of reading it here is not to audit it. Two things in it are worth
having.

FIRST, it is independent confirmation of the recurrence. Somebody reasoning
through the problem from scratch, on camera, arrives at min of the same three
neighbours plus one. That is worth more than my own file agreeing with itself.

SECOND, its edge handling is better than what this file had. Initialising the
three neighbours to 0 and overwriting each only when it exists means a cell on
the top row or the left column gets min(0, ...) + 1 = 1 with no special case at
all. Section 2 now does it that way. The version I wrote first had a separate
`if row == 0 or column == 0: side = 1` branch, which is two code paths where one
will do, and the edge case is exactly where two paths tend to disagree.

One difference kept deliberately: the names here are `diagonal`, `above` and
`left`, because in the video `left` holds dp[i-1][j], which is the cell ABOVE,
and `right` holds dp[i][j-1], which is the cell to the LEFT. That costs nothing
while you are writing it and a great deal when you read it back a week later.

The video's function also returns max(rowwise_max), the side length. The problem
asks for the AREA, so this file squares it at the end -- see the note under the
worked example.


COMPLEXITY
----------
    time  O(n*m)   one pass, constant work per cell
    space O(n*m)   for the table, or O(m) with a rolling row -- section 4

Brute force, for comparison: try every top-left corner and every side length and
check every cell of each candidate. That is O(n*m*min(n,m)^3) in the obvious
form -- section 1, kept only to check the DP against.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_largest_square   every candidate square, checked cell by cell
    2. largest_square               the O(nm) DP
    3. locate_square                where the winning square actually is
    4. largest_square_rolling       one row of the table, O(m) space
    5. largest_square_no_diagonal   the min-of-two bug, run to show what breaks
    6. the video's example, worked
    7. agreement checks

Run with:
    python3 Farmer_Problem.py
"""

import random

# The grid from the interviewer's screen. 6 rows, 5 columns.
VIDEO_LAND = [
    [0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]

# A grid built to make the diagonal term matter; used in section 5.
DIAGONAL_TRAP_LAND = [
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
]


# =====================================================================
# 1. BRUTE FORCE -- every candidate square
# =====================================================================
# Follows the statement literally: for every top-left corner and every side
# length that still fits on the grid, check whether every cell inside is good.
#
# top_row / left_column - the candidate's top-left corner
# side                  - the candidate's side length
#
# Returns the best side length and where it was found, so the DP has something
# independent to be checked against.

def brute_force_largest_square(land):
    row_count = len(land)
    column_count = len(land[0])
    best_side = 0
    best_corner = None

    for top_row in range(row_count):
        for left_column in range(column_count):
            largest_possible = min(row_count - top_row, column_count - left_column)
            for side in range(1, largest_possible + 1):
                all_good = all(
                    land[top_row + row_offset][left_column + column_offset] == 1
                    for row_offset in range(side)
                    for column_offset in range(side))
                if not all_good:
                    break                       # bigger sides contain this one
                if side > best_side:
                    best_side = side
                    best_corner = (top_row, left_column)

    return best_side, best_corner


# =====================================================================
# 2. THE DP -- one number per cell
# =====================================================================
# land          - the matrix of 1s (good) and 0s (bad)
# side          - the table; side[i][j] is the side length of the largest good
#                 square whose BOTTOM-RIGHT corner is (i, j)
# row, column   - the cell being filled on this pass
#
# Row 0 and column 0 are special only in that two of their neighbours are off
# the grid: a square ending on the top row or left column can never be bigger
# than 1. That is handled by the bounds check rather than by a separate
# initialisation pass, so there is one code path.
#
# The loops run row-major, so all three neighbours -- up-left, up, left -- are
# already final when they are read. The same "loop order is a topological order"
# guarantee as ../Knight_Rewards/.
#
# Returns the AREA, because that is what the farmer asked for, plus the side and
# the table for display and reconstruction.

def largest_square(land):
    row_count = len(land)
    column_count = len(land[0])
    side = [[0] * column_count for _ in range(row_count)]

    best_side = 0
    for row in range(row_count):
        for column in range(column_count):
            if land[row][column] == 0:
                continue                        # bad land: the 0 already there stands

            # Missing neighbours count as 0, so a cell on the top row or the
            # left column automatically gets 1 + min(0, ...) = 1. This is the
            # interviewer's idiom from the video and it is neater than a
            # separate `if row == 0 or column == 0` branch -- one code path
            # instead of two, and the edge case falls out of the arithmetic.
            diagonal = above = left = 0
            if row > 0 and column > 0:
                diagonal = side[row - 1][column - 1]
            if row > 0:
                above = side[row - 1][column]
            if column > 0:
                left = side[row][column - 1]

            side[row][column] = min(diagonal, above, left) + 1
            best_side = max(best_side, side[row][column])

    return best_side * best_side, best_side, side


# =====================================================================
# 3. WHERE THE SQUARE IS
# =====================================================================
# The table gives the area; the farmer also needs to know which field to plough.
#
# No walk-back is needed here, unlike the bunny and knight tracebacks: the
# winning cell IS the bottom-right corner, and the side length is stored in it,
# so the top-left corner is pure arithmetic.
#
# Ties are broken by taking the first maximum in row-major order.

def locate_square(side_table, best_side):
    if best_side == 0:
        return None

    for row, row_values in enumerate(side_table):
        for column, value in enumerate(row_values):
            if value == best_side:
                return (row - best_side + 1, column - best_side + 1,   # top-left
                        row, column)                                    # bottom-right
    return None


# =====================================================================
# 4. ONE ROW INSTEAD OF THE TABLE
# =====================================================================
# Each cell reads only the row above and the cell to its left, so the whole
# table is never needed at once -- the same observation that shrinks Fibonacci
# to two variables and subset sum to one row.
#
# previous_row     - the finished row above
# current_row      - the row being built
#
# O(m) space instead of O(nm). As everywhere else in this collection, the price
# is that the square can no longer be LOCATED afterwards, only measured -- the
# table it would be found in has been thrown away.

def largest_square_rolling(land):
    column_count = len(land[0])
    previous_row = [0] * column_count
    best_side = 0

    for row_values in land:
        current_row = [0] * column_count
        for column, value in enumerate(row_values):
            if value == 0:
                current_row[column] = 0
            elif column == 0:
                current_row[column] = 1
            else:
                current_row[column] = 1 + min(previous_row[column - 1],
                                              previous_row[column],
                                              current_row[column - 1])
            best_side = max(best_side, current_row[column])
        previous_row = current_row

    return best_side * best_side


# =====================================================================
# 5. THE BUG: FORGETTING THE DIAGONAL
# =====================================================================
# Identical to section 2 except the min covers only "above" and "left". It is a
# natural thing to write -- those are the two directions a square grows in, and
# the diagonal feels redundant. It is not: the diagonal is the only term that
# can see whether the INTERIOR of the proposed square is good.
#
# Run in section 7, where it claims a 3 x 3 square containing a 0.

def largest_square_no_diagonal(land):
    row_count = len(land)
    column_count = len(land[0])
    side = [[0] * column_count for _ in range(row_count)]
    best_side = 0

    for row in range(row_count):
        for column in range(column_count):
            if land[row][column] == 0:
                continue

            above = left = 0
            if row > 0:
                above = side[row - 1][column]
            if column > 0:
                left = side[row][column - 1]

            side[row][column] = min(above, left) + 1
            best_side = max(best_side, side[row][column])

    return best_side * best_side, best_side, side


# =====================================================================
# 6. DISPLAY
# =====================================================================

def print_land(land, corner=None, table=None):
    """Print the grid; if a corner is given, mark the winning square with #."""
    inside = set()
    if corner is not None:
        top_row, left_column, bottom_row, right_column = corner
        inside = {(row, column)
                  for row in range(top_row, bottom_row + 1)
                  for column in range(left_column, right_column + 1)}

    column_count = len(land[0])
    print("        " + "".join(f"{column:>3}" for column in range(column_count)))
    for row, row_values in enumerate(land):
        cells = ""
        for column, value in enumerate(row_values):
            mark = "#" if (row, column) in inside else str(value)
            cells += f"{mark:>3}"
        table_part = ""
        if table is not None:
            table_part = "     " + "".join(f"{value:>3}" for value in table[row])
        print(f"    {row:>2} |{cells}{table_part}")


# =====================================================================
# 7. RUN THE VIDEO'S EXAMPLE
# =====================================================================

print("=" * 78)
print("THE FARMER PROBLEM   -- Lecture 4-5, slide 23 (via the linked video)")
print("=" * 78)

area, best_side, side_table = largest_square(VIDEO_LAND)
corner = locate_square(side_table, best_side)

print(f"\nthe land from the interviewer's screen"
      f"   ({len(VIDEO_LAND)} rows x {len(VIDEO_LAND[0])} columns)\n")
print("           land                    side[i][j]")
print_land(VIDEO_LAND, table=side_table)

print(f"\n  side[i][j] = the side of the biggest good square ENDING at (i,j)")
print(f"  the largest entry is {best_side}, at "
      f"({corner[2]},{corner[3]})  -- that cell is the square's BOTTOM-RIGHT corner")

print(f"\nthe square itself, marked #:\n")
print_land(VIDEO_LAND, corner=corner)

print(f"\n  top-left     ({corner[0]}, {corner[1]})")
print(f"  bottom-right ({corner[2]}, {corner[3]})")
print(f"  side   = {best_side}")
print(f"  AREA   = {best_side} x {best_side} = {area}      <- what the farmer asked for")
print(f"\n  note the answer is {area}, not {best_side}. the question says 'maximum AREA',")
print(f"  and the DP computes a SIDE -- the squaring at the end is not a detail.")

brute_side, brute_corner = brute_force_largest_square(VIDEO_LAND)
print(f"\n  brute force over every candidate square agrees: side {brute_side}, "
      f"area {brute_side * brute_side}, at {brute_corner}")
print(f"  rolling O(m)-space version agrees: area {largest_square_rolling(VIDEO_LAND)}")

print(f"\n  the interesting cell is ({corner[2]},{corner[3]}), where side = {best_side}:")
row, column = corner[2], corner[3]
print(f"    land[{row}][{column}] = {VIDEO_LAND[row][column]} (good), so it is 1 + min of three neighbours")
print(f"      diagonal side[{row-1}][{column-1}] = {side_table[row-1][column-1]}")
print(f"      above    side[{row-1}][{column}]   = {side_table[row-1][column]}")
print(f"      left     side[{row}][{column-1}]   = {side_table[row][column-1]}")
print(f"    1 + min({side_table[row-1][column-1]}, {side_table[row-1][column]}, "
      f"{side_table[row][column-1]}) = {side_table[row][column]}")

print(f"\n  and the cell right of it, ({row},{column+1}), collapses back to "
      f"{side_table[row][column+1]}:")
print(f"    the land there is good, but the diagonal above-left is "
      f"{side_table[row-1][column]} and directly above is {side_table[row-1][column+1]},")
print(f"    so 1 + min({side_table[row-1][column]}, {side_table[row-1][column+1]}, "
      f"{side_table[row][column]}) = {side_table[row][column+1]}.")
print(f"    one bad cell above it caps the whole corner -- that is the min at work.")


# =====================================================================
# 8. WHY ALL THREE NEIGHBOURS ARE NEEDED
# =====================================================================

print("\n" + "=" * 78)
print("DROPPING THE DIAGONAL TERM")
print("=" * 78)

correct_area, correct_side, correct_table = largest_square(DIAGONAL_TRAP_LAND)
wrong_area, wrong_side, wrong_table = largest_square_no_diagonal(DIAGONAL_TRAP_LAND)
correct_corner = locate_square(correct_table, correct_side)
wrong_corner = locate_square(wrong_table, wrong_side)

print(f"\n  a grid with a single bad cell in the middle:\n")
print("           land              correct side[i][j]    1 + min(above, left)")
column_count = len(DIAGONAL_TRAP_LAND[0])
print("        " + "".join(f"{c:>3}" for c in range(column_count)))
for row in range(len(DIAGONAL_TRAP_LAND)):
    land_cells = "".join(f"{v:>3}" for v in DIAGONAL_TRAP_LAND[row])
    right_cells = "".join(f"{v:>3}" for v in correct_table[row])
    wrong_cells = "".join(f"{v:>3}" for v in wrong_table[row])
    print(f"    {row:>2} |{land_cells}      {right_cells}          {wrong_cells}")

print(f"\n  correct:  side {correct_side}, area {correct_area}")
print(f"  buggy:    side {wrong_side}, area {wrong_area}")
print(f"  brute force says side {brute_force_largest_square(DIAGONAL_TRAP_LAND)[0]}")

if wrong_corner is not None:
    top_row, left_column, bottom_row, right_column = wrong_corner
    print(f"\n  the buggy version claims a {wrong_side} x {wrong_side} square at rows "
          f"{top_row}-{bottom_row}, columns {left_column}-{right_column}:")
    for row in range(top_row, bottom_row + 1):
        print(f"      {' '.join(str(DIAGONAL_TRAP_LAND[row][column]) for column in range(left_column, right_column + 1))}")
    print(f"  which contains a 0. it is not a square of good land at all.")

print(f"\n  above and left both measure squares that touch X's own row or column.")
print(f"  neither of them can see the INTERIOR of the proposed square -- only the")
print(f"  diagonal neighbour is positioned to. drop it and the recurrence stops")
print(f"  checking the middle.")


# =====================================================================
# 9. AGREEMENT CHECK
# =====================================================================
# Random grids against the brute force, including all-good and all-bad grids and
# long thin shapes, where an off-by-one in the edge handling would show. Every
# located square is re-verified cell by cell -- the area can be right while the
# reported position is wrong.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(17)
trial_count = 3000
area_disagreements = 0
rolling_disagreements = 0
location_disagreements = 0
diagonal_bug_caught = 0

for _ in range(trial_count):
    row_count = random.randint(1, 8)
    column_count = random.randint(1, 8)
    good_chance = random.choice((0.3, 0.6, 0.9, 1.0))
    land = [[1 if random.random() < good_chance else 0
             for _ in range(column_count)] for _ in range(row_count)]

    dp_area, dp_side, dp_table = largest_square(land)
    brute_side, _ = brute_force_largest_square(land)

    if dp_area != brute_side * brute_side:
        area_disagreements += 1
    if largest_square_rolling(land) != dp_area:
        rolling_disagreements += 1

    located = locate_square(dp_table, dp_side)
    if dp_side > 0:
        top_row, left_column, bottom_row, right_column = located
        square_is_good = all(
            land[row][column] == 1
            for row in range(top_row, bottom_row + 1)
            for column in range(left_column, right_column + 1))
        right_shape = (bottom_row - top_row + 1 == dp_side
                       and right_column - left_column + 1 == dp_side)
        if not (square_is_good and right_shape):
            location_disagreements += 1
    elif located is not None:
        location_disagreements += 1

    if largest_square_no_diagonal(land)[0] != dp_area:
        diagonal_bug_caught += 1

print(f"\n{trial_count} random grids, up to 8 x 8, good-land density 0.3 to 1.0\n")
print(f"  dp vs brute force                  {trial_count - area_disagreements}/{trial_count}")
print(f"  rolling row vs full table          {trial_count - rolling_disagreements}/{trial_count}")
print(f"  located square is good and square  {trial_count - location_disagreements}/{trial_count}")
print(f"\n  the no-diagonal version disagreed on {diagonal_bug_caught} of the "
      f"{trial_count} grids")
print(f"  -- it is not a rare bug, it is wrong on roughly "
      f"{100 * diagonal_bug_caught // trial_count}% of random input")


# === How it Runs ===
#
# --- largest_square ---
# side is an n x m table of zeros, filled row by row, left to right. there is no
# separate base case and no edge special-case: a bad cell is skipped, leaving the
# 0 that was already there, and for a good cell any neighbour that is off the
# grid counts as 0, so min(0, ...) + 1 = 1 for the whole top row and left column
# without a branch (this is the video's idiom -- see the docstring)
# every other cell reads exactly three already-final neighbours -- up-left, up,
# left -- all of which row-major order has already visited
# constant work per cell, so O(nm) in total
#
# filling the table for the video's land:
#
#     land                    side[i][j]
#     0 1 1 0 1               0 1 1 0 1
#     1 1 0 1 0               1 1 0 1 0
#     0 1 1 1 0               0 1 1 1 0
#     1 1 1 1 0               1 1 2 2 0
#     1 1 1 1 1               1 2 2 3 1
#     0 0 0 0 0               0 0 0 0 0
#
# row 0 and column 0 just copy the land: nothing bigger than 1 x 1 can end there
# row 3 is where the first 2 appears. at (3,2):
#     land is good; diagonal side[2][1] = 1, above side[2][2] = 1, left side[3][1] = 1
#     1 + min(1, 1, 1) = 2   -- a 2 x 2 square of good land ends at (3,2)
# row 4, cell (4,3) is the answer:
#     diagonal side[3][2] = 2, above side[3][3] = 2, left side[4][2] = 2
#     1 + min(2, 2, 2) = 3   -- a 3 x 3 square ends at (4,3)
#     its top-left is (4-3+1, 3-3+1) = (2, 1), so rows 2-4, columns 1-3:
#         1 1 1
#         1 1 1
#         1 1 1
#     area = 3 * 3 = 9
#
# the very next cell, (4,4), drops straight back to 1 even though its land is
# good: above is side[3][4] = 0, because the land at (3,4) is bad. one 0 in the
# wrong place caps the corner completely. that is what taking the MIN means --
# the most constrained direction decides, and no amount of room elsewhere helps
#
# --- why the answer is a maximum over the whole table ---
# every square has exactly one bottom-right corner, so as the table is filled,
# every possible square of good land is measured exactly once, at its own corner
# there is no separate search: the largest entry in the table IS the answer, and
# the scan for it is folded into the same pass
#
# --- locate_square ---
# no walk-back is needed, unlike the bunny and knight tracebacks. the winning
# cell is the bottom-right corner and it stores the side, so
#     top-left = (row - side + 1, column - side + 1)
# is the whole reconstruction. the recurrence stored enough to invert directly
#
# --- largest_square_rolling ---
# the same thing with two rows instead of n: previous_row for the two upward
# lookups, current_row for the leftward one
# the diagonal is previous_row[column - 1] -- which must be read BEFORE
# current_row[column - 1] overwrites nothing (they are separate lists here, so
# unlike the subset sum row there is no ordering trap)
# O(m) space, and the square can no longer be located, only measured

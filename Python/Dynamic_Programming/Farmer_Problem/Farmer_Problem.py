r"""
THE FARMER PROBLEM  (maximal square of good land)
Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slide 23.

Notes: [[Farmer Problem — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Farmer Problem — Code Notes.md

What is in this file:
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
# Notes: [[Farmer Problem — Code Notes#1. Brute force — every candidate square]] (variables)

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
# Notes: [[Farmer Problem — Code Notes#2. The DP — one number per cell]] (variables, edges, loop order)

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
# Notes: [[Farmer Problem — Code Notes#3. Where the square is]]

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
# Notes: [[Farmer Problem — Code Notes#4. One row instead of the table]] (variables)

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


# Notes: [[Farmer Problem — Code Notes#How it runs]] (the video's land, traced)

# 2D grid: a list of lists, one inner list per row
# Python has no real 2D type; grid[row][column] is two ordinary list lookups

rows = 3
columns = 4

# Building it the safe way: the inner [0] * columns runs again for every row,
# so each row is its own, separate list
grid = [[0] * columns for _ in range(rows)]
# [[0, 0, 0, 0],
#  [0, 0, 0, 0],
#  [0, 0, 0, 0]]

# Reading and writing one square
grid[1][2] = 5  # row 1, column 2
whole_row = grid[1]  # [0, 0, 5, 0], one index gives a whole row
one_square = grid[1][2]  # 5, two indexes give one number
row_count = len(grid)  # 3
column_count = len(grid[0])  # 4, the length of one row

# Visiting every square, in the order P3_3A uses (row by row, left to right)
for row in range(rows):
    for column in range(columns):
        grid[row][column] = row * 10 + column  # each square holds its own coordinates
# [[ 0,  1,  2,  3],
#  [10, 11, 12, 13],
#  [20, 21, 22, 23]]

# Neighbours: check the index exists before you use it
row, column = 0, 0
if column + 1 < columns:
    right_value = grid[row][column + 1]  # 1
if row + 1 < rows:
    below_value = grid[row + 1][column]  # 10
if row - 1 >= 0:
    above_value = grid[row - 1][column]  # never runs: row 0 has nothing above
# Careful: grid[-1] does NOT fail, it quietly wraps round to the last row
last_row = grid[-1]  # [20, 21, 22, 23]

# The trap: [[0] * columns] * rows copies the SAME row object 3 times
shared_grid = [[0] * columns] * rows
shared_grid[0][0] = 1  # change one square...
# ...and every row changes: [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
rows_are_shared = shared_grid[0] is shared_grid[1]  # True
safe_rows_are_shared = grid[0] is grid[1]  # False

# Alternative: one flat list, square (row, column) lives at row * columns + column
flat_grid = [0] * (rows * columns)
flat_grid[1 * columns + 2] = 5  # same square as grid[1][2]
# [0, 0, 0, 0,  0, 0, 5, 0,  0, 0, 0, 0]

# Rows don't have to be the same length; Python won't stop you (a "jagged" grid)
jagged_grid = [[1, 2, 3], [4], [5, 6]]
row_lengths = [len(grid_row) for grid_row in jagged_grid]  # [3, 1, 2]

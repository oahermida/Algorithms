"""
Gas fields
Henk owns a rectangular piece of land to mine gas
Henks land can be divided in n x 3 cells
At most, one mining installation per cell
Each cell also has a number indicating it's potential profit
He is allowed to place as many installations as he wants, under the constraint
that no two installations are in horizontally or vertically adjacent cells.

Goal: Can you help Henk to determine the maximum profit he would make if he places the mining installations in the optimal spots?

variables:
n: the number of rows of henks field
profits (my name): profit value number, organized in n rows of 3 columns

Constraints
    • In each test case, 1 ≤ n ≤ 2 000 000.
    • Profits are nonnegative.
    • In each test case, the sum of profits over all cells does not exceed 2^64 − 1.
    • CPU time limit: 2 seconds per test case.
    • Memory limit: 5 MiB per test case.


placing as many x's as posible is not necesarily the best strat.


for one column:
Array = [50, 3, 1, 50, 9, 8, 7, 1]
tapped = Array[0]
untapped = 0
#following rows:
for i in range(1, len(Array)): #starts at the second row
    tapped_current = untapped + Array[i]
    # If this row isn't tapped, the row above can be either
    if tapped > untapped:
        untapped = tapped
    tapped = tapped_current
best_combo = max(tapped, untapped)

print(best_combo)

"""

# #==== COMMENT B4 SUBMISSION =====
# import sys
# import os

# if sys.stdin.isatty():
#     here = os.path.dirname(os.path.abspath(__file__))
#     sys.stdin = open(os.path.join(here, "5A_Sample.txt"))

# #====================================


# n = int(input())
# mining_field = []
# for i in range(n):
#     row = input().split()
#     for j in range(len(row)):
#         row[j] = int(row[j])
#     mining_field.append(row)    
# print(f"mining_field = {mining_field}")



# none = 0
# left = mining_field[0][0]
# middle = mining_field[0][1]
# right = mining_field[0][2]
# left_right = mining_field[0][0] + mining_field[0][2]



# for i in range(1,len(mining_field)):
#     none_current = 0 + max(left, middle, right, left_right)
#     left_current = mining_field[i][0] + max(none, middle, right)
#     middle_current = mining_field[i][1] + max(none, left, right, left_right)
#     right_current = mining_field[i][2] + max(none, left, middle)
#     left_right_current = mining_field[i][0] + mining_field[i][2] + max(none, middle)
#     none = none_current
#     left = left_current
#     middle = middle_current
#     right = right_current
#     left_right = left_right_current

# best_combo = max(none, left, middle, right, left_right)
# print(best_combo)

n = int(input())

#for three columns a row can take the following valid shapes:
#none        [ ][ ][ ]
#left        [x][ ][ ]
#middle      [ ][x][ ]
#right       [ ][ ][x]
#left_right  [x][ ][x]

none = 0
left = 0
middle = 0
right = 0
left_right = 0

#compatible rows with the row above:
#none: none, left, middle, right, left_right
#left: none, middle, right
#middle: none, left, right, left_right
#right: none, left, middle
#left_right: none, middle

for _ in range(n):
    row = input().split()
    left_cell = int(row[0])
    middle_cell = int(row[1])
    right_cell = int(row[2])

    new_none = max(none, left, middle, right, left_right)
    new_left = left_cell + max(none, middle, right)
    new_middle = middle_cell + max(none, left, right, left_right)
    new_right = right_cell + max(none, left, middle)
    new_left_right = left_cell + right_cell + max(none, middle)

    none = new_none
    left = new_left
    middle = new_middle
    right = new_right
    left_right = new_left_right

print(max(none, left, middle, right, left_right))
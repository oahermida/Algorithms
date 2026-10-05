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


[x][ ][x]    [ 1][  ][ 3]
[ ][x][ ]    [  ][ 5][  ]
[x][ ][x]    [ 7][  ][ 9]
[ ][x][ ]    [  ][11][  ]
[x][ ][x]    [13][  ][15]
             total = 64

[ ][x][ ]    [  ][ 2][  ]
[x][ ][x]    [ 4][  ][ 6]
[ ][x][ ]    [  ][ 8][  ]
[x][ ][x]    [10][  ][12]
[ ][x][ ]    [  ][14][  ]
             total = 56

[x][ ][x]    [ 1][  ][ 3]
[ ][x][ ]    [  ][ 5][  ]
[ ][ ][ ]    [  ][  ][  ]
[ ][ ][x]    [  ][  ][12]
[ ][ ][ ]    [  ][  ][  ]
             total = 21

[x][ ][ ]    [100][  0][  0]
[ ][ ][x]    [  0][  0][100]
[x][ ][ ]    [100][  0][  0]
             answer = 300

[x][ ][x]    [  5][  9][  5]
             answer = 10

[ ][x][ ]    [  5][ 11][  5]
             answer = 11

[ ][x][ ]    [  1][100][  1]
[x][ ][x]    [  1][100][  1]
             answer = 102

[ ][ ][ ]    [  0][  0][  0]
[ ][ ][ ]    [  0][  0][  0]
             answer = 0

[ ][x][ ]    [  0][999][  0]
             answer = 999

what im thinking is that the middle row is still key, at least for comparison.

[x][ ][x]    [ 50][  0][ 50]
[ ][ ][ ]    [  9][  9][  9]
[ ][x][ ]    [  0][ 50][  0]
             answer = 150

this example proves that placing as many x's as posible is not necesarily the best strat.
Profits are never negative, so if a cell's neighbours are all empty, adding an installation there never lowers the
total.

could i consider dividing the field in chunks?
    not really, since those chunks would be arbitrary

this might involve a 3sum if im not mistaken


"""

# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "5A_Sample.txt"))

# #====================================
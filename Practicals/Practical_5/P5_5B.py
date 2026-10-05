"""
Eau De Robinet
Treetown's roads form a binary tree.
Every junction has a cost to place a water tap there
A junction is covered iif it has a tap, or a tap is at most d road segments away
Goal: cover every junction for the minimum total cost

Input:
first line: n (number of layers of the tree) and d
then n lines, one per layer, giving each junction's cost
children of the ith junction on line l are the (2i - 1)th and (2i)th junctions on line l + 1
-1 = no junction there (all its descendants are -1 too; the root is never -1)

Output: the minimum total cost

Constraints
    • In each test case, 1 ≤ n ≤ 20.
    • Normal version: 0 ≤ d ≤ 1.
    • In each test case, the sum of the costs of all junctions is less than 10^18.
    • For each (existing) junction, the cost to place a water tap is nonnegative.
    • CPU time limit: 3 seconds per test case.
    • Memory limit: 2 GiB per test case.

Sample (d = 1):
            [3]
      [4]          [1]
   [-1]  [0]    [7]   [9]
answer = 1   (taps on 0 and 1)

Hard version
    • 2 ≤ d ≤ 10^9 (the only difference from the normal version).
    • 100 test cases: start at 10 points, −1 per failing test.
"""

# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "5B_Sample.txt"))

# #====================================

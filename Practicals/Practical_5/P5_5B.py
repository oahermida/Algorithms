"""
Eau De Robinet
Treetown's roads form a binary tree.
Every junction has a cost to place a water tap there
A junction is covered iff it has a tap, or a tap is at most d road segments away
(distance = number of roads on the path between them, going up and down the tree is both fine)
Goal: cover every junction for the minimum total cost

Input:
first line: n (number of layers) and d
then n lines, one per layer: the tap cost of each junction
children: each junction gets the next pair on the line below
-1: empty spot

variables:
n: number of layers in the tree (= number of cost lines in the input)
d: max number of road segments between a junction and the tap covering it
    in normal: 0 or 1
l: a layer (line) of the tree. root is layer 1, cost[0] in py
i: a junction's position within its layer; 1st junction in the input, index 0 in python
cost (my name): list of layers, cost[l][i] = cost of a tap at junction i on layer l (-1 = no junction)

indexing (0-indexed, python):
children of cost[l][i] are cost[l+1][2*i] and cost[l+1][2*i + 1]
    in english: a junction's 2 children are on the next line, at double its position and the spot after
parent of cost[l][i] is cost[l-1][i // 2]
    in english: a junction's parent is on the line above, at half its position (rounded down)

how the tree works:
The input lists the tree one line (layer) at a time, starting with the root on top. Every junction
has 2 spots for children on the line below, so each line is twice as long as the one above it.
The 1st junction owns the 1st pair below it, the 2nd junction owns the 2nd pair, and so on.
A -1 is an empty spot with no junction; the spots below it are empty too, so they can all be skipped.
Moving down a line doubles your position, moving up a line halves it.

Output: the minimum total cost

Constraints
    • In each test case, 1 ≤ n ≤ 20.
    • Normal version: 0 ≤ d ≤ 1.
    • In each test case, the sum of the costs of all junctions is less than 10^18.
    • For each (existing) junction, the cost to place a water tap is nonnegative.
    • CPU time limit: 3 seconds per test case.
    • Memory limit: 2 GiB per test case.

Sample (d = 1):
3 1
3
4 1
-1 0 7 9

          [3]
     [4]       [1]
  [-1] [0]   [7] [9]

line 0: 3 -> 3 is at position 0
line 1: 4 1 -> 4 is at position 0, 1 is at position 1
line 2: -1 0 7 9 -> -1 is at 0, 0 is at 1, 7 is at 2, 9 is at 3
answer = 1 (taps on 0 and 1: 0 covers 4, 1 covers 3, 7, 9)

Hard version
    • 2 ≤ d ≤ 10^9 (the only difference from the normal version).
    • 100 test cases: start at 10 points, −1 per failing test.    
 
"""

#==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "5B_Sample.txt"))

#====================================

#==== Input =====
nd = input().split()
n = int(nd[0])
d = int(nd[1])

costs = []
for i in range(n):
    layer = input().split()
    for j in range(len(layer)):
        layer[j] = int(layer[j])
    costs.append(layer)
#====================================
print(f"costs = {costs}")

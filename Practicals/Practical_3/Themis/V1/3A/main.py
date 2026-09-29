"""
Context:
    There is a robot playground: an n x m grid.
    A group of antimatter robots starts in the top-left square and moves through the grid
    !only RIGHT or DOWN, one square per step.

variables:
    n: number of rows
    m: number of columns
    k: the number in a square (what it means depends on its sign):
        k > 0: k antimatter robots
        k < 0: |k| normal robots
        k = 0: barrier (can't be entered)
    group: how many antimatter robots are moving together right now

top-left square (start):
    The robots in the top-left square
    they leave one robot behind, and the rest move on.

Entering a square:
    the robots in that square react with the group:
        If antimatter (k > 0), they join the group: group + k
        If normal (k < 0), they annihilate in pairs: group - |k|
            If that is 0 or less, the whole group is done for
            !group + k either way (normal robots are negative)
    *Then*, one robot stays behind and the rest (group - 1) move on to the next square
        The robot left behind stays in that square for the rest of the experiment.
        !it never affects the answer

When it stops:
    * it reaches the bottom-right square (goal)
    * it is annihilated completely
    * exactly 1 robot is left: 
        it has to stay and can't move

Question: 
    the robots pick the best route. 
    What is the maximum number of robots in the bottom-right square?

Input: a line containing n and m, followed by n lines of m numbers (k)
    Example:
        4 4 (n and m )
        10 -3 -2 3
        -6 0 -1 0
        2 -1 1 1
        0 0 3 -1
    Output: 2
    Explanation:
        down-down-right-right-down-right
        [10] - [-6] - [2] - [-1] - [1] - [3] - [-1]
        group: 10, (9-6)=3, (2+2)=4, (3-1)=2, (1+1)=2, (1+3)=4, (3-1)=2

Output: one number

Constraints:
• In each test case:
    * 2 ≤ n, m ≤ 4000
    * -100 000 ≤ k ≤ 100 000
    * the answer is at least 1
    * the top-left square has at least 2 robots
    * the bottom-right square is never a barrier
• CPU time limit: 3 seconds per test case.
• Memory limit: 50 MiB per test case.
"""

# # #==== COMMENT B4 SUBMISSION =====
# import sys
# import os

# if sys.stdin.isatty():
#     here = os.path.dirname(os.path.abspath(__file__))
#     sys.stdin = open(os.path.join(here, "3A_Sample.txt"))

# # #====================================

#==== Input ====
nm = input().split()
n = int(nm[0])
m = int(nm[1])
grid = [None] * n

for row in range(n):
    numbers = input().split()
    grid[row] = [int(number) for number in numbers]

#================

NEGATIVE_INFINITY = float("-inf")

def max_group_at_goal(grid):
    n = len(grid) # number of rows
    m = len(grid[0]) # number of columns

    best_group = [[NEGATIVE_INFINITY] * m for _ in range(n)]
    best_group[0][0] = grid[0][0]

    for row in range(n): #the square above is always done already
        for column in range(m): #the square to the left is always done already
            if row == 0 and column == 0: # start square
                continue 

            best_arriving = NEGATIVE_INFINITY
            if row - 1 >= 0 and best_group[row - 1][column] >= 2: # above exists and can send
                best_arriving = max(best_arriving, best_group[row - 1][column] - 1) # one stays behind
            if column - 1 >= 0 and best_group[row][column - 1] >= 2: # left exists and can send
                best_arriving = max(best_arriving, best_group[row][column - 1] - 1) # one stays behind

            if grid[row][column] == 0: # barrier
                best_group[row][column] = 0
            else: # meets square's robots
                best_group[row][column] = grid[row][column] + best_arriving # join (k > 0) or annihilate (k < 0)

    return best_group[n - 1][m - 1], best_group


#==== Output ====
answer, best_group_table = max_group_at_goal(grid)
# print(best_group_table)
print(answer)

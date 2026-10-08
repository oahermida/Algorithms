"""
Eau De Robinet
Treetown's roads form a binary tree.
Every junction has a cost to place a water tap there
A junction is covered iff it has a tap, or a tap is at most d road segments away
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
i: a junction's position within its layer
cost (my name): list of layers, cost[l][i] = cost of a tap at junction i on layer l (-1 = no junction)

how the tree works:
The input lists the tree one line (layer) at a time, starting with the root on top. Every junction
has 2 spots for children on the line below, so each line is twice as long as the one above it
The 1st junction owns the 1st pair below it, the 2nd junction owns the 2nd pair, and so on.
A -1 is an empty spot with no junction; the spots below it are empty too, so they can all be skipped.
moving down a line doubles your position, moving up a line halves it.

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

answer = 1 (taps on 0 and 1: 0 covers 4, 1 covers 3, 7, 9)

Hard version
    • 2 ≤ d ≤ 10^9 (the only difference from the normal version).
    • 100 test cases: start at 10 points, −1 per failing test.    

    

"""

# #==== COMMENT B4 SUBMISSION =====
# import sys
# import os

# if sys.stdin.isatty():
#     here = os.path.dirname(os.path.abspath(__file__))
#     sys.stdin = open(os.path.join(here, "5B_Sample.txt"))

# #====================================

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
# print(f"costs = {costs}")
final_cost = 0
# d=0
"""
d = 0: a tap covers only its own junction, so every junction needs its own tap.
the answer is just the sum of all costs, skipping the -1s

d = 1: a tap covers its own junction plus its neighbours

if cost(parent) <= cost(leaf)1 + cost(leaf)2 never put a tap on a leaf.
a bottom-up approach is probably best, dividing it in subtrees
compare which child is the cheapest
then compare with it's parent
if cost(parent) <= cost(leaf)1 + cost(leaf)2 never put a tap on a leaf.

Compare two leafs with their parent
if sum two leafs >= to parent:
    never put one on the leafs
    in which case you have to put one on the parent

this sort of creates a new floor
                         A[10]
            B[8]                           C[1]
      D[5]           E[9]           [-1]            F[7]
  G[3]    H[3]    [-1]   I[4]    [-1]    [-1]   J[2]    K[6]
you have to put one in D[5], which means that then B[8] is already covered
then youd check the other leaf pairs
at the end J[2]+K[6]>F[7], same treatment
this means that B[8] is already covered, and that I[4] has to get one
A[10] also needs one
A[10] kinda also always sets the flow entirely
it becomes a binary problem of root covered or root used

what if per node i store: cost if used, cost if covered AND cost if unexposed
    used(v) = cost(v) + min(used(L), covered(L), unexposed(L)) + min(used(R), covered(R), unexposed(R))
    unexposed(v) = covered(L) + covered(R)
    covered(v) = min(used(L), covered(L)) + min(used(R), covered(R)) + min( used(L) − min(used(L), covered(L)), used(R) − min(used(R), covered(R)) )

Leaf: used= cost, covered= ∞, unexposed= 0
One child is -1: drop every term for that child
answer: at the root, the min(used, covered)
root.used = cost(root) + for each existing child c: min(c.used, c.covered, c.unexposed) which also includes every decendant
root.covered = for each existing child c: min(c.used, c.covered) + the smallest (c.used - min(c.used, c.covered)) over the children, which forces at least one child to tap

"""
if d == 0:
    for row in costs:
        for c in row:
            if c != -1:
                final_cost += c
    print(final_cost)
else:
    class Junction:
        def __init__(self, used, covered, unexposed):
            self.used = used
            self.covered = covered
            self.unexposed = unexposed

    INF = float("inf") # impossible
    below = None

    #going through the levels from the bottom up
    for l in range(n-1, -1, -1): #start, stop, step
        current = [] # the current layer's junctions

        # going through the junctions in the current layer
        for i in range(len(costs[l])):
            cost = costs[l][i] # tap cost of this junction
            if cost == -1: #if the junction doesn't exist, add a None to current
                current.append(None)
                continue
            children = [] # the existing children of this junction
            if below is not None: #if there is a layer below the current one
                left_child = below[2*i]
                right_child = below[2*i + 1]
                if left_child is not None: # skip -1 spots
                    children.append(left_child)
                if right_child is not None:
                    children.append(right_child)
            if not children: #leaf threfore cant be covered by a child
                current.append(Junction(cost, INF, 0)) #used = cost, covered impossible, unexposed free
                continue
            else: #internal junction so combine the childrens values
                #calculate the used, covered, and unexposed costs for the current junction
                used = cost
                unexposed = 0
                covered = 0
                extra = INF
                for child in children: # add each child's contribution
                    used += min(child.used, child.covered, child.unexposed) #tap covers the child
                    unexposed += child.covered # no tap here, so the child must be covered by its own children
                    best = min(child.used, child.covered) # cheapest state where the child is covered
                    covered += best
                    extra = min(extra, child.used - best) # cheapest price of forcing one child to tap
                covered += extra # make sure at least one child has a tap
                current.append(Junction(used, covered, unexposed)) # store this junction's values
        below = current # current becomes the layer below the current one
    root = below[0] #layer 0 has only the root
    print(min(root.used, root.covered)) # unexposed isn't allowed


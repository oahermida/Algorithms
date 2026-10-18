"""
7A — Treasure collector
Aron is in the Marvelous Mud Maze: n mud rooms connected by m one-way mud tunnels.
He enters through a one-way door into room 1 and can only leave through the exit door in room n.

Room i holds r(i) hidden treasures, tunnel j holds t(j) hidden treasures.
Visiting a room or going through a tunnel collects all its treasures, but each treasure can only be collected once.
Rooms and tunnels may be visited as often as he likes,
but it all has to happen in a single run that starts in room 1 and ends in room n.

Input:
first line: n (number of rooms) and m (number of tunnels)
then n lines, one per room: r
    r: the treasures in that room
then m lines, one per tunnel: a b t
    a: the room the tunnel starts in
    b: the room the tunnel leads to
    t: the treasures in that tunnel

Goal: collect as many treasures as possible on one route from room 1 to room n
Output: the maximum number of treasures, or IMPOSSIBLE if room n can't be reached from room 1
    the graph may be disconnected


Constraints
    • In all test cases, 0 ≤ n ≤ 200 000 and 0 ≤ m ≤ 1 000 000.
    • The amount of hidden treasures in any room or tunnel is nonnegative.
    • The total amount of hidden treasures in the maze does not exceed 2^31 − 1.
    • CPU time limit: 2 seconds per test case.
    • Memory limit: 256 MiB per test case.
"""
# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "7A_Sample.txt"))

# #====================================

#==== Input =====
nm = input().split()
n = int(nm[0])
m = int(nm[1])

rooms = []
for i in range(n):
    rooms.append(int(input()))

tunnels = []
for j in range(m):
    tunnel = input().split()
    for k in range(len(tunnel)):
        tunnel[k] = int(tunnel[k])
    tunnels.append(tunnel)
#====================================

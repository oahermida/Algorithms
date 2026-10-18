r"""
DINIC'S ALGORITHM -- BLOCKING FLOWS ON A LEVEL GRAPH
Not in CLRS. Dinitz (1970); Erickson, Algorithms, ch. 10 notes; any
competitive-programming reference. O(V^2 E).

What is in this file:
    1. the residual network, as one capacity matrix
    2. build_levels           BFS gives every vertex its distance from s
    3. blocking_flow          DFS that only steps one level down, many paths per phase
    4. run it on CLRS Figure 26.1 (max flow 23), phase by phase
    5. agreement check against a brute-force minimum cut

Run with:
    python3 Dinic.py
"""

import random
import sys
from collections import deque

sys.setrecursionlimit(10000)


# =====================================================================
# 1. THE RESIDUAL NETWORK
# =====================================================================
# residual[u][v] is how much more can still go from u to v: the spare
# capacity on u->v plus the flow on v->u that could be undone.

def build_residual(vertex_count, edges):
    residual = [[0] * vertex_count for _ in range(vertex_count)]
    for start, end, capacity in edges:
        residual[start][end] += capacity
    return residual


# =====================================================================
# 2. LEVELS -- one BFS per phase
# =====================================================================
# level[v] is the fewest arrows from the source to v in the residual
# network. Only arrows from level i to level i + 1 are used this phase:
# those are exactly the arrows on shortest paths.

def build_levels(residual, source):
    vertex_count = len(residual)
    level = [-1] * vertex_count
    level[source] = 0
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbour in range(vertex_count):
            if level[neighbour] == -1 and residual[vertex][neighbour] > 0:
                level[neighbour] = level[vertex] + 1
                queue.append(neighbour)
    return level


# =====================================================================
# 3. BLOCKING FLOW -- many shortest paths per phase
# =====================================================================
# next_neighbour[v] remembers which neighbour v should try next. A
# neighbour that led nowhere is never tried again in this phase, which is
# what keeps a phase at O(VE). The phase ends when no shortest path is
# left; the next BFS then finds strictly longer ones.

def push_down(residual, level, next_neighbour, vertex, sink, limit):
    if vertex == sink:
        return limit
    vertex_count = len(residual)
    while next_neighbour[vertex] < vertex_count:
        neighbour = next_neighbour[vertex]
        if residual[vertex][neighbour] > 0 and level[neighbour] == level[vertex] + 1:
            sent = push_down(residual, level, next_neighbour, neighbour, sink,
                             min(limit, residual[vertex][neighbour]))
            if sent > 0:
                residual[vertex][neighbour] -= sent
                residual[neighbour][vertex] += sent
                return sent
        next_neighbour[vertex] += 1  # dead end or full: skip it for the rest of the phase
    return 0


def dinic(vertex_count, edges, source, sink, log=None):
    residual = build_residual(vertex_count, edges)
    total_flow = 0
    while True:
        level = build_levels(residual, source)
        if level[sink] == -1:
            break
        next_neighbour = [0] * vertex_count
        phase_flow = 0
        phase_paths = 0
        while True:
            sent = push_down(residual, level, next_neighbour, source, sink, float("inf"))
            if sent == 0:
                break
            phase_flow += sent
            phase_paths += 1
        total_flow += phase_flow
        if log is not None:
            log.append((level[sink], phase_paths, phase_flow, total_flow))
    return total_flow


# =====================================================================
# 4. RUN IT -- CLRS Figure 26.1 (p. 710)
# =====================================================================

FIGURE_26_1_EDGES = [(0, 1, 16), (0, 2, 13), (2, 1, 4), (1, 3, 12), (3, 2, 9),
                     (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]

print("=" * 78)
print("DINIC   -- CLRS Figure 26.1 network")
print("=" * 78)

log = []
total_flow = dinic(6, FIGURE_26_1_EDGES, 0, 5, log=log)
for phase, (distance, phase_paths, phase_flow, running_total) in enumerate(log, start=1):
    print(f"  phase {phase}: shortest paths have {distance} arrows, "
          f"{phase_paths} path{'s' if phase_paths > 1 else ''} carrying {phase_flow:>2}   |f| = {running_total}")
print(f"\n  maximum flow = {total_flow} after {len(log)} phases (CLRS says 23)")
print("  each phase is one BFS; Edmonds-Karp would spend one BFS per path instead")


# =====================================================================
# 5. AGREEMENT CHECK -- against a brute-force minimum cut
# =====================================================================

def brute_force_min_cut(vertex_count, edges, source, sink):
    others = [vertex for vertex in range(vertex_count) if vertex not in (source, sink)]
    best = None
    for mask in range(1 << len(others)):
        source_side = {source} | {others[bit] for bit in range(len(others)) if mask >> bit & 1}
        cut = sum(capacity for start, end, capacity in edges
                  if start in source_side and end not in source_side)
        best = cut if best is None else min(best, cut)
    return best


def random_network(rng):
    vertex_count = rng.randint(2, 8)
    edges = []
    for start in range(vertex_count):
        for end in range(vertex_count):
            if start != end and rng.random() < 0.35:
                edges.append((start, end, rng.randint(1, 10)))
    return vertex_count, edges


print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

rng = random.Random(26)
trial_count = 3000
agreements = 0
for _ in range(trial_count):
    vertex_count, edges = random_network(rng)
    if dinic(vertex_count, edges, 0, vertex_count - 1) == brute_force_min_cut(vertex_count, edges, 0, vertex_count - 1):
        agreements += 1

print(f"\n  {trial_count} random networks, 2-8 vertices, roads both ways allowed")
print(f"  dinic vs brute-force min cut   {agreements}/{trial_count}")

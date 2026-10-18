r"""
PUSH-RELABEL -- MAXIMUM FLOW WITHOUT AUGMENTING PATHS
CLRS 3rd ed., 26.4, pp. 736-747 (GENERIC-PUSH-RELABEL, p. 741).
Active vertices are taken first in, first out, which gives O(V^3).

What is in this file:
    1. the residual network, as one capacity matrix
    2. push and relabel       the two basic operations [pp. 739-740]
    3. push_relabel           the preflow, then work until no vertex overflows
    4. run it on CLRS Figure 26.1 (max flow 23), with operation counts
    5. agreement check against a brute-force minimum cut

Run with:
    python3 Push_Relabel.py
"""

import random
from collections import deque


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
# 2. PUSH AND RELABEL [pp. 739-740]
# =====================================================================
# excess[u] is flow that has arrived at u but not left yet (a preflow may
# break conservation for a while). height[u] says which way water runs:
# u may only push to a neighbour exactly one level lower.

def push(residual, excess, start, end):
    amount = min(excess[start], residual[start][end])
    residual[start][end] -= amount
    residual[end][start] += amount
    excess[start] -= amount
    excess[end] += amount
    return amount


def relabel(residual, height, vertex):
    lowest = min(height[neighbour] for neighbour in range(len(residual))
                 if residual[vertex][neighbour] > 0)
    height[vertex] = lowest + 1  # just high enough to push to the lowest neighbour with room


# =====================================================================
# 3. PUSH-RELABEL [GENERIC-PUSH-RELABEL, p. 741]
# =====================================================================
# Start: the source sits at height V and floods every arrow leaving it.
# Then any overflowing vertex either pushes downhill or, if it can't,
# rises. Flow that can't reach the sink climbs above V and runs back to
# the source. When nothing overflows, the preflow is a maximum flow.

def push_relabel(vertex_count, edges, source, sink, counts=None):
    residual = build_residual(vertex_count, edges)
    height = [0] * vertex_count
    excess = [0] * vertex_count
    height[source] = vertex_count

    active = deque()
    for neighbour in range(vertex_count):  # INITIALIZE-PREFLOW [p. 740]
        if residual[source][neighbour] > 0:
            excess[source] += residual[source][neighbour]
            push(residual, excess, source, neighbour)
            if neighbour != sink:
                active.append(neighbour)

    push_count = relabel_count = 0
    while active:
        vertex = active.popleft()
        while excess[vertex] > 0:  # discharge it completely before moving on
            pushed = False
            for neighbour in range(vertex_count):
                if residual[vertex][neighbour] > 0 and height[vertex] == height[neighbour] + 1:
                    was_idle = excess[neighbour] == 0
                    push(residual, excess, vertex, neighbour)
                    push_count += 1
                    if was_idle and neighbour not in (source, sink):
                        active.append(neighbour)
                    pushed = True
                    if excess[vertex] == 0:
                        break
            if not pushed:
                relabel(residual, height, vertex)
                relabel_count += 1

    if counts is not None:
        counts.update(pushes=push_count, relabels=relabel_count, heights=height)
    return excess[sink]


# =====================================================================
# 4. RUN IT -- CLRS Figure 26.1 (p. 710)
# =====================================================================

FIGURE_26_1_NAMES = ["s", "v1", "v2", "v3", "v4", "t"]
FIGURE_26_1_EDGES = [(0, 1, 16), (0, 2, 13), (2, 1, 4), (1, 3, 12), (3, 2, 9),
                     (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]

print("=" * 78)
print("PUSH-RELABEL   -- CLRS 26.4, Figure 26.1 network")
print("=" * 78)

counts = {}
total_flow = push_relabel(6, FIGURE_26_1_EDGES, 0, 5, counts=counts)
print(f"\n  maximum flow = {total_flow} (CLRS says 23)")
print(f"  {counts['pushes']} pushes, {counts['relabels']} relabels, no augmenting paths at all")
print("  final heights: " + ", ".join(f"{name} {height}" for name, height
                                       in zip(FIGURE_26_1_NAMES, counts["heights"])))
print("  the sink stays at 0 and the source at V = 6; a vertex above 6 sent flow back")


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
    if push_relabel(vertex_count, edges, 0, vertex_count - 1) == brute_force_min_cut(vertex_count, edges, 0, vertex_count - 1):
        agreements += 1

print(f"\n  {trial_count} random networks, 2-8 vertices, roads both ways allowed")
print(f"  push-relabel vs brute-force min cut   {agreements}/{trial_count}")

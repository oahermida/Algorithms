r"""
EDMONDS-KARP -- FORD-FULKERSON WITH SHORTEST AUGMENTING PATHS
CLRS 3rd ed., 26.2, "The Edmonds-Karp algorithm", pp. 727-730.

What is in this file:
    1. the residual network, as one capacity matrix
    2. edmonds_karp           augmenting paths found by breadth-first search
    3. run it on CLRS Figure 26.1 (max flow 23), path by path
    4. path lengths never shrink (Lemma 26.7), shown on a random network
    5. the minimum cut, read off the last search
    6. agreement check against a brute-force minimum cut

Run with:
    python3 Edmonds_Karp.py
"""

import random
from collections import deque


# =====================================================================
# 1. THE RESIDUAL NETWORK [26.2, p. 715]
# =====================================================================
# residual[u][v] is how much more can still go from u to v: the spare
# capacity on u->v plus the flow on v->u that could be undone.

def build_residual(vertex_count, edges):
    residual = [[0] * vertex_count for _ in range(vertex_count)]
    for start, end, capacity in edges:
        residual[start][end] += capacity
    return residual


# =====================================================================
# 2. EDMONDS-KARP [p. 727]
# =====================================================================
# Breadth-first search reaches every vertex by the fewest arrows, so the
# path it hands back is a shortest one. parent[v] is v's slip: the vertex
# the search arrived from. The search stops as soon as the sink has one.

def find_path_bfs(residual, source, sink):
    vertex_count = len(residual)
    parent = [None] * vertex_count
    parent[source] = source
    queue = deque([source])
    while queue and parent[sink] is None:
        vertex = queue.popleft()
        for neighbour in range(vertex_count):
            if parent[neighbour] is None and residual[vertex][neighbour] > 0:
                parent[neighbour] = vertex
                queue.append(neighbour)
    if parent[sink] is None:
        return None, parent
    path = [sink]
    while path[-1] != source:
        path.append(parent[path[-1]])
    return path[::-1], parent


def edmonds_karp(vertex_count, edges, source, sink, log=None):
    residual = build_residual(vertex_count, edges)
    total_flow = 0
    while True:
        path, parent = find_path_bfs(residual, source, sink)
        if path is None:
            break
        bottleneck = min(residual[start][end] for start, end in zip(path, path[1:]))
        for start, end in zip(path, path[1:]):
            residual[start][end] -= bottleneck
            residual[end][start] += bottleneck
        total_flow += bottleneck
        if log is not None:
            log.append((path, bottleneck, total_flow))
    reached = [vertex for vertex in range(vertex_count) if parent[vertex] is not None]
    return total_flow, reached


# =====================================================================
# 3. RUN IT -- CLRS Figure 26.1 (p. 710)
# =====================================================================

FIGURE_26_1_NAMES = ["s", "v1", "v2", "v3", "v4", "t"]
FIGURE_26_1_EDGES = [(0, 1, 16), (0, 2, 13), (2, 1, 4), (1, 3, 12), (3, 2, 9),
                     (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]

print("=" * 78)
print("EDMONDS-KARP   -- CLRS 26.2, Figure 26.1 network")
print("=" * 78)

log = []
total_flow, reached = edmonds_karp(6, FIGURE_26_1_EDGES, 0, 5, log=log)
for round_number, (path, bottleneck, running_total) in enumerate(log, start=1):
    route = " -> ".join(FIGURE_26_1_NAMES[vertex] for vertex in path)
    print(f"  path {round_number}: {route:<28} {len(path) - 1} arrows, carries {bottleneck:>2}   |f| = {running_total}")
print(f"\n  maximum flow = {total_flow} after {len(log)} paths (CLRS says 23)")


# =====================================================================
# 4. PATH LENGTHS NEVER SHRINK [Lemma 26.7, p. 727]
# =====================================================================
# Each round fills at least one arrow on a shortest path, and with BFS the
# shortest path length can only stay the same or grow. That is what caps
# the rounds at O(VE) whatever the capacities (Theorem 26.8, p. 729), and
# the whole algorithm at O(VE^2).

print("\n" + "=" * 78)
print("PATH LENGTHS, ONE RANDOM 30-VERTEX NETWORK")
print("=" * 78)

rng = random.Random(7)
big_edges = [(start, end, rng.randint(1, 1000)) for start in range(30) for end in range(30)
             if start != end and rng.random() < 0.15]
big_log = []
big_flow, _ = edmonds_karp(30, big_edges, 0, 29, log=big_log)
lengths = [len(path) - 1 for path, _, _ in big_log]
print(f"\n  {len(lengths)} paths, lengths in order: {lengths}")
print(f"  never shorter than the one before: {all(a <= b for a, b in zip(lengths, lengths[1:]))}")
print(f"  maximum flow = {big_flow}")


# =====================================================================
# 5. THE MINIMUM CUT, FOR FREE [Theorem 26.6, p. 723]
# =====================================================================
# The last search fails to reach the sink. The vertices it did reach are
# one side of a minimum cut, and the arrows leaving that side are all full.

print("\n" + "=" * 78)
print("THE MINIMUM CUT, FIGURE 26.1")
print("=" * 78)

crossing = [(start, end, capacity) for start, end, capacity in FIGURE_26_1_EDGES
            if start in reached and end not in reached]
print(f"\n  reached by the last search: {[FIGURE_26_1_NAMES[vertex] for vertex in reached]}")
for start, end, capacity in crossing:
    print(f"  crossing arrow {FIGURE_26_1_NAMES[start]} -> {FIGURE_26_1_NAMES[end]}  capacity {capacity}")
print(f"  cut capacity = {sum(capacity for _, _, capacity in crossing)} = maximum flow {total_flow}")


# =====================================================================
# 6. AGREEMENT CHECK -- against a brute-force minimum cut
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
    flow, _ = edmonds_karp(vertex_count, edges, 0, vertex_count - 1)
    if flow == brute_force_min_cut(vertex_count, edges, 0, vertex_count - 1):
        agreements += 1

print(f"\n  {trial_count} random networks, 2-8 vertices, roads both ways allowed")
print(f"  edmonds-karp vs brute-force min cut   {agreements}/{trial_count}")

r"""
FORD-FULKERSON -- MAXIMUM FLOW BY ANY AUGMENTING PATH
CLRS 3rd ed., 26.2, pp. 714-731 (FORD-FULKERSON, p. 724).

What is in this file:
    1. the residual network, as one capacity matrix
    2. ford_fulkerson         augmenting paths found by depth-first search
    3. run it on CLRS Figure 26.1 (max flow 23), path by path
    4. the trap of CLRS Figure 26.7: the worst path choices take 2000 rounds
    5. agreement check against a brute-force minimum cut

Run with:
    python3 Ford_Fulkerson.py
"""

import itertools
import random
import sys

sys.setrecursionlimit(10000)


# =====================================================================
# 1. THE RESIDUAL NETWORK [26.2, p. 715]
# =====================================================================
# residual[u][v] is how much more can still go from u to v: the spare
# capacity on u->v plus the flow on v->u that could be undone. Sending x
# along u->v takes x off residual[u][v] and adds x to residual[v][u].
# Two roads in opposite directions just share the two cells.

def build_residual(vertex_count, edges):
    residual = [[0] * vertex_count for _ in range(vertex_count)]
    for start, end, capacity in edges:
        residual[start][end] += capacity
    return residual


def send(residual, path, amount):
    for start, end in zip(path, path[1:]):
        residual[start][end] -= amount
        residual[end][start] += amount


# =====================================================================
# 2. FORD-FULKERSON WITH DEPTH-FIRST SEARCH [p. 724]
# =====================================================================

def find_path_dfs(residual, source, sink):
    vertex_count = len(residual)
    visited = [False] * vertex_count

    def explore(vertex, path):
        if vertex == sink:
            return path
        visited[vertex] = True
        for neighbour in range(vertex_count):
            if not visited[neighbour] and residual[vertex][neighbour] > 0:
                found = explore(neighbour, path + [neighbour])
                if found:
                    return found
        return None

    return explore(source, [source])


def ford_fulkerson(vertex_count, edges, source, sink, find_path=find_path_dfs, log=None):
    residual = build_residual(vertex_count, edges)
    total_flow = 0
    path_count = 0
    while True:
        path = find_path(residual, source, sink)
        if path is None:
            break
        bottleneck = min(residual[start][end] for start, end in zip(path, path[1:]))
        send(residual, path, bottleneck)
        total_flow += bottleneck
        path_count += 1
        if log is not None:
            log.append((path, bottleneck, total_flow))
    return total_flow, path_count


# =====================================================================
# 3. RUN IT -- CLRS Figure 26.1 (p. 710)
# =====================================================================

FIGURE_26_1_NAMES = ["s", "v1", "v2", "v3", "v4", "t"]
FIGURE_26_1_EDGES = [(0, 1, 16), (0, 2, 13), (2, 1, 4), (1, 3, 12), (3, 2, 9),
                     (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]

print("=" * 78)
print("FORD-FULKERSON   -- CLRS 26.2, Figure 26.1 network")
print("=" * 78)

log = []
total_flow, path_count = ford_fulkerson(6, FIGURE_26_1_EDGES, 0, 5, log=log)
for round_number, (path, bottleneck, running_total) in enumerate(log, start=1):
    route = " -> ".join(FIGURE_26_1_NAMES[vertex] for vertex in path)
    print(f"  path {round_number}: {route:<34} carries {bottleneck:>2}   |f| = {running_total}")
print(f"\n  maximum flow = {total_flow} after {path_count} paths (CLRS says 23)")


# =====================================================================
# 4. THE TRAP -- CLRS Figure 26.7 (p. 726)
# =====================================================================
# Ford-Fulkerson only says "any path with room". Here a path finder that
# always picks the path with the SMALLEST bottleneck keeps going through the
# middle arrow u->v (capacity 1), forwards and then backwards, adding 1 per
# round. CLRS uses a million; 1000 keeps the run short. Plain DFS happens
# not to fall into it on this graph, which is why the chooser is explicit.

def find_path_worst(residual, source, sink):
    vertex_count = len(residual)
    middle = [vertex for vertex in range(vertex_count) if vertex not in (source, sink)]
    worst_path, worst_bottleneck = None, None
    for length in range(len(middle) + 1):
        for inner in itertools.permutations(middle, length):
            path = [source, *inner, sink]
            bottleneck = min(residual[start][end] for start, end in zip(path, path[1:]))
            if bottleneck > 0 and (worst_bottleneck is None or bottleneck < worst_bottleneck):
                worst_path, worst_bottleneck = path, bottleneck
    return worst_path


TRAP_EDGES = [(0, 1, 1000), (0, 2, 1000), (1, 2, 1), (1, 3, 1000), (2, 3, 1000)]  # s u v t

print("\n" + "=" * 78)
print("THE TRAP   -- CLRS Figure 26.7, capacities 1000 and a middle arrow of 1")
print("=" * 78)

worst_flow, worst_paths = ford_fulkerson(4, TRAP_EDGES, 0, 3, find_path=find_path_worst)
dfs_flow, dfs_paths = ford_fulkerson(4, TRAP_EDGES, 0, 3)
print(f"\n  worst path choices:  |f| = {worst_flow} after {worst_paths} paths")
print(f"  depth-first search:  |f| = {dfs_flow} after {dfs_paths} paths")
print("\n  same answer, but the number of rounds is only bounded by |f*| itself:")
print("  O(E |f*|). Edmonds-Karp removes that dependence on the capacities.")


# =====================================================================
# 5. AGREEMENT CHECK -- against a brute-force minimum cut
# =====================================================================
# Max-flow min-cut (Theorem 26.6, p. 723): the maximum flow equals the
# smallest total capacity of arrows leaving any set that holds the source
# but not the sink. Trying every such set is slow but certainly right.

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
    flow, _ = ford_fulkerson(vertex_count, edges, 0, vertex_count - 1)
    if flow == brute_force_min_cut(vertex_count, edges, 0, vertex_count - 1):
        agreements += 1

print(f"\n  {trial_count} random networks, 2-8 vertices, roads both ways allowed")
print(f"  ford-fulkerson vs brute-force min cut   {agreements}/{trial_count}")

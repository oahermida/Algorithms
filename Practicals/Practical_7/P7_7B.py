"""
7B — Smooth criminal
There are n locations connected by m oneway roads. k of the locations have a police office.
Road i can carry at most f(i) vehicles per minute.
crime commited at location l, so the police must go there.
Every police office has an infinite supply of officers, and there is no other traffic,
so the police can use the full capacity of every road

Input:
first line: n (number of locations), m (number of roads), k (number of police offices), l (the crime location)
then m lines, one per road: a b f
    a: the location the road starts at
    b: the location the road leads to (a != b)
    f: the road's capacity in vehicles per minute
    between any two locations there is at most one road in each direction
then k lines, one per police office: the location it is at
    all distinct, none of them is l

Goal: send as many police vehicles per minute as possible from all k offices to location l
Output: the maximum number of police vehicles arriving at l per minute, or 0 if l can't be reached from any office

Constraints
    • In all test cases, 1 ≤ n ≤ 300 and 1 ≤ m ≤ 500.
    • Every road's capacity is a positive integer, at most 1000.
    • The roadmap need not be planar, and may not be connected.
    • CPU time limit: 2 seconds per test case.
    • Memory limit: 256 MiB per test case.
"""
# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "7B_Sample.txt"))

# #====================================

#==== Input =====
nmkl = input().split()
n = int(nmkl[0])
m = int(nmkl[1])
k = int(nmkl[2])
l = int(nmkl[3])

roads = []
for i in range(m):
    road = input().split()
    for j in range(len(road)):
        road[j] = int(road[j])
    roads.append(road)

offices = []
for i in range(k):
    offices.append(int(input()))
supersouce_i = 0

INF = float('inf')
for office in offices:
    roads.append((supersouce_i, office, INF))
#====================================
"""
First thought is that this is kinda like ford-fulkerson
but that one only works with one source
so you either have to figure out a way to work with more than one sources
or merge them

CLRS chp 26:
Several sources are no harder than ordinary max flow
merge them by adding one new vertex
the supersource s, with an arrow of capacity INF from s to every original source.
s supplies as much flow as any source needs

Then run any normal one-source max-flow algorithm from s.

the k police offices are the sources, l is the only sink

"""
vertex_count = n + 1 #supersource

def build_residual(vertex_count, edges):
    residual = [[0] * vertex_count for _ in range(vertex_count)]
    for start, end, capacity in edges:
        residual[start][end] += capacity
    return residual


def send(residual, path, amount):
    for start, end in zip(path, path[1:]):
        residual[start][end] -= amount
        residual[end][start] += amount


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


def ford_fulkerson(vertex_count, edges, source, sink, find_path=find_path_dfs):
    residual = build_residual(vertex_count, edges)
    total_flow = 0
    while True:
        path = find_path(residual, source, sink)
        if path is None:
            break
        bottleneck = min(residual[start][end] for start, end in zip(path, path[1:]))
        send(residual, path, bottleneck)
        total_flow += bottleneck
    return total_flow
print(ford_fulkerson(vertex_count, roads, supersouce_i, l))
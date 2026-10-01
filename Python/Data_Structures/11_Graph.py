# Graph: points (vertices) joined by lines (edges)
# Two usual ways to store one: an adjacency list or an adjacency matrix

# The graph used below (undirected):  A - B, A - C, B - D, C - D
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]

# 1. Adjacency list: dict from each vertex to a list of its neighbours
# Memory grows with the number of edges; best for sparse graphs
adjacency_list = {}
for start, end in edges:
    adjacency_list.setdefault(start, []).append(end)
    adjacency_list.setdefault(end, []).append(start)  # undirected: add both ways
# {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C"]}
neighbours_of_a = adjacency_list["A"]  # ["B", "C"]

# 2. Adjacency matrix: a 2D grid, matrix[i][j] = 1 if there's an edge i - j
# Memory is vertices x vertices; "is there an edge?" is one lookup
vertices = ["A", "B", "C", "D"]
index_of = {vertex: position for position, vertex in enumerate(vertices)}
matrix = [[0] * len(vertices) for _ in vertices]
for start, end in edges:
    matrix[index_of[start]][index_of[end]] = 1
    matrix[index_of[end]][index_of[start]] = 1
#     A  B  C  D
# A [[0, 1, 1, 0],
# B  [1, 0, 0, 1],
# C  [1, 0, 0, 1],
# D  [0, 1, 1, 0]]
edge_a_d = matrix[index_of["A"]][index_of["D"]] == 1  # False

# Weighted graph: store (neighbour, weight) pairs instead of just neighbours
weighted = {"A": [("B", 4), ("C", 1)], "B": [("D", 2)], "C": [("D", 5)], "D": []}
total_weight = 0
for vertex, neighbours in weighted.items():
    for neighbour, weight in neighbours:
        total_weight += weight  # 12

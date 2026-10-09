"""
Brocode explains: https://youtu.be/8mJ-OhcfpYg?si=wlil__dRIytyT5uO
"""

A = [5, 2, 4, 6, 1, 3]
n = len(A)

for j in range(1, n):
    key = A[j]
    i = j - 1
    while i >= 0 and A[i] > key:
        A[i + 1] = A[i]
        i -= 1
    A[i + 1] = key


# === How it Runs ===
# Notes: [[Insert Sort — Code Notes#How it runs]] (outer and inner loop, traps, trace)

print(A)

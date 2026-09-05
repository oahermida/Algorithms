# Insertion sort.
#
# Invariant: at the top of each pass, A[0 .. j-1] is already sorted.
#
# j   - index of the element being inserted; runs from 1 (index 0 is a
#       sorted prefix of one) to the end of the list.
# key - a copy of A[j], saved because the shifting below overwrites slot j.
# i   - scans leftward from j-1 through the sorted prefix, shifting each
#       element greater than key one slot right, and stopping at the first
#       element that isn't greater (or at i = -1, past the front).
#
# key then lands at A[i + 1], the gap the shifting opened, which extends the
# sorted prefix to A[0 .. j].
#
# insert_sort_traced.py in this directory is this same program with print
# statements added, for watching it run. Edit this file, not that one.

A = [5, 2, 4, 6, 1, 3]
n = len(A)

for j in range(1, n):
    key = A[j]
    i = j - 1
    while i >= 0 and A[i] > key:
        A[i + 1] = A[i]
        i -= 1
    A[i + 1] = key

print(A)

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
# --- the outer loop ---
# j walks from 1 to n-1. it starts at 1 and NOT 0, because A[0:1] is a single element and is therefore already sorted (same idea as merge sort's len(A) <= 1)
# at the start of every pass A[0:j] is ALREADY SORTED and holds the first j elements. that region grows by one each pass - this is the loop invariant
# key = A[j] is the element being placed. it MUST be saved before any shifting, because line 8 overwrites A[j] on the very first shift
# i = j - 1 starts you at the last element of the sorted region, just left of key
# --- the inner loop ---
# while i >= 0 and A[i] > key: walk leftwards through the sorted region looking for where key belongs
# A[i + 1] = A[i] copies the bigger element one slot to the RIGHT, opening a hole. nothing is swapped - key is safe in its own variable
# the loop stops for one of two reasons: i ran off the left end (key is the new smallest), or A[i] is not bigger than key (found the spot)
# the order of the and matters: i >= 0 is checked FIRST. python's negative indexing means A[-1] would silently read the LAST element instead of erroring
# A[i + 1] = key drops key into the hole. it's i + 1 and not i because the loop decremented i one step past the right slot before stopping
# --- dont get confused ---
# this sorts A IN PLACE. there is no new list and nothing is returned - A itself is rearranged, which is why print(A) shows it sorted (the opposite of Merge_Sort.py)
# > and not >= is what makes it stable: an equal element is not bigger, so the loop stops and key lands to its RIGHT, keeping the original order
# --- traced out of Claude, for A = [5, 2, 4, 6, 1, 3] ---
#   j=1  key=2  shifts 1  -> [2, 5, 4, 6, 1, 3]
#   j=2  key=4  shifts 1  -> [2, 4, 5, 6, 1, 3]
#   j=3  key=6  shifts 0  -> [2, 4, 5, 6, 1, 3]   already in place, the inner loop never runs
#   j=4  key=1  shifts 4  -> [1, 2, 4, 5, 6, 3]   the new smallest, walks all the way to the front
#   j=5  key=3  shifts 3  -> [1, 2, 3, 4, 5, 6]
# those shift counts are the whole cost story: already-sorted input shifts 0 every pass -> O(n), reversed input shifts j every pass -> O(n^2)
# insertion sort is ADAPTIVE, merge sort is not - merge sort costs the same n log n on every input

print(A)

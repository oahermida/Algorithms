# Insertion sort - instrumented copy.
#
# Generated from insert_sort.py in this directory. That file is the clean
# algorithm and the one to edit; this one is the same program with print
# statements added around it, and nothing else changed.
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
# Each trace line below is tagged [Ln] with the line of the algorithm it is
# reporting on. The numbers are looked up from this file at startup, so they
# stay correct even if the code moves around.

import pathlib

SOURCE = pathlib.Path(__file__).read_text().splitlines()


def line_of(statement):
    """Return the 1-based line number where `statement` appears in this file."""
    for number, text in enumerate(SOURCE, start=1):
        if text.strip() == statement:
            return number
    raise ValueError(f"statement not found in source: {statement!r}")


def tag(number=None):
    """A fixed-width [Ln] label, or blank padding for lines with no code line."""
    return f"[L{number:>2}] " if number else "       "


A = [5, 2, 4, 6, 1, 3]
n = len(A)

L_FOR = line_of("for j in range(1, n):")
L_KEY = line_of("key = A[j]")
L_I = line_of("i = j - 1")
L_WHILE = line_of("while i >= 0 and A[i] > key:")
L_SHIFT = line_of("A[i + 1] = A[i]")
L_DEC = line_of("i -= 1")
L_INSERT = line_of("A[i + 1] = key")

THICK = "=" * 72
THIN = "-" * 72

print(THICK)
print("INSERTION SORT")
print(f"start: {A}   (n = {n})")
print(THICK)

total_comparisons = 0
total_shifts = 0

for j in range(1, n):
    print()
    print(THIN)
    print(f"{tag(L_FOR)}PASS j = {j}   -   inserting A[{j}] into A[0..{j - 1}]")
    print(THIN)
    sorted_range = f"A[0..{j - 1}]"
    key_range = f"A[{j}]"
    rest_range = f"A[{j + 1}..]"
    print(f"{tag()}  {sorted_range:<9} sorted    : {A[:j]}")
    print(f"{tag()}  {key_range:<9} inserting : {A[j]}")
    print(f"{tag()}  {rest_range:<9} untouched : {A[j + 1:]}")

    key = A[j]
    print(f"{tag(L_KEY)}  key = A[{j}] = {key}   (saved copy - slot {j} is about to be overwritten)")

    i = j - 1
    print(f"{tag(L_I)}  i starts at {i}   (last index of A[0..{j - 1}])")
    print(f"{tag(L_WHILE)}  scanning leftward:")

    shifts = 0
    while i >= 0 and A[i] > key:
        print(f"{tag(L_WHILE)}    A[{i}] = {A[i]} > key = {key}   ->   shift it right into slot {i + 1}")
        A[i + 1] = A[i]
        shifts += 1
        print(f"{tag(L_SHIFT)}       A is now {A}   (slot {i + 1} is a duplicate)")
        i -= 1
        print(f"{tag(L_DEC)}       i -> {i}")

    if i < 0:
        print(f"{tag(L_WHILE)}    i = {i}   ->   walked off the front; key is smaller than everything in A[0..{j - 1}]")
        comparisons = shifts
    else:
        print(f"{tag(L_WHILE)}    A[{i}] = {A[i]} <= key = {key}   ->   stop; key belongs just right of here")
        comparisons = shifts + 1

    if shifts == 0:
        print(f"{tag(L_INSERT)}  no shifts needed - key already sits in the right place at index {i + 1}")
    else:
        print(f"{tag(L_INSERT)}  gap at index {i + 1}   ->   dropping key = {key} into it")

    A[i + 1] = key
    print(f"{tag(L_INSERT)}  A = {A}")
    print(f"{tag()}  A[0..{j}] sorted is now {A[:j + 1]}")
    print(f"{tag()}  this pass: {comparisons} comparison(s), {shifts} shift(s)")

    total_comparisons += comparisons
    total_shifts += shifts

print()
print(THICK)
print("DONE")
print(f"result: {A}")
print(f"total comparisons: {total_comparisons}")
print(f"total shifts:      {total_shifts}")
print(THICK)

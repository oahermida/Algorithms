r"""
LONGEST COMMON SUBSEQUENCE (LCS)
Lecture 4-5, slides 16-22; CLRS 3rd ed., section 15.4 (pp. 390-397).

Notes: [[LCS — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/LCS — Code Notes.md

What is in this file:
    1. brute_force_lcs         every subsequence of X, O(n * 2^m)
    2. lcs_table               the lecture's algorithm             [slide 19]
    3. restore_lcs             the actual subsequence, walking back on c
    4. lcs_length_rolling      two rows instead of the grid, O(n) space
    5. the slide's examples, with the table printed as slide 21 draws it
    6. tests: hand cases, then random cases against brute force

Run with:
    python3 LCS.py
"""

import random
from itertools import combinations

# The examples from the slides and the book.
SLIDE_X = "ACCGTTGAC"  # slide 16
SLIDE_Y = "ACAACTTGAGTA"  # slide 16, answer ACCTTGA
TABLE_X = "ACCGTT"  # slide 20-22, the rows of the table
TABLE_Y = "ACAACT"  # slide 20-22, the columns, answer ACCT
CLRS_X = "ABCBDAB"  # CLRS Figure 15.8
CLRS_Y = "BDCABA"  # CLRS Figure 15.8, answer BCBA


# =====================================================================
# 1. BRUTE FORCE -- every subsequence of the first sequence
# =====================================================================
# Notes: [[LCS — Code Notes#1. Brute force — every subsequence of the first sequence]] (variables, running time)

def is_subsequence(candidate, sequence):
    position = 0
    for letter in sequence:
        if position < len(candidate) and candidate[position] == letter:
            position += 1
    return position == len(candidate)


def brute_force_lcs(first_sequence, second_sequence):
    for subsequence_length in range(len(first_sequence), -1, -1):
        for kept_positions in combinations(range(len(first_sequence)), subsequence_length):
            candidate = "".join(first_sequence[position] for position in kept_positions)
            if is_subsequence(candidate, second_sequence):
                return candidate
    return ""


# =====================================================================
# 2. THE LECTURE'S ALGORITHM [slide 19]
# =====================================================================
# Notes: [[LCS — Code Notes#2. The lecture's algorithm]] (variables, indexing)

def lcs_table(first_sequence, second_sequence):
    row_count = len(first_sequence)
    column_count = len(second_sequence)
    table = [[0] * (column_count + 1) for _ in range(row_count + 1)]

    for row in range(1, row_count + 1):
        for column in range(1, column_count + 1):
            if first_sequence[row - 1] == second_sequence[column - 1]:
                table[row][column] = table[row - 1][column - 1] + 1  # match: diagonal + 1
            else:
                table[row][column] = max(table[row - 1][column], table[row][column - 1])

    return table[row_count][column_count], table


# =====================================================================
# 3. RESTORE THE SUBSEQUENCE -- walking back on c
# =====================================================================
# Notes: [[LCS — Code Notes#3. Restore the subsequence — walking back on c]] (walk-back rule, variables)

def restore_lcs(first_sequence, second_sequence, table):
    letters = []
    row = len(first_sequence)
    column = len(second_sequence)

    while row > 0 and column > 0:
        if first_sequence[row - 1] == second_sequence[column - 1]:
            letters.append(first_sequence[row - 1])  # case 1: in the LCS
            row -= 1
            column -= 1
        elif table[row - 1][column] >= table[row][column - 1]:
            row -= 1  # case 2: drop the letter of X
        else:
            column -= 1  # case 3: drop the letter of Y

    letters.reverse()
    return "".join(letters)


# =====================================================================
# 4. TWO ROWS INSTEAD OF THE GRID [CLRS page 396, Exercise 15.4-4]
# =====================================================================
# Notes: [[LCS — Code Notes#4. Two rows instead of the grid]] (variables, space)

def lcs_length_rolling(first_sequence, second_sequence):
    if len(second_sequence) > len(first_sequence):
        first_sequence, second_sequence = second_sequence, first_sequence

    previous_row = [0] * (len(second_sequence) + 1)
    for letter_of_first in first_sequence:
        current_row = [0] * (len(second_sequence) + 1)
        for column in range(1, len(second_sequence) + 1):
            if letter_of_first == second_sequence[column - 1]:
                current_row[column] = previous_row[column - 1] + 1
            else:
                current_row[column] = max(previous_row[column], current_row[column - 1])
        previous_row = current_row

    return previous_row[len(second_sequence)]


# =====================================================================
# 5. PRINTING THE TABLE THE WAY SLIDE 21 DRAWS IT
# =====================================================================
# Header row "0  A:1  C:2 ..." is Y with positions. Side column is X.

def print_table(first_sequence, second_sequence, table):
    header = "        0    " + "".join(f"{letter}:{position:<3}"
                                    for position, letter in enumerate(second_sequence, start=1))
    print(header)
    for row in range(len(first_sequence) + 1):
        label = "0" if row == 0 else f"{first_sequence[row - 1]}:{row}"
        cells = "".join(f"{table[row][column]:<5}" for column in range(len(second_sequence) + 1))
        print(f"  {label:>4}  {cells}")


# =====================================================================
# 6. RUN THE SLIDE'S EXAMPLES
# =====================================================================

print("=" * 78)
print("LONGEST COMMON SUBSEQUENCE   -- Lecture 4-5, slides 16-22;  CLRS 15.4")
print("=" * 78)

print(f"\nThe table for X = {TABLE_X}, Y = {TABLE_Y}   [slide 21]\n")
table_length, slide_table = lcs_table(TABLE_X, TABLE_Y)
print_table(TABLE_X, TABLE_Y, slide_table)
print(f"\n  c[6, 6] = {table_length}, restored: {restore_lcs(TABLE_X, TABLE_Y, slide_table)}"
      f"   (slide 22 says length 4, ACCT)")

for first_sequence, second_sequence, source in ((SLIDE_X, SLIDE_Y, "slide 16, expects ACCTTGA"),
                                                (CLRS_X, CLRS_Y, "CLRS Fig 15.8, expects BCBA")):
    length, table = lcs_table(first_sequence, second_sequence)
    print(f"\n  X = {first_sequence}, Y = {second_sequence}   [{source}]")
    print(f"    length {length}, restored {restore_lcs(first_sequence, second_sequence, table)}")


# =====================================================================
# 7. TESTS
# =====================================================================
# Hand cases: (X, Y, expected length). Then for every case, the restored string
# must have that length AND be a subsequence of both inputs. A restored string
# can differ from the slide's when several LCSs exist; both are right.

print("\n" + "=" * 78)
print("TESTS")
print("=" * 78 + "\n")

test_cases = [
    (TABLE_X, TABLE_Y, 4),  # slide 22
    (SLIDE_X, SLIDE_Y, 7),  # slide 16
    (CLRS_X, CLRS_Y, 4),  # CLRS Figure 15.8
    ("", "ABC", 0),  # an empty sequence
    ("ABC", "ABC", 3),  # identical
    ("ABC", "DEF", 0),  # nothing in common
    ("AAAA", "AA", 2),  # repeated letters
    ("ABCBA", "ABCBA"[::-1], 5),  # a palindrome against itself reversed
]

all_passed = True
for first_sequence, second_sequence, expected in test_cases:
    length, table = lcs_table(first_sequence, second_sequence)
    restored = restore_lcs(first_sequence, second_sequence, table)
    rolling = lcs_length_rolling(first_sequence, second_sequence)
    restored_ok = (len(restored) == expected
                   and is_subsequence(restored, first_sequence)
                   and is_subsequence(restored, second_sequence))
    passed = length == expected and rolling == expected and restored_ok
    all_passed = all_passed and passed
    print(f"{'PASS' if passed else 'FAIL'}  lcs({first_sequence!r}, {second_sequence!r})"
          f" = {length} ({restored!r}), expected {expected}")

# Random cases against brute force. Small alphabet so matches are common.
random.seed(4)
trial_count = 2000
failures = 0
for _ in range(trial_count):
    first_sequence = "".join(random.choice("ABC") for _ in range(random.randint(0, 9)))
    second_sequence = "".join(random.choice("ABC") for _ in range(random.randint(0, 9)))
    expected = len(brute_force_lcs(first_sequence, second_sequence))
    length, table = lcs_table(first_sequence, second_sequence)
    restored = restore_lcs(first_sequence, second_sequence, table)
    if (length != expected
            or lcs_length_rolling(first_sequence, second_sequence) != expected
            or len(restored) != expected
            or not is_subsequence(restored, first_sequence)
            or not is_subsequence(restored, second_sequence)):
        failures += 1

passed = failures == 0
all_passed = all_passed and passed
print(f"\n{'PASS' if passed else 'FAIL'}  {trial_count} random pairs (length 0-9, letters ABC):"
      f" table, rolling and restore agree with brute force"
      f" ({trial_count - failures}/{trial_count})")

print(f"\n{'ALL PASS' if all_passed else 'SOME TESTS FAILED'}")

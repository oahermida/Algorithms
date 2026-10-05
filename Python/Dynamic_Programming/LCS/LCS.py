r"""
LONGEST COMMON SUBSEQUENCE (LCS)
================================

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 16-22. Also CLRS
3rd edition, section 15.4, pages 390-397 (PDF pages 411-418).

    LCS [slide 16]
        Input:     Two sequences X = [x1, x2, ... xm], Y = [y1, y2, ..., yn].
        Question:  Longest common subsequence.

        Example:   X = ACCGTTGAC,  Y = ACAACTTGAGTA
                   Output: ACCTTGA.

A SUBSEQUENCE keeps the order but may skip letters. It does not have to be one
unbroken block. That is the "non-contiguous" in the slide's title.

    X = A C C G T T G A C          keep positions 1 2 3 5 6 7 8
        A C C . T T G A .      ->  ACCTTGA

    Y = A C A A C T T G A G T A    keep positions 1 2 5 6 7 8 9
        A C . . C T T G A . . .  ->  ACCTTGA


THE PREFIXES AND THE TABLE [slide 17]
-------------------------------------
    Denote Xi = x1, x2, ..., xi,  Yj = y1, y2, ..., yj.
    Hence, Xm = X, Yn = Y.
    Denote by c[i, j] the length of longest common subsequence of sequences
    Xi, Yj.

So c[i, j] answers a smaller question: "how long is the LCS if I only look at
the first i letters of X and the first j letters of Y?" The full answer is the
bottom-right cell, c[m, n].


THE THREE CASES [slides 17-18; CLRS Theorem 15.1, page 392]
-----------------------------------------------------------
    Let Z = z1, z2, ..., zk be some longest common subsequence of X and Y.
      1. xm = yn and zk = xm then Zk-1 is the LCS of Xm-1 and Yn-1
      2. xm != yn and zk != xm then Z is LCS of Xm-1 and Yn
      3. xm != yn and zk != yn then Z is LCS of Xm and Yn-1

Look only at the LAST letter of each prefix:

    the last letters MATCH       -> that letter ends the LCS. Drop it from
                                    both and solve the rest.
    the last letters DIFFER      -> at least one of them is not in the LCS.
                                    Try dropping each one, keep the better.

That gives the recurrence [slide 18]:

                 | 0                              if i = 0 or j = 0
        c[i,j] = | c[i-1, j-1] + 1                if i, j > 0 and xi = yj
                 | max{ c[i, j-1], c[i-1, j] }    if i, j > 0 and xi != yj

One cell, drawn:

                     j-1         j
                 +-----------+-----------+
          i-1    | c[i-1,j-1]| c[i-1,j]  |
                 +-----------+-----------+
           i     | c[i,j-1]  |  c[i,j]   |
                 +-----------+-----------+

        match:     c[i,j] = 1 + the cell diagonally up-left
        no match:  c[i,j] = the bigger of the cell above and the cell left

Every cell reads only cells above it or to its left. So filling row by row,
left to right, always has the inputs ready.


THE PSEUDOCODE [slide 19]
-------------------------
    LCS(X, Y)
    m = length(X), n = length(Y)
    Create matrix c of size m + 1 x n + 1 with 0 values
    for i in {1, .., m} do
       for j in {1, .., n} do
           if xi = yj then
               c[i, j] = c[i - 1, j - 1] + 1
           else
               c[i, j] = max{c[i - 1, j], c[i, j - 1]}
    return R[n]

Time O(mn). Space O(mn) for the table.


TYPOS IN THE SLIDES
-------------------
    - Slide 18 writes the max as "max{c[i, j-1], c[i-1], j}". The bracket is
      in the wrong place. It means max{c[i, j-1], c[i-1, j]}.
    - Slide 18 says the answer is "c[n, m]". The table is (m+1) x (n+1) with i
      running over X, so the answer is c[m, n].
    - Slide 19 ends with "return R[n]". There is no R. It means return c[m, n].
    - Slide 16 writes "Yn" with a capital Y inside the list y1, ..., Yn. It is
      just yn.
None of these change the method. The slide 21 table is correct, and section 6
reprints it from the code.


THE BOOK VS THE SLIDES
----------------------
CLRS fills a second table b of arrows ("diagonal", "up", "left") and prints
the LCS from it with PRINT-LCS (page 395). The slides only build c. CLRS also
notes (page 396) that b is not needed: the arrow can be worked out again from
c and the two letters. Section 3 does exactly that, so it needs only c.

CLRS breaks ties ("up" when c[i-1, j] >= c[i, j-1]). Section 3 uses the same
rule, so it prints CLRS's own answer BCBA for Figure 15.8.


WHAT IS IN THIS FILE
--------------------
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
# Try every subsequence of first_sequence, longest first. Return the first one
# that is also a subsequence of second_sequence.
#
# subsequence_length: how many letters this round keeps
# kept_positions: which positions of first_sequence are kept
#
# O(n * 2^m): 2^m subsequences, each checked in O(n). Only for testing.

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
# first_sequence: X, length m
# second_sequence: Y, length n
# table: c; table[row][column] is the LCS length of the first `row` letters
#        of X and the first `column` letters of Y
# row: i in the slide, 1 .. m
# column: j in the slide, 1 .. n
#
# Row 0 and column 0 stay 0: an empty prefix has no common subsequence.
# Python strings start at 0, so letter x_i is first_sequence[row - 1].
#
# O(mn) time and space.

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
# The table gives a length. To get the letters, start at c[m, n] and ask which
# case of the recurrence made this cell:
#
#   letters match           -> this letter is in the LCS. Take it, go diagonal.
#   c[i-1, j] >= c[i, j-1]  -> the value came from above. Go up.
#   otherwise               -> the value came from the left. Go left.
#
# row / column: where the walk stands now
# letters: the LCS letters found so far, collected back to front
#
# Same tie rule as CLRS ("up" on a tie), so CLRS's example gives BCBA.
# O(m + n): every step moves up, left, or both.

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
# Each row reads only itself and the row above. So keep two rows and swap.
#
# previous_row: row i-1 of the table
# current_row: row i, being filled
#
# Put the SHORTER sequence along the columns, so the rows are as short as
# possible: O(min(m, n)) space.
#
# Like every rolling version in this folder, it gives up restoring: the old
# rows are gone, so the walk-back has nothing to walk on.

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

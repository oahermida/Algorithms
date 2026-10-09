"""
MATRIX MULTIPLICATION THE CLRS WAY  (recursive, Strassen)
CLRS 3rd ed., section 4.2 (pp. 75-82).

Notes: [[Matrix Multiplication CLRS — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Matrix Multiplication CLRS — Code Notes.md

What is in this file:
    0. Submatrix (the index-calculation window), adding, subtracting
    1. square_matrix_multiply              triple loop, the reference answer
    2. square_matrix_multiply_recursive    8 products, Theta(n^3)
    3. strassen                            7 products, Theta(n^lg 7)
    4. tests: Exercise 4.2-1 by hand, then random matrices

Run with:
    python3 Matrix_Multiplication_CLRS.py
"""

import random


# =====================================================================
# 0. HELPERS
# =====================================================================
# A matrix is a list of rows. [[1, 3], [7, 5]] is
#     ( 1  3 )
#     ( 7  5 )

class Submatrix:
    # A square window onto part of a matrix.
    # matrix: the list of rows the numbers really live in
    # top_row: which row of `matrix` is row 0 of the window
    # left_column: which column of `matrix` is column 0 of the window
    # size: the window is size x size

    def __init__(self, matrix, top_row=0, left_column=0, size=None):
        self.matrix = matrix
        self.top_row = top_row
        self.left_column = left_column
        self.size = len(matrix) if size is None else size

    def entry(self, row, column):
        return self.matrix[self.top_row + row][self.left_column + column]

    def quadrants(self):
        # CLRS line 5: partition by index calculation, Theta(1).
        # Returns X11, X12, X21, X22 -- top left, top right, bottom left,
        # bottom right.
        half = self.size // 2
        return (Submatrix(self.matrix, self.top_row, self.left_column, half),
                Submatrix(self.matrix, self.top_row, self.left_column + half, half),
                Submatrix(self.matrix, self.top_row + half, self.left_column, half),
                Submatrix(self.matrix, self.top_row + half, self.left_column + half, half))


def add(first, second):
    # first + second, as a new matrix. Both are Submatrix windows.
    return [[first.entry(row, column) + second.entry(row, column)
             for column in range(first.size)]
            for row in range(first.size)]


def subtract(first, second):
    # first - second, as a new matrix.
    return [[first.entry(row, column) - second.entry(row, column)
             for column in range(first.size)]
            for row in range(first.size)]


def write_quadrant(answer, top_row, left_column, block):
    # Copy `block` into `answer` with its top-left corner at
    # (top_row, left_column). CLRS p. 78: "we use index calculations to place
    # the results of the matrix additions into the correct positions of
    # matrix C".
    for row, block_row in enumerate(block):
        for column, value in enumerate(block_row):
            answer[top_row + row][left_column + column] = value


def check_power_of_two(matrix_a, matrix_b):
    size = len(matrix_a)
    if size == 0 or size & (size - 1) != 0 or len(matrix_b) != size:
        raise ValueError(f"CLRS assumes two n x n matrices with n a power of 2 "
                         f"(p. 76); got {len(matrix_a)} and {len(matrix_b)} rows")


# =====================================================================
# 1. SQUARE-MATRIX-MULTIPLY  (CLRS p. 75) -- the reference answer
# =====================================================================
# Not one of the two algorithms asked for. It is equation (4.8) written as
# loops, and the tests check the other two against it.
#
# row, column: which entry c_ij of the answer is being filled (the book's i, j)
# inner: walks along row `row` of A and down column `column` of B (the book's k)

def square_matrix_multiply(matrix_a, matrix_b):
    size = len(matrix_a)  # line 1: n = A.rows
    answer = [[0] * size for _ in range(size)]  # line 2: let C be a new n x n matrix
    for row in range(size):  # line 3
        for column in range(size):  # line 4
            for inner in range(size):  # line 6 (line 5's c_ij = 0 is done above)
                answer[row][column] += matrix_a[row][inner] * matrix_b[inner][column]  # line 7
    return answer  # line 8


# =====================================================================
# 2. SQUARE-MATRIX-MULTIPLY-RECURSIVE  (CLRS p. 77) -- Theta(n^3)
# =====================================================================
# Notes: [[Matrix Multiplication CLRS — Code Notes#2. SQUARE-MATRIX-MULTIPLY-RECURSIVE — Theta(n³)]] (variables)

def square_matrix_multiply_recursive(window_a, window_b):
    size = window_a.size  # line 1: n = A.rows
    answer = [[0] * size for _ in range(size)]  # line 2: let C be a new n x n matrix

    if size == 1:  # line 3
        answer[0][0] = window_a.entry(0, 0) * window_b.entry(0, 0)  # line 4
        return answer

    a_11, a_12, a_21, a_22 = window_a.quadrants()  # line 5: partition A
    b_11, b_12, b_21, b_22 = window_b.quadrants()  # line 5: partition B
    half = size // 2  # line 5: C is partitioned by these offsets

    def product(first, second):
        return Submatrix(square_matrix_multiply_recursive(first, second))

    write_quadrant(answer, 0, 0, add(product(a_11, b_11), product(a_12, b_21)))  # line 6: C11
    write_quadrant(answer, 0, half, add(product(a_11, b_12), product(a_12, b_22)))  # line 7: C12
    write_quadrant(answer, half, 0, add(product(a_21, b_11), product(a_22, b_21)))  # line 8: C21
    write_quadrant(answer, half, half, add(product(a_21, b_12), product(a_22, b_22)))  # line 9: C22
    return answer  # line 10


def multiply_recursive(matrix_a, matrix_b):
    check_power_of_two(matrix_a, matrix_b)
    return square_matrix_multiply_recursive(Submatrix(matrix_a), Submatrix(matrix_b))


# =====================================================================
# 3. STRASSEN'S METHOD  (CLRS pp. 79-82) -- Theta(n^lg 7)
# =====================================================================
# Notes: [[Matrix Multiplication CLRS — Code Notes#3. Strassen's method — Theta(n to the lg 7)]] (variables, base case)

def strassen_recursive(window_a, window_b):
    size = window_a.size
    answer = [[0] * size for _ in range(size)]

    if size == 1:
        answer[0][0] = window_a.entry(0, 0) * window_b.entry(0, 0)
        return answer

    # Step 1: divide, by index calculation. Theta(1).
    a_11, a_12, a_21, a_22 = window_a.quadrants()
    b_11, b_12, b_21, b_22 = window_b.quadrants()
    half = size // 2

    # Step 2: ten sums and differences. Theta(n^2).
    sum_1 = Submatrix(subtract(b_12, b_22))  # S1 = B12 - B22
    sum_2 = Submatrix(add(a_11, a_12))  # S2 = A11 + A12
    sum_3 = Submatrix(add(a_21, a_22))  # S3 = A21 + A22
    sum_4 = Submatrix(subtract(b_21, b_11))  # S4 = B21 - B11
    sum_5 = Submatrix(add(a_11, a_22))  # S5 = A11 + A22
    sum_6 = Submatrix(add(b_11, b_22))  # S6 = B11 + B22
    sum_7 = Submatrix(subtract(a_12, a_22))  # S7 = A12 - A22
    sum_8 = Submatrix(add(b_21, b_22))  # S8 = B21 + B22
    sum_9 = Submatrix(subtract(a_11, a_21))  # S9 = A11 - A21
    sum_10 = Submatrix(add(b_11, b_12))  # S10 = B11 + B12

    # Step 3: seven recursive products. 7T(n/2).
    def product(first, second):
        return Submatrix(strassen_recursive(first, second))

    product_1 = product(a_11, sum_1)  # P1 = A11 * S1
    product_2 = product(sum_2, b_22)  # P2 = S2 * B22
    product_3 = product(sum_3, b_11)  # P3 = S3 * B11
    product_4 = product(a_22, sum_4)  # P4 = A22 * S4
    product_5 = product(sum_5, sum_6)  # P5 = S5 * S6
    product_6 = product(sum_7, sum_8)  # P6 = S7 * S8
    product_7 = product(sum_9, sum_10)  # P7 = S9 * S10

    # Step 4: combine into the quarters of C. Theta(n^2).
    # Each add/subtract returns a plain matrix, so wrap it before the next one.
    def plus(first, second):
        return Submatrix(add(first, second))

    def minus(first, second):
        return Submatrix(subtract(first, second))

    answer_11 = plus(minus(plus(product_5, product_4), product_2), product_6)  # C11 = P5 + P4 - P2 + P6
    answer_12 = plus(product_1, product_2)  # C12 = P1 + P2
    answer_21 = plus(product_3, product_4)  # C21 = P3 + P4
    answer_22 = minus(minus(plus(product_5, product_1), product_3), product_7)  # C22 = P5 + P1 - P3 - P7

    write_quadrant(answer, 0, 0, answer_11.matrix)
    write_quadrant(answer, 0, half, answer_12.matrix)
    write_quadrant(answer, half, 0, answer_21.matrix)
    write_quadrant(answer, half, half, answer_22.matrix)
    return answer


def strassen(matrix_a, matrix_b):
    check_power_of_two(matrix_a, matrix_b)
    return strassen_recursive(Submatrix(matrix_a), Submatrix(matrix_b))


# =====================================================================
# 4. TESTS
# =====================================================================

print("=" * 72)
print("MATRIX MULTIPLICATION, CLRS 4.2")
print("=" * 72 + "\n")

identity_4 = [[1 if row == column else 0 for column in range(4)] for row in range(4)]
sample_4 = [[2, -1, 0, 3], [4, 3, 5, -2], [-2, 7, 1, 0], [6, 0, -3, 1]]

# Each case: (description, A, B, expected C)
test_cases = [
    ("Exercise 4.2-1, p. 82", [[1, 3], [7, 5]], [[6, 8], [4, 2]], [[18, 14], [62, 66]]),
    ("1 x 1", [[7]], [[6]], [[42]]),
    ("identity on the left", identity_4, sample_4, sample_4),
    ("identity on the right", sample_4, identity_4, sample_4),
    ("zero matrix", [[0, 0], [0, 0]], [[1, 2], [3, 4]], [[0, 0], [0, 0]]),
    ("negatives", [[-1, 2], [3, -4]], [[-5, 6], [7, -8]], [[19, -22], [-43, 50]]),
]

pass_count = 0
fail_count = 0

for description, matrix_a, matrix_b, expected in test_cases:
    for method_name, method in (("SQUARE-MATRIX-MULTIPLY-RECURSIVE", multiply_recursive),
                                ("Strassen", strassen)):
        result = method(matrix_a, matrix_b)
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{status}  {method_name:<34}{description}")
        if status == "FAIL":
            print(f"      expected {expected}\n      got      {result}")

# The inputs must not be changed: the windows only read them.
untouched_a = [[1, 3], [7, 5]]
untouched_b = [[6, 8], [4, 2]]
strassen(untouched_a, untouched_b)
multiply_recursive(untouched_a, untouched_b)
status = "PASS" if (untouched_a, untouched_b) == ([[1, 3], [7, 5]], [[6, 8], [4, 2]]) else "FAIL"
pass_count += status == "PASS"
fail_count += status == "FAIL"
print(f"{status}  inputs unchanged after both methods")

# A size that is not a power of 2 is refused, as CLRS assumes on p. 76.
try:
    strassen([[1, 2, 3]] * 3, [[1, 2, 3]] * 3)
    status = "FAIL"
except ValueError:
    status = "PASS"
pass_count += status == "PASS"
fail_count += status == "FAIL"
print(f"{status}  3 x 3 refused (not a power of 2)")

# Random check against SQUARE-MATRIX-MULTIPLY. Fixed seed, so every run uses
# the same cases.
random.seed(42)
trial_count = 0
random_failures = 0
for size in (1, 2, 4, 8, 16, 32):
    for _ in range(20):
        matrix_a = [[random.randint(-20, 20) for _ in range(size)] for _ in range(size)]
        matrix_b = [[random.randint(-20, 20) for _ in range(size)] for _ in range(size)]
        expected = square_matrix_multiply(matrix_a, matrix_b)
        trial_count += 1
        if (multiply_recursive(matrix_a, matrix_b) != expected
                or strassen(matrix_a, matrix_b) != expected):
            random_failures += 1

status = "PASS" if random_failures == 0 else "FAIL"
pass_count += status == "PASS"
fail_count += status == "FAIL"
print(f"{status}  {trial_count} random pairs, n = 1..32: both match "
      f"SQUARE-MATRIX-MULTIPLY ({random_failures} disagreements)")

print(f"\n{pass_count} PASS, {fail_count} FAIL")

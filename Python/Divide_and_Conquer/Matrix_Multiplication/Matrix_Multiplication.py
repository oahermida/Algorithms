"""
MATRIX MULTIPLICATION  (naive, divide and conquer, Strassen)
Advanced Algorithms, Lecture 2, slides 23-27; CLRS 3rd ed., section 4.2 (pp. 75-82).

Notes: [[Matrix Multiplication — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Matrix Multiplication — Code Notes.md

What is in this file:
    0. helpers: add, subtract, split into quadrants, join, pad
    1. multiply_naive                 triple loop, O(n^3)       [slide 23]
    2. multiply_divide_and_conquer    8 block products, O(n^3)  [slide 24]
    3. multiply_strassen              7 block products, O(n^2.81)
                                                                [slides 25-26]
    4. counting multiplications: n^3 vs 8^k vs 7^k
    5. tests: hand cases and random cases

Run with:
    python3 Matrix_Multiplication.py
"""

import random


# =====================================================================
# 0. HELPERS
# =====================================================================
# A matrix is a list of rows. Each row is a list of numbers.
# [[1, 2],
#  [3, 4]] is the 2 x 2 matrix with 1 2 on top and 3 4 below.

def add_matrices(first_matrix, second_matrix):
    return [[first_value + second_value
             for first_value, second_value in zip(first_row, second_row)]
            for first_row, second_row in zip(first_matrix, second_matrix)]


def subtract_matrices(first_matrix, second_matrix):
    return [[first_value - second_value
             for first_value, second_value in zip(first_row, second_row)]
            for first_row, second_row in zip(first_matrix, second_matrix)]


def split_into_quadrants(matrix):
    # Cut an n x n matrix (n even) into four n/2 x n/2 blocks:
    # top left (11), top right (12), bottom left (21), bottom right (22).
    half = len(matrix) // 2
    top_left = [row[:half] for row in matrix[:half]]
    top_right = [row[half:] for row in matrix[:half]]
    bottom_left = [row[:half] for row in matrix[half:]]
    bottom_right = [row[half:] for row in matrix[half:]]
    return top_left, top_right, bottom_left, bottom_right


def join_quadrants(top_left, top_right, bottom_left, bottom_right):
    # The reverse of split_into_quadrants: glue four blocks back together.
    top_rows = [left_row + right_row for left_row, right_row in zip(top_left, top_right)]
    bottom_rows = [left_row + right_row
                   for left_row, right_row in zip(bottom_left, bottom_right)]
    return top_rows + bottom_rows


def next_power_of_two(number):
    power = 1
    while power < number:
        power *= 2
    return power


def pad_to_size(matrix, size):
    # Add zero columns on the right and zero rows at the bottom until the
    # matrix is size x size.
    padded_rows = [row + [0] * (size - len(row)) for row in matrix]
    padded_rows += [[0] * size for _ in range(size - len(matrix))]
    return padded_rows


def run_padded(recursive_method, left_matrix, right_matrix, counter):
    # Pad both matrices to one power-of-two square size, multiply, then cut
    # the answer back to rows_of_left x columns_of_right.
    #
    # row_count: rows of the left matrix, and so rows of the answer
    # inner_count: columns of left = rows of right; the length of each
    #              row-times-column pairing
    # column_count: columns of the right matrix, and so columns of the answer
    # size: the padded square size, a power of two
    row_count = len(left_matrix)
    inner_count = len(right_matrix)
    column_count = len(right_matrix[0]) if right_matrix else 0
    if row_count == 0 or inner_count == 0 or column_count == 0:
        return [[0] * column_count for _ in range(row_count)]

    size = next_power_of_two(max(row_count, inner_count, column_count))
    padded_answer = recursive_method(pad_to_size(left_matrix, size),
                                     pad_to_size(right_matrix, size), counter)
    return [row[:column_count] for row in padded_answer[:row_count]]


# =====================================================================
# 1. NAIVE -- the triple loop [slide 23; CLRS p. 75]
# =====================================================================
# Notes: [[Matrix Multiplication — Code Notes#1. Naive — the triple loop]] (variables)

def multiply_naive(left_matrix, right_matrix, counter=None):
    row_count = len(left_matrix)
    inner_count = len(right_matrix)
    column_count = len(right_matrix[0]) if right_matrix else 0

    answer = [[0] * column_count for _ in range(row_count)]
    for row in range(row_count):
        for column in range(column_count):
            entry_total = 0
            for inner in range(inner_count):
                entry_total += left_matrix[row][inner] * right_matrix[inner][column]
                if counter is not None:
                    counter["multiplications"] += 1
            answer[row][column] = entry_total
    return answer


# =====================================================================
# 2. DIVIDE AND CONQUER, 8 PRODUCTS [slide 24; CLRS p. 77]
# =====================================================================
# Notes: [[Matrix Multiplication — Code Notes#2. Divide and conquer, 8 products]] (variables, recurrence)

def divide_and_conquer_square(left_matrix, right_matrix, counter):
    if len(left_matrix) == 1:  # base case: one number times one number
        counter["multiplications"] += 1
        return [[left_matrix[0][0] * right_matrix[0][0]]]

    left_11, left_12, left_21, left_22 = split_into_quadrants(left_matrix)
    right_11, right_12, right_21, right_22 = split_into_quadrants(right_matrix)

    def product(first_block, second_block):
        return divide_and_conquer_square(first_block, second_block, counter)

    answer_11 = add_matrices(product(left_11, right_11), product(left_12, right_21))
    answer_12 = add_matrices(product(left_11, right_12), product(left_12, right_22))
    answer_21 = add_matrices(product(left_21, right_11), product(left_22, right_21))
    answer_22 = add_matrices(product(left_21, right_12), product(left_22, right_22))

    return join_quadrants(answer_11, answer_12, answer_21, answer_22)


def multiply_divide_and_conquer(left_matrix, right_matrix, counter=None):
    if counter is None:
        counter = {"multiplications": 0}
    return run_padded(divide_and_conquer_square, left_matrix, right_matrix, counter)


# =====================================================================
# 3. STRASSEN, 7 PRODUCTS [slides 25-26; CLRS pp. 79-82]
# =====================================================================
# Notes: [[Matrix Multiplication — Code Notes#3. Strassen, 7 products]] (variables, recurrence)

def strassen_square(left_matrix, right_matrix, counter):
    if len(left_matrix) == 1:  # base case: one number times one number
        counter["multiplications"] += 1
        return [[left_matrix[0][0] * right_matrix[0][0]]]

    left_11, left_12, left_21, left_22 = split_into_quadrants(left_matrix)
    right_11, right_12, right_21, right_22 = split_into_quadrants(right_matrix)

    def product(first_block, second_block):
        return strassen_square(first_block, second_block, counter)

    plus = add_matrices
    minus = subtract_matrices

    product_1 = product(plus(left_11, left_22), plus(right_11, right_22))  # M1
    product_2 = product(plus(left_21, left_22), right_11)  # M2
    product_3 = product(left_11, minus(right_12, right_22))  # M3
    product_4 = product(left_22, minus(right_21, right_11))  # M4
    product_5 = product(plus(left_11, left_12), right_22)  # M5
    product_6 = product(minus(left_21, left_11), plus(right_11, right_12))  # M6
    product_7 = product(minus(left_12, left_22), plus(right_21, right_22))  # M7

    answer_11 = plus(minus(plus(product_1, product_4), product_5), product_7)  # M1 + M4 - M5 + M7
    answer_12 = plus(product_3, product_5)  # M3 + M5
    answer_21 = plus(product_2, product_4)  # M2 + M4
    answer_22 = plus(plus(minus(product_1, product_2), product_3), product_6)  # M1 - M2 + M3 + M6

    return join_quadrants(answer_11, answer_12, answer_21, answer_22)


def multiply_strassen(left_matrix, right_matrix, counter=None):
    if counter is None:
        counter = {"multiplications": 0}
    return run_padded(strassen_square, left_matrix, right_matrix, counter)


# =====================================================================
# 4. COUNTING MULTIPLICATIONS -- where the 7 pays off
# =====================================================================
# For n = 2^k:
#     naive and 8-product recursion both do n^3 = 8^k number multiplications.
#     Strassen does 7^k = n^log2(7) = n^2.807.
# The ratio grows by 8/7 every time n doubles.

print("=" * 72)
print("MATRIX MULTIPLICATION   -- Lecture 2, slides 23-27;  CLRS 4.2")
print("=" * 72)

slide_left = [[1, 2], [3, 4]]  # (a b / c d) with numbers
slide_right = [[5, 6], [7, 8]]  # (x y / z t) with numbers
print(f"\nslide 23's 2 x 2 formula with numbers: {slide_left} . {slide_right}")
print(f"  naive:       {multiply_naive(slide_left, slide_right)}")
print(f"  8 products:  {multiply_divide_and_conquer(slide_left, slide_right)}")
print(f"  Strassen:    {multiply_strassen(slide_left, slide_right)}")
print("  a*x + b*z = 1*5 + 2*7 = 19, a*y + b*t = 1*6 + 2*8 = 22, and so on.")

print("\nNumber multiplications done, n x n random matrices:\n")
print(f"{'n':>6}{'naive':>12}{'8 products':>14}{'Strassen':>12}{'ratio':>9}")
print("-" * 53)
random.seed(4)
for size in (1, 2, 4, 8, 16, 32):
    left_matrix = [[random.randint(-9, 9) for _ in range(size)] for _ in range(size)]
    right_matrix = [[random.randint(-9, 9) for _ in range(size)] for _ in range(size)]
    counts = []
    for method in (multiply_naive, multiply_divide_and_conquer, multiply_strassen):
        counter = {"multiplications": 0}
        method(left_matrix, right_matrix, counter)
        counts.append(counter["multiplications"])
    print(f"{size:>6}{counts[0]:>12,}{counts[1]:>14,}{counts[2]:>12,}"
          f"{counts[0] / counts[2]:>9.2f}")
print("\n  naive and 8 products match exactly: n^3. Strassen is 7^k.")
print("  In Python the extra additions and list copying make Strassen SLOWER")
print("  in seconds at these sizes. Real libraries switch to the naive loop")
print("  below a cut-off size for the same reason.")


# =====================================================================
# 5. TESTS
# =====================================================================

identity_3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
sample_3 = [[2, -1, 0], [4, 3, 5], [-2, 7, 1]]

# Each case: (left matrix, right matrix, expected answer)
test_cases = [
    ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),  # slide 23's shape
    ([[7]], [[6]], [[42]]),  # 1 x 1
    (identity_3, sample_3, sample_3),  # identity on the left: 3 needs padding to 4
    (sample_3, identity_3, sample_3),  # identity on the right
    ([[0, 0], [0, 0]], [[1, 2], [3, 4]], [[0, 0], [0, 0]]),  # zero matrix
    ([[1, 2, 3]], [[4], [5], [6]], [[32]]),  # row times column: 1x3 . 3x1
    ([[4], [5], [6]], [[1, 2, 3]], [[4, 8, 12], [5, 10, 15], [6, 12, 18]]),  # column times row
    ([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]], [[58, 64], [139, 154]]),  # 2x3 . 3x2
    ([[-1, 2], [3, -4]], [[-5, 6], [7, -8]], [[19, -22], [-43, 50]]),  # negatives
]

print("\n" + "=" * 72)
print("TESTS")
print("=" * 72 + "\n")

pass_count = 0
fail_count = 0

for left_matrix, right_matrix, expected in test_cases:
    for method_name, method in (("multiply_naive", multiply_naive),
                                ("multiply_divide_and_conquer", multiply_divide_and_conquer),
                                ("multiply_strassen", multiply_strassen)):
        result = method(left_matrix, right_matrix)
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{status}  {method_name}({left_matrix}, {right_matrix}) = {result}")
    print()

# Random check against the naive version. Fixed seed, so every run uses the
# same cases. Shapes are random too, so padding gets exercised.
random.seed(23)
trial_count = 300
random_failures = 0

for _ in range(trial_count):
    row_count = random.randint(1, 9)
    inner_count = random.randint(1, 9)
    column_count = random.randint(1, 9)
    left_matrix = [[random.randint(-20, 20) for _ in range(inner_count)]
                   for _ in range(row_count)]
    right_matrix = [[random.randint(-20, 20) for _ in range(column_count)]
                    for _ in range(inner_count)]
    expected = multiply_naive(left_matrix, right_matrix)
    if (multiply_divide_and_conquer(left_matrix, right_matrix) != expected
            or multiply_strassen(left_matrix, right_matrix) != expected):
        random_failures += 1

status = "PASS" if random_failures == 0 else "FAIL"
if status == "PASS":
    pass_count += 1
else:
    fail_count += 1
print(f"{status}  {trial_count} random matrix pairs (sizes 1-9, any shape): "
      f"8 products and Strassen match naive ({random_failures} disagreements)")

print(f"\n{pass_count} PASS, {fail_count} FAIL")

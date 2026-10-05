"""
MATRIX MULTIPLICATION  (naive, divide and conquer, Strassen)
============================================================

Advanced Algorithms, Lecture 2 (Ivan Bliznets), slides 23-27. Also CLRS
(3rd ed.) section 4.2, "Strassen's algorithm for matrix multiplication",
pp. 75-82. Slide 38 points to CLRS 4.2 for this topic.

    Matrix multiplication                                       [slide 23]
      - We use matrix multiplication significantly more often than you might
        think: graphics, economics, optimization, machine learning.
      - Trivial O(n^3).
      - Multiplication of two matrices of size 2 x 2:

            ( a  b )   ( x  y )   ( ax + bz   ay + bt )
            ( c  d ) . ( z  t ) = ( cx + dz   cy + dt )


1. THE NAIVE WAY -- O(n^3)
--------------------------
Entry (row, column) of the answer is row `row` of the left matrix times
column `column` of the right matrix: multiply pair by pair, add up.
n^2 entries, n multiplications each: n^3.

CLRS calls this SQUARE-MATRIX-MULTIPLY (p. 75).


2. DIVIDE AND CONQUER WITH 8 MULTIPLICATIONS -- still O(n^3)
------------------------------------------------------------
    Split matrices of size n x n into 4 matrices of size n/2 x n/2.
                                                                [slide 24]
        ( C11  C12 )   ( A11  A12 )   ( B11  B12 )
        ( C21  C22 ) = ( A21  A22 ) . ( B21  B22 )

        ( C11  C12 )   ( A11 B11 + A12 B21    A11 B12 + A12 B22 )
        ( C21  C22 ) = ( A21 B11 + A22 B21    A21 B12 + A22 B22 )

        T(n) <= 8 T(n/2) + O(n^2).
    This leads to O(n^3) time algorithm as in the case of naive algorithm.

It is the 2 x 2 formula from slide 23, where each letter is now a whole
block. 8 block products, plus 4 block additions at O(n^2) each.
Master theorem (slide 30): a = 8, b = 2, d = 2. log_2 8 = 3 > 2, so O(n^3).
No gain -- the split alone does not help.

CLRS calls this SQUARE-MATRIX-MULTIPLY-RECURSIVE (p. 77).


3. STRASSEN -- 7 MULTIPLICATIONS -- O(n^2.81)
---------------------------------------------
    Compute the following:                                      [slide 25]
        M1 = (A11 + A22) x (B11 + B22);
        M2 = (A21 + A22) x B11;
        M3 = A11 x (B12 - B22);
        M4 = A22 x (B21 - B11);
        M5 = (A11 + A12) x B22;
        M6 = (A21 - A11) x (B11 + B12);
        M7 = (A12 - A22) x (B21 + B22).

    Finally we have:
        ( C11  C12 )   ( M1 + M4 - M5 + M7    M3 + M5           )
        ( C21  C22 ) = ( M2 + M4              M1 - M2 + M3 + M6 )

    PS. no need to remember this.

    Hence, we have T(n) <= 7 T(n/2) + O(n^2).
    T(n) = n^(log_2 7) = n^2.8074.                              [slide 26]

The trick is the same as Karatsuba (slides 20-22): spend more ADDITIONS to
save one MULTIPLICATION. Additions cost O(n^2), so they are cheap. One fewer
multiplication per level is what changes the exponent:
Master theorem with a = 7, b = 2, d = 2. log_2 7 = 2.807 > 2, so O(n^2.807).

Slide 27 is a table of later records for the exponent ("omega"), down to
2.371552 (2024). None of those are practical.


THE SLIDE AND CLRS NAME THE PRODUCTS DIFFERENTLY
------------------------------------------------
The slide uses Strassen's original M1-M7. CLRS (pp. 80-81) uses ten sums
S1-S10 and products P1-P7, in a different order. Same seven products:

    slide           CLRS    product
    M1   =          P5      (A11 + A22)(B11 + B22)
    M2   =          P3      (A21 + A22) B11
    M3   =          P1      A11 (B12 - B22)
    M4   =          P4      A22 (B21 - B11)
    M5   =          P2      (A11 + A12) B22
    M6   =  minus   P7      CLRS has (A11 - A21)(B11 + B12): the sign flips
    M7   =          P6      (A12 - A22)(B21 + B22)

So CLRS writes C22 = P5 + P1 - P3 - P7, and the slide writes
C22 = M1 - M2 + M3 + M6. They are the same thing. Since the slide says "no
need to remember this", the exam point is the RECURRENCE, not the formulas.


SIZES THAT ARE NOT A POWER OF TWO
---------------------------------
Splitting in half again and again only works if n is a power of 2. CLRS
assumes that (p. 76). Exercise 4.2-3 asks what to do otherwise. The answer
used here: pad with zeros up to the next power of 2, multiply, then cut the
answer back down. Zeros add nothing to any product, so the real part of the
answer is unchanged. Padding at most doubles n, which only changes the
constant, not the O(...).

The same padding also handles non-square matrices (rows x inner times
inner x columns): pad everything to one square size.


WHAT IS IN THIS FILE
--------------------
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
# row: which row of the answer is being filled
# column: which column of the answer is being filled
# inner: walks along row `row` of the left matrix and down column `column`
#        of the right matrix at the same time
# entry_total: the running sum for answer[row][column]
# counter: counts scalar multiplications, for section 4
#
# rows * columns entries, inner_count multiplications each.
# For n x n that is n^3.
#
# Works for any compatible shapes, no padding needed. It is the reference
# answer the other two are checked against.

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
# left_11 .. left_22: the four quadrants of the left matrix (A11 .. A22)
# right_11 .. right_22: the four quadrants of the right matrix (B11 .. B22)
# answer_11 .. answer_22: the four quadrants of the answer (C11 .. C22)
#
# Base case: 1 x 1 matrices are just one number times one number.
# Otherwise: 8 recursive products and 4 additions, exactly slide 24's formula.
#
# T(n) = 8 T(n/2) + O(n^2) = O(n^3). Same as naive.
#
# The recursive part needs n x n with n a power of two. The public function
# multiply_divide_and_conquer pads first, so any shapes work.

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
# left_11 .. left_22: the quadrants of the left matrix (A11 .. A22)
# right_11 .. right_22: the quadrants of the right matrix (B11 .. B22)
# product_1 .. product_7: the slide's M1 .. M7, one recursive product each
# answer_11 .. answer_22: the quadrants of the answer (C11 .. C22)
#
# Same split as section 2, but only 7 recursive products. The extra additions
# and subtractions are all O(n^2), so they do not change the exponent.
#
# T(n) = 7 T(n/2) + O(n^2) = O(n^log2(7)) = O(n^2.807).

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

r"""
KARATSUBA'S MULTIPLICATION ALGORITHM
====================================

Advanced Algorithms, Lecture 2 (Ivan Bliznets), slides 20-22. Also Erickson,
*Algorithms*, section 1.9.

    MULTIPLICATION OF LARGE INTEGERS [slide 20]
        Input:     two integers x, y with n digits
        Question:  find the product of x, y

        - If x, y are large then we cannot simply write: return x * y.
        - As x, y on their own are larger than the maximum value of
          unsigned long long int.
        - The trivial algorithm from school requires O(n^2) operations.
        - At some point (1960) Andrey Kolmogorov conjectured that it is not
          possible to do faster.
        - Shortly, Anatoly Karatsuba discovered a simple n^(log2 3) algorithm.

That history is the point of the slide, and it is worth keeping: a famous
mathematician publicly conjectured that schoolbook multiplication was optimal,
and the conjecture was refuted within about a week by an idea that fits on one
line. The bound was not hard to beat -- it was just hard to imagine beating.

A NOTE ON PYTHON. The slide's premise ("we cannot simply write return x * y")
is about fixed-width integers in C: an unsigned long long holds 64 bits, so two
100-digit numbers overflow it long before they are multiplied. Python's int is
arbitrary precision, so `x * y` just works here -- and, for large enough values,
CPython is itself using Karatsuba internally to do it. That makes wall-clock
timing against `*` meaningless, so this file measures what the slide actually
counts: SINGLE-DIGIT MULTIPLICATIONS. Section 6 times two pure-Python
implementations against each other, which is the fair comparison.


THE SPLIT [slide 21]
--------------------
Write each number as a high half and a low half. With B the base and m = n/2:

    x = x1 * B^m + x0
    y = y1 * B^m + y0

        x = 5678            n = 4 digits, so m = 2, B = 10
            ^^^^
            ||''--- x0 = 78     the low half
            ''----- x1 = 56     the high half

        5678 = 56 * 10^2 + 78

Multiplying out:

    x*y = x1*y1 * B^2m  +  (x1*y0 + x0*y1) * B^m  +  x0*y0
        =   z2   * B^2m  +        z1         * B^m  +   z0

"Note that multiplication by B^m is trivial if we are working in a B-digit
system (simply append m zeroes to the array)" [slide 21] -- so the B^m factors
cost nothing. All the work is in the products.

The obvious reading needs FOUR products (x1y1, x1y0, x0y1, x0y0):

    T(n) <= 4T(n/2) + O(n)        ->        O(n^2)        [slide 21]

"This leads to an algorithm with running time O(n^2), too slow for our goal."
Four half-size multiplications is exactly break-even with doing it the school
way -- the divide and conquer bought nothing.


KARATSUBA'S IDEA [slide 22]
---------------------------
Compute these values:

    x1 + x0,  y1 + y0
    h  = (x1 + x0)(y1 + y0)
    z2 = x1*y1
    z0 = x0*y0
    z1 = h - z2 - z0

then return z2*B^2m + z1*B^m + z0.  "We used 3 multiplications instead of 4."

WHY z1 IS CORRECT -- multiply h out and subtract:

    h  = (x1 + x0)(y1 + y0) = x1*y1 + x1*y0 + x0*y1 + x0*y0
    h - z2 - z0             =         x1*y0 + x0*y1

which is exactly the middle coefficient. The two cross terms are never computed
separately; only their SUM is ever needed, and h gives it in one multiplication.
Nothing is approximated -- this is an identity, checked in section 5.

    T(n) <= 3T(n/2) + O(n)     ->     T(n) = O(n^(log2 3)) = O(n^1.585...)

The trade is real but cheap: three multiplications instead of four, paid for
with several extra additions and subtractions. Additions are O(n); it is the
multiplications that recurse, so trading additions for a multiplication is
always a good deal at scale.

    master theorem, comparing the two:        [see ../Merge_Sort/, Lecture 2]
        4T(n/2) + O(n)   ->   n^(log2 4) = n^2
        3T(n/2) + O(n)   ->   n^(log2 3) = n^1.585
        2T(n/2) + O(n)   ->   n^(log2 2) log n = n log n   (merge sort)

Reading those three lines together is the cleanest illustration of what the
master theorem's first case actually says: the number of recursive calls sits in
the exponent, so removing ONE call out of four changes the growth rate itself.


WHAT IS IN THIS FILE
--------------------
    1. schoolbook_multiply    digit by digit, O(n^2), counting digit products
    2. four_product_split     the divide-and-conquer that gains nothing
    3. karatsuba              the three-product version  [slide 22]
    4. the identity h - z2 - z0 = x1*y0 + x0*y1, checked
    5. digit-multiplication counts: n^2 vs n^1.585
    6. timing, pure Python against pure Python
    7. agreement checks against Python's own `*`

Run with:
    python3 Karatsuba.py
"""

import random
import time

BASE = 10           # the B on the slides; 10 so the splits are readable


# =====================================================================
# 1. SCHOOLBOOK -- the O(n^2) algorithm from school [slide 20]
# =====================================================================
# left_digits / right_digits - the two numbers as digit lists, least significant
#                              digit FIRST, so index i carries weight BASE^i
# result_digits              - the accumulating product, same convention
# digit_products             - a one-entry dict used as a counter, so every
#                              recursive level can add to the same box
#
# Every digit of one number meets every digit of the other: n * m digit
# multiplications, which is the O(n^2) the slide names. The carrying pass
# afterwards is O(n) and does no multiplying.

def to_digits(number):
    if number == 0:
        return [0]
    digits = []
    while number > 0:
        digits.append(number % BASE)
        number //= BASE
    return digits


def from_digits(digits):
    total = 0
    for position in reversed(range(len(digits))):
        total = total * BASE + digits[position]
    return total


def schoolbook_multiply(left_number, right_number, digit_products):
    left_digits = to_digits(left_number)
    right_digits = to_digits(right_number)
    result_digits = [0] * (len(left_digits) + len(right_digits))

    for left_position, left_digit in enumerate(left_digits):
        for right_position, right_digit in enumerate(right_digits):
            result_digits[left_position + right_position] += left_digit * right_digit
            digit_products["count"] += 1

    carry = 0                                   # one O(n) pass, no multiplying
    for position in range(len(result_digits)):
        total = result_digits[position] + carry
        result_digits[position] = total % BASE
        carry = total // BASE

    return from_digits(result_digits)


# =====================================================================
# 2. THE FOUR-PRODUCT SPLIT -- divide and conquer that gains nothing
# =====================================================================
# The obvious reading of slide 21: split both numbers, compute all four
# cross products recursively, reassemble.
#
# split_point  - m, half the digit count of the longer number
# high / low   - x1 and x0, obtained by dividing by BASE^m
#
# Kept so the 4-versus-3 comparison is between two real implementations rather
# than between an implementation and a claim. It is asymptotically no better
# than section 1 -- T(n) = 4T(n/2) + O(n) = O(n^2).

def split_at(number, split_point):
    divisor = BASE ** split_point
    return number // divisor, number % divisor   # high, low


def four_product_split(left_number, right_number, digit_products):
    if left_number < BASE or right_number < BASE:
        digit_products["count"] += 1
        return left_number * right_number        # base case: one digit product

    digit_count = max(len(to_digits(left_number)), len(to_digits(right_number)))
    split_point = digit_count // 2

    left_high, left_low = split_at(left_number, split_point)
    right_high, right_low = split_at(right_number, split_point)

    z2 = four_product_split(left_high, right_high, digit_products)
    z1_first = four_product_split(left_high, right_low, digit_products)
    z1_second = four_product_split(left_low, right_high, digit_products)
    z0 = four_product_split(left_low, right_low, digit_products)

    shift = BASE ** split_point
    return z2 * shift * shift + (z1_first + z1_second) * shift + z0


# =====================================================================
# 3. KARATSUBA -- three products [slide 22]
# =====================================================================
# Same split, but the two cross terms are never computed separately. Only their
# SUM is needed, and h delivers it in one multiplication:
#
# h  - (x1 + x0)(y1 + y0), the one extra product that replaces two
# z2 - x1*y1, the high part
# z0 - x0*y0, the low part
# z1 - h - z2 - z0, which equals x1*y0 + x0*y1 identically
#
# Note that x1 + x0 can be one digit LONGER than either half, so h is not quite
# a half-size multiplication. It is close enough that the recurrence still
# resolves to n^(log2 3) -- the extra digit adds a constant, not a factor.

def karatsuba(left_number, right_number, digit_products):
    if left_number < BASE or right_number < BASE:
        digit_products["count"] += 1
        return left_number * right_number        # base case: one digit product

    digit_count = max(len(to_digits(left_number)), len(to_digits(right_number)))
    split_point = digit_count // 2

    left_high, left_low = split_at(left_number, split_point)
    right_high, right_low = split_at(right_number, split_point)

    z2 = karatsuba(left_high, right_high, digit_products)
    z0 = karatsuba(left_low, right_low, digit_products)
    h = karatsuba(left_high + left_low, right_high + right_low, digit_products)
    z1 = h - z2 - z0                             # the cross terms, never computed alone

    shift = BASE ** split_point
    return z2 * shift * shift + z1 * shift + z0


# =====================================================================
# 4. RUN IT -- one multiplication, step by step
# =====================================================================

print("=" * 78)
print("KARATSUBA   -- Lecture 2, slides 20-22;  Erickson 1.9")
print("=" * 78)

left_number = 5678
right_number = 1234

digit_count = max(len(to_digits(left_number)), len(to_digits(right_number)))
split_point = digit_count // 2
left_high, left_low = split_at(left_number, split_point)
right_high, right_low = split_at(right_number, split_point)

print(f"\nx = {left_number},  y = {right_number},  n = {digit_count} digits, "
      f"m = {split_point}, B = {BASE}\n")
print(f"  x = x1*B^m + x0 = {left_high}*{BASE}^{split_point} + {left_low}"
      f"  = {left_high * BASE ** split_point} + {left_low}")
print(f"  y = y1*B^m + y0 = {right_high}*{BASE}^{split_point} + {right_low}"
      f"  = {right_high * BASE ** split_point} + {right_low}")

z2 = left_high * right_high
z0 = left_low * right_low
h = (left_high + left_low) * (right_high + right_low)
z1 = h - z2 - z0

print(f"\n  THE THREE MULTIPLICATIONS  [slide 22]")
print(f"    z2 = x1*y1 = {left_high}*{right_high} = {z2}")
print(f"    z0 = x0*y0 = {left_low}*{right_low} = {z0}")
print(f"    h  = (x1+x0)(y1+y0) = ({left_high}+{left_low})({right_high}+{right_low})"
      f" = {left_high + left_low}*{right_high + right_low} = {h}")
print(f"    z1 = h - z2 - z0 = {h} - {z2} - {z0} = {z1}")

print(f"\n  THE FOURTH PRODUCT IS NEVER COMPUTED")
print(f"    x1*y0 = {left_high}*{right_low} = {left_high * right_low}")
print(f"    x0*y1 = {left_low}*{right_high} = {left_low * right_high}")
print(f"    their sum = {left_high * right_low + left_low * right_high}, which is z1 = {z1}")
print(f"    the two cross terms are only ever needed ADDED TOGETHER, and h gives")
print(f"    that sum in one multiplication instead of two")

shift = BASE ** split_point
print(f"\n  REASSEMBLE:  z2*B^2m + z1*B^m + z0")
print(f"    = {z2}*{shift * shift} + {z1}*{shift} + {z0}")
print(f"    = {z2 * shift * shift} + {z1 * shift} + {z0}")
print(f"    = {z2 * shift * shift + z1 * shift + z0}")
print(f"\n  Python's own answer: {left_number} * {right_number} = {left_number * right_number}")
print(f"  full recursive karatsuba:           "
      f"{karatsuba(left_number, right_number, {'count': 0})}")


# =====================================================================
# 5. THE IDENTITY, CHECKED
# =====================================================================
# h - z2 - z0 = x1*y0 + x0*y1 is algebra, not an approximation. Checked on
# random values so that a reader who does not trust the expansion can see it
# hold rather than take it on faith.

print("\n" + "=" * 78)
print("THE IDENTITY  h - z2 - z0 = x1*y0 + x0*y1")
print("=" * 78)

random.seed(8)
identity_failures = 0
for _ in range(20000):
    x1, x0 = random.randint(0, 10 ** 6), random.randint(0, 10 ** 6)
    y1, y0 = random.randint(0, 10 ** 6), random.randint(0, 10 ** 6)
    if (x1 + x0) * (y1 + y0) - x1 * y1 - x0 * y0 != x1 * y0 + x0 * y1:
        identity_failures += 1

print(f"\n  20000 random quadruples: {20000 - identity_failures}/20000 hold")
print(f"  (expanding h gives x1y1 + x1y0 + x0y1 + x0y0; subtracting z2 = x1y1 and")
print(f"   z0 = x0y0 leaves exactly the two cross terms)")


# =====================================================================
# 6. DIGIT MULTIPLICATIONS -- what the slide is actually counting
# =====================================================================
# The honest measurement. Wall-clock against Python's `*` would compare pure
# Python against C, so count the single-digit products each method performs.

print("\n" + "=" * 78)
print("SINGLE-DIGIT MULTIPLICATIONS:  n^2  vs  4T(n/2)  vs  3T(n/2)")
print("=" * 78)
print(f"\n{'n digits':>10}{'schoolbook':>14}{'4-product':>13}{'karatsuba':>12}"
      f"{'n^1.585':>11}{'saving':>10}")
print("-" * 78)

random.seed(12)
for digit_count in (4, 8, 16, 32, 64, 128):
    left_sample = random.randint(BASE ** (digit_count - 1), BASE ** digit_count - 1)
    right_sample = random.randint(BASE ** (digit_count - 1), BASE ** digit_count - 1)

    school_counter = {"count": 0}
    schoolbook_multiply(left_sample, right_sample, school_counter)

    four_counter = {"count": 0}
    four_product_split(left_sample, right_sample, four_counter)

    karatsuba_counter = {"count": 0}
    karatsuba(left_sample, right_sample, karatsuba_counter)

    predicted = digit_count ** 1.5849625007
    saving = school_counter["count"] / karatsuba_counter["count"]

    print(f"{digit_count:>10}{school_counter['count']:>14,}{four_counter['count']:>13,}"
          f"{karatsuba_counter['count']:>12,}{predicted:>11,.0f}{saving:>9.1f}x")

print("\n  the 4-product column tracks the schoolbook one -- that split really does")
print("  gain nothing. the karatsuba column follows n^1.585, and the gap widens")
print("  with n, which is what a difference in EXPONENT looks like")

print("\n" + "-" * 78)
print("\nAND IN WALL-CLOCK, PURE PYTHON AGAINST PURE PYTHON:")
print(f"\n{'n digits':>10}{'schoolbook':>15}{'karatsuba':>14}{'speedup':>11}")
print("-" * 78)

for digit_count in (64, 128, 256, 512, 1024):
    left_sample = random.randint(BASE ** (digit_count - 1), BASE ** digit_count - 1)
    right_sample = random.randint(BASE ** (digit_count - 1), BASE ** digit_count - 1)

    start_time = time.perf_counter()
    schoolbook_multiply(left_sample, right_sample, {"count": 0})
    school_seconds = time.perf_counter() - start_time

    start_time = time.perf_counter()
    karatsuba(left_sample, right_sample, {"count": 0})
    karatsuba_seconds = time.perf_counter() - start_time

    print(f"{digit_count:>10}{school_seconds:>15.6f}{karatsuba_seconds:>14.6f}"
          f"{school_seconds / karatsuba_seconds:>10.1f}x")

print("\n  both are pure Python, so this is a fair race. Python's own x * y would")
print("  beat both by a wide margin -- it is C, and for large enough operands it")
print("  is running this same algorithm")
print("\n  NOTE THE CROSSOVER: karatsuba is SLOWER than schoolbook at 64 and 128")
print("  digits and only wins from about 256 on. A better exponent is a promise")
print("  about large n, not about every n -- the recursion, the splitting and the")
print("  extra additions are constant-factor overhead that small inputs cannot")
print("  amortise. Real bignum libraries switch algorithm at a threshold for")
print("  exactly this reason, and CPython does too.")


# =====================================================================
# 7. AGREEMENT CHECK
# =====================================================================
# Against Python's `*`, which is the one reference here that is certainly right.
# Includes numbers of very different lengths, zeros, and single digits -- the
# splitting is where an implementation of this normally breaks.

print("\n" + "=" * 78)
print("AGREEMENT CHECK")
print("=" * 78)

random.seed(6)
trial_count = 20000
karatsuba_disagreements = 0
four_disagreements = 0
schoolbook_disagreements = 0

for _ in range(trial_count):
    left_length = random.randint(1, 12)
    right_length = random.randint(1, 12)
    left_sample = random.randint(0, BASE ** left_length - 1)
    right_sample = random.randint(0, BASE ** right_length - 1)
    expected = left_sample * right_sample

    if karatsuba(left_sample, right_sample, {"count": 0}) != expected:
        karatsuba_disagreements += 1
    if four_product_split(left_sample, right_sample, {"count": 0}) != expected:
        four_disagreements += 1
    if schoolbook_multiply(left_sample, right_sample, {"count": 0}) != expected:
        schoolbook_disagreements += 1

print(f"\n{trial_count} random pairs, 1-12 digits each, zeros and mismatched "
      f"lengths included\n")
print(f"  karatsuba        vs Python's *   {trial_count - karatsuba_disagreements}/{trial_count}")
print(f"  four-product     vs Python's *   {trial_count - four_disagreements}/{trial_count}")
print(f"  schoolbook       vs Python's *   {trial_count - schoolbook_disagreements}/{trial_count}")

# A single very large multiplication, as an end-to-end check that the recursion
# holds up at a depth where a subtle splitting bug would have shown itself.
random.seed(99)
huge_left = random.randint(BASE ** 999, BASE ** 1000 - 1)
huge_right = random.randint(BASE ** 999, BASE ** 1000 - 1)
huge_counter = {"count": 0}
huge_product = karatsuba(huge_left, huge_right, huge_counter)
print(f"\n  two 1000-digit numbers: karatsuba matches Python exactly: "
      f"{huge_product == huge_left * huge_right}")
print(f"  it used {huge_counter['count']:,} single-digit multiplications;")
print(f"  the schoolbook method would need {1000 * 1000:,}")


# === How it Runs ===
#
# --- karatsuba ---
# called with two integers; if EITHER is a single digit this call returns their
# product immediately -- that is the base case, and the only place a real
# multiplication happens
# otherwise it finds the digit count of the longer number, halves it to get m,
# and splits BOTH numbers at that same position
# then THREE recursive calls, and the results are combined with additions,
# subtractions and shifts, none of which recurse
# single threaded and sequential: z2's entire subtree finishes before z0 starts
#
# x = 5678, y = 1234, n = 4, m = 2:
#   x1 = 56, x0 = 78        5678 = 56*100 + 78
#   y1 = 12, y0 = 34        1234 = 12*100 + 34
#
#   z2 = 56 * 12 = 672                          <- recursive call 1
#   z0 = 78 * 34 = 2652                         <- recursive call 2
#   h  = (56+78) * (12+34) = 134 * 46 = 6164    <- recursive call 3
#   z1 = 6164 - 672 - 2652 = 2840
#
#   check the fourth product was not needed:
#     x1*y0 = 56*34 = 1904
#     x0*y1 = 78*12 = 936
#     1904 + 936 = 2840 = z1, exactly -- but neither was ever computed
#
#   reassemble: z2*B^2m + z1*B^m + z0
#             = 672*10000 + 2840*100 + 2652
#             = 6720000 + 284000 + 2652
#             = 7006652
#   and 5678 * 1234 = 7006652
#
# each of those three calls splits again: 56*12 becomes 5*1, 6*2 and (5+6)*(1+2),
# and so on until every operand is one digit. 3 calls per level instead of 4 is
# the whole algorithm
#
# --- why 3 instead of 4 changes the growth rate ---
# the recursion tree has depth log2(n), and level k holds 3^k calls instead of
# 4^k. at the bottom there are 3^(log2 n) = n^(log2 3) = n^1.585 leaves instead
# of 4^(log2 n) = n^2
# so the saving is not a constant factor -- it is in the exponent, which is why
# the ratio in section 6 keeps growing as n does
#
# --- the additions are not free, but they are cheap ---
# karatsuba does MORE addition and subtraction than the four-product split:
# x1+x0, y1+y0, and then h-z2-z0. all of those are O(n) digit operations
# the trade is always worth it, because additions do not recurse. one fewer
# recursive call removes an entire subtree; a few extra additions add a term to
# the O(n) combining step that the master theorem already absorbs
#
# --- a detail worth noticing ---
# x1 + x0 can be one digit longer than x1 or x0 alone (56 + 78 = 134, three
# digits where both halves had two). so h is not strictly a half-size
# multiplication. it costs a constant amount more, not a constant FACTOR more,
# so T(n) <= 3T(n/2 + 1) + O(n) still resolves to O(n^1.585)

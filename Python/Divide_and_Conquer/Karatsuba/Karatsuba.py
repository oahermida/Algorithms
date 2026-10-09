r"""
KARATSUBA'S MULTIPLICATION ALGORITHM
Advanced Algorithms, Lecture 2, slides 20-22; Erickson, Algorithms, 1.9.

Notes: [[Karatsuba — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Karatsuba — Code Notes.md

What is in this file:
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
# Notes: [[Karatsuba — Code Notes#1. Schoolbook — the O(n²) algorithm from school]] (variables)

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
# Notes: [[Karatsuba — Code Notes#2. The four-product split — divide and conquer that gains nothing]] (variables)

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
# Notes: [[Karatsuba — Code Notes#3. Karatsuba — three products]] (variables)

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


# Notes: [[Karatsuba — Code Notes#How it runs]]

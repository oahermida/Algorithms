r"""
RADIX SORT -- digit by digit, least significant first, with a STABLE sort
=========================================================================

Advanced Algorithms, Lecture 6-7 (Ivan Bliznets), slides 41-44. Also CLRS 3rd
ed., section 8.3 (RADIX-SORT, p. 198). Builds on ../Counting_Sort/
Counting_Sort.py; the per-digit counting sort is repeated here so this file
runs on its own.

    Some magic [slide 41]
        Initial    Sorted by        Sorted by       Sorted by
        array      1-st digit       2-nd digit      3-rd digit
                   (last)
         843         761              101             101
         761         101              901             112
         112         901              303             303
         101         112              605             605
         303         843              112             761
         605         303              843             843
         901         605              761             901

    Radix sort [slide 42]
        Arrays with n integers that have d digits in the k-numeral system can
        be sorted in O(d(n + k)) time.

        RADIX-SORT(A, d)
          for i in {1, .., d} do
              sort array A using i-th digit as a key using stable sorting
          end for
        Here, we numerate the digits from the least significant digits. This is
        very important.

"k-numeral system" means base k: decimal is k = 10, binary is k = 2. This file
calls it `base`, and d is `digit_count`.

The magic is in the first column: sorting by the LAST digit first looks
backwards. It works because each later pass is stable. Look at the third pass:
101 and 112 both have first digit 1, so that pass treats them as equal and
leaves them in the order the second pass left them -- and the second pass had
already put 101 before 112, because 0 < 1 in the middle digit.


WHY IT WORKS [slide 43]
-----------------------
    - After the i-th sorting, the numbers created by the last i digits are in
      increasing order.
    - Base of induction for i = 1 is clear.
    - If new numbers are different by the i+1 digit then they are in the right
      order [as] we sort by the [(i+1)]-th digit.
    - If [(i+1)]-th digits are equal then result follows from the fact that
      sorting is stable and induction assumption.

(Slide 43 writes "i-th" in the last two bullets; the digit being sorted in the
step is the (i+1)-th.)

The two cases of the induction step are the whole story:
    the new digits DIFFER  -> this pass puts them in order by itself
    the new digits are EQUAL -> this pass must keep the order the earlier passes
                                built. That is exactly what "stable" means.
Without stability the second case fails. Section 4 runs radix sort with an
unstable counting sort and shows the wrong output.


WHY LEAST SIGNIFICANT FIRST [slide 44]
--------------------------------------
    Initial    Sorted by        Sorted by       Sorted by
    array      leading digit    2-nd digit      1-rd digit     <- slide typo: "last digit"
     843         112              101             101
     761         101              303             901
     112         303              605             761
     101         605              901             112
     303         761              112             303
     605         843              843             843
     901         901              761             605           <- NOT sorted

Same stable sort, opposite digit order. Each pass is stable, so the LAST pass
has the final say, and the last pass looks at the least important digit. The
result is sorted by the last digit, with ties broken by the middle one. The
most important digit must be sorted LAST.


RUNNING TIME [slide 42; CLRS Lemma 8.3]
---------------------------------------
    d passes, each a counting sort on n numbers with keys 0..base-1
    each pass O(n + base), total O(d(n + base))

With d constant and base = O(n) that is O(n), below the n log n comparison
bound of slide 37 -- for the same reason counting sort is: digits are used as
indexes, not compared.


WHAT IS IN THIS FILE
--------------------
    1. digit_of                  one digit of a number in a given base
    2. counting_sort_by_digit    the stable pass, plus an unstable variant
    3. radix_sort                slide 42 / CLRS p. 198
    4. three demonstrations      slide 41, slide 44, and the unstable failure
    5. tests

Run with:
    python3 Radix_Sort.py
"""

import random


# =====================================================================
# 1. ONE DIGIT
# =====================================================================
# number: a non-negative integer
# digit_index: 0 for the last (least significant) digit, 1 for the one
#              before it, and so on
# base: the k of slide 42
#
# Example in base 10: digit_of(843, 0) = 3, digit_of(843, 1) = 4,
# digit_of(843, 2) = 8. Integer-divide to drop the digits on the right, then
# take the remainder to drop the digits on the left.

def digit_of(number, digit_index, base=10):
    return (number // base ** digit_index) % base


def digit_count_of(largest, base=10):
    # how many digits the largest number has (d on slide 42); at least 1
    digit_count = 1
    while largest >= base ** digit_count:
        digit_count += 1
    return digit_count


# =====================================================================
# 2. COUNTING SORT ON ONE DIGIT [slide 40; CLRS 8.2]
# =====================================================================
# values: the numbers to sort; not changed, a new list is returned
# digit_index, base: which digit is the key
# backwards: True = the slide 40 stable pass. False = the same loop run
#            forwards, which reverses equal keys: sorted by this digit, but
#            NOT stable. Only section 4 uses False.
# counts: after counting, counts[digit] = how many have that digit; after the
#         running totals, how many have a digit <= it
# output: the result list
#
# See ../Counting_Sort/Counting_Sort.py for the full explanation, including why
# the decrement comes before the placement in 0-indexed code.

def counting_sort_by_digit(values, digit_index, base=10, backwards=True):
    counts = [0] * base
    for number in values:
        counts[digit_of(number, digit_index, base)] += 1
    for digit in range(1, base):
        counts[digit] += counts[digit - 1]  # running totals

    output = [None] * len(values)
    order = reversed(values) if backwards else values
    for number in order:
        digit = digit_of(number, digit_index, base)
        counts[digit] -= 1
        output[counts[digit]] = number
    return output


# =====================================================================
# 3. RADIX SORT [slide 42; CLRS 8.3, p. 198]
# =====================================================================
# values: non-negative integers; not changed, a new list is returned
# base: the k of slide 42, 10 unless given
# digit_count: d, the number of digits of the largest value
# digit_index: the digit sorted in this pass, 0 = least significant
# stable: False swaps in the unstable pass, for section 4 only
# show: print the list after every pass, the way slide 41 lays it out
#
#     RADIX-SORT(A, d)
#     1 for i = 1 to d
#     2     use a stable sort to sort array A on digit i
#
# Shorter numbers simply have 0 in their high digits (7 is 007), so no padding
# is needed.

def radix_sort(values, base=10, stable=True, show=False):
    if not values:
        return []
    if min(values) < 0:
        raise ValueError("this radix sort handles non-negative integers only")
    digit_count = digit_count_of(max(values), base)
    result = list(values)
    for digit_index in range(digit_count):  # least significant FIRST
        result = counting_sort_by_digit(result, digit_index, base, backwards=stable)
        if show:
            print(f"  after sorting by digit {digit_index} from the right: {result}")
    return result


# =====================================================================
# 4. THREE DEMONSTRATIONS
# =====================================================================
# msd_first_sort: the slide 44 mistake. The same stable pass, but the digits
# are taken most significant first. Every pass is correct and stable; the
# order of the passes is what is wrong.

SLIDE_VALUES = [843, 761, 112, 101, 303, 605, 901]  # slides 41 and 44


def msd_first_sort(values, base=10, show=False):
    digit_count = digit_count_of(max(values), base)
    result = list(values)
    for digit_index in range(digit_count - 1, -1, -1):  # most significant FIRST
        result = counting_sort_by_digit(result, digit_index, base)
        if show:
            print(f"  after sorting by digit {digit_index} from the right: {result}")
    return result


def show_demonstrations():
    print("\nSlide 41: least significant digit first, stable pass")
    print("  start:", SLIDE_VALUES)
    radix_sort(SLIDE_VALUES, show=True)

    print("\nSlide 44: MOST significant digit first, stable pass")
    print("  start:", SLIDE_VALUES)
    wrong = msd_first_sort(SLIDE_VALUES, show=True)
    print(f"  sorted? {wrong == sorted(SLIDE_VALUES)}")

    # The unstable pass reverses equal digits. Watch 101 and 112:
    #   pass 2 (middle digit) puts 101 before 112, correctly, since 0 < 1
    #   pass 3 (first digit) sees a tie, 1 and 1, and REVERSES them
    # That is slide 43's "digits are equal" case failing: the earlier work is
    # thrown away. The output ends 112 101 ..., not sorted.
    print("\nUnstable pass (forwards loop), least significant digit first")
    print("  start:", SLIDE_VALUES)
    broken = radix_sort(SLIDE_VALUES, stable=False, show=True)
    print(f"  sorted? {broken == sorted(SLIDE_VALUES)}")


# =====================================================================
# 5. TESTS -- checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([7], "one element"),
        ([31, 13, 31, 4, 13, 4], "duplicates"),
        ([55, 55, 55], "all equal"),
        ([1, 22, 333, 4444], "already sorted, different lengths"),
        ([4444, 333, 22, 1, 0], "reversed"),
        (SLIDE_VALUES, "slide 41"),
        ([329, 457, 657, 839, 436, 720, 355], "CLRS figure 8.3"),
        ([0, 0, 10, 100, 1000], "zeros and powers of ten"),
    ]

    for values, description in test_cases:
        check(f"radix_sort {values} ({description})", radix_sort(values), sorted(values))

    check("digit_of(843, 1)", digit_of(843, 1), 4)
    check("base 2: [5, 3, 7, 0, 6]", radix_sort([5, 3, 7, 0, 6], base=2), [0, 3, 5, 6, 7])
    check("base 16: [255, 16, 15, 256]", radix_sort([255, 16, 15, 256], base=16), [15, 16, 255, 256])

    # the two broken versions really are broken on the slide's numbers
    check("slide 44 order (MSD first) sorts?", msd_first_sort(SLIDE_VALUES) == sorted(SLIDE_VALUES), False)
    check("unstable pass sorts?", radix_sort(SLIDE_VALUES, stable=False) == sorted(SLIDE_VALUES), False)

    original = [30, 10, 20]
    radix_sort(original)
    check("caller's list untouched", original, [30, 10, 20])

    for base in [2, 10, 16]:
        random_failures = 0
        for trial in range(200):
            length = random.randint(0, 80)
            values = [random.randint(0, 99999) for position in range(length)]
            if radix_sort(values, base) != sorted(values):
                random_failures += 1
        check(f"200 random lists, base {base}: mismatches", random_failures, 0)

    show_demonstrations()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

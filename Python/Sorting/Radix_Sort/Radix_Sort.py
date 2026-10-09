r"""
RADIX SORT -- digit by digit, least significant first, with a STABLE sort
Lecture 6-7 (Ivan Bliznets), slides 41-44; CLRS 3rd ed., section 8.3 (p. 198).

Notes: [[Radix Sort — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Radix Sort — Code Notes.md

What is in this file:
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
# Notes: [[Radix Sort — Code Notes#1. One digit]] (variables, example)

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
# Notes: [[Radix Sort — Code Notes#2. Counting sort on one digit]] (variables)

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
#     RADIX-SORT(A, d)
#     1 for i = 1 to d
#     2     use a stable sort to sort array A on digit i
#
# Notes: [[Radix Sort — Code Notes#3. Radix sort]] (variables, short numbers)

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

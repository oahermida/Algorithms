r"""
COUNTING SORT -- sorting integers 0..M in O(n + M), without comparisons
Lecture 6-7 (Ivan Bliznets), slides 37-40; CLRS 3rd ed., section 8.2 (p. 195).

Notes: [[Counting Sort — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Counting Sort — Code Notes.md

What is in this file:
    1. counting_sort_simple    slide 39, typo fixed: numbers only
    2. counting_sort           slide 40 / CLRS: records by key, stable
    3. CLRS figure 8.2         the count array after each step, printed
    4. stability               backwards pass vs. a forwards pass
    5. tests

Run with:
    python3 Counting_Sort.py
"""

import random


# =====================================================================
# 1. COUNT, THEN REWRITE [slide 39]
# =====================================================================
# values: the numbers to sort, each in 0..max_value; sorted in place
# max_value: M, the largest value allowed
# counts: C; counts[value] is how many times value occurs
# write_position: k on the slide, the next slot of values to fill
#
# Two passes over values and one over counts: O(n + M).

def counting_sort_simple(values, max_value):
    counts = [0] * (max_value + 1)
    for value in values:
        counts[value] += 1

    write_position = 0
    for value in range(max_value + 1):
        while counts[value] > 0:
            values[write_position] = value  # the slide writes i here; it means j
            write_position += 1
            counts[value] -= 1


# =====================================================================
# 2. RUNNING TOTALS AND A BACKWARDS PASS [slide 40; CLRS 8.2, p. 195]
# =====================================================================
# Notes: [[Counting Sort — Code Notes#2. Running totals and a backwards pass]] (variables)

def counting_sort(items, max_value=None, key=lambda item: item):
    if not items:
        return []
    if max_value is None:
        max_value = max(key(item) for item in items)
    if min(key(item) for item in items) < 0:
        raise ValueError("counting sort needs keys in 0..max_value")

    # step 1: count each key
    counts = [0] * (max_value + 1)
    for item in items:
        counts[key(item)] += 1

    # step 2: running totals -- counts[value] becomes "how many keys <= value"
    for value in range(1, max_value + 1):
        counts[value] += counts[value - 1]

    # step 3: place items from the BACK, so equal keys keep their order
    output = [None] * len(items)
    for position in range(len(items) - 1, -1, -1):
        item_key = key(items[position])
        counts[item_key] -= 1  # decrement first: 0-indexed output
        output[counts[item_key]] = items[position]
    return output


# =====================================================================
# 3. CLRS FIGURE 8.2, STEP BY STEP
# =====================================================================
# The same steps as counting_sort, with the count array printed after each.
# The CLRS figure shows C after counting as 2 0 2 3 0 1 and after the running
# totals as 2 2 4 7 7 8. Here the output slots are 0-indexed, so each is one
# lower than in the figure.

def show_figure_8_2():
    figure_values = [2, 5, 3, 0, 2, 3, 0, 3]
    max_value = 5
    print("\nCLRS figure 8.2:  A =", figure_values, " M =", max_value)

    counts = [0] * (max_value + 1)
    for value in figure_values:
        counts[value] += 1
    print("  (a) counts, how many EQUAL each value:  ", counts)

    for value in range(1, max_value + 1):
        counts[value] += counts[value - 1]
    print("  (b) running totals, how many AT MOST:    ", counts)

    output = [None] * len(figure_values)
    for position in range(len(figure_values) - 1, -1, -1):
        value = figure_values[position]
        counts[value] -= 1
        output[counts[value]] = value
        shown = " ".join("." if slot is None else str(slot) for slot in output)
        print(f"      place A[{position}] = {value} at slot {counts[value]}:  {shown}")
    print("  (f) sorted:", output)


# =====================================================================
# 4. WHY BACKWARDS -- stability, shown
# =====================================================================
# counting_sort_forwards is counting_sort with only the direction of the last
# loop changed. It still produces the keys in order, but equal keys come out
# REVERSED. For plain numbers nobody can tell. For records you can.
#
# students: (grade, name) pairs, listed alphabetically; sorted by grade only

def counting_sort_forwards(items, max_value, key=lambda item: item):
    counts = [0] * (max_value + 1)
    for item in items:
        counts[key(item)] += 1
    for value in range(1, max_value + 1):
        counts[value] += counts[value - 1]
    output = [None] * len(items)
    for item in items:  # FORWARDS: the first copy grabs the last slot
        counts[key(item)] -= 1
        output[counts[key(item)]] = item
    return output


def show_stability():
    students = [(8, "Anna"), (6, "Bram"), (8, "Chloe"), (6, "Daan"), (9, "Eva")]
    by_grade = lambda student: student[0]
    print("\nStability (slide 40): students listed alphabetically, sorted by grade")
    print("  input:     ", students)
    print("  backwards: ", counting_sort(students, 10, by_grade), " <- Anna before Chloe")
    print("  forwards:  ", counting_sort_forwards(students, 10, by_grade), " <- order flipped")


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


def simple_sorted(values):
    # counting_sort_simple works in place; run it on a copy
    working_copy = list(values)
    counting_sort_simple(working_copy, max(values, default=0))
    return working_copy


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([4], "one element"),
        ([3, 1, 3, 2, 3, 1, 0], "duplicates"),
        ([5, 5, 5, 5], "all equal"),
        ([0, 1, 2, 3, 4, 5], "already sorted"),
        ([5, 4, 3, 2, 1, 0], "reversed"),
        ([2, 5, 3, 0, 2, 3, 0, 3], "CLRS figure 8.2"),
        ([3, 2, 1, 5, 4], "a permutation, what sort_enum handles"),
        ([0, 100, 0, 50], "gaps: most counts stay 0"),
    ]

    for values, description in test_cases:
        check(f"counting_sort        {values} ({description})", counting_sort(values), sorted(values))
        check(f"counting_sort_simple {values} ({description})", simple_sorted(values), sorted(values))

    # stability: equal keys must keep their input order, which is exactly what
    # Python's sorted() guarantees too
    students = [(8, "Anna"), (6, "Bram"), (8, "Chloe"), (6, "Daan"), (9, "Eva")]
    check("records by grade, stable",
          counting_sort(students, 10, key=lambda student: student[0]),
          sorted(students, key=lambda student: student[0]))

    original = [3, 1, 2]
    counting_sort(original)
    check("caller's list untouched", original, [3, 1, 2])

    random_failures = 0
    for trial in range(300):
        length = random.randint(0, 100)
        max_value = random.randint(0, 30)
        values = [random.randint(0, max_value) for position in range(length)]
        if counting_sort(values) != sorted(values) or simple_sorted(values) != sorted(values):
            random_failures += 1
    check("300 random lists: mismatches", random_failures, 0)

    random_failures = 0
    for trial in range(300):
        records = [(random.randint(0, 9), trial_tag) for trial_tag in range(random.randint(0, 40))]
        if counting_sort(records, 9, key=lambda record: record[0]) != sorted(records, key=lambda record: record[0]):
            random_failures += 1
    check("300 random record lists, stability: mismatches", random_failures, 0)

    show_figure_8_2()
    show_stability()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

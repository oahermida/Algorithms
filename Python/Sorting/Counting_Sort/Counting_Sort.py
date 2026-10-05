r"""
COUNTING SORT -- sorting integers 0..M in O(n + M), without comparisons
=======================================================================

Advanced Algorithms, Lecture 6-7 (Ivan Bliznets), slides 37-40. Also CLRS 3rd
ed., section 8.2 (COUNTING-SORT, p. 195).

    Sorting: lower bound [slide 37]
        Given n distinct integers a1, ..., an after sorting we end up with some
        permutation. Any of n! permutations is possible. Hence, we need at
        least log(n!) comparisons.   log(n!) ~ n log n

    Counting Sort [slide 38]
        - However, we can sort faster if we use not only comparisons.
        - For example: Counting Sort.
        - If we know that all our numbers are from 0 to M and M = O(n) then we
          can sort in O(n) time.

The n log n lower bound is only for algorithms that learn about the input by
comparing two elements. Counting sort never compares two elements. It uses each
value as an INDEX into an array, which is a different kind of question with M+1
possible answers instead of 2. That is how it gets under n log n. The price is
the assumption: the values must be small whole numbers.


HOW THIS DIFFERS FROM ../sort_enum/sort_enum.py
-----------------------------------------------
sort_enum puts each value v straight into position v-1. That works only when
the input is a permutation of 1..n: every value appears exactly once, so every
value owns exactly one slot. Real counting sort drops that assumption:
    DUPLICATES. A value may appear many times, or not at all. So the slot for a
        value is not "v-1" but "however many values are <= v". Counting finds
        that out.
    THE RUNNING-TOTALS STEP. Turning "how many equal v" into "how many are
        <= v" is a prefix sum over the count array. sort_enum never needs it,
        because for a permutation the answer is always just v.
    STABILITY. With duplicates there is a choice of which copy goes where. The
        backwards pass makes equal values keep their original order. That is
        what lets radix sort use counting sort as a building block.


VERSION 1: COUNT, THEN REWRITE [slide 39]
-----------------------------------------
    COUNTINGSORT-1(Array X, int M)
      n <- length(X)
      C <- new array of length M + 1 full of zeroes
      for i in {0, .., n-1} do
          C[X[i]] <- C[X[i]] + 1
      end for
      k <- 0
      for j in {0, .., M} do
          while C[j] > 0 do
              X[k] <- i, k <- k + 1           <- SLIDE TYPO: should be X[k] <- j
              C[j] <- C[j] - 1
          end while
      end for

Count how often each value occurs, then write each value out that many times.
The written value must be j (the value whose count is being used up), not i
(a leftover loop variable from the first loop).

This sorts plain numbers. It cannot sort RECORDS by a key (students by grade,
numbers by one digit), because it throws the original items away and writes
fresh copies of the keys. Version 2 moves the original items.


VERSION 2: RUNNING TOTALS AND A BACKWARDS PASS [slide 40; CLRS p. 195]
---------------------------------------------------------------------
    COUNTINGSORT-2(Array X, int M)
      n <- length(X)
      C <- new array of length M + 1 full of zeroes
      Y <- new array of length n
      for i in {0, .., n-1} do
          C[X[i]] <- C[X[i]] + 1
      end for
      for j in {1, .., M} do
          C[j] <- C[j] + C[j-1]                 <- running totals
      end for
      for j in {n-1, .., 0} do                  <- backwards
          Y[C[X[j]]] <- X[j]
          C[X[j]] <- C[X[j]] - 1
      end for
    Running time O(n + M).
    This sorting is stable! That means that if the keys of objects o1, o2
    coincide, and object o1 is to the left of o2 in the initial array then in
    a new sorted array: o1 is also to the left of o2.

After the running totals, C[v] = how many elements are <= v. So the LAST copy
of v belongs in the C[v]-th slot. Walking X backwards meets the last copy
first, puts it in that slot, and decrements C[v] so the next copy (further
left in X) goes one slot earlier. Equal values come out in their original
order: stable.

AN OFF-BY-ONE ON THE SLIDE. The slide's Y has length n and the loop runs
j = n-1 .. 0, so it is 0-indexed. But C[v] counts elements, so it runs 1..n:
the slide would write the largest element to Y[n], one past the end. CLRS has
the same two lines in this order, but CLRS indexes B from 1, where it is
correct. In 0-indexed code, DECREMENT FIRST, then place:
        C[X[j]] <- C[X[j]] - 1
        Y[C[X[j]]] <- X[j]

Why backwards? Going forwards with the same decrement-and-place would put the
FIRST copy of v in the LAST slot for v, reversing equal values. Still sorted,
but not stable. Section 4 shows both, and ../Radix_Sort/Radix_Sort.py shows
what that breaks.


RUNNING TIME
------------
    count:           n steps
    running totals:  M steps
    placing:         n steps
    total:           O(n + M)

That is O(n) only when M = O(n), slide 38's condition. Sorting 10 numbers
between 0 and 10^9 would build a billion-slot count array.


WHAT IS IN THIS FILE
--------------------
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
# items: the things to sort (slide X); numbers, or records with a key
# max_value: M, the largest key allowed
# key: turns an item into its integer key in 0..max_value; for plain numbers
#      the item is its own key. Radix sort passes "one digit of the number".
# counts: C. After step 1 counts[value] = how many keys EQUAL value. After
#         step 2 counts[value] = how many keys are AT MOST value.
# output: Y, the sorted result, a new list
# position: j on the slide, walking items from the back
#
# Returns a new list; items is not changed.

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

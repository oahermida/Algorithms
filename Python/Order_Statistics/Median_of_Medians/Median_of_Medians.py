r"""
MEDIAN OF MEDIANS -- the k-th smallest element in WORST-CASE O(n)
=================================================================

Advanced Algorithms, Lecture 6-7 (Ivan Bliznets), slides 9-14. Also CLRS 3rd
ed., section 9.3 (SELECT, pp. 220-222). The randomized version is in
../QuickSelect/QuickSelect.py; read that first, this file only changes HOW THE
PIVOT IS CHOSEN.

    Avoid chances [slide 9]
        - Running time of the QuickSelect algorithm depends on randomness
          that might be undesirable in some applications.
        - Can we find k-smallest element in O(n) time even in the worst case?
        - Yes, we can!

QuickSelect is fast when the pivot lands near the middle and slow when it lands
near an end. Median of medians spends O(n) extra work to pick a pivot that is
GUARANTEED to be near the middle: at least 30% of the elements are on each side
of it. Then every round throws away at least 30%, with no luck involved.


THE ALGORITHM [slides 10-11]
----------------------------
    - Split array A into n/5 groups A1, A2, ..., A(n/5), each containing 5
      elements.
    - For each i in {1, 2, ..., n/5} find a median in Ai. Denote this median
      by mi.
    - Each group has a constant number of elements. Hence, for all groups it
      takes O(n) time.
    - Among all elements m1, m2, ..., m(n/5) find median recursively. Denote
      it by x.
    - Find position of x in the whole array. Let this position be j.
    - We know that j >= 3n/10 and j <= 7n/10.
    - After that run our algorithm recursively on one of the parts A[0, j-1]
      or A[j+1, n-1].

"Find position of x" means: partition the array around x, the same split
QuickSelect does, but with x as the pivot instead of a random element. CLRS
says the same thing: "SELECT uses the deterministic partitioning algorithm
PARTITION from quicksort ... modified to take the element to partition around
as an input parameter."

Note there are TWO recursive calls, and they do different jobs:
    call 1  select on the n/5 medians, to FIND the pivot x
    call 2  select on one side of x, to CONTINUE the search


WHY x IS NEAR THE MIDDLE [slide 11]
-----------------------------------
Sort each group into a column, smallest at the bottom, and order the columns by
their median. x is the median of the middle row:

                 groups with median < x      groups with median > x
                  .     .     .     .    .    #     #     #     #
                  .     .     .     .    .    #     #     #     #
    medians ->    o     o     o     o    x    #     #     #     #
                  -     -     -     -    -    .     .     .     .
                  -     -     -     -    -    .     .     .     .

    #  is >= x: it sits above a median that is >= x (slide's "red cloud")
    -  is <= x: it sits below a median that is <= x (slide's "bottom left")

Half of the n/5 medians are >= x, and each of those columns brings 3 elements
that are >= x (its median and the two above it). So at least
    3 * (1/2) * (n/5)  =  3n/10
elements are >= x. By the same picture at least 3n/10 are <= x. So whichever
side the second call keeps, it has at most n - 3n/10 = 7n/10 elements.

The slide's "j >= 3n/10" is the rounded version. CLRS (p. 221) counts exactly:
the leftover group with fewer than 5 elements and x's own group may not
contribute 3, so it is at least 3n/10 - 6, and the second call gets at most
7n/10 + 6 elements. Slide 13 mentions this ("not 100% rigorous").


THE RECURRENCE [slides 12-13]
-----------------------------
    - Find m1, ..., m(n/5) takes cn time for some c.
    - Find median among m1, ..., m(n/5) takes T(n/5).
    - Find position of x in A takes n operations.
    - Additional recursive run is called on array of size j - 1 or n - j
      which is at most 7n/10.
    - Hence, T(n) <= T(n/5) + T(7n/10) + (c+1)n.
    - What gives us a Master theorem in this case?
    - It give us nothing, as it is not applicable here.

The master theorem needs ONE recursive term a*T(n/b). This has two with
different sizes. So the slides prove it by induction instead:

    Take d such that d/10 >= (c+1) ...
    T(n) <= T(n/5) + T(7n/10) + (c+1)n
         <= dn/5 + 7dn/10 + (c+1)n  =  (9d/10 + c + 1)n  <=  dn.

(Slide 13 writes "We claim that T(n) <= n"; it means T(n) <= dn.)

The intuition behind the 9/10: picture the recursion tree. The root does about
n work. Its children work on n/5 and 7n/10 elements, which together is 9n/10.
Their children together get (9/10)^2 n, and so on. The total is
    n * (1 + 9/10 + (9/10)^2 + ...)  =  10n,
a geometric series, so O(n). Everything rests on 1/5 + 7/10 < 1.


WHY GROUPS OF 5
---------------
Redo the counting with groups of g:

    g = 3:  half the n/3 columns bring 2 each  ->  n/3 thrown away, 2n/3 left
            T(n) <= T(n/3) + T(2n/3) + O(n)      1/3 + 2/3 = 1
            Every level of the tree does n work, there are log n levels:
            O(n log n). No better than sorting.
    g = 5:  half the n/5 columns bring 3 each  ->  3n/10 thrown away, 7n/10 left
            T(n) <= T(n/5) + T(7n/10) + O(n)     1/5 + 7/10 = 9/10 < 1
            O(n).
    g = 7:  half the n/7 columns bring 4 each  ->  2n/7 thrown away, 5n/7 left
            T(n) <= T(n/7) + T(5n/7) + O(n)      1/7 + 5/7 = 6/7 < 1
            Also O(n), but sorting each group costs more.

5 is the smallest group size where the fractions add up to LESS than 1. Odd
sizes are used so every group has one true middle element. Section 5 puts
groups of 3, 5 and 7 side by side.


SLIDE 14
--------
    Knowing how to find a median in O(n) deterministic time you can derandomize
    QUICKSORT so it will be working using O(n log n) time in the worst case.
    However, generally there is no need to do this on practice.

Using select to find the exact median as quicksort's pivot gives the recurrence
T(n) = 2T(n/2) + O(n) = O(n log n), always. "No need in practice" because the
constant in select is larger (section 5 measures about 8 comparisons per
element, against about 3.4 for QuickSelect), and random pivots are already
fast on average.


DUPLICATES
----------
CLRS assumes the elements are DISTINCT. The answers below are correct with
duplicates too, but the 3n/10 guarantee is not: the single-pivot partition puts
all copies of x on one side, so an array of identical values loses only one
element per round. The usual fix is a three-way split (< x, = x, > x) and
returning x whenever the wanted rank falls in the middle block. That is beyond
the slides, so it is only described here.


WHAT IS IN THIS FILE
--------------------
    1. insertion_sort_group  sort one group of at most 5 (CLRS step 2)
    2. partition_around      partition with a GIVEN pivot value (CLRS step 4)
    3. select                the slide 10-11 algorithm
    4. kth_smallest          a wrapper that copies the input and uses ranks 1..n
    5. group sizes           3, 5 and 7: worst-case recurrence and real runs
    6. tests

Run with:
    python3 Median_of_Medians.py
"""

import random

# Counts every comparison between two elements, for section 5.
stats = {"comparisons": 0}


# =====================================================================
# 1. SORT ONE SMALL GROUP [CLRS 9.3 step 2]
# =====================================================================
# group: a short list, at most group_size elements, sorted in place
# position: the element being inserted into the sorted part on its left
# current: its value
# slot: where it will go; moves left while the value there is bigger
#
# Plain insertion sort (CLRS 2.1). A group has a constant number of elements, so
# this is O(1) per group and O(n) over all n/5 groups -- slide 10's
# "for all groups it takes O(n) time".

def insertion_sort_group(group):
    for position in range(1, len(group)):
        current = group[position]
        slot = position - 1
        while slot >= 0:
            stats["comparisons"] += 1
            if group[slot] <= current:
                break
            group[slot + 1] = group[slot]  # shift the bigger value right
            slot -= 1
        group[slot + 1] = current


# =====================================================================
# 2. PARTITION AROUND A GIVEN VALUE [slide 11 "find position of x"; CLRS 9.3 step 4]
# =====================================================================
# values: the list, rearranged in place
# low, high: the piece being split, both ends included
# pivot_value: x, the median of medians
# pivot_spot: where x currently is, found by a scan
# small_end: last position of the "<= x" region (CLRS PARTITION's i)
# scan: the position being looked at (CLRS PARTITION's j)
#
# Same Lomuto partition as ../QuickSelect/QuickSelect.py, with one extra first
# step: find x and swap it to the end, so the usual "pivot is the last element"
# code works unchanged. Returns x's final position, the slide's j.

def partition_around(values, low, high, pivot_value):
    pivot_spot = values.index(pivot_value, low, high + 1)
    values[pivot_spot], values[high] = values[high], values[pivot_spot]
    small_end = low - 1
    for scan in range(low, high):
        stats["comparisons"] += 1
        if values[scan] <= pivot_value:
            small_end += 1
            values[small_end], values[scan] = values[scan], values[small_end]
    values[small_end + 1], values[high] = values[high], values[small_end + 1]
    return small_end + 1


# =====================================================================
# 3. SELECT -- the k-th smallest, worst-case O(n) [slides 10-11; CLRS 9.3]
# =====================================================================
# values: the list, rearranged in place as it goes
# low, high: the piece still being searched
# wanted_rank: which smallest we want, counted from 1, relative to the piece
# group_size: 5 in the lecture; a parameter only so section 5 can try 3 and 7
# medians: one median per group, m1 .. m(n/5) on slide 10
# pivot_value: x, the median of the medians
# pivot_position: where x lands after the split (slide j)
# pivot_rank: x's rank inside the piece, j - low + 1
#
# Small pieces (at most one group) are just sorted directly. That is the base
# case slide 13 needs ("on instances with at most 200 elements ...").
# The lower median is used for groups and for the medians, CLRS's convention.
#
# After the split, the three-way decision is identical to QuickSelect.

def select(values, low, high, wanted_rank, group_size=5):
    size = high - low + 1
    if size <= group_size:
        piece = values[low:high + 1]
        insertion_sort_group(piece)
        values[low:high + 1] = piece
        return values[low + wanted_rank - 1]

    # steps 1-2: split into groups and take each group's median
    medians = []
    for group_start in range(low, high + 1, group_size):
        group = values[group_start:min(group_start + group_size, high + 1)]
        insertion_sort_group(group)
        medians.append(group[(len(group) - 1) // 2])  # lower median of the group

    # step 3: first recursive call -- the median of the medians
    pivot_value = select(medians, 0, len(medians) - 1, (len(medians) + 1) // 2, group_size)

    # step 4: split the piece around x
    pivot_position = partition_around(values, low, high, pivot_value)
    pivot_rank = pivot_position - low + 1

    # step 5: second recursive call -- only on the side holding the answer
    if wanted_rank == pivot_rank:
        return values[pivot_position]
    if wanted_rank < pivot_rank:
        return select(values, low, pivot_position - 1, wanted_rank, group_size)
    return select(values, pivot_position + 1, high, wanted_rank - pivot_rank, group_size)


# =====================================================================
# 4. A FRIENDLY WRAPPER
# =====================================================================
# Copies first so the caller's list is left alone. Rank 1 is the minimum.

def kth_smallest(values, wanted_rank, group_size=5):
    if not 1 <= wanted_rank <= len(values):
        raise ValueError("wanted_rank must be between 1 and len(values)")
    working_copy = list(values)
    return select(working_copy, 0, len(working_copy) - 1, wanted_rank, group_size)


def median(values):
    return kth_smallest(values, (len(values) + 1) // 2)


# =====================================================================
# 5. WHY 5 -- groups of 3, 5 and 7 compared
# =====================================================================
# Two tables.
#
# TABLE 1, the worst case. worst_case_work evaluates the recurrence itself:
#     T(n) = n + T(number of groups) + T(what is left after the split)
# where "what is left" assumes the split is as bad as the counting in the
# docstring allows. T(n) / n is the cost per element.
#   groups of 5 and 7: it levels off (towards 10 and 7) -> O(n)
#   groups of 3:       it climbs by the same step every time n grows tenfold,
#                      which is what log n looks like -> O(n log n)
# It counts elements handled, not the cost of sorting each group, so 7 looks
# cheapest here. Sorting groups of 7 costs more per group, which evens it out.
#
# TABLE 2, real runs. Comparisons per element while finding the median of a
# shuffled list. Random input almost never produces the worst split, so all
# three group sizes look similar here. The guarantee is about the worst case,
# which is why table 1 is the one that shows the difference.
#
# group_count: how many groups the piece splits into, n/g rounded up
# thrown_away: elements certainly on the far side of x, (g+1)/2 per column for
#              half of the columns

def worst_case_work(size, group_size, memo):
    if size <= group_size:
        return size
    if (size, group_size) not in memo:
        group_count = -(-size // group_size)  # ceiling division
        thrown_away = (group_size + 1) // 2 * (-(-group_count // 2))
        memo[(size, group_size)] = (size + worst_case_work(group_count, group_size, memo)
                                    + worst_case_work(size - thrown_away, group_size, memo))
    return memo[(size, group_size)]


def show_group_sizes():
    memo = {}
    print("\nWorst case from the recurrence: work per element (slides 12-13)")
    print(f"  {'n':>9}  {'groups of 3':>11}  {'groups of 5':>11}  {'groups of 7':>11}")
    for size in [10 ** exponent for exponent in range(2, 8)]:
        row = [worst_case_work(size, group_size, memo) / size for group_size in [3, 5, 7]]
        print(f"  {size:>9}  {row[0]:>11.2f}  {row[1]:>11.2f}  {row[2]:>11.2f}")

    print("\nReal runs on shuffled input: comparisons per element, finding the median")
    print(f"  {'n':>9}  {'groups of 3':>11}  {'groups of 5':>11}  {'groups of 7':>11}")
    random.seed(5)
    for size in [500, 2500, 12500, 62500]:
        shuffled = random.sample(range(size), size)
        row = []
        for group_size in [3, 5, 7]:
            stats["comparisons"] = 0
            kth_smallest(shuffled, (size + 1) // 2, group_size)
            row.append(stats["comparisons"] / size)
        print(f"  {size:>9}  {row[0]:>11.2f}  {row[1]:>11.2f}  {row[2]:>11.2f}")


# =====================================================================
# 6. TESTS -- every rank checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


def all_ranks(values, group_size=5):
    return [kth_smallest(values, rank, group_size) for rank in range(1, len(values) + 1)]


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([42], "one element"),
        ([3, 1, 3, 2, 3, 1, 2, 2, 3, 1, 1, 3], "duplicates"),
        ([7] * 13, "all equal"),
        (list(range(1, 18)), "already sorted"),
        (list(range(17, 0, -1)), "reversed"),
        ([3, 2, 9, 0, 7, 5, 4, 8, 6, 1], "CLRS exercise 9.2-4"),
        ([-5, 0, 12, -3, 8, 22, -9], "negatives"),
    ]

    for values, description in test_cases:
        check(f"all ranks of {values} ({description})", all_ranks(values), sorted(values))

    check("median of 0..24 shuffled", median(random.sample(range(25), 25)), 12)

    original = [9, 4, 7, 1, 8, 2, 6]
    kth_smallest(original, 3)
    check("caller's list untouched", original, [9, 4, 7, 1, 8, 2, 6])

    # randomized: lengths up to 200 so the recursion goes several levels deep
    for group_size in [3, 5, 7]:
        random_failures = 0
        for trial in range(200):
            length = random.randint(1, 200)
            values = [random.randint(-50, 50) for position in range(length)]
            wanted_rank = random.randint(1, length)
            if kth_smallest(values, wanted_rank, group_size) != sorted(values)[wanted_rank - 1]:
                random_failures += 1
        check(f"200 random lists, groups of {group_size}: mismatches", random_failures, 0)

    show_group_sizes()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

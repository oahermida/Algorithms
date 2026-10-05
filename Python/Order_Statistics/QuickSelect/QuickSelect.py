r"""
QUICKSELECT -- the k-th smallest element in expected O(n)
=========================================================

Advanced Algorithms, Lecture 6-7 (Ivan Bliznets), slides 3-9 -- the same deck as
the heap file (../../Data_Structures/08_Heap.py). Also CLRS 3rd ed., section 9.2
(RANDOMIZED-SELECT, p. 216) and section 7.1 (PARTITION, p. 171).

    k-th smallest element [slide 6]
        - It is trivial to find the minimum or maximum element in an array
          using O(n) time algorithm.
        - k-th smallest element can be easily found in O(kn) time or in
          O(n log n) time.
        - Can we find the n/2-smallest (i.e. median) element in O(n) time?
        - Can we find the k-th smallest element in O(n) time for any k?

The "easy" O(n log n) answer is: sort, then read position k-1. QuickSelect does
better by NOT sorting. It partitions once, like quicksort, and then throws away
the side that cannot contain the answer. Quicksort recurses into both sides;
QuickSelect recurses into one. That single difference turns n log n into n.


THE SLIDE'S PSEUDOCODE [slide 7]
--------------------------------
    QUICKSELECT(Array A, int l, int r, int k)
    if l = r then
        return A[l]
    end if
    p <- random number from {A[l], A[l+1], ..., A[r]}
    Split array A[l : r] into A[l : j-1], p = A[j], A[j+1, r]
    if k = j - l + 1 then
        return A[l]                       <- SLIDE TYPO, see below
    end if
    if k < j - l + 1 then
        QuickSelect(A, l, j-1, k)
    else
        QuickSelect(A, j+1, r, k - (j - l + 1))
    end if

Three things to notice:

    k IS RELATIVE TO THE PIECE. "k-th smallest" always means k-th smallest of
    A[l..r], not of the whole array. That is why the right-hand call subtracts
    j - l + 1: everything left of the pivot, plus the pivot, is smaller, so it
    has been "used up".

    j - l + 1 IS THE PIVOT'S RANK. After the split the pivot sits at position j,
    and there are j - l elements to its left inside the piece. So the pivot is
    the (j - l + 1)-th smallest of the piece. CLRS calls this number k and the
    wanted rank i; the slide calls the wanted rank k. This file calls them
    `pivot_rank` and `wanted_rank` so the two cannot be mixed up.

    THE TYPO. When the ranks match, the answer is the PIVOT, which is A[j], not
    A[l]. CLRS line 6 returns A[q] (its name for j). A[l] is just whatever
    landed at the left edge of the piece. The code below returns A[j].

The slide says "split" without saying how. The lecture never shows a partition
procedure (quicksort was covered in Programming Fundamentals -- Lecture 1,
slide 11). This file uses CLRS's Lomuto PARTITION (section 7.1), with the random
pivot swapped to the end first, which is exactly CLRS's RANDOMIZED-PARTITION
(section 7.3, p. 179). ../../Sorting/Quicksort/Quicksort.py uses the same one.


WHY EXPECTED O(n) [slide 8]
---------------------------
    - After each step with probability at least 1/2 size of the array
      decreases by one quarter.
    - If this was happening always we would have the following recurrence:
      T(n) <= T(3n/4) + O(n).
    - By master theorem we have that T(n) = O(n).

Why "probability at least 1/2": a random pivot lands in the middle half of the
sorted order (between the 25% and 75% marks) half the time. Then both sides have
at most 3n/4 elements, so whichever side we keep, a quarter is gone.

Why T(n) <= T(3n/4) + O(n) is linear: the work per level shrinks geometrically,
    n + 3n/4 + 9n/16 + ...  =  n * 1 / (1 - 3/4)  =  4n.
The master theorem says the same: a = 1, b = 4/3, f(n) = n, and n^(log_b a) =
n^0 = 1, so f wins (case 3) and T(n) = Theta(n).

    Avoid chances [slide 9]
        - Running time of the QuickSelect algorithm depends on randomness
          that might be undesirable in some applications.

The WORST case is still O(n^2): if every pivot happens to be the largest
element, each round removes only one element. Section 5 forces that by picking
the last element as pivot on sorted input. The fix with a guaranteed O(n) is
median of medians: ../Median_of_Medians/Median_of_Medians.py.


WHAT IS IN THIS FILE
--------------------
    1. partition             CLRS 7.1 (Lomuto), the "split" step
    2. randomized_partition  CLRS 7.3, random pivot then partition
    3. quick_select          the slide 7 algorithm, typo fixed
    4. kth_smallest          a wrapper that copies the input and uses ranks 1..n
    5. comparison counts     expected linear vs. the forced quadratic case
    6. slide 3's shop        the median minimises the total distance
    7. tests

Run with:
    python3 QuickSelect.py
"""

import random

# Counts every "A[j] <= x" comparison inside partition, so section 5 can show
# the running time instead of just claiming it.
stats = {"comparisons": 0}


# =====================================================================
# 1. PARTITION -- the "split" step [CLRS 7.1, p. 171]
# =====================================================================
#     PARTITION(A, p, r)
#     1 x = A[r]
#     2 i = p - 1
#     3 for j = p to r - 1
#     4     if A[j] <= x
#     5         i = i + 1
#     6         exchange A[i] with A[j]
#     7 exchange A[i + 1] with A[r]
#     8 return i + 1
#
# values: the list being rearranged in place
# low, high: the piece being split, both ends included (CLRS p, r)
# pivot: the value everything is compared with; always values[high] (CLRS x)
# small_end: last position of the "<= pivot" region (CLRS i)
# scan: the position being looked at (CLRS j)
#
# While scanning, the piece is four regions:
#   low .. small_end          <= pivot
#   small_end+1 .. scan-1     >  pivot
#   scan .. high-1            not looked at yet
#   high                      the pivot itself
# At the end the pivot swaps into small_end + 1, between the two regions, which
# is its final sorted position. That position is returned.

def partition(values, low, high):
    pivot = values[high]
    small_end = low - 1
    for scan in range(low, high):
        stats["comparisons"] += 1
        if values[scan] <= pivot:
            small_end += 1  # grow the "<= pivot" region by one
            values[small_end], values[scan] = values[scan], values[small_end]
    values[small_end + 1], values[high] = values[high], values[small_end + 1]
    return small_end + 1


# =====================================================================
# 2. RANDOM PIVOT [slide 7 line 4; CLRS 7.3, p. 179]
# =====================================================================
#     RANDOMIZED-PARTITION(A, p, r)
#     1 i = RANDOM(p, r)
#     2 exchange A[r] with A[i]
#     3 return PARTITION(A, p, r)
#
# chosen: a random position in low..high; its value becomes the pivot
#
# partition always uses the LAST element as pivot, so picking a random pivot
# just means swapping a random element into the last spot first.

def randomized_partition(values, low, high):
    chosen = random.randint(low, high)
    values[high], values[chosen] = values[chosen], values[high]
    return partition(values, low, high)


# =====================================================================
# 3. QUICKSELECT [slide 7; CLRS RANDOMIZED-SELECT, p. 216]
# =====================================================================
# values: the list, rearranged in place as it goes
# low, high: the piece still being searched (slide l, r)
# wanted_rank: which smallest we want, counted from 1, RELATIVE to the piece
#              (slide k, CLRS i)
# pivot_position: where the pivot ended up after the split (slide j, CLRS q)
# pivot_rank: the pivot's rank inside the piece, j - l + 1 (CLRS k)
#
# Three outcomes after the split:
#   wanted_rank == pivot_rank  -> the pivot is the answer
#   wanted_rank <  pivot_rank  -> the answer is left of the pivot, same rank
#   wanted_rank >  pivot_rank  -> the answer is right of the pivot; the left
#                                 side and the pivot are pivot_rank elements
#                                 already passed, so subtract them
#
# split_pivot is the partition to use. It defaults to the random one; section 5
# passes the plain last-element partition to show the worst case.

def quick_select(values, low, high, wanted_rank, split_pivot=randomized_partition):
    if low == high:  # one element left: it must be the answer
        return values[low]
    pivot_position = split_pivot(values, low, high)
    pivot_rank = pivot_position - low + 1
    if wanted_rank == pivot_rank:
        return values[pivot_position]  # the slide writes A[l] here; it means A[j]
    if wanted_rank < pivot_rank:
        return quick_select(values, low, pivot_position - 1, wanted_rank, split_pivot)
    return quick_select(values, pivot_position + 1, high,
                        wanted_rank - pivot_rank, split_pivot)


# =====================================================================
# 4. A FRIENDLY WRAPPER
# =====================================================================
# quick_select scrambles its list. This copies first, so the caller's list is
# left alone, and checks the rank is in range. Rank 1 is the minimum, rank
# len(values) the maximum.

def kth_smallest(values, wanted_rank, split_pivot=randomized_partition):
    if not 1 <= wanted_rank <= len(values):
        raise ValueError("wanted_rank must be between 1 and len(values)")
    working_copy = list(values)
    return quick_select(working_copy, 0, len(working_copy) - 1, wanted_rank, split_pivot)


def median(values):
    # the lower median, rank ceil(n/2), the same convention CLRS uses
    return kth_smallest(values, (len(values) + 1) // 2)


# =====================================================================
# 5. HOW MUCH WORK -- slide 8 and slide 9, measured
# =====================================================================
# Random pivot on shuffled input: comparisons / n stays roughly constant as n
# grows. That is what "expected O(n)" looks like. (For the median the expected
# count is about 3.4n; CLRS 9.2 proves an upper bound of 4n.)
#
# Last-element pivot on sorted input, asking for the minimum: the pivot is
# always the maximum of the piece, so each round removes only that one element.
# Total comparisons (n-1) + (n-2) + ... + 1 = n(n-1)/2. That is slide 9's
# "depends on randomness": the algorithm is the same, only the luck is gone.

def count_comparisons(values, wanted_rank, split_pivot):
    stats["comparisons"] = 0
    kth_smallest(values, wanted_rank, split_pivot)
    return stats["comparisons"]


def show_work():
    print("\nComparisons made (slide 8: expected O(n); slide 9: worst case O(n^2))")
    print(f"  {'n':>6}  {'random pivot, median':>22}  {'per element':>11}"
          f"  {'last pivot, sorted, min':>24}  {'n(n-1)/2':>9}")
    random.seed(7)
    for size in [100, 200, 400, 800]:
        shuffled = random.sample(range(size), size)
        random_count = count_comparisons(shuffled, (size + 1) // 2, randomized_partition)
        worst_count = count_comparisons(list(range(size)), 1, partition)
        print(f"  {size:>6}  {random_count:>22}  {random_count / size:>11.2f}"
              f"  {worst_count:>24}  {size * (size - 1) // 2:>9}")


# =====================================================================
# 6. SLIDE 3: WHERE TO OPEN THE SHOP
# =====================================================================
#     BEST PLACE
#     Input:    A set X of real numbers x1, x2, ..., xn.
#     Question: Find y with the minimum value of sum |y - xi|.
#     The best such place is the median of the set.
#
# Moving the shop one step right gets it one step closer to every house on its
# right and one step further from every house on its left. At the median the
# two groups are the same size, so no step helps.

def total_distance(shop, houses):
    return sum(abs(shop - house) for house in houses)


def show_shop():
    houses = [1, 2, 6, 7, 30]
    best = median(houses)
    average = sum(houses) / len(houses)
    print("\nSlide 3: houses at", houses)
    print(f"  shop at the median  {best}:    total distance {total_distance(best, houses)}")
    print(f"  shop at the average {average}:  total distance {total_distance(average, houses):g}")


# =====================================================================
# 7. TESTS -- every rank checked against sorted()
# =====================================================================
failures = 0


def check(label, result, expected):
    global failures
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        failures += 1
    print(f"{status}  {label} = {result}, expected {expected}")


def all_ranks(values, split_pivot=randomized_partition):
    # the k-th smallest for every k, which should rebuild sorted(values)
    return [kth_smallest(values, rank, split_pivot) for rank in range(1, len(values) + 1)]


if __name__ == "__main__":
    random.seed(2026)

    test_cases = [
        ([], "empty"),
        ([42], "one element"),
        ([3, 1, 3, 2, 3, 1], "duplicates"),
        ([7, 7, 7, 7], "all equal"),
        ([1, 2, 3, 4, 5, 6], "already sorted"),
        ([6, 5, 4, 3, 2, 1], "reversed"),
        ([2, 8, 7, 1, 3, 5, 6, 4], "CLRS figure 7.1"),
        ([-5, 0, 12, -3, 8], "negatives"),
    ]

    for values, description in test_cases:
        check(f"all ranks of {values} ({description})", all_ranks(values), sorted(values))
        check(f"  same, last-element pivot", all_ranks(values, partition), sorted(values))

    check("median([5, 1, 4, 2, 3])", median([5, 1, 4, 2, 3]), 3)
    check("median([4, 1, 3, 2]) (lower median)", median([4, 1, 3, 2]), 2)

    original = [9, 4, 7, 1]
    kth_smallest(original, 2)
    check("caller's list untouched", original, [9, 4, 7, 1])

    # randomized: 300 lists, random lengths, many repeated values
    random_failures = 0
    for trial in range(300):
        length = random.randint(1, 60)
        values = [random.randint(-20, 20) for position in range(length)]
        wanted_rank = random.randint(1, length)
        if kth_smallest(values, wanted_rank) != sorted(values)[wanted_rank - 1]:
            random_failures += 1
    check("300 random lists, random rank: mismatches", random_failures, 0)

    show_work()
    show_shop()

    print(f"\n{'ALL PASS' if failures == 0 else f'{failures} FAILED'}")

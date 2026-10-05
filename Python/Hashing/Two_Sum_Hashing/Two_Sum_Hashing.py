r"""
2-SUM VIA HASHING
=================

Advanced Algorithms, Lecture 9 "Hashtables" (Ivan Bliznets), slides 5-12.
CLRS 3rd ed., 11.1 (direct-address tables, p. 254) and 11.2 (chaining).

This is the hash-set version that ../../Array_Techniques/2_SUM/2_Sum.py
mentions in its docstring but does not build. Same question, same names:
left_array, right_array, target.


THE PROBLEM [slide 5]
---------------------
    2-SUM PROBLEM (REFORMULATED)
    Input:      Two arrays of positive integer numbers A, B of length n,
                number s.
    Question:   Are there i, j such that A[i] + B[j] = s?

    At this point, we know how to solve it in O(n log n) time.

That O(n log n) is the sort in 2_Sum.py (two pointers or binary search).
Hashing removes the log n: O(n) expected time.

The trick in one line: A[i] + B[j] = s means A[i] = s - B[j]. So put every A
value somewhere you can look up in O(1), then for each B value ask "is
s - B[j] in there?".


STEP 1: A DIRECT ACCESS TABLE [slide 6; CLRS 11.1]
--------------------------------------------------
    for i from 0 to n - 1 do
       C[A[i]] = 1
    end for
    for i from 0 to n - 1 do
       if C[s - B[i]] == 1 then
            return 'Yes'
       end if
    end for
    return 'No'

    - We need to initialize array C
    - Size of C can be huge compared with n
    - Direct Access table

The VALUE is the index. So C needs one cell for every value up to the largest
A value. A = [3, 1000000] needs a million cells for two numbers, and filling
them with 0 first costs a million steps. Time and space are O(n + max A), not
O(n). Section 2 prints that size.

The slide also skips a bounds check: s - B[i] can be negative or bigger than
any A value. Then C[s - B[i]] is outside the array. Section 2 checks first.


STEP 2: SQUEEZE THE VALUES WITH A FUNCTION [slides 7-8]
-------------------------------------------------------
    If only we knew a function h such that:
      1. h(x) can be computed in O(1) time for each x <= U;
      2. for all x in A: h(x) <= M and M = O(n)
      3. for all x, y in A: h(x) != h(y)
    then we can do the following:
      1. Create array C of size M
      2. Put A[i] into position h(A[i]) in the array C
      3. For each j check if C[h(s - B[j])] equals s - B[j].

Now C has O(n) cells, not O(max A). The cell stores the VALUE itself, not a 1.
That is needed: a different number can have the same h, so finding SOMETHING
in the cell is not enough. You must check it is s - B[j].

Pseudocode [slide 8]:

    C <- new array of size 5n
    for i from 0 to n - 1 do
       C[h(A[i])] = A[i]
    end for
    for i from 0 to n - 1 do
       if C[h(s - B[i])] == A[i] then        <- ERRATUM, see below
            return 'Yes'
       end if
    end for
    return 'No'


THE ERRATUM ON SLIDE 8
----------------------
The check should be

       if C[h(s - B[i])] == s - B[i] then

as slide 7's step 3 says. A[i] is the wrong thing to compare with: in the
second loop, i walks over B, so A[i] is an unrelated A value. Example: A = [16],
B = [24], s = 33, h(x) = x mod 7. Cell h(16) = 2 holds 16. s - B[0] = 9 and
h(9) = 2, so the cell holds 16, and 16 == A[0]. The literal slide says Yes.
But 16 + 24 = 40. Section 6 runs this.


STEP 3: WHEN h IS NOT ONE-TO-ONE [slides 9-12]
----------------------------------------------
Condition 3 (no two A values share a cell) is the problem. Slide 12:

    Unfortunately, by Pigeonhole principle there is no single function that
    works for all X subset of {1, 2, ..., U} if U > M.
    That is why we relax our requirements to h and allow randomness.

Slide 11 shows it with h(x) = x mod 7: 16 and 9 both go to cell 2, 4 and 18
both go to cell 4. With one value per cell, the second one OVERWRITES the
first, and the algorithm can miss a real pair.

The fix is the rest of Lecture 9: a hash table with chaining (each cell holds
a LIST) and a random h (slide 14). See ../Hash_Table/Hash_Table.py. Then:

    insert every A value     n inserts,  O(1) expected each
    look up every s - B[j]   n searches, O(1) expected each
    total                    O(n) expected

Python's set is a hash table too (slide 4), so `value in set` gives the same
O(n) with one line. The price, as 2_Sum.py says, is O(n) extra memory.


OTHER SLIDE NOTES
-----------------
    Slide 5 says A and B both have length n. The examples on slides 9-11 have
    6 values in A and 7 in B. The code here allows different lengths.
    Slides 10-11 list s - B = {22, 9, -1, 27, 25, 16}: six values. B has seven.
    33 - 29 = 4 is missing, and 4 is in A. So 4 + 29 = 33 is a second pair.
    Slide 7 condition 3 should say "for all x != y in A".
    s - B[j] can be negative (33 - 34 = -1 on slide 10). The slide takes
    -1 mod 7 = 6. Python's % does that too. A C-style % gives -1.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_two_sum       every pair, O(n^2), the reference
    2. direct_access_two_sum     slide 6, table as big as max A
    3. slide_array_two_sum       slide 8 (corrected), one value per cell
    4. chained_two_sum           slide 14's table, O(n) expected
    5. set_two_sum               the same with Python's set
    6. the slides' examples, the erratum, and an overwrite that loses a pair
    7. random checks against brute force

Run with:
    python3 Two_Sum_Hashing.py
"""

import random

# The lecture's two examples [slides 9, 11].
SLIDE_RIGHT_ARRAY = [11, 24, 34, 6, 29, 8, 17]
SLIDE_TARGET = 33
EXAMPLE_ONE_LEFT = [4, 16, 10, 26, 21, 34]
EXAMPLE_TWO_LEFT = [4, 16, 9, 26, 18, 34]


def mod_seven(value):
    return value % 7


# =====================================================================
# 1. BRUTE FORCE -- the reference answer
# =====================================================================
# Same as 2_Sum.py: every left value against every right value.
# Returns the pair (left_value, right_value), or None.
#
# O(n^2) pairs.

def brute_force_two_sum(left_array, right_array, target):
    for left_value in left_array:
        for right_value in right_array:
            if left_value + right_value == target:
                return (left_value, right_value)
    return None


# =====================================================================
# 2. DIRECT ACCESS TABLE [slide 6; CLRS 11.1]
# =====================================================================
# present: C; present[value] is True when value is in left_array
# table_size: max(left_array) + 1, one cell per possible value
# wanted: s - B[i], the left value that would complete the pair
#
# The bounds check (0 <= wanted < table_size) is missing on the slide.
#
# O(n + max A) time and space. The max A part is the whole problem.

def direct_access_two_sum(left_array, right_array, target):
    table_size = max(left_array) + 1
    present = [False] * table_size  # "We need to initialize array C"
    for left_value in left_array:
        present[left_value] = True

    for right_value in right_array:
        wanted = target - right_value
        if 0 <= wanted < table_size and present[wanted]:
            return (wanted, right_value)
    return None


# =====================================================================
# 3. THE SLIDE 8 ARRAY, CORRECTED [slides 7-8]
# =====================================================================
# cells: C, one value per cell, None means empty
# hash_function: h; must give different cells to different A values
# wanted: s - B[i]
#
# Correct ONLY when h is one-to-one on left_array (slide 7, condition 3).
# If two A values share a cell, the later one overwrites the earlier one.
# A "Yes" is always right (the value is checked). A "No" can be wrong.
#
# The cell count is slide 8's 5n, unless the caller gives one (the slides'
# examples use x mod 7, so 7 cells).
#
# O(n) time, if h is O(1).

def slide_array_two_sum(left_array, right_array, target, hash_function, cell_count=None):
    if cell_count is None:
        cell_count = 5 * len(left_array)
    cells = [None] * cell_count
    for left_value in left_array:
        cells[hash_function(left_value)] = left_value  # a collision overwrites

    for right_value in right_array:
        wanted = target - right_value
        if cells[hash_function(wanted)] == wanted:  # the slide has "== A[i]"
            return (wanted, right_value)
    return None


# The slide's LITERAL check, kept only to show the erratum. Do not use.
# right_index walks over B, and the slide compares with A[right_index].
def slide_array_two_sum_literal(left_array, right_array, target, hash_function, cell_count):
    cells = [None] * cell_count
    for left_value in left_array:
        cells[hash_function(left_value)] = left_value
    for right_index in range(min(len(left_array), len(right_array))):
        wanted = target - right_array[right_index]
        if cells[hash_function(wanted)] == left_array[right_index]:
            return "Yes"
    return "No"


# =====================================================================
# 4. A CHAINED HASH SET [slide 14; CLRS 11.2]
# =====================================================================
# A cut-down copy of ChainedHashTable from ../Hash_Table/Hash_Table.py, so
# this file runs on its own. Keys only, no values: 2-SUM only asks "is it in?".
#
# buckets: m lists; each list holds the A values that hash there
# prime: p, a prime bigger than any key looked up
# multiplier: a, random, 0 < a < p
# offset: b, random, 0 <= b < p
#
# h(x) = ((a*x + b) mod p) mod m, drawn once when the set is made (slide 23).
# Passing hash_function replaces it, so the slide's x mod 7 can be replayed.

def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def next_prime_above(number):
    candidate = number + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


class ChainedHashSet:
    def __init__(self, slot_count, universe_limit, random_generator=random, hash_function=None):
        self.buckets = [[] for _ in range(slot_count)]
        if hash_function is None:
            prime = next_prime_above(universe_limit)
            multiplier = random_generator.randint(1, prime - 1)
            offset = random_generator.randint(0, prime - 1)

            def hash_function(key):
                return ((multiplier * key + offset) % prime) % slot_count
        self.hash_function = hash_function

    def add(self, key):
        chain = self.buckets[self.hash_function(key)]
        if key not in chain:
            chain.append(key)

    def contains(self, key):
        return key in self.buckets[self.hash_function(key)]

    def show(self, indent="    "):
        for slot_index, chain in enumerate(self.buckets):
            marker = "  <- collision" if len(chain) > 1 else ""
            print(f"{indent}[{slot_index}] {chain}{marker}")


# =====================================================================
# 5. 2-SUM WITH THE CHAINED SET, AND WITH PYTHON'S set
# =====================================================================
# seen: the hash set holding every left value
# slot_count: m = n, so the load factor n/m is at most 1 [slide 17]
#   (a caller that passes its own hash_function passes its slot_count too)
# universe_limit: U; must cover every key hashed, A values AND s - B[j]
# wanted: s - B[j]
#
# A values are positive (slide 5), so a wanted value below 1 cannot be in A.
# It is skipped before hashing, which keeps every hashed key in 0..U.
#
# O(n) expected: n adds and n lookups, each O(1 + n/m) = O(1) on average.

def chained_two_sum(left_array, right_array, target, random_generator=random,
                    hash_function=None, slot_count=None):
    if slot_count is None:
        slot_count = max(1, len(left_array))
    universe_limit = max(max(left_array), target)
    seen = ChainedHashSet(slot_count, universe_limit, random_generator, hash_function)
    for left_value in left_array:
        seen.add(left_value)

    for right_value in right_array:
        wanted = target - right_value
        if wanted >= 1 and seen.contains(wanted):
            return (wanted, right_value)
    return None


# seen: a Python set, which is a hash table underneath
def set_two_sum(left_array, right_array, target):
    seen = set(left_array)
    for right_value in right_array:
        wanted = target - right_value
        if wanted in seen:
            return (wanted, right_value)
    return None


# =====================================================================
# TEST HELPER
# =====================================================================

failure_count = 0


def check(description, condition):
    global failure_count
    status = "PASS" if condition else "FAIL"
    if not condition:
        failure_count += 1
    print(f"{status}  {description}")


def is_valid_pair(pair, left_array, right_array, target):
    if pair is None:
        return False
    left_value, right_value = pair
    return left_value in left_array and right_value in right_array and left_value + right_value == target


# =====================================================================
# 6. THE SLIDES' EXAMPLES [slides 9-11]
# =====================================================================
# Trace: for each B value, show s - B[j], its cell under x mod 7, and what the
# cell holds. That is the slide 10 picture, one row per lookup.

def trace_slide_lookup(left_array, title):
    print(f"\n{title}")
    print(f"    A = {left_array}")
    print(f"    B = {SLIDE_RIGHT_ARRAY},  s = {SLIDE_TARGET},  h(x) = x mod 7\n")

    slide_cells = [None] * 7
    for left_value in left_array:
        if slide_cells[mod_seven(left_value)] is not None:
            print(f"    {left_value} goes to cell {mod_seven(left_value)},"
                  f" OVERWRITING {slide_cells[mod_seven(left_value)]}")
        slide_cells[mod_seven(left_value)] = left_value
    print(f"    slide 8 array (one value per cell): {slide_cells}\n")

    chained_set = ChainedHashSet(7, 0, hash_function=mod_seven)
    for left_value in left_array:
        chained_set.add(left_value)
    print("    chained table (a list per cell):")
    chained_set.show(indent="      ")
    print()

    for right_value in SLIDE_RIGHT_ARRAY:
        wanted = SLIDE_TARGET - right_value
        slot_index = mod_seven(wanted)
        chain = chained_set.buckets[slot_index]
        verdict = "FOUND" if wanted in chain else "no"
        print(f"    B = {right_value:>2}: s - B = {wanted:>2}, h = {slot_index},"
              f" list {chain} -> {verdict}")


print("=" * 78)
print("2-SUM VIA HASHING   -- Lecture 9, slides 5-12")
print("=" * 78)

trace_slide_lookup(EXAMPLE_ONE_LEFT, "slide 10, Example 1 (no collisions)")
trace_slide_lookup(EXAMPLE_TWO_LEFT, "slide 11, Example 2 (16,9 and 4,18 collide)")
print("\n    note B = 29: s - B = 4, which slides 10-11 leave out of their list.\n")

for left_array, example_name in ((EXAMPLE_ONE_LEFT, "Example 1"), (EXAMPLE_TWO_LEFT, "Example 2")):
    expected_found = brute_force_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET) is not None
    results = {
        "direct access": direct_access_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET),
        "slide 8 array": slide_array_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET, mod_seven, 7),
        "chained x mod 7": chained_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET,
                                           hash_function=mod_seven, slot_count=7),
        "chained random": chained_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET,
                                          random.Random(9)),
        "python set": set_two_sum(left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET),
    }
    for method_name, pair in results.items():
        check(f"{example_name}, {method_name}: {pair}",
              is_valid_pair(pair, left_array, SLIDE_RIGHT_ARRAY, SLIDE_TARGET) and expected_found)

# 2_Sum.py's own example, so the two files can be compared.
print()
two_sum_left = [2, 7, 11, 15]
two_sum_right = [9, 1, 6, 3]
check(f"2_Sum.py example, target 20: {set_two_sum(two_sum_left, two_sum_right, 20)}",
      set_two_sum(two_sum_left, two_sum_right, 20) == (11, 9)
      and chained_two_sum(two_sum_left, two_sum_right, 20, random.Random(1)) == (11, 9))
check("2_Sum.py example, target 100: no pair",
      set_two_sum(two_sum_left, two_sum_right, 100) is None
      and chained_two_sum(two_sum_left, two_sum_right, 100, random.Random(1)) is None
      and direct_access_two_sum(two_sum_left, two_sum_right, 100) is None)


print("\n" + "=" * 78)
print("WHY THE DIRECT ACCESS TABLE IS NOT O(n)   [slide 6]")
print("=" * 78 + "\n")

huge_left = [3, 1000000]
huge_right = [5, 1000000]
print(f"    A = {huge_left}, B = {huge_right}, s = 1000003")
print(f"    n = 2, but the table needs max(A) + 1 = {max(huge_left) + 1} cells\n")
check("direct access still answers correctly: (3, 1000000)",
      direct_access_two_sum(huge_left, huge_right, 1000003) == (3, 1000000))
check("a chained table for the same input has only n = 2 lists",
      len(ChainedHashSet(len(huge_left), 1000003, random.Random(4)).buckets) == 2
      and chained_two_sum(huge_left, huge_right, 1000003, random.Random(4)) is not None)


print("\n" + "=" * 78)
print("THE SLIDE 8 ERRATUM AND THE OVERWRITE PROBLEM")
print("=" * 78 + "\n")

# The erratum: A = [16], B = [24], s = 33. Cell 2 holds 16. s - 24 = 9 also
# hashes to 2. The literal check compares the cell with A[0] = 16 and says Yes.
erratum_left = [16]
erratum_right = [24]
literal_answer = slide_array_two_sum_literal(erratum_left, erratum_right, 33, mod_seven, 7)
print(f"    A = {erratum_left}, B = {erratum_right}, s = 33  (16 + 24 = 40)")
print(f"    literal slide check  'C[h(s - B[i])] == A[i]'      -> {literal_answer}")
corrected_answer = slide_array_two_sum(erratum_left, erratum_right, 33, mod_seven, 7)
corrected_text = "No" if corrected_answer is None else "Yes"
print(f"    corrected check      'C[h(s - B[i])] == s - B[i]'  -> {corrected_text}\n")
check("the literal slide check gives a false Yes", literal_answer == "Yes")
check("the corrected check says no pair", corrected_answer is None)

# The overwrite: A = [16, 9], B = [17], s = 33. 16 and 9 both hash to 2, so 9
# overwrites 16. The real pair 16 + 17 is lost. Chaining keeps both.
overwrite_left = [16, 9]
overwrite_right = [17]
print(f"\n    A = {overwrite_left}, B = {overwrite_right}, s = 33  (16 + 17 = 33)")
print(f"    16 mod 7 = 2 and 9 mod 7 = 2, so 9 overwrites 16 in the slide 8 array\n")
check("slide 8 array (one value per cell) misses the pair",
      slide_array_two_sum(overwrite_left, overwrite_right, 33, mod_seven, 7) is None)
check("chained table with the same x mod 7 finds (16, 17)",
      chained_two_sum(overwrite_left, overwrite_right, 33,
                      hash_function=mod_seven, slot_count=7) == (16, 17))


# =====================================================================
# 7. RANDOM CHECKS AGAINST BRUTE FORCE
# =====================================================================
# Positive values (slide 5), small range so pairs exist about half the time.
# Compare YES/NO only: methods may find different pairs when several work.
# Every pair returned is also checked to really add up to the target.
#
# The slide 8 array is tested for the one thing it does guarantee: when h
# collides, a Yes is still right, but a No may be wrong.

print("\n" + "=" * 78)
print("RANDOM CHECKS AGAINST BRUTE FORCE")
print("=" * 78 + "\n")

random_generator = random.Random(52)
trial_count = 20000
mismatch_counts = {"direct access": 0, "chained random": 0, "python set": 0}
invalid_pair_count = 0
slide_array_false_yes = 0
slide_array_false_no = 0

for _ in range(trial_count):
    left_length = random_generator.randint(1, 8)
    right_length = random_generator.randint(1, 8)
    random_left = [random_generator.randint(1, 40) for _ in range(left_length)]
    random_right = [random_generator.randint(1, 40) for _ in range(right_length)]
    random_target = random_generator.randint(2, 80)

    expected_found = brute_force_two_sum(random_left, random_right, random_target) is not None
    results = {
        "direct access": direct_access_two_sum(random_left, random_right, random_target),
        "chained random": chained_two_sum(random_left, random_right, random_target, random_generator),
        "python set": set_two_sum(random_left, random_right, random_target),
    }
    for method_name, pair in results.items():
        if (pair is not None) != expected_found:
            mismatch_counts[method_name] += 1
        if pair is not None and not is_valid_pair(pair, random_left, random_right, random_target):
            invalid_pair_count += 1

    slide_pair = slide_array_two_sum(random_left, random_right, random_target, mod_seven, 7)
    if slide_pair is not None and not expected_found:
        slide_array_false_yes += 1
    if slide_pair is None and expected_found:
        slide_array_false_no += 1

for method_name, mismatch_count in mismatch_counts.items():
    check(f"{method_name}: {trial_count - mismatch_count}/{trial_count} agree with brute force",
          mismatch_count == 0)
check("every pair returned really adds up to the target", invalid_pair_count == 0)
check("slide 8 array with x mod 7 never gives a false Yes", slide_array_false_yes == 0)
print(f"      (it gave a false No {slide_array_false_no} times -- the overwrite problem)")

print(f"\n{'ALL PASS' if failure_count == 0 else f'{failure_count} FAILED'}")

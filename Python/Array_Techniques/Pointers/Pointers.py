"""
Standard pointer patterns — one pointer and two pointers.

Notes: [[Pointers — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Pointers — Code Notes.md
"""


# ============================================================================
# PATTERN 1 — ONE POINTER, two sequences, the cursor never rewinds
# ============================================================================

def count_below(sorted_values, sorted_queries):
    """For each query, how many values are strictly less than it.

    Both lists must be sorted ascending. Because the queries only ever grow,
    the answer for a later query can never be smaller than for an earlier one,
    so the cursor never needs to go back to the start.
    """
    # The variables
    #   value_cursor  how many values are known to be < the query being handled
    #                 (also the index of the first value NOT yet counted)
    #   counts        one answer per query, in query order
    value_cursor = 0
    counts = []

    for query in sorted_queries:
        while value_cursor < len(sorted_values) and sorted_values[value_cursor] < query:
            value_cursor += 1
        counts.append(value_cursor)

    return counts


# ============================================================================
# PATTERN 2 — TWO POINTERS, two sorted sequences, one step each turn
# ============================================================================

def merge_sorted(left, right):
    """Merge two ascending lists into one ascending list.

    The merge step of merge sort. Exactly one pointer advances per iteration,
    so the total work is len(left) + len(right), never their product.
    """
    # The variables
    #   left_index   next item not yet taken from left
    #   right_index  next item not yet taken from right
    #   merged       the output, built in order
    left_index = 0
    right_index = 0
    merged = []

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:      # <= keeps equal items in left's order (stable)
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # one side is now exhausted; the other is already sorted and all of it is larger
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


# ============================================================================
# PATTERN 3 — TWO POINTERS, one sorted sequence, converging from both ends
# ============================================================================

def find_pair_with_sum(sorted_values, target):
    """Return the indices of two values that add to target, or None.

    Works because the list is sorted: if the current pair is too big, the only
    way to shrink it is to lower the high end; if too small, raise the low end.
    Each step eliminates one candidate permanently.
    """
    # The variables
    #   low_index   index of the smallest value still in play
    #   high_index  index of the largest value still in play
    low_index = 0
    high_index = len(sorted_values) - 1

    while low_index < high_index:
        total = sorted_values[low_index] + sorted_values[high_index]
        if total == target:
            return (low_index, high_index)
        elif total < target:
            low_index += 1          # need a bigger sum
        else:
            high_index -= 1         # need a smaller sum

    return None


# ============================================================================
# PATTERN 4 — TWO POINTERS, two sorted VIEWS of the same data (a sweep line)
# ============================================================================
# Notes: [[Pointers — Code Notes#Pattern 4 — two pointers, two sorted views of the same data (a sweep line)]] (where it came from)

# A license is a 3-field list. These constants name the fields, so that nothing
# below ever reads a bare row[0] / row[1] / row[2] and leaves you guessing.
DATE_LICENSE_STARTS = 0      # first day the license is valid,          as yyyymmdd
DATE_LICENSE_EXPIRES = 1     # first day it is NO LONGER valid,         as yyyymmdd
NAME_OF_COMPANY = 2          # unused here, listed so the layout is complete

# Why yyyymmdd integers: written in that order, a plain integer comparison IS a
# chronological comparison (20250105 < 20250107), so leap years, month lengths
# and date parsing never enter into it.
#
# Why EXPIRES is exclusive: a license valid up to but not including its expiry
# date means two licenses overlap exactly when
#     start_of_A < expiry_of_B  and  start_of_B < expiry_of_A
# which is why the comparison below is a strict "<" and not "<=". A license
# expiring on the same morning another one starts does not count as an overlap.


def busiest_day(licenses_sorted_by_start, licenses_sorted_by_expiry):
    """How many licenses are valid at once on the busiest day, and which day that is.

    Notes: [[Pointers — Code Notes#busiest_day]]
    """
    # The variables
    #   index_of_next_license_to_start   position in the by-start view: the next
    #                                    license whose start-event has not been played
    #   index_of_next_license_to_expire  position in the by-expiry view: the next
    #                                    license whose expiry-event has not been played
    #   licenses_valid_right_now         running count of open licenses at the
    #                                    moment the sweep has reached
    #   most_licenses_valid_at_once      the largest value that count has ever held
    #   date_of_busiest_day              the date on which it held that value
    index_of_next_license_to_start = 0
    index_of_next_license_to_expire = 0
    licenses_valid_right_now = 0
    most_licenses_valid_at_once = 0
    date_of_busiest_day = 0          # stays 0 when the input is empty

    while (index_of_next_license_to_start < len(licenses_sorted_by_start)
           and index_of_next_license_to_expire < len(licenses_sorted_by_expiry)):

        # The two licenses currently under the pointers. Pulling them out as
        # named rows is what removes the [ ][ ] double-subscript from the test.
        next_license_to_start = licenses_sorted_by_start[index_of_next_license_to_start]
        next_license_to_expire = licenses_sorted_by_expiry[index_of_next_license_to_expire]

        # The only two dates the comparison actually cares about.
        date_next_license_starts = next_license_to_start[DATE_LICENSE_STARTS]
        date_next_license_expires = next_license_to_expire[DATE_LICENSE_EXPIRES]

        if date_next_license_starts < date_next_license_expires:
            # The next event in time is an OPENING: one more license goes valid
            # before anything currently valid runs out.
            licenses_valid_right_now += 1

            # A record can only ever be set on an opening, never on a closing,
            # so this check lives in this branch alone.
            if licenses_valid_right_now > most_licenses_valid_at_once:
                most_licenses_valid_at_once = licenses_valid_right_now
                date_of_busiest_day = date_next_license_starts

            index_of_next_license_to_start += 1
        else:
            # The next event in time is a CLOSING: a license expires before (or
            # on the same day as) the next one starts, so the count drops.
            licenses_valid_right_now -= 1
            index_of_next_license_to_expire += 1

    # The loop ends as soon as the by-start view is exhausted. Everything left
    # in the by-expiry view is a closing, and closings only ever lower the
    # count, so no record can be hiding in the tail - nothing is missed.
    return most_licenses_valid_at_once, date_of_busiest_day


def licenses_valid_on(licenses, date):
    """Every company whose license covers `date`, sorted by name.

    The companion step to busiest_day: that returns the day, this says who was
    on the road that day. Expiry is exclusive, hence <= start and > expiry.
    """
    names_of_companies_valid_on_that_day = []

    for license_record in licenses:
        starts_on_or_before_date = license_record[DATE_LICENSE_STARTS] <= date
        expires_after_date = license_record[DATE_LICENSE_EXPIRES] > date
        if starts_on_or_before_date and expires_after_date:
            names_of_companies_valid_on_that_day.append(license_record[NAME_OF_COMPANY])

    return sorted(names_of_companies_valid_on_that_day)


# Notes: [[Pointers — Code Notes#How it runs]] (traces of all four functions)


print(count_below([10, 20, 30, 40], [15, 25, 100]))  # [1, 2, 4] — cursor ends at 4, having moved forward only
print(count_below([10, 20, 30, 40], [5]))  # [0] — every value is bigger, cursor never moves
print(count_below([], [1, 2]))  # [0, 0] — no values at all, the bounds guard stops the while immediately
print(count_below([10, 20], [20, 20]))  # [1, 1] — strictly less, so 20 does not count itself

print(merge_sorted([2, 4, 5], [1, 3, 6]))  # [1, 2, 3, 4, 5, 6] — the classic interleave
print(merge_sorted([], [1, 2]))  # [1, 2] — empty side, loop never runs, extend does the work
print(merge_sorted([1, 2], []))  # [1, 2] — same in mirror
print(merge_sorted([1, 1], [1]))  # [1, 1, 1] — ties all kept, left first

print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 10))  # (2, 3) — 4 + 6
print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 12))  # (0, 5) — 1 + 11, found on the first step
print(find_pair_with_sum([1, 3, 4, 6, 8, 11], 100))  # None — pointers meet without a hit
print(find_pair_with_sum([5], 10))  # None — one element, low_index < high_index is false immediately

# the Themis 2B example, dates already turned into yyyymmdd integers
example_licenses = [
    [20250101, 20250110, "SuperBus"],
    [20250103, 20250107, "UltraBus++"],
    [20250105, 20250109, "Buzzzer"],
    [20241221, 20250102, "Hector's bus company"],
]
example_by_start = sorted(example_licenses, key=lambda row: row[DATE_LICENSE_STARTS])
example_by_expiry = sorted(example_licenses, key=lambda row: row[DATE_LICENSE_EXPIRES])

print(busiest_day(example_by_start, example_by_expiry))  # (3, 20250105) — the worked trace above
print(licenses_valid_on(example_licenses, 20250105))  # ['Buzzzer', 'SuperBus', 'UltraBus++'] — the three, by name
print(busiest_day([], []))  # (0, 0) — no licenses, the bounds guard stops the while immediately
print(busiest_day([[20250101, 20250102, "Solo"]], [[20250101, 20250102, "Solo"]]))  # (1, 20250101) — one license is its own busiest day

# back-to-back licenses: one expires the morning the next starts, so they never overlap
touching = [[20250101, 20250105, "Early"], [20250105, 20250110, "Late"]]
print(busiest_day(sorted(touching, key=lambda row: row[DATE_LICENSE_STARTS]),
                  sorted(touching, key=lambda row: row[DATE_LICENSE_EXPIRES])))  # (1, 20250101) — exclusive expiry, no overlap

"""
KADANE'S ALGORITHM -- maximum subarray in O(n)

Input:   a list of numbers (at least one)
Output:  the largest sum of any CONTIGUOUS, non-empty slice of it

    [-2, 1, -3, 4, -1, 2, 1, -5, 4]  ->  6    (the slice 4, -1, 2, 1)
"""

# Notes: [[Kadane — Code Notes#The key question]] (the two variables)

#=== plan in comments first, then the code under it===
# Notes: [[Kadane — Code Notes#My plan]]

def kadane(values):
    """
    This version outputs the LARGEST SUM OF ANY CONTIGUOUS SEQUENCE OF NUMBERS
    Not their locations!
    """
    # set them to -inf so there is never something smaller to begin with
    # so on the first pass the else (start fresh) always runs: -inf + values[i] is still -inf
    best_ending_here = float("-inf")
    best_so_far = float("-inf")

    for i in range(0, len(values)):

        # step 1:
        # EXTEND: if the slice ending one step back plus the current value
        # beats starting over with the current value alone
        if best_ending_here + values[i] >= values[i]:
            best_ending_here = best_ending_here + values[i]
        else:
            # START FRESH: if the current value alone beats extending
            # (the slice behind has a negative sum, so it can only hurt)
            best_ending_here = values[i]

        # step 2: new high score?
        if best_ending_here > best_so_far:
            best_so_far = best_ending_here
    # return the sum of the highest value sequence
    return best_so_far



def kadane_locate(values):
    """
    This version outputs the LARGEST SUM OF ANY CONTIGUOUS SEQUENCE OF NUMBERS and THEIR LOCATIONS
    """
    # set them to -inf so there is never something smaller to begin with
    # so on the first pass the else (start fresh) always runs: -inf + values[i] is still -inf
    best_ending_here = float("-inf")
    best_so_far = float("-inf")

    positions = []
    best_positions =[ ]
    for i in range(0, len(values)):
        # step 1:
        # EXTEND: if the slice ending one step back plus the current value
        # beats starting over with the current value alone
        if best_ending_here + values[i] >= values[i]:
            best_ending_here = best_ending_here + values[i]
            positions.append(i)
        else:
            # START FRESH: if the current value alone beats extending
            # (the slice behind has a negative sum, so it can only hurt)
            best_ending_here = values[i]
            # it should already include i when it rests
            positions = [i]

        # step 2: new high score?
        if best_ending_here > best_so_far:
            best_so_far = best_ending_here
            best_positions =[]
            best_positions.extend(positions)
    # return the sum of the highest value sequence and its begining and ending positions
    return best_so_far, best_positions[0], best_positions[-1]


# --- tests: run with  python Kadane.py ---

test_cases = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),  # the classic
    ([1, 2, 3], 6),  # all positive: take everything
    ([5], 5),  # a single element
    ([-3, -1, -2], -1),  # all negative: the answer is not 0
    ([2, -1, 2], 3),  # a dip worth crossing
    ([2, -5, 3], 3),  # a dip NOT worth crossing
]

for values, expected in test_cases:
    result = kadane(values)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}  kadane({values}) = {result}, expected {expected}")


# --- kadane_locate tests: expected is (sum, start index, end index) ---

locate_test_cases = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], (6, 3, 6)),  # the slice 4, -1, 2, 1
    ([1, 2, 3], (6, 0, 2)),  # the whole list
    ([5], (5, 0, 0)),  # the only element
    ([-3, -1, -2], (-1, 1, 1)),  # just the -1
    ([2, -1, 2], (3, 0, 2)),  # the whole list, dip included
    ([2, -5, 3], (3, 2, 2)),  # just the 3
]

print()
for values, expected in locate_test_cases:
    result = kadane_locate(values)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}  kadane_locate({values}) = {result}, expected {expected}")

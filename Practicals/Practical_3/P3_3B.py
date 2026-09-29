"""
Context:
    Ivan has n cards lying in a row, each with an integer written on it.
    he marks some of them red.

variables:
    n: number of cards
    a: the cards, left to right
    f: f[i] = longest non-decreasing run that can start at card i (level)
    tails: tails[index] = lowest -a that ends a run of length index + 1 (always sorted)
    L: the most red cards possible (first number printed)
    neg: every -a[i], grouped by level
    start: level k is neg[start[k]:start[k + 1]]
    first: the red card all the way to the left
    cur: the latest red card picked
    red-score: cur - first (second number printed)

Marking rules:
    1- Left to right, the red nunbers never go down
        Equal is allowed: 4, 4, 5 is fine
        !cards in between don't matter
    2- Mark as many cards as possible
    3- Tie: lexicorgaphically smallest
        first red number as small as possible, then the second, and so on
    4- Still a tie: any of them (the answer is the same)

the Algorithm:
    right to left, fill f
        !we scan right to left, so negate (-a):
            a run going up left to right then also goes up in scan order
    group the cards by level (counting sort)
        One level is sorted: a card can't be <= a card to its right on the same level
        (it would then start a longer run)
    Walk down the levels, always taking the smallest card that still fits
        !the smallest valid card is also the one all the way to the right, so it always is after the previous pick

Question:
    How many cards does Ivan mark red, and what is his red-score?

Input: a line containing n, followed by one line of n numbers (the cards)
    Example:
        11 (n)
        4 3 5 4 8 12 6 27 33 29 5
    Output: 6 26

Output: the count and the red-score, separated by a space

Constraints:
• In each test case:
    * 1 ≤ n ≤ 4 000 000
    * -100 000 000 ≤ number on a card ≤ 100 000 000
• CPU time limit: 2 seconds per test case.
• Memory limit: 256 MiB per test case.
"""

# #==== COMMENT B4 SUBMISSION =====
# import sys
# import os

# if sys.stdin.isatty():
#     here = os.path.dirname(os.path.abspath(__file__))
#     sys.stdin = open(os.path.join(here, "3B_Sample.txt"))

# #====================================
from array import array #C ints: exactly 4 bytes each


#==== Input ====


def read_ints(line):
    a = array('i')
    CHUNK = 2 ** 20 #characters per piece
    start, length = 0, len(line)
    while start < length:
        end = min(start + CHUNK, length)
        if end < length:  # not the last piece
            cut = line.rfind(' ', start, end)
            if cut > start:
                end = cut
        a.extend(map(int, line[start:end].split()))
        start = end
    return a

#================


def card_game():
    n = int(input())
    a = read_ints(input())

    #fill f, right to left
    f = array('i', bytes(4 * n))  # n zeros
    tails = array('i')
    size = 0  #len(tails), saves a len() call per card
    for i in range(n - 1, -1, -1):
        b = -a[i]
        if size == 0 or tails[size - 1] <= b:   # b extends the longest run, no search needed
            tails.append(b)
            size += 1
            f[i] = size
            continue
        # binary search
        #  first index with tails[index] > b 
        # (ends up in lo)
        lo, hi = 0, size - 1  # tails[size - 1] > b is already known
        while lo < hi:
            mid = (lo + hi) >> 1  # (lo + hi) // 2
            if tails[mid] <= b:
                lo = mid + 1
            else:
                hi = mid
        tails[lo] = b  # better (lower) end for a run of length lo + 1
        f[i] = lo + 1
    L = size

    #group -a by level (counting sort)
    start = array('i', bytes(4 * (L + 2)))
    for k in f:  # count the cards on each level
        start[k + 1] += 1
    for k in range(1, L + 2): #counts - where each level begins
        start[k] += start[k - 1]
    fill = array('i', start) # next free slot per level
    neg = array('i', bytes(4 * n))
    for i in range(n):
        k = f[i]
        neg[fill[k]] = -a[i]
        fill[k] += 1
    del f, fill, a # free memory

    #greedy walk down the levels
    first = -neg[start[L + 1] - 1] #smallest card on the top level
    cur = first
    for k in range(L - 1, 0, -1):
        # binary search in level k: first index with neg[index] > -cur (ends up in lo)
        x = -cur
        lo, hi = start[k], start[k + 1]
        while lo < hi:
            mid = (lo + hi) >> 1
            if neg[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        cur = -neg[lo - 1] # one to the left: smallest a >= cur

    #==== Output ====
    print(L, cur - first)


card_game()

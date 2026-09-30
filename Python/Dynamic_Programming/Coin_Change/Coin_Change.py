"""
COIN CHANGE -- fewest coins to make an amount (DP)

Input:   a list of coin values (each available as many times as you like)
         and a target amount
Output:  the fewest coins that add up to exactly the amount,
         or -1 if no combination of coins can make it

    coins [1, 2, 5], amount 11  ->  3    (5 + 5 + 1)
"""


def coin_change(coins, amount):
    # plan in comments first, then the code under it

    pass


# --- tests: run with  python Coin_Change.py ---

test_cases = [
    ([1, 2, 5], 11, 3),  # the classic: 5 + 5 + 1
    ([1, 3, 4], 6, 2),  # 3 + 3: "biggest coin first" gives 4 + 1 + 1 = 3
    ([2], 3, -1),  # impossible: only even amounts
    ([1], 0, 0),  # amount 0 needs no coins
    ([2, 5, 10], 7, 2),  # 5 + 2: no 1-coin to fall back on
    ([186, 419, 83, 408], 6249, 20),  # big amount: brute force is too slow here
]

for coins, amount, expected in test_cases:
    result = coin_change(coins, amount)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}  coin_change({coins}, {amount}) = {result}, expected {expected}")

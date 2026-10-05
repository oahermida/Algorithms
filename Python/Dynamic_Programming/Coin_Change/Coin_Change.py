"""
COIN CHANGE -- fewest coins to make an amount (DP)

Input:   a list of coin values (each available as many times as you like)
         and a target amount
Output:  the fewest coins that add up to exactly the amount,
         or -1 if no combination of coins can make it

    coins [1, 2, 5], amount 11  ->  3    (5 + 5 + 1)

Constraints:
    * HOW MANY different coins: 1 to 12
        e.g. coins = [1, 2, 5] has 3 different coins
    * HOW BIG each coin is: any positive whole number, no size repeats
        e.g. test 6 has a coin worth 419
    * 0 <= amount <= 10 000
    * unlimited supply: any coin can be used any number of times
    * there is not always a 1-coin, so some amounts can't be made (-> -1)

    i get a list of coins values of coin values (coins) and a taget amount (amount)
    there are between 1 and 12 DIFFERENT coins (len(coins)), each can be any size
    amount is 0 or more (amount 0 -> 0 coins)
    unlimited supply

    ==========================================================
    my first guess is a quick check comparing the target to the value of the largest coin
    if its equal, its just one of that coin
    if its lower, we check with the smaller and continue until the smallest value
    if its higher well then the main code runs

    potentially, i could run a similar drill with the highest value coin, but this time checking if the target can be divisable by it
    if yes, then its just the result of that division
    if no, then we check whats the closest number that i can get to with the highest coin
    from there, i get a smaller target number, kinda like target2
    i could repeat the process until i can reach that number
    -------------------------------------------------------------------------
    WRONG: biggest-coin-first can use more coins than needed (coins [1, 3, 4], amount 6: 4+1+1 = 3 coins, but 3+3 = 2)
    ======================================================================
    HINT: suppose someone hands you a cheat sheet with the fewest coins
    for every amount SMALLER than your target (coins [1, 3, 4]):

        amount        0  1  2  3  4  5  6
        fewest coins  0  1  2  1  1  2  ?

    To make 6, there has to be a LAST coin you drop in: a 1, a 3 or a 4.
        - If the last coin is a 3, what amount did you have BEFORE it?
          How many coins did that take, according to the sheet?
        - Same question for 1 and for 4.
        - Which of the three is best?

    Once you can fill in the ?, the rest follows: YOU build the cheat sheet,
    left to right, starting at 0. Same move as Kadane: there each position
    reused the answer one step back, here each amount reuses the answers
    for SMALLER amounts.
    ======================================================================
    second idea, with said cheat sheet
    then we would start with 0, which is already fixed
    then 1, which assuming there is a 1, its just one. otherwise it's impossible and position 1 should be -1
    then 2, which is either 2 or two 1s, otherwise it's -1
    from then on i get diminishing returns from this workflow.
    but i still need to build the table
    for 3 i would check if 2 is higher than -1
    if so, it would be 2   
        plus one coin if any coin gets exactly there
            but what if you have only 5s and 1s, if 4 was 4 1s, 
            then the new solution isnt adding one 1, its changing the coins to a 5 
            so it would first have to check something else
            if the previous value's result can be "compressed" now that the target is higher
                the compression would go something like:
                with coins 1 5 10
                target: 5
                previous result: four 1s
                we should check if a higher denomination can get to the target exactly
                first with 10
                then with 5
                then the result would be 1 coin of 5
                if i follow this logic for every number along the way, i would always have the right combo

    ======================================================================
    THE METHOD IN PLAIN WORDS

    1. Make a cheat sheet with one box for every amount from 0 up to the
       target. Each box will hold the fewest coins needed to pay exactly
       that amount.

    2. The box for 0 holds 0, because paying nothing takes no coins.
       Mark every other box "impossible" for now.

    3. Fill the boxes one at a time, from small amounts to big ones.
       For the amount you're working on:
        - Go through your coins one by one, and imagine that coin is the
          LAST one you hand over.
        - If the coin is bigger than the amount, skip it: it can't be
          part of the payment.
        - Otherwise, work out how much you'd have paid BEFORE that last
          coin: the amount minus the coin's value.
        - Look up that smaller amount's box. It's already filled, because
          you work from small to big.
        - If that box says "impossible", this coin doesn't lead anywhere,
          so skip it.
        - Otherwise, the total for this option is that box's number plus
          one, for the last coin itself.
        - Once every coin has been tried, write the SMALLEST total you
          found into the box. If no coin worked, the box stays "impossible".

    4. When the target's box is filled, that's the answer. If it still
       says "impossible", the answer is -1.

    Example, amount 6 with coins 1, 3 and 4:
        last coin 1: paid 5 before it, box 5 says 2 -> this option costs 3
        last coin 3: paid 3 before it, box 3 says 1 -> this option costs 2
        last coin 4: paid 2 before it, box 2 says 2 -> this option costs 3
        smallest is 2, so box 6 gets 2

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

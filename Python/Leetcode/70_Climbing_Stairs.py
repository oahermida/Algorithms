"""
LeetCode 70 -- Climbing Stairs
LeetCode problem 70.

Notes: [[LeetCode 70 Climbing Stairs — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/LeetCode 70 Climbing Stairs — Code Notes.md
"""
import math
# math.factorial(5)

# Notes: [[LeetCode 70 Climbing Stairs — Code Notes#Counting the orderings with factorials]] (formula, variables, check)
target = 8

def naive_way(target):
    """
    The naive way to solve it
    """
    ways = 0
    combo = []
    all_combos = []
    
    only_twos = target // 2 #this is the ammount of 2s i need to get as close as possible to the target
    missing_ones = []
    used_twos = []
    i = 0
    twos_in_combo = 0
    ones_in_combo = 0
    l_twos_in_combo = []
    l_ones_in_combo = []
    
    while only_twos >= 0:
        #at the current amount of use of 2, we save them
        #and by how many ones we are short
        used_twos.append(only_twos)
        missing_ones.append(target - (only_twos*2))

        #at the current amount of use of 2, we add them to the combo list
        for _ in range(used_twos[i]):
            combo.append(2)
            twos_in_combo += 1
        #and the missing ones
        for _ in range(missing_ones[i]):
            combo.append(1)
            ones_in_combo += 1
        #get one less two for the next round
        only_twos -= 1
        #save to the collection of combos
        all_combos.append(combo)
        combo = []
        #save how many ones and twos i used for each combo
        l_twos_in_combo.append(twos_in_combo)
        twos_in_combo = 0
        l_ones_in_combo.append(ones_in_combo)
        ones_in_combo = 0
        #reset i
        i += 1
    for twos, ones in zip(l_twos_in_combo, l_ones_in_combo):
        moves = twos + ones
        ways += math.factorial(moves) // (math.factorial(twos) * math.factorial(ones))




    return ways



class Solution(object):
    def climbStairs(self, n):
        """
        DP version

        Notes: [[LeetCode 70 Climbing Stairs — Code Notes#DP version]]
        """
        if n == 1:
            return 1
        steps = [1,2]
        while n > len(steps):
            steps.append(steps[-1]+steps[-2])
        return steps[-1]
        

    def climbStairsConstantSpace(self, n):
        """
        DP version with O(1) space: each value only needs the two before it,
        so keep those two in variables instead of the whole list
        """
        previous, current = 1, 1  # ways to reach 0 stairs, ways to reach 1 stair
        for _ in range(n - 1):
            previous, current = current, previous + current
        return current

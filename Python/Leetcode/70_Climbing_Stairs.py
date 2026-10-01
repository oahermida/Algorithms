"""
You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1:

Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:

Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

Constraints:
    1 <= n <= 45

one off method:
if i want to calculate the ways that there are to get 50 with 5s and 1s
i have to first calculate how many 5s fit at most
50/5=10 a whole number, so it is possible
but, i could also do it with 9 5s and 5 1s
also with 8 5s and 10 1s
and so on
untill i get to 50 1s

if i want to calculate how many ways are there to get to 49 now 
i would check dividing it by 5 again and see that it is not round
i could use the result of a flored division to see the closest i can get to it with 5s
then i would subtract the closest amount i can get to from 50
and fill that ammount with 1s
from there resume the logic of the previous paragraph

if the order of 5s and 1s is taken into account, then i would also need to count the amount of permutation

thinking of it as if i had to solve it without dp:
getting to:
1- one way (1)
2- two ways (2, 1+1)
3- two ways (2+1, 1+1+1)
4- three ways (2+2, 2+1+1, 1+1+1+1)
5- three ways (2+2+1, 2+1+1+1, 1+1+1+1+1)
6- four ways (2+2+2, 2+2+1+1, 2+1+1+1+1, 1+1+1+1+1+1)
7- four ways (2+2+2+1, 2+2+1+1+1, 2+1+1+1+1+1, 1+1+1+1+1+1+1)
it feels like its always going to be that patter of 2,2,3,3,4,4 etc
but this doesnt account for ordering

in each individual case i can think of every unpermutated solution as a list
i could build a list of list with the unpermuated lists
then i calculate the possible permutations of each and add them up

DP
you create an array listing in how many ways you can reach the previous value
for 1, it's only one (1 combo)


"""
import math
# math.factorial(5)

#  If some numbers repeat: divide by the factorial of each repeat count.
#   n! / (count₁! × count₂! × …)
#
#  For this problem the only repeated values are 2s and 1s, so there are two counts:
#   twos: how many 2-steps the climb uses, from n // 2 down to 0
#   ones: the 1-steps that fill the rest, n - 2 * twos
#   moves: how many steps the climb takes in total, twos + ones
#  For each value of twos, the orderings of that one combination are
#   moves! / (twos! × ones!)
#  Add those up over every value of twos to get the answer.
#  Use // for the division so the result stays an int.
#  Check, n = 4: twos 2 -> 2!/(2!·0!) = 1, twos 1 -> 3!/(1!·2!) = 3, twos 0 -> 4!/(0!·4!) = 1, total 5
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

        getting to:
        1- one way (1)
        2- two ways (2, 1+1)
        3- two ways (2+1, 1+1+1)
        4- three ways (2+2, 2+1+1, 1+1+1+1)
        5- three ways (2+2+1, 2+1+1+1, 1+1+1+1+1)
        6- four ways (2+2+2, 2+2+1+1, 2+1+1+1+1, 1+1+1+1+1+1)
        7- four ways (2+2+2+1, 2+2+1+1+1, 2+1+1+1+1+1, 1+1+1+1+1+1+1)
        it feels like its always going to be that patter of 2,2,3,3,4,4 etc

        getting to, counting every ordering:
        1- one way (1)
        2- two ways (2, 1+1)
        3- three ways (2+1, 1+2, 1+1+1)
        4- five ways (2+2, 2+1+1, 1+2+1, 1+1+2, 1+1+1+1)
        5- eight ways (2+2+1, 2+1+2, 1+2+2, 2+1+1+1, 1+2+1+1, 1+1+2+1, 1+1+1+2, 1+1+1+1+1)
        6- thirteen ways (2+2+2, 2+2+1+1, 2+1+2+1, 2+1+1+2, 1+2+2+1, 1+2+1+2, 1+1+2+2, 2+1+1+1+1, 1+2+1+1+1, 1+1+2+1+1, 1+1+1+2+1, 1+1+1+1+2, 1+1+1+1+1+1)
        7- twenty-one ways (2+2+2+1, 2+2+1+2, 2+1+2+2, 1+2+2+2, 2+2+1+1+1, 2+1+2+1+1, 2+1+1+2+1, 2+1+1+1+2, 1+2+2+1+1, 1+2+1+2+1, 1+2+1+1+2, 1+1+2+2+1, 1+1+2+1+2, 1+1+1+2+2, 2+1+1+1+1+1, 1+2+1+1+1+1, 1+1+2+1+1+1, 1+1+1+2+1+1, 1+1+1+1+2+1, 1+1+1+1+1+2, 1+1+1+1+1+1+1)
        the pattern is 1, 2, 3, 5, 8, 13, 21: each number is the two before it added up

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

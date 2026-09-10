"""
Grading formula:
    E^2 + E * A + M^2 + M * A = F
    Cleaner: (E^2) + (E*A) + (M^2) + (M*A) = F

Explanation of the formula:
    E: Final exam grade
    A: Assignment grade
    M: Midterm grade
    F: Final computed grade

Input:
    n: an int and k: a grade
    3 arrays of lenght n:
        Each array will be placed on its own separate line
        A1: Contains the values for E
        A2: Contains the values for A
        A3: Contains the values for M
        They are not necessarily in the same order (e.g, the first grades in each array do not necessarily belong to the same student). 
        Grades will always have at most one decimal point. (Though they will not be necessarily bound to being between 1 and 10
An example input: 
    4 380.0
    3.1 4.9 2.1 10.0
    1 3.3 9 3.4
    10.0 9.3 1.1 8

Output: 
    You should print out "IMPOSSIBLE", should there be no combination which can create the desired grade, 
    otherwise you should print out "POSSIBLE" followed by the numbers plugged into the formula.
    There will always be at most one solution within all numbers. 
    Numbers should always be printed with one decimal of accuracy (even if they are integers!).
        POSSIBLE 
        10.0^2 + 10.0*9.0 + 10.0^2 + 10.0*9.0 = 380.0
        Explanation:
        you pick the values of 10.0, 9 and 10.0 for the values of E, A and M respectively. 
        Plugging these into the formula yields 380, which is the number were looking for. 
        As such, its possible for us to create the number 380 from the given grades.

Constraints:
    In each test case, 1 ≤ k ≤ 2^58, 1 ≤ n ≤ 2 * 10^4, 0 ≤ Ei, Ai, Mi ≤ 2^20, for all i. 
    CPU time limit: 2 seconds per test case. 
    Memory limit: 4 MiB per test case.

Run with:
cd /home/oscar/Documents/Code/Algorithms/Practicals/Practical_1
python3 P1_1B.py < 1B_Sample.txt

"""

# The plan:
# Translate the input into variables
# Undertand what those constraints mean for my variable types
# Understand the relationship between those variables in the given formula
# 

# === Input ===
A1_E = []
A2_A = []
A3_M = []
# remember that: "the first grades in each array do not necessarily belong to the same student"

nk = input().split()
n = int(nk[0])

# k is also gonna be tricky, floats are only exact up to 2^53 but k can go up to 2^58.
# pythons ints have no limit so im fine here, C wont be.

"""
!!!!!!!!!!!!!!!!!!!!!!!!!THERE MIGHT BE EDGE CASES THAT MESS THIS UP!!!!!!!!!!!!!!!!!!!!!!!!
There are floats all over the place, rounding them into int looses info. doing math with them is wrong cause binary numbers.
Therefore, the only way to deal with this is to instead of doing 3.1 * 4.2 we do 31 * 42.

Every term becomes a grade times a grade, so the formula comes out x100, not x10.
5.3*5.9 = 31.27
53*59 = 3127

==========>       thats why k_scaled should be *100 and not *10 like the arrays.      <==========

Nothing gets divided for the comparison, only right at the end when i print the numbers back out as decimals.
"""
k = nk[1]
k_scaled = round(float(nk[1]) * 100)   # x100


StrA1_E = input().split()
StrA2_A = input().split()
StrA3_M = input().split()

# doing math with floats is a gotcha tho so i need to round
# tho remember "Numbers should always be printed with one decimal of accuracy (even if they are integers!)."

for i in range (n):
    A1_E.append(round(float(StrA1_E[i]) * 10)) # x10
for i in range (n):
    A2_A.append(round(float(StrA2_A[i]) * 10))
for i in range (n):
    A3_M.append(round(float(StrA3_M[i]) * 10))

 

# print(n)
# print(k)
# print(A1_E)
# print(A2_A)
# print(A3_M)

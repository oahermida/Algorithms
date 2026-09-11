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



# k is also gonna be tricky, floats are only exact up to 2^53 but k can go up to 2^58.
# pythons ints have no limit so im fine here, C wont be.


# !!!!!!!!!!!!!!!!!!!!!!!!!THERE MIGHT BE EDGE CASES THAT MESS THIS UP!!!!!!!!!!!!!!!!!!!!!!!!
# There are floats all over the place, rounding them into int looses info. doing math with them is wrong cause binary numbers.
# Therefore, the only way to deal with this is to instead of doing 3.1 * 4.2 we do 31 * 42.

# Every term becomes a grade times a grade, so the formula comes out x100, not x10.
# 5.3*5.9 = 31.27
# 53*59 = 3127

# ==========>       thats why k_scaled should be *100 and not *10 like the arrays.      <==========

# Nothing gets divided for the comparison, only right at the end when i print the numbers back out as decimals.
nk = input().split()
n = int(nk[0])
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



# ================================= The Algorithm =================================
# =================================================================================
"""
Input: gotten
Goal:
    I need to know whether some E, A, M from three arrays satisfy E^2 + E*A + M^2 + M*A = k

Looking at the formula, A is the one that multiplies the two other variables on that side of the equation
Fix A and the formula splits into two independent halves: one holding only E, the other only M. A 2-SUM is needed

From now on variable names have to be descriptive or ill loose my shit
E^2 + chosen_A * E      +       M^2 + chosen_A * M      = k
        E side                          M side

side_E and side_M could be the name of the variables in the 2sum

now, this involves many arrays each with multiple options to choose from, 
so i should sketch how i would calculate the different possibilities for side_E and side_M
these arrays should be filled with sorted(A1_E) and sorted(A3_M).
sorted(list) (native python)


The plan:

1. Sort A1_E and A3_M once, before the loop starts.
        Sorting inside the loop would cost n log n per pass and would be game over.

2. The value of chosen_A is set as it loops over A2_A. One pass per candidate A value, SO n PASSES.
        A2_A is NOT sorted, doesnt need to be.

3. Inside a pass, build two arrays side_E and side_M: from (already sorted) E, and (already sorted) M respectively.


4. Two-pointer walk over side_E and side_M, against k_scaled. Two INDICES,
   starting at opposite ends, each only ever moving one way:
       E_low_index: starts at 0, the smallest side_E, and climbs
       M_high_index: starts at the end, the largest side_M, and descends

       side_E[E_low_index] + side_M[M_high_index] vs k_scaled:
           too small: E_low_index += 1 (reach for a bigger side_E)
           too big: M_high_index -= 1 (reach for a smaller side_M)
           equal: bingo, stop

   Either index running off its end means no pair exists FOR THIS chosen_A. The loop just moves on to the next chosen_A.
   IMPOSSIBLE is only true once ALL n passes have run and none of them matched.

5. Themis wants a print. POSSIBLE plus the filled-in formula (i think the formula should go on a separate line) if a pass matched,
    IMPOSSIBLE if none did. 
    !ATTENTION! format:
        1 - grades are x10 ints and must print with one decimal. Use:
            f"{value//10}.{value%10}"
            value//10 (whole part), value%10 (first digit after the ".").
            Note: it never creates a float

        2 - k is the number after the "=" in the printed line. k_scaled is x100
            (not x10 like the grade arrays), so use:
            f"{k_scaled//100}.{(k_scaled//10)%10}"
         
        3 - REMEMBER: no spaces anywhere in the formula line.

Run with:
cd /home/oscar/Documents/Code/Algorithms/Practicals/Practical_1
python3 P1_1B.py < 1B_Sample.txt
"""
# n (int) - grades per array. example: 4
# k (str) - the target as the raw TEXT. For PRINTING only. Scale:   x1 example:    "380.0"
# k_scaled (int) - that same target as an exact integer. For COMPARING only. Scale:    x100 example:    38000
# A1_E (list[int]) - the possible values for E. Scale:  x10 example:     [31, 49, 21, 100]
# A2_A (list[int]) - the possible values for A. Scale:  x10 example:     [10, 33, 90, 34]
# A3_M (list[int]) - the possible values for M. Scale:  x10 example:     [100, 93, 11, 80]
# E^2 + chosen_A * E      +       M^2 + chosen_A * M      = k
#         E side                          M side

# 1 -Sorting
A1_E = sorted(A1_E)
A3_M = sorted(A3_M)
side_E = []
side_M = []

# 2/3 - Looping for Chose A
# god knows how to do this in C
# for i, chosen_A in enumerate(A2_A):
#     side_E.append((A1_E[i]**2)+(chosen_A*A1_E[i]))
#     side_M.append((A3_M[i]**2)+(chosen_A*A3_M[i]))

# Problem: there should be an array for every possible A put in side_E and side_M
# wait no, i dont have to, i can keep adding it to the same array and then determine to which A they belong based on n
# before i fix this: every chosen_A currently being computed with just one E and one M. I have to make every chosen_A compute with every E and M

# for i in range(len(A2_A)):
#     chosen_A = A2_A[i]
#     for E in A1_E:
#         side_E.append((E**2)+(chosen_A*E))
#     for M in A3_M:
#         side_M.append((M**2)+(chosen_A*M))   

#Comes out already sorted, yay
#wait, i can create a list of lists
#that might be too memory inneficient and a pain in the ass to port to C
#so i think this has to go inside the 2-Sum


# grades are stored x10, so 93 -> "9.3" and 100 -> "10.0". Never goes through a float.
def one_decimal(value_x10):
    return f"{value_x10 // 10}.{value_x10 % 10}"


# target is k_scaled
def two_sum(target):
    side_E = []
    side_M = []
    for i in range(len(A2_A)):
        chosen_A = A2_A[i]
        if len(side_E) == n: #or side_m
            side_E = []
            side_M = []
        for E in A1_E:
            side_E.append((E**2)+(chosen_A*E))
        for M in A3_M:
            side_M.append((M**2)+(chosen_A*M)) 
        E_low_index = 0
        M_high_index = n -1
        while E_low_index < len(side_E) and M_high_index >= 0:
            left_value = side_E[E_low_index]
            right_value = side_M[M_high_index]
            paired_total = left_value + right_value

            if paired_total == target:
                # side_E was built from A1_E in order, so the same index gives back the grade
                E_text = one_decimal(A1_E[E_low_index])
                A_text = one_decimal(chosen_A)
                M_text = one_decimal(A3_M[M_high_index])
                # k from k_scaled (x100), not the raw text, so an input like "380" still prints "380.0"
                k_text = f"{k_scaled // 100}.{(k_scaled // 10) % 10}"
                print("POSSIBLE")
                print(f"{E_text}^2+{E_text}*{A_text}+{M_text}^2+{M_text}*{A_text}={k_text}")
                return
            if paired_total < target:
                E_low_index += 1
            else:
                M_high_index -= 1
    print("IMPOSSIBLE")

"""
if im not mistaken, this is a O(n^2)
"""
# === Output ===
two_sum(k_scaled)

"""
Context:
    There is a tunnel that will get very busy with busses. 
    The authorities want to know on which day is the number of valid licenses the largest.
Variables:

Input:
    Number n followed by n lines
        Each line contains the info of one license that is given out:
            The first day on which the license is valid.(dd.mm.yyyy)                    
            The first day it's no longer valid (expires)
            Name of the company owning the license
    Example:
        4
        01.01.2025 10.01.2025 SuperBus
        03.01.2025 07.01.2025 UltraBus++
        05.01.2025 09.01.2025 Buzzzer
        21.12.2024 02.01.2025 Hector's bus company

Output:
    Busiest day: 05.01.2025
    Buzzzer
    SuperBus
    UltraBus++
    You must always print a newline at the end of the output. This is also the case for all future exercises in this course (and most other courses).

Constraints:
    All:
        - In all test cases, 1 ≤ n ≤ 200 000.
        - The names of bus companies consist only of alphabetic letters (both upper- and lowercase) and the characters ‘+’, ‘-’, ‘$’, ‘%’, ‘ ’ (space), ‘'’ (ASCII 39), and ‘!’.
        Company names do not start or end with a space.
        - The name of each company is at most 20 characters long.
        - Each license is valid for at least one full day.
        - All dates in the input are between 01.01.2000 and 31.12.2999, inclusive.
        - You should take leap years into account. Please note that this is not as hard as it might seem.
        - There is no bus company that has acquired more than one license (that is, a bus company cannot appear multiple times in the input).
        - CPU time limit: 1 second per test case. • Memory limit: 256 MiB per test case.
    Most importantly for python:
        - Each license is valid for at least one full day.
        - All dates in the input are between 01.01.2000 and 31.12.2999, inclusive.
        - You should take leap years into account. Please note that this is not as hard as it might seem.
        - There is no bus company that has acquired more than one license (that is, a bus company cannot appear multiple times in the input).

"""

"""
How to calculate if dates overlap:
    When checking 2: sd(start date) ed(expired, so not incl)
        (sd1 <= sd2 and ed1 > sd2) or (sd2<=sd1 and ed2>sd1)
        or
        sd1 < ed2 and sd2 < ed1 

How to order dates:
turn them (or consider them) as yyyy.mm.dd

How to handle the input:
n = int(first input())
after n, split() is sure to always get 2 strings sd1 ed1 first
if the name of the company doesnt have spaces (i.e. len = 3) we're good
if name of the company has spaces, (i.e.len > 3) then A[0] and A[1] are sd1 and ed1 and the rest should be merged as a single string adding the spaces in between)
.split(maxsplit=2) does it
"""

# # #==== COMMENT B4 SUBMISSION =====
# import sys
# import os

# if sys.stdin.isatty():
#     here = os.path.dirname(os.path.abspath(__file__))
#     sys.stdin = open(os.path.join(here, "2Bexample.txt"))

# # #====================================

# ==== Input ====
n = int(input())
lines = []
for i in range(n):
    lines.append(input().split(maxsplit=2))
    lines[i][0] = lines[i][0][6:]+lines[i][0][3:5]+lines[i][0][:2]
    lines[i][0] = int(lines[i][0])
    lines[i][1] = lines[i][1][6:]+lines[i][1][3:5]+lines[i][1][:2]
    lines[i][1] = int(lines[i][1])


start_s_lines = sorted(lines, key=lambda row: row[0]) #sort by whose license begins first


end_s_lines= sorted(lines, key=lambda row: row[1])

def double_pointer(left, right):
    left_index = 0
    right_index = 0
    counter = 0
    best_counter = 0
    date_b_c = 0 #start date of the best_counter coming from the start_s_lines
    while left_index < len(left) and right_index < len(right):
        if left[left_index][0] < right[right_index][1]: # if the *start time* of *start_s_lines[left_index]* < *end time* of *end_s_lines[right_index]*    
            counter +=1
            if counter > best_counter:
                best_counter = counter
                date_b_c = left[left_index][0]
            left_index += 1
        else:
            counter -=1
            right_index += 1


    return best_counter, date_b_c
  
overlap, date = double_pointer(start_s_lines, end_s_lines)
#overlap only used for debugging
# sd1 < ed2 and sd2 < ed1
company_names = []
for company in lines:
    if company[0] <= date and company[1] > date:
        company_names.append(company[2])

company_names = sorted(company_names)
date = str(date)
date = date[6:]+"."+date[4:6]+"."+date[:4]
print(f"Busiest day: {date}")
for company in company_names:
    print(company)




"""
Comparing grades:
n: number of students who take an exam
i(1<=i<=n): individual student number
g(i): the grade of student i
l(i): the number of people who were still in the exam hall when student i left
j: another student i is comparing with
G: the difference in grade that students would consider admirable (iif they obtained it leaving earlier)(from the perspective of the worst performer)

They may leave the exam hall at any time, but never change their answers after the fact

Grades are uploaded to Lightspace, every student can see theirs and eachoter's grade.
They can also see at what time each student left the exam hall.

Naturally, students compare their results:
    They respect eachother iif student j's grade (g(j)) is at least G points higher 
    than student i's grade (g(i)) AND student i left the exam hall later than student j.
        That is: (g(i) + G) <= g(j) AND l(i) < l(j)

GOAL: Figure out how many students each student respects
OUTPUT: For each student i, you should print a line with the number of students that this student respects.
"""
# ===== DELETE BEFORE SUBMISSION =====
import sys
from pathlib import Path
sys.stdin = open(Path(__file__).parent / "example.txt")
#=====================================

#==== Input ====
nG = input().split()
n = int(nG[0])
G = int(nG[1])
ngl = []
all_ngl = []
for i in range(n):
    gl = input().split()
    g = int(gl[0])
    l = int(gl[1])
    ngl.append(i)
    ngl.append(g)
    ngl.append(l)
    all_ngl.append(ngl)
    ngl = []

# print(f"unsorted all_ngl: {all_ngl}")
# print(f"n: {n}")
# print(f"G: {G}")
# print(f"g: {g}")
# print(f"l: {l}")
#================

#==== merge_sort ====
def merge_sort(A):
    if len(A) <= 1: #this is fine if A = [[1,2,3]] len(A) = 1
        return A

    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]: #indexing for the second item inside each listed ngl
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# print(f"Sorted all_ngl: {merge_sort(all_ngl)}")
all_ngl = merge_sort(all_ngl)
all_impressed_by = []
impressed_by = 0
enu = 0
enu_impressed_by = []
for i in range(n):
    bottom = i
    for _ in range(bottom + 1,n):
        i_wow = all_ngl[i][1] + G
        if bottom < n-1:
            bottom += 1
        if i_wow <= all_ngl[bottom][1] and all_ngl[i][2] < all_ngl[bottom][2]:
            impressed_by += 1#check it doesnt break if 0
    enu = all_ngl[i][0]
    enu_impressed_by.append(enu)
    enu_impressed_by.append(impressed_by)
    all_impressed_by.append(enu_impressed_by)
    enu_impressed_by =[]
    impressed_by = 0
    

final_array = [None] * n
for i in range(n):
    final_array[all_impressed_by[i][0]] = all_impressed_by[i][1]




# print(f"impressed by: {all_impressed_by}")
# print(f"Output:\n{final_array}")
for i in final_array:
    print(i)

#currently it just check each with their immediate higher up
"""
sorted_g = merge_sort(g)
sorted_l = merge_sort(l)

# print(f"Ordered g: {sorted_g}")
# print(f"Ordered l: {sorted_l}")

Stream of conciousness:
now, the sorted arrays are good for comparing vaules, but loose the ordered connection between g(i) and l(i)
    a) potentially, i could use ennumerate to keep that info, but idk if its worth it since i would have to severely edit the merge sort
    b) alternatively, i could compare with the order of the original array.
    c) again alternatively, i could create a list of arrays with (original order number),g(i),l(i) for each student and sort it based on g(i)
        if i do it this way, for each number i only have to check their superiors, and see if their g(i),l(i)meet their requirements
        however, i need to bare in mind that i need to print them in order as output

            if enumerated, they could be sorted with something like:
            array = [3,2,1,5,4]
            temp_n = len(array)
            final_array = [None] * temp_n

            for i in range(temp_n):
                final_array[array[i]-1] = array[i] 

            print(final_array)

plan c it is
"""

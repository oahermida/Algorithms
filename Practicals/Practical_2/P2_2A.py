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

# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "example.txt"))

# #====================================

#==== Input ====
nG = input().split()
n = int(nG[0])
G = int(nG[1])
all_ngl = [None] * n

for i in range(n):
    gl = input().split()
    g = int(gl[0])
    l = int(gl[1])
    all_ngl[l] = [i, g, l]
#since l counts down by one from n-1 with each student that leaves,
#and is unique to every student
#filling that list with all_ngl[l] works perfectly.

# all_ngl is in leaving order: slot 0 left at the end, n-1 first

#================
answers = [0] * n
#==== merge_sort ====
def merge_sort(A):
    if len(A) <= 1: #A = [[1,2,3]] len(A) = 1
        return A

    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])

    return merge(left, right)

def merge(left, right):
    # it is possble to sort even more efficiently by taking advantage of the uniqueness of l
    # every merge, from the deepest: left = potential respecters, right = possible respectees 
    # Everyone in right left EARLIER than everyone in left   
    # both halves are already sorted by grade, so one forward pointer
    # everything from index_respected onward should be equal to or bigger than wow
    # the first grade equal to or bigger than wow vouches for the following students
    index_respected = 0
    for student in left: # left is in ascending grade order
        wow = student[1] + G
        while index_respected < len(right) and right[index_respected][1] < wow:
            index_respected += 1
        answers[student[0]] += len(right) - index_respected #adds the result in the right order (student[0] = all_ngl[l][0])


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



merge_sort(all_ngl)

# print(f"answers: {answers}")
for i in answers:
    print(i)


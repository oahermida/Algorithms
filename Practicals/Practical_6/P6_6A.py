"""
6A — Generators
Bob must alternate between hacking AC and DC generators. The first generator that Bob hacks can be of any type: either AC or DC.
he needs a certain number of experience points (XP) to hack them

Bob initially has x experience points,
and each generator i that he hacks, increases his XP with s(i) points.
This XP increase happens after having hacked the generator. 

Each generator also has a difficulty score d(i):
Bob can only hack a generator i if his XP is at least d(i). 

Bob’s goal is to hack as many power generators as possible, 
and he can hack them in any order he wants, provided he keeps switching between AC and DC generators.

Can you help Bob?
    last time i didnt help his cousing (the builder) 
    we ended up with a wooncrisis so im going to now

Input:
first line: n (number of generators) and x (Bob's starting XP)
then n lines, one per generator: t d s
    t: the generator's type, 0 or 1 (AC or DC)
    d: its difficulty, Bob needs XP >= d to hack it
    s: the XP Bob gains after hacking it

Goal: Bob’s goal is to hack as many power generators as possible
Output: the number of generators that Bob can hack if he uses an optimal strategy    

Constraints
    • In all test cases, 1 ≤ n ≤ 75 000.
    • In all test cases, 0 ≤ x ≤ 500.
    • For each generator i: 0 ≤ di ≤ 1 000 000 and 0 ≤ si ≤ 1 000.
    • CPU time limit: 3 seconds per test case. All tests run under Valgrind.
    • Memory limit: 256 MiB per test case.
"""
# #==== COMMENT B4 SUBMISSION =====
import sys
import os

if sys.stdin.isatty():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.stdin = open(os.path.join(here, "6A_Sample.txt"))

# #====================================

#==== Input =====
nx = input().split()
n = int(nx[0])
x = int(nx[1])

generators = []
for i in range(n):
    generator = input().split()
    for j in range(len(generator)):
        generator[j] = int(generator[j])
    generators.append(generator)
#====================================

#==== Heap =====
def parent_of(position):
    return (position - 1) // 2

def upheap(heap, position):
    # move the value at position up while it is bigger than its parent
    while position > 0 and heap[position] > heap[parent_of(position)]:
        parent = parent_of(position)
        heap[position], heap[parent] = heap[parent], heap[position]  # swap
        position = parent

def downheap(heap, position, size):
    # move the value at position down while a child is bigger than it
    # size: how much of the list counts as heap (heap sort shrinks it)
    while True:
        left = 2 * position + 1
        right = 2 * position + 2
        largest = position
        if left < size and heap[left] > heap[largest]:
            largest = left
        if right < size and heap[right] > heap[largest]:
            largest = right
        if largest == position:  # both children are smaller: done
            return
        heap[position], heap[largest] = heap[largest], heap[position]  # swap with the bigger child
        position = largest

def add(heap, value):
    heap.append(value)  # new value goes in the next free spot at the bottom
    upheap(heap, len(heap) - 1)  # then climbs to where it belongs

def extract_max(heap):
    largest = heap[0]
    last = heap.pop()  # take the bottom-right value off
    if heap:  # if anything is left, put it at the root and let it sink
        heap[0] = last
        downheap(heap, 0, len(heap))
    return largest
#====================================

generators.sort(key=lambda generator: generator[1]) #sort by d (difficulty)
print(f"generators = {generators}")

AC_gen, AD_gen = [], []

for generator in generators:
    if generator[0] == 0:
        AC_gen.append(generator)
    else:
        AD_gen.append(generator)

"""
so now i have two lists sorted by their d (difficulty)
because i have to zigzag between the two of them, that creates a checkers pattern
therefore i probably have to check both options
what im envisioning is a zigzag with greedy approach

Keep a pointer into each sorted group
whenever your XP goes up, advance that
pointer past every generator that has just become affordable, 
and move them into that type's "affordable" pool
a generator gets moved once and never moves back.

as XP grows, i could walk the pointer along AC_gen and AD_gen

a heap would give me the maximum s the fastest
greedy with a heap plus trying both starts
"""    
print(f"AC_gen = {AC_gen}")
print(f"AD_gen = {AD_gen}")

# AC_gen = [[0, 4, 1], [0, 10, 5], [0, 22, 9]]
# AD_gen = [[1, 3, 2], [1, 7, 3]]
AC_pointer = 0
AD_pointer = 0
















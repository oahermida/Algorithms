r"""
DYNAMIC PROGRAMMING OVER TREES -- THE BEST PARTY
================================================

Advanced Algorithms, Lecture 4-5 (Ivan Bliznets), slides 39-52. Also Erickson,
*Algorithms*, section 3.10 "Dynamic Programming on Trees" (maximum independent
set in a tree). No CLRS section; CLRS Problem 15-6 "Planning a company party"
is the same story as an exercise.

    BEST PARTY [slide 39]
        HR department decided to organize a party. Studies showed that people
        feel uncomfortable if their immediate boss is also at the same party.
        It is known that each employee has at most one boss. Each person has a
        value that indicate how happy he will be if he attends the party. Your
        job as a director of the HR department invite some employees such that
        sum of their happiness is maximum.

"At most one boss" makes the company a TREE: the boss is the parent. "Not with
your immediate boss" means no parent and child both invited. A set of vertices
with no edge inside it is an INDEPENDENT SET. So the problem is: the
maximum-weight independent set in a tree [slides 40-41].

    The slide's company [slides 40-41]:

                          Alice 10  (v1)
                       /             \
               Jonh 7 (v2)          Hans 2 (v5)
               /       \             /        \
         Ivan 1 (v3)  Kate 12 (v4)  Maria 2 (v6)  Jesper 3 (v8)
                                     |
                                    Bob 17 (v7)

    (Slide 40 spells it "Jonh". Kept as written.)

In a general graph this problem is NP-hard. On a tree it is O(n).


THE SUBTREE [slide 42]
----------------------
    For each vertex t denote by Tt a subtree containing t and all its
    descendants.

So T(v2) is Jonh's department: Jonh, Ivan, Kate. The subproblem is "the best
party inside one department".


THE TWO STATES [slide 43]
-------------------------
    D[v, 0] - maximum independent set in Tv that does not contain v, i.e. the
              best party in the department that is headed by v and v does not
              come.
    D[v, 1] - maximum independent set in Tv that contains v, i.e. the best
              party in the department that is headed by v and v comes.
    h(v)    - weight of vertex v, i.e. happiness of employee v.

    If v is a leaf then D[v, 0] = 0 and D[v, 1] = h(v).

Same trick as the dominating set in a path: one extra bit (does the head come?)
is exactly what the parent needs to know.


THE RECURRENCE [slide 45]
-------------------------
    Let u be a vertex and u1, u2, ..., uk its children then:
      D[u, 1] = h(u) + D[u1, 0] + D[u2, 0] + ... + D[uk, 0]
      D[u, 0] = max{D[u1, 0], D[u1, 1]} + ... + max{D[uk, 0], D[uk, 1]}

    Output: max{D[r, 0], D[r, 1]},  r - root of the tree   [slide 50]

                         u
                  .------+------.
                 u1     u2  ... uk

        u COMES:      every child must stay home         -> add D[child, 0]
        u STAYS HOME: each child is free; take its better -> add max of both
                      option, independently per child

Why the children are independent [slide 51]: two different departments share
no boss-employee pair. So once u's choice is fixed, each child's subtree can be
solved alone and the results added up.

The order: a vertex needs its children first. So compute "from bottom to top"
[slide 43] -- a POST-ORDER traversal.

The slide's tree, filled in [slides 44-50], written "h, D[v,0], D[v,1]":

                          v1: 10, 33, 43
                    /                       \
           v2: 7, 13, 7                 v5: 2, 20, 19
           /          \                  /           \
    v3: 1, 0, 1   v4: 12, 0, 12   v6: 2, 17, 2    v8: 3, 0, 3
                                       |
                                  v7: 17, 0, 17

    answer max{33, 43} = 43: Alice, Ivan, Kate, Bob, Jesper.


RUNNING TIME [slide 52]
-----------------------
    n nodes, at most n - 1 children each: O(n) * O(n) = O(n^2).
    "This is inaccurate upper bound."
    Each node costs time proportional to its number of children. Summed over
    all nodes that is sum deg(vi) = O(|E|), and a tree has |E| = n - 1.
    So the running time is O(n).


TYPO IN THE SLIDES
------------------
    - Slide 45 writes "D[u, 1] = h(v) + ...". The vertex is u, so h(u).


THE BOOK VS THE SLIDES
----------------------
    - Erickson's vertices have no weight: he maximises the NUMBER of guests,
      so his "1 +" is the slides' "h(u) +". Section 4 uses weights.
    - Erickson calls the two states MISyes(v) and MISno(v). They are the
      slides' D[v, 1] and D[v, 0].
    - Erickson first gives a ONE-state recurrence that looks at children and
      GRANDCHILDREN:
          MIS(v) = max{ sum of MIS(w) over children w,
                        h(v) + sum of MIS(x) over grandchildren x }
      Section 4 implements it too, and the tests check it agrees.
    - Erickson stores the values inside the tree nodes. The slides use a table
      D. Here D is a dict keyed by (vertex, 0 or 1).
    - The slides assume one root r. "At most one boss" also allows SEVERAL
      bosses-of-nobody, i.e. a forest. This file handles a forest by adding
      up the answers of all the roots.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_party        every set of guests, O(n * 2^n)
    2. best_party_memo          the recurrence, recursive with a memo table
    3. best_party_postorder     the same, iterative post-order, no recursion
    4. best_party_grandchildren Erickson's one-state version
    5. restore_guests           WHO is invited, walking down from the root
    6. the slide's company, printed as slides 44-50 annotate it
    7. why the iterative version matters: a very deep tree
    8. tests: hand cases, then random trees against brute force

Run with:
    python3 Tree_DP.py
"""

import random
from itertools import combinations

# The slide's company [slides 40-41]. Vertex k here is v(k+1) on the slide.
SLIDE_NAMES = ["Alice", "Jonh", "Ivan", "Kate", "Hans", "Maria", "Bob", "Jesper"]
SLIDE_HAPPINESS = [10, 7, 1, 12, 2, 2, 17, 3]
SLIDE_BOSSES = [None, 0, 1, 1, 0, 4, 5, 4]  # boss of each employee; None = head of company
# The slide's annotated values "h, D[v,0], D[v,1]" for v1 .. v8 [slide 50].
SLIDE_ANNOTATIONS = [(10, 33, 43), (7, 13, 7), (1, 0, 1), (12, 0, 12),
                     (2, 20, 19), (2, 17, 2), (17, 0, 17), (3, 0, 3)]


def children_lists(bosses):
    children = [[] for _ in bosses]
    for employee, boss in enumerate(bosses):
        if boss is not None:
            children[boss].append(employee)
    return children


def roots_of(bosses):
    return [employee for employee, boss in enumerate(bosses) if boss is None]


# =====================================================================
# 1. BRUTE FORCE -- every set of guests
# =====================================================================
# Try every subset. Keep it if no guest's boss is also a guest.
#
# guest_count: how many guests this round invites
# guests: one particular choice of that many employees
#
# O(n * 2^n). Only for testing.

def brute_force_party(happiness, bosses):
    best_total = 0
    best_guests = []
    for guest_count in range(len(happiness) + 1):
        for guests in combinations(range(len(happiness)), guest_count):
            guest_set = set(guests)
            if any(bosses[guest] in guest_set for guest in guests):
                continue  # someone's boss is here
            total = sum(happiness[guest] for guest in guests)
            if total > best_total:
                best_total = total
                best_guests = list(guests)
    return best_total, best_guests


# =====================================================================
# 2. THE RECURRENCE, RECURSIVE WITH A MEMO TABLE [slides 43-45]
# =====================================================================
# happiness: h(v) for each employee
# bosses: the boss (parent) of each employee, None for a root
# table: D; table[(vertex, 1)] = best party in T(vertex) with vertex coming,
#        table[(vertex, 0)] = best party in T(vertex) without vertex
# vertex: the head of the department being solved
#
# The recursion visits children before it finishes the parent, so this IS the
# bottom-to-top order, done by the call stack. The memo means each vertex is
# solved once. A tree has no shared subtrees, so the memo never actually hits
# here -- it is kept because it is the lecture's table D, and section 5 reads
# it to restore the guests.
#
# O(n) time. Recursion depth = height of the tree (see section 7).

def best_party_memo(happiness, bosses):
    children = children_lists(bosses)
    table = {}

    def solve(vertex):
        if (vertex, 0) in table:
            return
        coming = happiness[vertex]  # D[u, 1] starts at h(u)
        staying_home = 0  # D[u, 0] starts at 0
        for child in children[vertex]:
            solve(child)
            coming += table[(child, 0)]  # u comes: child stays home
            staying_home += max(table[(child, 0)], table[(child, 1)])  # child is free
        table[(vertex, 1)] = coming
        table[(vertex, 0)] = staying_home

    answer = 0
    for root in roots_of(bosses):
        solve(root)
        answer += max(table[(root, 0)], table[(root, 1)])
    return answer, table


# =====================================================================
# 3. THE SAME, ITERATIVE POST-ORDER -- no recursion
# =====================================================================
# order: every vertex, listed so that each one comes after all its children
# stack: vertices still to be listed
#
# Build the order with an explicit stack: pop a vertex, write it down, push
# its children. That lists every parent BEFORE its children (a pre-order).
# Reversed, every child comes before its parent -- which is all the
# recurrence needs.
#
# Then one plain loop over that order fills D, same formulas as section 2.
# O(n) time, O(n) space, and no recursion depth limit.

def best_party_postorder(happiness, bosses):
    children = children_lists(bosses)
    order = []
    stack = roots_of(bosses)
    while stack:
        vertex = stack.pop()
        order.append(vertex)
        stack.extend(children[vertex])
    order.reverse()  # children now come before their parent

    table = {}
    for vertex in order:
        coming = happiness[vertex]
        staying_home = 0
        for child in children[vertex]:
            coming += table[(child, 0)]
            staying_home += max(table[(child, 0)], table[(child, 1)])
        table[(vertex, 1)] = coming
        table[(vertex, 0)] = staying_home

    answer = sum(max(table[(root, 0)], table[(root, 1)]) for root in roots_of(bosses))
    return answer, table


# =====================================================================
# 4. ERICKSON'S ONE-STATE VERSION -- children and grandchildren
# =====================================================================
# best: best[vertex] = MIS(vertex), the best party in T(vertex), whoever comes
#
#   best[v] = max( sum of best[w] over children w,            v stays home
#                  h(v) + sum of best[x] over grandchildren x ) v comes, so
#                                                               children stay home
#
# Same post-order as section 3. Each vertex adds to its parent once and to its
# grandparent once, so it is still O(n) (Erickson's argument).

def best_party_grandchildren(happiness, bosses):
    children = children_lists(bosses)
    order = []
    stack = roots_of(bosses)
    while stack:
        vertex = stack.pop()
        order.append(vertex)
        stack.extend(children[vertex])
    order.reverse()

    best = [0] * len(happiness)
    for vertex in order:
        skip_total = sum(best[child] for child in children[vertex])
        keep_total = happiness[vertex] + sum(best[grandchild]
                                             for child in children[vertex]
                                             for grandchild in children[child])
        best[vertex] = max(skip_total, keep_total)

    return sum(best[root] for root in roots_of(bosses))


# =====================================================================
# 5. RESTORE THE GUESTS -- walking DOWN from the root
# =====================================================================
# The table says how good the best party is. To find who comes, start at the
# root and go down, the opposite way to how the table was filled:
#
#   a vertex whose boss COMES         -> must stay home (state 0)
#   a vertex whose boss STAYS HOME    -> free: take the better of D[v,1], D[v,0]
#
# pending: (vertex, may_come) pairs still to decide; may_come is False when
#          the boss is coming
# guests: the answer
#
# Ties go to "comes". O(n).

def restore_guests(bosses, table):
    children = children_lists(bosses)
    guests = []
    pending = [(root, True) for root in roots_of(bosses)]
    while pending:
        vertex, may_come = pending.pop()
        comes = may_come and table[(vertex, 1)] >= table[(vertex, 0)]
        if comes:
            guests.append(vertex)
        for child in children[vertex]:
            pending.append((child, not comes))
    guests.sort()
    return guests


def is_valid_party(guests, bosses):
    guest_set = set(guests)
    return all(bosses[guest] not in guest_set for guest in guests)


# =====================================================================
# 6. RUN THE SLIDE'S EXAMPLE [slides 44-50]
# =====================================================================

print("=" * 78)
print("BEST PARTY / INDEPENDENT SET IN A TREE   -- Lecture 4-5, slides 39-52;  Erickson 3.10")
print("=" * 78)

answer, slide_table = best_party_postorder(SLIDE_HAPPINESS, SLIDE_BOSSES)
slide_guests = restore_guests(SLIDE_BOSSES, slide_table)

print("\nEach vertex as the slides annotate it: h, D[v,0], D[v,1]\n")
for vertex, name in enumerate(SLIDE_NAMES):
    boss = SLIDE_BOSSES[vertex]
    boss_name = "--" if boss is None else SLIDE_NAMES[boss]
    print(f"  v{vertex + 1} {name:<7} boss {boss_name:<6}  "
          f"{SLIDE_HAPPINESS[vertex]:>3}, {slide_table[(vertex, 0)]:>3}, {slide_table[(vertex, 1)]:>3}")

print(f"\n  answer max{{D[v1,0], D[v1,1]}} = max{{{slide_table[(0, 0)]}, {slide_table[(0, 1)]}}} = {answer}")
print(f"  guests: {', '.join(SLIDE_NAMES[guest] for guest in slide_guests)}"
      f"  ({' + '.join(str(SLIDE_HAPPINESS[guest]) for guest in slide_guests)})")


# =====================================================================
# 7. A VERY DEEP TREE -- why the iterative version exists
# =====================================================================
# A company that is one long chain of command: everyone has exactly one
# report. The recursion in section 2 goes one call deeper per level, and
# Python stops at about 1000 levels.

print("\n" + "=" * 78)
print("A CHAIN OF COMMAND 100 000 PEOPLE LONG")
print("=" * 78)

chain_length = 100_000
chain_bosses = [None] + list(range(chain_length - 1))
chain_happiness = [1] * chain_length
try:
    best_party_memo(chain_happiness, chain_bosses)
    print("\n  recursive memo version: finished")
except RecursionError:
    print("\n  recursive memo version: RecursionError -- the tree is too deep for the call stack")
chain_answer, _ = best_party_postorder(chain_happiness, chain_bosses)
print(f"  iterative post-order:   {chain_answer}   (every second person: 100 000 / 2)")


# =====================================================================
# 8. TESTS
# =====================================================================

print("\n" + "=" * 78)
print("TESTS")
print("=" * 78 + "\n")

all_passed = True


def report(passed, message):
    global all_passed
    all_passed = all_passed and passed
    print(f"{'PASS' if passed else 'FAIL'}  {message}")


def check_all_versions(happiness, bosses):
    # returns the answer, and whether every version and the restore agree with it
    memo_answer, memo_table = best_party_memo(happiness, bosses)
    post_answer, post_table = best_party_postorder(happiness, bosses)
    grand_answer = best_party_grandchildren(happiness, bosses)
    guests = restore_guests(bosses, post_table)
    agree = (memo_answer == post_answer == grand_answer
             and memo_table == post_table
             and is_valid_party(guests, bosses)
             and sum(happiness[guest] for guest in guests) == post_answer)
    return post_answer, agree


annotations_match = all(
    (SLIDE_HAPPINESS[vertex], slide_table[(vertex, 0)], slide_table[(vertex, 1)]) == SLIDE_ANNOTATIONS[vertex]
    for vertex in range(len(SLIDE_NAMES)))
report(annotations_match, "every vertex matches the slide 50 annotations h, D[v,0], D[v,1]")

hand_cases = [
    (SLIDE_HAPPINESS, SLIDE_BOSSES, 43),  # slide 50
    ([5], [None], 5),  # one person
    ([5, 9], [None, 0], 9),  # boss and one report: invite the happier
    ([5, 3, 3], [None, 0, 0], 6),  # two reports beat their boss
    ([7, 3, 3], [None, 0, 0], 7),  # the boss beats two reports
    ([1, 1, 1, 1], [None, 0, 1, 2], 2),  # a chain of four: every second one
    ([4, 6], [None, None], 10),  # a forest of two separate bosses
    ([-5, 2], [None, 0], 2),  # negative happiness: leave that person home
]
for happiness, bosses, expected in hand_cases:
    answer, agree = check_all_versions(happiness, bosses)
    report(answer == expected and agree, f"party{happiness} bosses{bosses} = {answer}, expected {expected}")

# Random trees and forests against brute force. Each new employee picks a
# boss among the earlier ones, or none.
random.seed(10)
trial_count = 1500
failures = 0
for _ in range(trial_count):
    employee_count = random.randint(1, 13)
    bosses = [None] + [random.choice([None] + list(range(employee))) if random.random() < 0.1
                       else random.randrange(employee) for employee in range(1, employee_count)]
    happiness = [random.randint(-5, 20) for _ in range(employee_count)]
    answer, agree = check_all_versions(happiness, bosses)
    if answer != brute_force_party(happiness, bosses)[0] or not agree:
        failures += 1
report(failures == 0, f"{trial_count} random trees and forests (1-13 people, happiness -5..20)"
       f" agree with brute force ({trial_count - failures}/{trial_count})")

print(f"\n{'ALL PASS' if all_passed else 'SOME TESTS FAILED'}")

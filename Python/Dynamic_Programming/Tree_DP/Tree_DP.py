r"""
DYNAMIC PROGRAMMING OVER TREES -- THE BEST PARTY
Lecture 4-5, slides 39-52; Erickson, Algorithms, section 3.10.

Notes: [[Tree DP — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Tree DP — Code Notes.md

What is in this file:
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
# Notes: [[Tree DP — Code Notes#2. The recurrence, recursive with a memo table]] (variables, order, depth)

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
# Notes: [[Tree DP — Code Notes#3. The same, iterative post-order — no recursion]] (variables, how the order is built)

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
# Notes: [[Tree DP — Code Notes#4. Erickson's one-state version — children and grandchildren]] (the recurrence)

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
# Notes: [[Tree DP — Code Notes#5. Restore the guests — walking down from the root]] (walk-down rule, variables)

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

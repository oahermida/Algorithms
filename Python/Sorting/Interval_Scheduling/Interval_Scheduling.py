"""
INTERVAL SCHEDULING  (independent set in an interval graph)
===========================================================

Advanced Algorithms, Lecture 1 (Ivan Bliznets), slides 23-25. Also CLRS
(3rd ed.) section 16.1, "An activity-selection problem", pp. 415-422.

    INDEPENDENT SET IN INTERVAL GRAPH [slide 23]
        Input:     n tasks described by starting time a_i and ending time b_i
                   for each i in {1, 2, ..., n}.
        Question:  You can perform only one task at a time. Schedule your work
                   such that you complete the largest amount of tasks.

        Example:   Input array [(2, 10), (5, 14), (2, 8), (12, 20), (18, 22),
                                (1, 30), (21, 25)]
                   Output: (2, 10), (12, 20), (21, 25).

Slides 24-25 are blank in the PDF. The algorithm was worked on the board.
Slide 26 lists it under "Application of sorting algorithms", so the intended
method is: sort, then sweep. That is the CLRS greedy algorithm.


WHY "INTERVAL GRAPH"
--------------------
Draw one dot per task. Join two dots with a line when the tasks overlap in
time. That drawing is the interval graph. A set of tasks you can ALL do is a
set of dots with no line between any two of them -- an "independent set".
So "most tasks" = "largest independent set". Same problem, two names.


THE GREEDY RULE -- EARLIEST FINISH FIRST
----------------------------------------
    1. Sort the tasks by their END time.
    2. Walk through them in that order.
    3. Take a task if it starts after the last taken task ended.
       Otherwise skip it.

CLRS writes this as GREEDY-ACTIVITY-SELECTOR (p. 421), assuming the
activities are already sorted by finish time f_1 <= f_2 <= ... <= f_n:

    GREEDY-ACTIVITY-SELECTOR(s, f)
    1  n = s.length
    2  A = {a_1}
    3  k = 1
    4  for m = 2 to n
    5      if s[m] >= f[k]
    6          A = A U {a_m}
    7          k = m
    8  return A

Why it is safe (CLRS Theorem 16.1, p. 418): take ANY best schedule. Swap its
first task for the task that finishes earliest overall. That task ends no
later, so it cannot clash with anything after it. The schedule is still valid
and still the same size. So some best schedule starts with the
earliest-finishing task. Take it, throw away everything that clashes, and
repeat the argument on what is left.

Picking the task that ends first leaves the most time for the rest.


TWO THINGS TO WATCH
-------------------
    TOUCHING INTERVALS. Is (2, 10) compatible with (10, 12)? The slide does not
    say. CLRS uses half-open intervals [s, f), so a task may start at the exact
    moment the previous one ends: the test is  start >= last_end.  This file
    follows CLRS. If the course wanted closed intervals, change >= to >.
    The slide's example never has two tasks touching, so its answer is the
    same either way.

    THE SLIDE'S OUTPUT IS ONE OF SEVERAL. Greedy on the slide's input returns
    (2, 8), (12, 20), (21, 25), not (2, 10), (12, 20), (21, 25). Both have 3
    tasks, and 3 is the maximum. The question asks for the largest NUMBER of
    tasks, so both are correct. (2, 8) comes first because it ends at 8,
    before (2, 10) ends at 10.


WHAT IS IN THIS FILE
--------------------
    1. brute_force_schedule      every subset, O(2^n * n^2)
    2. greedy_schedule           sort by end time, sweep, O(n log n)
                                                   [slides 23-26; CLRS 16.1]
    3. other greedy rules that LOOK reasonable and fail  [CLRS exercise 16.1-3]
    4. the slide's example
    5. tests: hand cases and random cases

Run with:
    python3 Interval_Scheduling.py
"""

import random
from itertools import combinations

# The example from slide 23.
SLIDE_TASKS = [(2, 10), (5, 14), (2, 8), (12, 20), (18, 22), (1, 30), (21, 25)]


# =====================================================================
# 0. WHEN DO TWO TASKS CLASH?
# =====================================================================
# Half-open intervals, as in CLRS: [start, end).
# Two tasks are compatible when one ends before (or exactly when) the other
# starts. Every method below uses this one function, so they all agree on
# what "clash" means.

def compatible(first_task, second_task):
    first_start, first_end = first_task
    second_start, second_end = second_task
    return first_end <= second_start or second_end <= first_start


# =====================================================================
# 1. BRUTE FORCE -- every subset
# =====================================================================
# Try subsets from the BIGGEST size down. The first subset where every pair
# is compatible is a best answer.
#
# subset_size: how many tasks this round tries to fit in
# chosen: one particular group of that many tasks
#
# Up to 2^n subsets, and checking one costs O(n^2) pairs: O(2^n * n^2).
# Only usable for small n. It is here to check the greedy against.

def brute_force_schedule(tasks):
    for subset_size in range(len(tasks), 0, -1):
        for chosen in combinations(tasks, subset_size):
            if all(compatible(first_task, second_task)
                   for first_task, second_task in combinations(chosen, 2)):
                return sorted(chosen, key=lambda task: task[1])
    return []


# =====================================================================
# 2. GREEDY -- earliest finish first [slides 23-26; CLRS 16.1, p. 421]
# =====================================================================
# tasks_by_end: the tasks sorted by end time, earliest end first
# chosen: the tasks taken so far, in the order they were taken
# last_end: the end time of the last task taken; a new task must start at or
#           after this. Starts at -infinity so the first task is always taken.
#
# The sort is O(n log n). The sweep is one pass, O(n). Total O(n log n).

def greedy_schedule(tasks):
    tasks_by_end = sorted(tasks, key=lambda task: task[1])
    chosen = []
    last_end = float("-inf")

    for task in tasks_by_end:
        start, end = task
        if start >= last_end:  # starts after the last taken task ends: take it
            chosen.append(task)
            last_end = end
    return chosen


# =====================================================================
# 3. GREEDY RULES THAT DO NOT WORK [CLRS exercise 16.1-3, p. 422]
# =====================================================================
# The sort key is the whole algorithm. Sorting by something else gives a
# greedy that looks just as sensible and is wrong.
#
# sort_key: which number to sort the tasks by before sweeping
# chosen: tasks taken so far
#
# A taken task must be compatible with EVERY task already taken. (With a
# different order, checking only the last one is not enough.)

def greedy_by(tasks, sort_key):
    chosen = []
    for task in sorted(tasks, key=sort_key):
        if all(compatible(task, taken_task) for taken_task in chosen):
            chosen.append(task)
    return chosen


def earliest_start(task):
    return task[0]


def shortest_length(task):
    return task[1] - task[0]


# =====================================================================
# 4. RUN THE SLIDE'S EXAMPLE [slide 23]
# =====================================================================

print("=" * 72)
print("INTERVAL SCHEDULING   -- Lecture 1, slides 23-25;  CLRS 16.1")
print("=" * 72)

print(f"\ntasks:          {SLIDE_TASKS}")
print(f"sorted by end:  {sorted(SLIDE_TASKS, key=lambda task: task[1])}\n")

greedy_answer = greedy_schedule(SLIDE_TASKS)
brute_answer = brute_force_schedule(SLIDE_TASKS)
print(f"greedy:         {greedy_answer}   ({len(greedy_answer)} tasks)")
print(f"brute force:    {brute_answer}   ({len(brute_answer)} tasks)")
print(f"slide's answer: [(2, 10), (12, 20), (21, 25)]   (3 tasks)")
print("\nAll three have 3 tasks. Greedy picks (2, 8) over (2, 10) because")
print("(2, 8) ends sooner. Any schedule with the most tasks is a correct answer.")

# Why the other rules fail, on the smallest inputs that show it.
long_first = [(0, 10), (1, 2), (3, 4), (5, 6)]
short_in_middle = [(0, 5), (4, 7), (6, 11)]

print("\nOther sort orders, and inputs where they lose:")
print(f"  earliest start on {long_first}")
print(f"    picks {greedy_by(long_first, earliest_start)},"
      f" best is {greedy_schedule(long_first)}")
print("    (the long task starts first and blocks everything)")
print(f"  shortest first on {short_in_middle}")
print(f"    picks {greedy_by(short_in_middle, shortest_length)},"
      f" best is {greedy_schedule(short_in_middle)}")
print("    (the short task overlaps both others)")


# =====================================================================
# 5. TESTS
# =====================================================================
# Different methods may return different schedules of the same size. So a
# test checks three things about the greedy answer:
#     - it has the expected NUMBER of tasks (the brute force decides this)
#     - every pair in it is compatible
#     - every task in it really came from the input

def is_valid_schedule(schedule, tasks):
    remaining_tasks = list(tasks)
    for task in schedule:
        if task not in remaining_tasks:
            return False
        remaining_tasks.remove(task)  # each task may only be used once
    return all(compatible(first_task, second_task)
               for first_task, second_task in combinations(schedule, 2))


# Each case: (tasks, expected number of tasks in a best schedule)
test_cases = [
    (SLIDE_TASKS, 3),  # slide 23
    ([], 0),  # nothing to do
    ([(1, 5)], 1),  # a single task
    ([(1, 3), (3, 5), (5, 7)], 3),  # touching ends: compatible under [s, f)
    ([(1, 4), (2, 5), (3, 6)], 1),  # all overlap each other
    ([(1, 2), (3, 4), (5, 6)], 3),  # no overlaps at all
    ([(0, 10), (1, 2), (3, 4), (5, 6)], 3),  # beats earliest-start
    ([(0, 5), (4, 7), (6, 11)], 2),  # beats shortest-first
    ([(1, 3), (1, 3), (1, 3)], 1),  # the same task three times
    # the eleven activities on CLRS p. 415 (traced in Figure 16.1): best has 4
    ([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11),
      (8, 12), (2, 14), (12, 16)], 4),
]

print("\n" + "=" * 72)
print("TESTS")
print("=" * 72 + "\n")

pass_count = 0
fail_count = 0

for tasks, expected_count in test_cases:
    for method_name, method in (("brute_force_schedule", brute_force_schedule),
                                ("greedy_schedule", greedy_schedule)):
        result = method(tasks)
        status = ("PASS" if len(result) == expected_count
                  and is_valid_schedule(result, tasks) else "FAIL")
        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{status}  {method_name}: {len(result)} tasks {result}, "
              f"expected {expected_count}")
    print()

# Random check: fixed seed, so every run uses the same cases.
random.seed(16)
trial_count = 2000
random_failures = 0

for _ in range(trial_count):
    task_count = random.randint(0, 9)
    tasks = []
    for _ in range(task_count):
        start = random.randint(0, 20)
        tasks.append((start, start + random.randint(1, 8)))

    greedy_result = greedy_schedule(tasks)
    if (len(greedy_result) != len(brute_force_schedule(tasks))
            or not is_valid_schedule(greedy_result, tasks)):
        random_failures += 1

status = "PASS" if random_failures == 0 else "FAIL"
if status == "PASS":
    pass_count += 1
else:
    fail_count += 1
print(f"{status}  {trial_count} random task lists: greedy matches brute force "
      f"({random_failures} disagreements)")

print(f"\n{pass_count} PASS, {fail_count} FAIL")

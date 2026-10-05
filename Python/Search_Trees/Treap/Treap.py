r"""
TREAP
=====

Advanced Algorithms, Lecture 8 (Ivan Bliznets), slides 30-33. The slides follow
Erickson's lecture notes "Treaps and Skip Lists", section 3.1 (the example on
slide 30 is his figure). CLRS has treaps as Problem 13-4 (3rd ed. pp. 333-335),
with the same min-heap convention.

Uses the rotations from ../Rotations/Rotations.py.


THE DEFINITION [slide 30]
-------------------------
    Treap (Tree + heap) - a randomized binary tree in which every node has both
    a search key and a priority
      - It is a binary tree for search keys (alphabetic order on letters)
      - It is a min-heap for priorities (numbers)

              ____M1_____
             /           \
            H2_         T3
           /   \       /
          G7  I4_     R5
         /       \   /
        A9      L8  O6

So the SMALLEST priority is at the root, and every node's priority is smaller
than its children's. Erickson's footnote admits the wording is awkward: "first
priority" wins, so smaller numbers sit higher.

Erickson also shows: with distinct keys and priorities, the treap is UNIQUE.
The smallest priority must be the root (heap), every smaller key goes left and
every bigger key goes right (search tree), and the same holds in each subtree.
Equivalently, the treap is the plain BST you get by inserting the keys in order
of increasing priority. Section 6 checks this by inserting slide 30's nodes in
many different orders and always getting the same tree.

WHY RANDOM PRIORITIES. The shape is the plain BST for "keys inserted in
priority order". If the priorities are random, that order is a random
permutation of the keys, whatever order the USER inserted them in. So even
sorted input, the plain BST's worst case, produces a random-looking tree.


INSERT [slide 31]
-----------------
    - Insert using binary search tree algorithm
    - Generate a random priority
    - Perform rotations to bubble up the node based on priority
        - If node is a left child, rotate right about parent
        - If node is a right child, rotate left about the parent
        - Stop when parent priority < node priority or node is root

This is a heap's upheap (../../Data_Structures/08_Heap.py), done with rotations
instead of swaps. A swap would break the search-tree order; a rotation keeps it
(Rotations.py, slide 19).


DELETE [slide 32]
-----------------
    There are three cases:
      - Node is a leaf, just remove it
      - Node has a single child, remove node and replace with child
      - Node has 2 children. Rotate the node down, always choosing rotation
        with the child that has the smallest priority. Continue as long as node
        has two children.

Why the child with the SMALLER priority: that child is about to become the
parent of the other one. If the larger one came up instead, it would sit above
a smaller priority and break the heap.

SLIDES vs ERICKSON. Erickson rotates the node down until it is a LEAF, then
cuts it off ("run the insertion algorithm backward in time"). The slide stops
as soon as the node has at most one child and splices it out, which saves the
last few rotations. Same final tree either way: once the node has one child,
rotating it further down just carries that child up, which is what splicing
does in one step.


RUNNING TIME [slide 33]
-----------------------
    Theorem. Average depth of Treap is O(log n).
    We do not discuss the proof in this course.

Search, insert and delete are all O(depth), so expected O(log n). The worst
case is still O(n) if the random priorities happen to come out sorted, but that
has negligible probability and does not depend on the input. Section 6 measures
the average depth on sorted input.


WHAT IS IN THIS FILE
--------------------
    1. TreapNode: key and priority
    2. rotations                         [slide 31, Rotations.py]
    3. search                            [slide 7: unchanged from BST]
    4. insert                            [slide 31]
    5. delete                            [slide 32]
    6. checks: BST property, heap property
    7. a top-down ASCII printer
    8. tests

Run with:
    python3 Treap.py
"""

import math
import random


# =====================================================================
# 1. THE NODE
# =====================================================================
# key: the search key (letters in the slide, any comparable value here)
# priority: the heap value; smaller means closer to the root
# left / right: the children, or None

class TreapNode:
    def __init__(self, key, priority):
        self.key = key
        self.priority = priority
        self.left = None
        self.right = None


# Where random priorities come from. Seeded so every run prints the same trees.
priority_source = random.Random(30)


# =====================================================================
# 2. ROTATIONS
# =====================================================================
# Subtree style, as in Rotations.py: pass the old top, get the new top back.
# rotate_right: the left child comes up   (slide 31: "left child, rotate right")
# rotate_left: the right child comes up

def rotate_right(old_top):
    new_top = old_top.left
    old_top.left = new_top.right  # B moves across
    new_top.right = old_top
    return new_top


def rotate_left(old_top):
    new_top = old_top.right
    old_top.right = new_top.left  # B moves across
    new_top.left = old_top
    return new_top


# =====================================================================
# 3. SEARCH
# =====================================================================
# Exactly the BST search. Priorities play no part in finding a key; they only
# decide the shape.

def search(node, key):
    while node is not None and key != node.key:
        node = node.left if key < node.key else node.right
    return node


# =====================================================================
# 4. INSERT [slide 31]
# =====================================================================
# node: the root of the subtree the key goes into
# priority: the new node's priority; random unless a test passes one in
#
# Going down: plain BST insert, the new node becomes a leaf.
# Coming back up: at each node on the path, if the child we just came from now
# has a SMALLER priority than this node, rotate it up. Once a parent with a
# smaller priority is reached, nothing changes from there up: "stop when parent
# priority < node priority".
#
# Expected O(log n).

def insert(node, key, priority=None):
    if node is None:
        if priority is None:
            priority = priority_source.random()
        return TreapNode(key, priority)
    if key < node.key:
        node.left = insert(node.left, key, priority)
        if node.left.priority < node.priority:
            node = rotate_right(node)  # it is a left child: rotate right
    elif key > node.key:
        node.right = insert(node.right, key, priority)
        if node.right.priority < node.priority:
            node = rotate_left(node)  # it is a right child: rotate left
    return node  # equal key: already present, nothing to do


# =====================================================================
# 5. DELETE [slide 32]
# =====================================================================
# node: the root of the subtree the key is deleted from
# new_top: the child that is rotated up above the doomed node
#
# Find the node as in search. Then:
#   leaf          -> return None (it is removed)
#   one child     -> return that child (it takes the node's place)
#   two children  -> rotate up the child with the smaller priority, so the
#                    doomed node sinks one level, then keep deleting from the
#                    side it sank into
#
# Expected O(log n).

def delete(node, key):
    if node is None:
        return None  # key not present
    if key < node.key:
        node.left = delete(node.left, key)
        return node
    if key > node.key:
        node.right = delete(node.right, key)
        return node

    if node.left is None:
        return node.right  # leaf (None) or right child only
    if node.right is None:
        return node.left  # left child only

    if node.left.priority < node.right.priority:
        new_top = rotate_right(node)  # doomed node is now new_top.right
        new_top.right = delete(new_top.right, key)
    else:
        new_top = rotate_left(node)  # doomed node is now new_top.left
        new_top.left = delete(new_top.left, key)
    return new_top


# =====================================================================
# 6. CHECKS
# =====================================================================
# is_bst: keys strictly inside the bounds handed down (lower / upper)
# is_min_heap: every child's priority is bigger than its parent's (slide 30)

def is_bst(node, lower=None, upper=None):
    if node is None:
        return True
    if (lower is not None and node.key <= lower) or (upper is not None and node.key >= upper):
        return False
    return is_bst(node.left, lower, node.key) and is_bst(node.right, node.key, upper)


def is_min_heap(node):
    if node is None:
        return True
    for child in (node.left, node.right):
        if child is not None and child.priority <= node.priority:
            return False
    return is_min_heap(node.left) and is_min_heap(node.right)


def in_order(node, visited):
    if node is not None:
        in_order(node.left, visited)
        visited.append(node.key)
        in_order(node.right, visited)
    return visited


def shape(node):
    # nested tuples, so two treaps can be compared for equal shape
    if node is None:
        return None
    return (node.key, node.priority, shape(node.left), shape(node.right))


def depth_total(node, depth=0):
    # sum of the depths of all nodes; the root has depth 0
    if node is None:
        return 0
    return depth + depth_total(node.left, depth + 1) + depth_total(node.right, depth + 1)


def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


# =====================================================================
# 7. TOP-DOWN ASCII PRINTER
# =====================================================================
# build_lines returns, for one subtree:
#   lines: the picture, one string per row, all the same width
#   width: that width
#   middle: the column where this subtree's root label sits
# Labels are key followed by priority, as on slide 30: "M1".

def label_of(node):
    priority = node.priority
    if isinstance(priority, float):
        priority = f"{priority:.2f}"[1:]  # 0.37 -> .37
    return f"{node.key}{priority}"


def build_lines(node):
    if node is None:
        return [], 0, 0
    label = label_of(node)
    label_width = len(label)
    left_lines, left_width, left_middle = build_lines(node.left)
    right_lines, right_width, right_middle = build_lines(node.right)

    if node.left is None and node.right is None:
        return [label], label_width, label_width // 2

    if node.right is None:
        first = " " * (left_middle + 1) + "_" * (left_width - left_middle - 1) + label
        second = " " * left_middle + "/" + " " * (left_width - left_middle - 1 + label_width)
        body = [line + " " * label_width for line in left_lines]
        return [first, second] + body, left_width + label_width, left_width + label_width // 2

    if node.left is None:
        first = label + "_" * right_middle + " " * (right_width - right_middle)
        second = " " * (label_width + right_middle) + "\\" + " " * (right_width - right_middle - 1)
        body = [" " * label_width + line for line in right_lines]
        return [first, second] + body, right_width + label_width, label_width // 2

    first = (" " * (left_middle + 1) + "_" * (left_width - left_middle - 1) + label
             + "_" * right_middle + " " * (right_width - right_middle))
    second = (" " * left_middle + "/" + " " * (left_width - left_middle - 1 + label_width + right_middle)
              + "\\" + " " * (right_width - right_middle - 1))
    row_count = max(len(left_lines), len(right_lines))
    left_lines += [" " * left_width] * (row_count - len(left_lines))
    right_lines += [" " * right_width] * (row_count - len(right_lines))
    body = [left_line + " " * label_width + right_line
            for left_line, right_line in zip(left_lines, right_lines)]
    return [first, second] + body, left_width + right_width + label_width, left_width + label_width // 2


def show(root, indent="    "):
    if root is None:
        print(indent + "(empty)")
        return
    for line in build_lines(root)[0]:
        print(indent + line.rstrip())


# =====================================================================
# 8. TESTS
# =====================================================================

def build(pairs):
    root = None
    for key, priority in pairs:
        root = insert(root, key, priority)
    return root


def check(label, condition):
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    return condition


all_passed = True

print("=" * 72)
print("TREAP   -- Lecture 8, slides 30-33;  Erickson 3.1;  CLRS Problem 13-4")
print("=" * 72)

# --- slide 30: Erickson's example --------------------------------------
slide_pairs = [("M", 1), ("H", 2), ("T", 3), ("G", 7), ("I", 4),
               ("R", 5), ("A", 9), ("L", 8), ("O", 6)]
slide_shape = ("M", 1,
               ("H", 2, ("G", 7, ("A", 9, None, None), None), ("I", 4, None, ("L", 8, None, None))),
               ("T", 3, ("R", 5, ("O", 6, None, None), None), None))

alphabetical = sorted(slide_pairs)
print(f"\nslide 30, inserted in alphabetical order {[key for key, _ in alphabetical]}:\n")
slide_root = build(alphabetical)
show(slide_root)
print()
all_passed &= check("alphabetical insertion rebuilds slide 30's treap exactly", shape(slide_root) == slide_shape)

# uniqueness: any insertion order gives the same treap (Erickson 3.1.1, CLRS 13-4a)
random.seed(31)
orders_tried = 200
same_every_time = True
for _ in range(orders_tried):
    shuffled = slide_pairs[:]
    random.shuffle(shuffled)
    if shape(build(shuffled)) != slide_shape:
        same_every_time = False
all_passed &= check(f"{orders_tried} random insertion orders all give the same treap (it is unique)",
                    same_every_time)

# --- Erickson's insertion example: S with priority -1 ----------------
slide_root = insert(slide_root, "S", -1)
print("\ninsert S with priority -1 (Erickson's example): it bubbles up to the root\n")
show(slide_root)
print()
all_passed &= check("S is the new root, with M on its left and T on its right",
                    slide_root.key == "S" and slide_root.left.key == "M" and slide_root.right.key == "T")
all_passed &= check("R moved from under T to under M (it is between M and S)",
                    slide_root.left.right.key == "R")

# --- deletion: S again, then the three slide 32 cases ----------------
slide_root = delete(slide_root, "S")
print("\ndelete S (two children: rotated down, then spliced out)\n")
show(slide_root)
print()
all_passed &= check("deleting S gives back slide 30's treap: delete undoes insert",
                    shape(slide_root) == slide_shape)

leaf_root = delete(build(slide_pairs), "L")
all_passed &= check("delete leaf L: I has no children left",
                    search(leaf_root, "I").right is None and is_min_heap(leaf_root))
one_child_root = delete(build(slide_pairs), "G")
all_passed &= check("delete G (one child): A takes its place under H",
                    one_child_root.left.left.key == "A" and is_min_heap(one_child_root))
two_children_root = delete(build(slide_pairs), "M")
print("\ndelete the root M (two children: H2 < T3, so H rotates up)\n")
show(two_children_root)
print()
all_passed &= check("H (priority 2) becomes the root, T (priority 3) its right child",
                    two_children_root.key == "H" and two_children_root.right.key == "T"
                    and is_bst(two_children_root) and is_min_heap(two_children_root))
missing_root = delete(build(slide_pairs), "Z")
all_passed &= check("delete missing key Z: treap unchanged", shape(missing_root) == slide_shape)

# --- randomized insert/delete ---------------------------------------
random.seed(32)
trial_count = 300
failures = 0
for _ in range(trial_count):
    root = None
    present = set()
    for _ in range(120):
        key = random.randint(0, 80)
        if random.random() < 0.6:
            root = insert(root, key)
            present.add(key)
        else:
            root = delete(root, key)
            present.discard(key)
        if not is_bst(root) or not is_min_heap(root) or in_order(root, []) != sorted(present):
            failures += 1
            break
print()
all_passed &= check(f"{trial_count} random runs of 120 inserts/deletes: BST property on keys, "
                    f"min-heap on priorities, in-order == sorted(set)", failures == 0)

# the treap equals the plain BST built in priority order (Erickson 3.1.1)
def plain_bst_insert(node, key, priority):
    if node is None:
        return TreapNode(key, priority)
    if key < node.key:
        node.left = plain_bst_insert(node.left, key, priority)
    else:
        node.right = plain_bst_insert(node.right, key, priority)
    return node

random.seed(33)
priority_order_matches = 0
for _ in range(trial_count):
    pairs = [(key, random.random()) for key in random.sample(range(1000), 60)]
    treap_root = build(pairs)
    bst_root = None
    for key, priority in sorted(pairs, key=lambda pair: pair[1]):
        bst_root = plain_bst_insert(bst_root, key, priority)
    priority_order_matches += shape(treap_root) == shape(bst_root)
all_passed &= check(f"treap == plain BST inserted in priority order, {priority_order_matches}/{trial_count}",
                    priority_order_matches == trial_count)

# --- slide 33: sorted input still gives logarithmic depth ------------
print()
for node_count in (100, 1000, 10000):
    root = None
    for key in range(node_count):
        root = insert(root, key)
    average_depth = depth_total(root) / node_count
    print(f"  {node_count:>6} sorted inserts: average depth {average_depth:5.1f}, height {height(root):>3}"
          f"   (plain BST: average {(node_count - 1) / 2:7.1f}, height {node_count - 1})"
          f"   2 ln n = {2 * math.log(node_count):4.1f}")
    all_passed &= check(f"average depth {average_depth:.1f} is O(log n): below 3 log2 n = "
                        f"{3 * math.log2(node_count):.1f}", average_depth < 3 * math.log2(node_count))

print("\n" + ("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"))

r"""
AVL TREE
========

Advanced Algorithms, Lecture 8 (Ivan Bliznets), slides 14-29. Built on the plain
search tree from ../BST/BST.py and the rotations from ../Rotations/Rotations.py.
CLRS only has AVL trees as a problem at the end of chapter 13 (Problem 13-3,
3rd ed. p. 333), so the lecture is the main source here.


THE PROBLEM [slide 14]
----------------------
    Deletions and Insertions can make our binary tree disbalanced.

Insert 1, 2, 3, ..., n into a plain BST and you get a path of height n - 1.
Every operation is O(h), so that is O(n). An AVL tree keeps h = O(log n).


THE DEFINITION [slide 15]
-------------------------
    - h(v) is the height of vertex v, i.e., the longest path from v to a leaf.
    - We say that the height of an empty tree is undefined.
    - AVL tree: self-balancing binary search tree such that for each vertex v
      and its two children u1, u2 we have
                    h(u1) - h(u2) in {-1, 0, 1}.
    - dis_T(v) = h(u1) - h(u2) is the disbalance at vertex v in a tree T.

Two conventions this file fixes:
    HEIGHT counts edges, so a leaf has height 0 (slide 17 confirms it: n0 = 1,
    a single node is a tree of height 0). The slide leaves the empty tree's
    height undefined; this file uses -1 so that "1 + max of the children"
    works everywhere. With -1, a node with one leaf child and no other child
    has disbalance 0 - (-1) = 1, which is allowed, as it should be.
    DISBALANCE is LEFT minus RIGHT. Slide 24 takes u1 as the left child
    ("WLOG assume h(u1) - h(u2) = 2" with u1 drawn on the left). So +2 means
    "too tall on the left" and -2 "too tall on the right".

Every node STORES its height, so checking a disbalance is O(1) instead of a
walk down the whole subtree. The price is that heights must be refreshed on the
way back up after every insert, delete and rotation.


THE HEIGHT BOUND [slide 17]
---------------------------
    Theorem. If an AVL tree T contains n elements, then the height of the tree
    is O(log n).
    - We prove that if AVL T has height h, then T has at least sqrt(2)^h
      vertices.
    - Let n_i be the smallest number of vertices that an AVL-tree of height i
      can contain.
    - Clearly n_0 = 1, n_1 = 2.
    - If tree has height i + 1 then at least one of its subtrees has height i.
    - Hence, the second subtree has a height of size at least i - 1, as we are
      working with an AVL tree.
    - Therefore, we have
          n_(i+1) >= 1 + n_i + n_(i-1) > 2 n_(i-1) >= 2 sqrt(2)^(i-1) = sqrt(2)^(i+1).
    - It follows that h <= log_sqrt(2) n.

(The slide's first bullet prints the exponent as n; it means h, the height.)

The recurrence n_(i+1) = 1 + n_i + n_(i-1) is Fibonacci plus one:
n_i = F(i + 3) - 1, with F(1) = F(2) = 1. Section 7 prints the table and
builds each smallest tree to show it really is that small.

log_sqrt(2) n = 2 log2 n. The slide's bound is deliberately loose; the
Fibonacci growth rate gives the sharper h < 1.44 log2(n + 2) (CLRS Problem
13-3 asks for this one). Both are O(log n), which is all the theorem needs.


INSERTION [slides 23-26]
------------------------
    - Insertion of one element can increase height of some subtrees at most by
      one.
    - Our idea: insert or delete as before and then try to fix potential
      disbalances by rotations and make tree balanced again.
    - Only the vertices on the path from v to the root can increase their
      height.
    - Going up from v to the root find the deepest vertex that violates
      disbalance constraint, i.e. such vertex x with children u1, u2 such that
      |h(u1) - h(u2)| = 2.
    - WLOG assume h(u1) - h(u2) = 2.  Two cases:
        1. h_T'(A) = h - 1 and h_T'(B) = h - 2,
        2. h_T'(A) = h - 2 and h_T'(B) = h - 1.

where A and B are u1's left and right subtrees. In this file's names:

    case I  [slide 25] = LL: A, the OUTER grandchild subtree, grew.
                         One right rotation at x.

                 x                     u1
                / \                   /  \
              u1   C     =>          A    x
             /  \                        / \
            A    B                      B   C

    case II [slide 26] = LR: B, the INNER grandchild subtree, grew.
                         Split B as z with subtrees B1, B2. Left rotation at
                         u1, then right rotation at x. z ends up on top.

                 x                  x                     z
                / \                / \                  /   \
              u1   C    =>        z   C     =>        u1     x
             /  \                / \                 /  \   / \
            A    z             u1   B2              A  B1  B2  C
                / \           /  \
              B1   B2        A    B1

    RR and RL are the mirror images (h(u1) - h(u2) = -2), the "WLOG" half the
    slide does not draw.

Why one rotation is not enough in case II: a right rotation at x would hang B
under x on the right, at the same depth it was, and the tree would lean just as
far the other way. Slide 22's guarantee needs A to be the tallest, which is
exactly case I. The first rotation in case II turns it into case I.

After an insertion's fix, the subtree has the same height it had BEFORE the
insertion, so nothing above it can be out of balance. One fix (one single or
one double rotation) per insertion is enough.


DELETION [slides 23, 27-29]
---------------------------
    - Similarly, deletion of one element can decrease height of some vertices
      at most by one.

Slides 27-29 are titled "Deletion I-III" but are blank in the PDF; the
material was done live. This file follows slide 23's plan: delete as in a
plain BST (copy-the-successor, slides 11-13), then walk back up fixing every
node that has disbalance +2 or -2 with the same four cases.

Two differences from insertion:
    - The child on the tall side can have disbalance 0, which insertion never
      produces. Then a SINGLE rotation is right (treat it as LL or RR). A
      double rotation there would leave the tree unbalanced.
    - A fix can shrink the subtree, so the node above may now be out of
      balance. Deletion may need a fix at every level, O(log n) rotations.


WHAT IS IN THIS FILE
--------------------
    1. AvlNode, with a stored height
    2. height helpers and the rotations, keeping heights right
    3. rebalance: the four cases                     [slides 24-26]
    4. insert                                        [slides 23-26]
    5. delete                                        [slides 11-13, 23]
    6. checks: BST property, stored heights, disbalance
    7. the height bound: n_i table and minimal trees [slide 17]
    8. a top-down ASCII printer
    9. tests

Run with:
    python3 AVL.py
"""

import math
import random


# =====================================================================
# 1. THE NODE
# =====================================================================
# key: the value stored here
# left / right: the children, or None
# height: h(v) from slide 15, stored so it is O(1) to read; a new node is a
#   leaf, height 0

class AvlNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0


# Every rebalance appends the case it used, so the tests can check which of the
# four cases fired.
case_log = []


# =====================================================================
# 2. HEIGHTS AND ROTATIONS
# =====================================================================
# node_height: stored height, -1 for the empty tree
# update_height: recompute one node's height from its children's stored ones
# disbalance: slide 15, left minus right
#
# The rotations are the subtree-style ones from Rotations.py, plus two height
# updates. Order matters: old_top is now BELOW new_top, so it is updated first.

def node_height(node):
    return node.height if node is not None else -1


def update_height(node):
    node.height = 1 + max(node_height(node.left), node_height(node.right))


def disbalance(node):
    return node_height(node.left) - node_height(node.right)


def rotate_right(old_top):
    new_top = old_top.left
    old_top.left = new_top.right  # B moves across
    new_top.right = old_top
    update_height(old_top)  # lower node first
    update_height(new_top)
    return new_top


def rotate_left(old_top):
    new_top = old_top.right
    old_top.right = new_top.left  # B moves across
    new_top.left = old_top
    update_height(old_top)
    update_height(new_top)
    return new_top


# =====================================================================
# 3. REBALANCE: THE FOUR CASES [slides 24-26]
# =====================================================================
# node: the slide's x, a node whose children's heights may differ by 2
# tall_child: the slide's u1, the child on the taller side
#
#   dis(x) = +2, dis(u1) >= 0  -> LL, case I:  right rotation at x
#   dis(x) = +2, dis(u1) <  0  -> LR, case II: left at u1, then right at x
#   dis(x) = -2, dis(u1) <= 0  -> RR, mirror of case I:  left rotation at x
#   dis(x) = -2, dis(u1) >  0  -> RL, mirror of case II: right at u1, then left at x
#
# The ">= 0" / "<= 0" include 0 for deletion's sake (see the docstring).
# Returns the new top of this subtree, which the caller hangs back in place.

def rebalance(node):
    update_height(node)
    balance = disbalance(node)

    if balance == 2:
        tall_child = node.left
        if disbalance(tall_child) >= 0:
            case_log.append("LL")
            return rotate_right(node)
        case_log.append("LR")
        node.left = rotate_left(tall_child)
        return rotate_right(node)

    if balance == -2:
        tall_child = node.right
        if disbalance(tall_child) <= 0:
            case_log.append("RR")
            return rotate_left(node)
        case_log.append("RL")
        node.right = rotate_right(tall_child)
        return rotate_left(node)

    return node  # already within {-1, 0, 1}


# =====================================================================
# 4. INSERT [slides 23-26]
# =====================================================================
# node: the root of the subtree the key goes into
#
# Plain recursive BST insert (slide 9's shape), and on the way back up every
# node on the path gets its height refreshed and is rebalanced if needed. The
# deepest bad node is met first, as slide 24 says, because the recursion
# unwinds from the bottom.
#
# O(log n): one walk down, one walk up.

def insert(node, key):
    if node is None:
        return AvlNode(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        return node  # unique values only (slide 5)
    return rebalance(node)


# =====================================================================
# 5. DELETE [slides 11-13 then 23]
# =====================================================================
# node: the root of the subtree the key is deleted from
# heir: the in-order successor, used when the node has two children
#
# The three BST cases from slides 11-13:
#   leaf or one child -> return the other child (None for a leaf)
#   two children      -> copy the successor's key up (slide 13), then delete
#                        the successor's key from the right subtree
# Then rebalance on the way back up. Unlike insert, more than one node on the
# path may need a fix.
#
# O(log n).

def delete(node, key):
    if node is None:
        return None  # key not present
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        heir = node.right
        while heir.left is not None:
            heir = heir.left
        node.key = heir.key  # (value of v) <- (value of w)
        node.right = delete(node.right, heir.key)
    return rebalance(node)


def search(node, key):
    while node is not None and key != node.key:
        node = node.left if key < node.key else node.right
    return node


# =====================================================================
# 6. CHECKS
# =====================================================================
# check_avl walks the whole tree and returns (is_valid, real_height).
# lower / upper: the open interval this subtree's keys must lie in
# It fails if any of these is false at any node:
#   - the key lies between lower and upper           (BST property)
#   - the stored height equals the real height       (bookkeeping)
#   - the disbalance is -1, 0 or 1                   (slide 15)

def check_avl(node, lower=None, upper=None):
    if node is None:
        return True, -1
    if (lower is not None and node.key <= lower) or (upper is not None and node.key >= upper):
        return False, 0
    left_valid, left_height = check_avl(node.left, lower, node.key)
    right_valid, right_height = check_avl(node.right, node.key, upper)
    real_height = 1 + max(left_height, right_height)
    valid = (left_valid and right_valid
             and node.height == real_height
             and abs(left_height - right_height) <= 1)
    return valid, real_height


def in_order(node, visited):
    if node is not None:
        in_order(node.left, visited)
        visited.append(node.key)
        in_order(node.right, visited)
    return visited


def count_nodes(node):
    return 0 if node is None else 1 + count_nodes(node.left) + count_nodes(node.right)


# =====================================================================
# 7. THE HEIGHT BOUND [slide 17]
# =====================================================================
# minimum_node_counts(top_height): n_0 .. n_top_height from the slide's
#   recurrence n_(i+1) = 1 + n_i + n_(i-1), with n_0 = 1, n_1 = 2.
#
# build_minimal_avl(tree_height): the smallest AVL tree of that height. Its
#   root has one child of height h - 1 and one of height h - 2, each also
#   minimal: exactly the two subtrees the slide's argument uses. Keys are
#   handed out in in-order so the result is a valid BST.
#   next_key: a one-element list, so the recursion can advance the counter

def minimum_node_counts(top_height):
    counts = [1, 2]
    while len(counts) <= top_height:
        counts.append(1 + counts[-1] + counts[-2])
    return counts[:top_height + 1]


def build_minimal_avl(tree_height, next_key):
    if tree_height < 0:
        return None
    left = build_minimal_avl(tree_height - 1, next_key)
    node = AvlNode(next_key[0])
    next_key[0] += 1
    node.left = left
    node.right = build_minimal_avl(tree_height - 2, next_key)
    update_height(node)
    return node


# =====================================================================
# 8. TOP-DOWN ASCII PRINTER
# =====================================================================
# build_lines returns, for one subtree:
#   lines: the picture, one string per row, all the same width
#   width: that width
#   middle: the column where this subtree's root label sits
# label_of: turns a node into its printed label

def build_lines(node, label_of):
    if node is None:
        return [], 0, 0
    label = label_of(node)
    label_width = len(label)
    left_lines, left_width, left_middle = build_lines(node.left, label_of)
    right_lines, right_width, right_middle = build_lines(node.right, label_of)

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


def show(root, with_heights=False, indent="    "):
    if root is None:
        print(indent + "(empty)")
        return
    if with_heights:
        label_of = lambda node: f"{node.key}:{node.height}"
    else:
        label_of = lambda node: str(node.key)
    for line in build_lines(root, label_of)[0]:
        print(indent + line.rstrip())


# =====================================================================
# 9. TESTS
# =====================================================================

def build(keys):
    root = None
    for key in keys:
        root = insert(root, key)
    return root


def check(label, condition):
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    return condition


all_passed = True

print("=" * 72)
print("AVL TREE   -- Lecture 8, slides 14-29")
print("=" * 72)

# --- slide 16: the example AVL tree -----------------------------------
case_log.clear()
slide_root = build([19, 3, 36, 17, 25, 100, 110])
print("\nslide 16 example (labels are key:height):\n")
show(slide_root, with_heights=True)
print()
all_passed &= check("slide 16 tree is AVL and needed no rotations",
                    check_avl(slide_root)[0] and case_log == [])

# --- the four cases, smallest possible trigger for each ----------------
print("\nthe four rebalance cases, each from three inserts:")
for keys, expected_case, slide_note in (([3, 2, 1], "LL", "case I, slide 25"),
                                        ([1, 2, 3], "RR", "mirror of case I"),
                                        ([3, 1, 2], "LR", "case II, slide 26"),
                                        ([1, 3, 2], "RL", "mirror of case II")):
    case_log.clear()
    root = build(keys)
    print(f"\n  insert {keys}  ->  {case_log}  ({slide_note})\n")
    show(root, indent="      ")
    print()
    all_passed &= check(f"{keys}: case {expected_case} fired, root is 2",
                        case_log == [expected_case] and root.key == 2 and check_avl(root)[0])

# --- slide 26 with real subtrees: z comes up -------------------------
# x = 50, u1 = 20, C = 70 with 80, A = 10 with 5, z = 30 with B1 = 25 and B2 = 35
case_log.clear()
slide_26_root = build([50, 20, 70, 10, 30, 80, 25, 35, 5])
case_log.clear()
before = in_order(slide_26_root, [])
print("\nbefore inserting 27 (labels key:height):\n")
show(slide_26_root, with_heights=True)
slide_26_root = insert(slide_26_root, 27)
print(f"\nafter inserting 27  ->  {case_log}:\n")
show(slide_26_root, with_heights=True)
print()
all_passed &= check("27 lands in B1 under z = 30; one LR fix lifts z = 30 to the root",
                    case_log == ["LR"] and slide_26_root.key == 30 and check_avl(slide_26_root)[0])

# --- deletion, with the tall child at disbalance 0 -------------------
case_log.clear()
deletion_root = build([2, 1, 4, 3, 5])
case_log.clear()
deletion_root = delete(deletion_root, 1)
print("\nbuild [2, 1, 4, 3, 5], delete 1:  node 2 is at -2 and its right child 4 is at 0\n")
show(deletion_root)
print()
all_passed &= check("deletion uses a single RR rotation when the tall child is balanced",
                    case_log == ["RR"] and deletion_root.key == 4 and check_avl(deletion_root)[0])

# deletion can need more than one fix: delete from the minimal tree of height 4
next_key = [1]
minimal_root = build_minimal_avl(4, next_key)
case_log.clear()
deepest_right = minimal_root
while deepest_right.right is not None:
    deepest_right = deepest_right.right
minimal_root = delete(minimal_root, deepest_right.key)
all_passed &= check(f"deleting from the minimal height-4 tree needed {len(case_log)} fixes {case_log} "
                    f"(insertion never needs more than one)",
                    len(case_log) >= 2 and check_avl(minimal_root)[0])

# --- random insert/delete ---------------------------------------------
random.seed(15)
failures = 0
max_fixes_per_insert = 0
trial_count = 300
for _ in range(trial_count):
    root = None
    present = set()
    for _ in range(120):
        key = random.randint(0, 80)
        case_log.clear()
        if random.random() < 0.6:
            root = insert(root, key)
            present.add(key)
            max_fixes_per_insert = max(max_fixes_per_insert, len(case_log))
        else:
            root = delete(root, key)
            present.discard(key)
        valid, _ = check_avl(root)
        if not valid or in_order(root, []) != sorted(present):
            failures += 1
            break
print()
all_passed &= check(f"{trial_count} random runs of 120 inserts/deletes: BST property, stored heights, "
                    f"|dis| <= 1, in-order == sorted(set)", failures == 0)
all_passed &= check(f"every insertion needed at most one fix (max seen: {max_fixes_per_insert})",
                    max_fixes_per_insert <= 1)

# --- slide 17: the height bound --------------------------------------
print("\nslide 17: n_i, the fewest nodes an AVL tree of height i can have\n")
print(f"{'i':>4}{'n_i':>8}{'F(i+3)-1':>10}{'sqrt(2)^i':>12}{'built tree':>12}")
print("-" * 46)
counts = minimum_node_counts(12)
fibonacci = [0, 1, 1]
while len(fibonacci) < 20:
    fibonacci.append(fibonacci[-1] + fibonacci[-2])
bound_ok = True
for tree_height, node_count in enumerate(counts):
    next_key = [1]
    minimal = build_minimal_avl(tree_height, next_key)
    built_count = count_nodes(minimal)
    print(f"{tree_height:>4}{node_count:>8}{fibonacci[tree_height + 3] - 1:>10}"
          f"{math.sqrt(2) ** tree_height:>12.1f}{built_count:>12}")
    bound_ok &= (node_count >= math.sqrt(2) ** tree_height
                 and node_count == fibonacci[tree_height + 3] - 1
                 and built_count == node_count
                 and check_avl(minimal)[0]
                 and minimal.height == tree_height)
print()
all_passed &= check("n_i >= sqrt(2)^i, n_i = F(i+3) - 1, and each minimal tree is a valid AVL tree "
                    "of height i with exactly n_i nodes", bound_ok)

# minimal trees are the worst case: removing any leaf either drops the height
# or breaks the AVL rule, so no smaller tree of that height exists.
# real_height / is_balanced ignore the stored heights, which go stale when a
# leaf is cut off by hand.

def real_height(subtree):
    if subtree is None:
        return -1
    return 1 + max(real_height(subtree.left), real_height(subtree.right))


def is_balanced(subtree):
    if subtree is None:
        return True
    return (abs(real_height(subtree.left) - real_height(subtree.right)) <= 1
            and is_balanced(subtree.left) and is_balanced(subtree.right))


def cut_leaf(root, key):
    # unlink the leaf holding key, with no rebalancing
    parent = root
    while True:
        child = parent.left if key < parent.key else parent.right
        if child.key == key:
            if key < parent.key:
                parent.left = None
            else:
                parent.right = None
            return
        parent = child


worst_case_ok = True
for tree_height in range(1, 8):
    minimal = build_minimal_avl(tree_height, [1])
    for key in in_order(minimal, []):
        node = search(minimal, key)
        if node.left is not None or node.right is not None:
            continue  # only leaves
        trimmed = build_minimal_avl(tree_height, [1])  # fresh copy to cut from
        cut_leaf(trimmed, key)
        if real_height(trimmed) == tree_height and is_balanced(trimmed):
            worst_case_ok = False
all_passed &= check("no leaf can be removed from a minimal tree keeping both its height and balance",
                    worst_case_ok)

# sorted input, the plain BST's worst case
for node_count in (100, 1000, 10000):
    root = build(range(node_count))
    loose_bound = math.log(node_count, math.sqrt(2))
    tight_bound = 1.44 * math.log2(node_count + 2)
    print(f"  {node_count:>6} sorted inserts: height {root.height:>2}   "
          f"slide bound log_sqrt2(n) = {loose_bound:5.1f}   1.44 log2(n+2) = {tight_bound:5.1f}")
    all_passed &= check(f"height {root.height} <= log_sqrt2({node_count})", root.height <= loose_bound)

print("\n" + ("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"))

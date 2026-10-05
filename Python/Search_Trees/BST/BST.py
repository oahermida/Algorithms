r"""
BINARY SEARCH TREE
==================

Advanced Algorithms, Lecture 8 (Ivan Bliznets), slides 3-13. The bibliography
(slide 34) points to CLRS chapter 12, which is where the transplant-style delete
in section 6 comes from (CLRS 3rd ed., section 12.3, TRANSPLANT p. 296,
TREE-DELETE p. 298).

The simpler file ../../Data_Structures/10_Binary_Tree.py has insert, in-order
and height only. This file is the full set of operations the lecture lists.


THE OPERATIONS [slide 3]
------------------------
    Binary Search Trees support the following basic operations:
      - Search
      - Min/Max
      - Find next (predecessor)
      - Find previous (successor)
      - Insert
      - Delete
    Running time O(h), h - height of the tree.
    The height of the tree in the worst case can be linear.
    However, AVL and red-black trees have O(log n) height.

Note: slide 3 swaps the two names. "Next" is the SUCCESSOR (the next bigger key)
and "previous" is the PREDECESSOR. This file uses the standard meaning.


THE ORDER RULE [slides 4-5]
---------------------------
    "left child" < "parent" < "right child"
    generally NOT a complete binary tree
    only unique values (this course)

So inserting a key that is already there does nothing (section 2).

The rule is about whole subtrees, not just children: every key in the left
subtree is smaller, every key in the right subtree is bigger. Section 8 checks
exactly that.


SEARCH AND INSERT [slides 7-9]
------------------------------
    algorithm SearchInSearchTree(T, n)               [slide 7]
        if T empty then return not found
        r <- the root of T,  x <- the value in r
        if n = x then return r
        if n < x then return SearchInSearchTree(left subtree of T, n)
        else return SearchInSearchTree(right subtree of T, n)

Slide 9 gives insert as recursive C code: walk down like a search, and when you
fall off the tree, put the new node there. Equal keys fall through both
branches, so they are ignored. Sections 2-3 do both walks with a loop instead of
recursion (CLRS's TREE-SEARCH and TREE-INSERT); the path taken is the same.


SUCCESSOR [slide 10]
--------------------
    algorithm InOrderSuccessor(T, v)
        input : search tree T with node v having two children
        u <- the right child of v
        w <- the lowest left descendant of u
        return w

The slide only needs the two-children case, because that is the only case
delete uses. Section 4 also handles "no right child" (CLRS TREE-SUCCESSOR,
p. 292): then the successor is the first ancestor you reach by stepping up
from a LEFT child.


DELETE [slides 11-13]
---------------------
    algorithm RemoveFromSearchTree(T, n)
        if there is no node with value n in T then return T
        v <- the node in T with value n
        if v is a leaf then
            return T with v removed
        else if v has 1 child then
            return T with v replaced by the child of v
        else /* the difficult case: v has two children */
            w <- InOrderSuccessor(T, v)
            (value of v) <- (value of w)
            /* now we use that w has no left child */
            if w has a right child then
                return T with w replaced by its right child
            else /* w has no children, so it is a leaf */
                return T with w removed

    Example [slide 13]: "removed former root node 12, replaced it with its
    inorder successor 15".

LECTURE vs CLRS. The lecture COPIES the successor's value into v and then
removes the successor's node. CLRS 3rd edition does not copy: it MOVES the
successor node itself into v's place with TRANSPLANT. Both give the same keys in
the same shape. The difference shows when other code holds a pointer to a node:
with copying, the node that "was 15" now holds 12's place and the old 15 node is
gone. CLRS p. 299 explains it chose moving for that reason.

This file has both: section 6 is the CLRS version, section 7 the slide version.
The tests run both and check they produce the same tree.


WHAT IS IN THIS FILE
--------------------
    1. TreeNode, with a parent pointer (CLRS style)
    2. insert                   [slides 8-9, CLRS p. 294]
    3. search                   [slide 7, CLRS p. 290]
    4. minimum and successor    [slide 10, CLRS pp. 291-292]
    5. in-order walk            [CLRS p. 288]
    6. delete, transplant style [CLRS pp. 296-298]
    7. delete, copy style       [slides 11-13]
    8. checks: BST property, parent pointers, height
    9. a top-down ASCII printer
   10. tests

Run with:
    python3 BST.py
"""

import random


# =====================================================================
# 1. THE NODE
# =====================================================================
# key: the value stored here
# left / right: the two children, or None
# parent: the node above, or None for the root
#
# The parent pointer is what lets successor walk UP and lets delete re-hang a
# subtree under the right node. 10_Binary_Tree.py has no parent pointer because
# it never needs to go up.

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class BinarySearchTree:
    def __init__(self):
        self.root = None  # empty tree


# =====================================================================
# 2. INSERT [slides 8-9, CLRS 12.3 p. 294]
# =====================================================================
# current: the node the walk is standing on
# trailing: the node one step behind; it becomes the new node's parent
#
# Walk down as in search. When current falls off the tree, trailing is the last
# real node, and the new node hangs under it on the correct side.
# A key that is already present is ignored (slide 5: unique values).
#
# O(h).

def insert(tree, key):
    trailing = None
    current = tree.root
    while current is not None:
        trailing = current
        if key == current.key:
            return current  # already there: do nothing
        if key < current.key:
            current = current.left
        else:
            current = current.right

    new_node = TreeNode(key)
    new_node.parent = trailing
    if trailing is None:
        tree.root = new_node  # tree was empty
    elif key < trailing.key:
        trailing.left = new_node
    else:
        trailing.right = new_node
    return new_node


# =====================================================================
# 3. SEARCH [slide 7, CLRS 12.2 p. 290]
# =====================================================================
# current: the node being compared with key
#
# Each comparison throws away one whole subtree. Returns the node, or None
# ("not found").
#
# O(h).

def search(tree, key):
    current = tree.root
    while current is not None and key != current.key:
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return current


# =====================================================================
# 4. MINIMUM AND SUCCESSOR [slide 10, CLRS 12.2 pp. 291-292]
# =====================================================================
# node: where the walk starts
# ancestor: the node above, while climbing
#
# minimum: keep going left. The leftmost node has the smallest key.
#
# successor, two cases:
#   right subtree exists -> the minimum of the right subtree  (slide 10)
#   no right subtree     -> climb while we are a RIGHT child; the first time we
#                           step up from a LEFT child, that parent is next.
#                           If we reach the root first, there is no successor.
#
# O(h) each.

def minimum(node):
    while node.left is not None:
        node = node.left
    return node


def successor(node):
    if node.right is not None:
        return minimum(node.right)  # slide 10: lowest left descendant of the right child
    ancestor = node.parent
    while ancestor is not None and node is ancestor.right:
        node = ancestor
        ancestor = ancestor.parent
    return ancestor


# =====================================================================
# 5. IN-ORDER WALK [CLRS 12.1 p. 288]
# =====================================================================
# Left subtree, then the node, then the right subtree. On a BST this lists the
# keys in sorted order, which is what the tests lean on.

def in_order(node, visited):
    if node is not None:
        in_order(node.left, visited)
        visited.append(node.key)
        in_order(node.right, visited)
    return visited


# =====================================================================
# 6. DELETE, CLRS TRANSPLANT STYLE [CLRS 12.3 pp. 296-298]
# =====================================================================
# transplant(tree, old_subtree, new_subtree):
#   hang new_subtree where old_subtree used to hang. Only the link from above
#   changes; old_subtree's own children are not touched.
#
# delete_node:
#   doomed: the node being removed (CLRS calls it z)
#   heir: its successor, used only in the two-children case (CLRS calls it y)
#
#   no left child   -> replace doomed by its right child (covers the leaf case,
#                      since that right child may be None)
#   no right child  -> replace doomed by its left child
#   two children    -> heir = minimum of the right subtree; heir has no left child.
#                      If heir is deeper than doomed's right child, first lift
#                      heir's right child into heir's place and give heir
#                      doomed's right subtree. Then put heir where doomed was
#                      and give it doomed's left subtree.
#
# O(h): the only walk is minimum().

def transplant(tree, old_subtree, new_subtree):
    if old_subtree.parent is None:
        tree.root = new_subtree
    elif old_subtree is old_subtree.parent.left:
        old_subtree.parent.left = new_subtree
    else:
        old_subtree.parent.right = new_subtree
    if new_subtree is not None:
        new_subtree.parent = old_subtree.parent


def delete_node(tree, doomed):
    if doomed.left is None:
        transplant(tree, doomed, doomed.right)
    elif doomed.right is None:
        transplant(tree, doomed, doomed.left)
    else:
        heir = minimum(doomed.right)
        if heir.parent is not doomed:
            transplant(tree, heir, heir.right)  # heir's right child takes heir's place
            heir.right = doomed.right
            heir.right.parent = heir
        transplant(tree, doomed, heir)
        heir.left = doomed.left
        heir.left.parent = heir


def delete(tree, key):
    doomed = search(tree, key)
    if doomed is not None:  # missing key: leave the tree alone (slide 11)
        delete_node(tree, doomed)


# =====================================================================
# 7. DELETE, THE SLIDE'S COPY STYLE [slides 11-13]
# =====================================================================
# doomed: the node holding the key (the slide's v)
# heir: its in-order successor (the slide's w)
#
# Same three cases as the slide. In the two-children case the heir's KEY is
# copied up into doomed, and then the heir's node is removed. The heir has no
# left child, so removing it is always case 1 or 2, never case 3 again.

def delete_by_copy(tree, key):
    doomed = search(tree, key)
    if doomed is None:
        return
    if doomed.left is not None and doomed.right is not None:
        heir = successor(doomed)  # slide 10
        doomed.key = heir.key  # (value of v) <- (value of w)
        doomed = heir  # now remove w instead; it has no left child
    only_child = doomed.left if doomed.left is not None else doomed.right
    transplant(tree, doomed, only_child)  # leaf: only_child is None


# =====================================================================
# 8. CHECKS
# =====================================================================
# is_bst: every key lies strictly between the bounds handed down from above.
#   lower / upper: the open interval this subtree's keys must fall in
#   Checking only "left child < parent" is not enough; a key deep in the left
#   subtree can still be bigger than the root.
#
# parents_consistent: every child's parent pointer points back at it.
#
# height: longest path in EDGES from node to a leaf, as slide 15 defines it.
#   A leaf has height 0. The slide calls the empty tree's height undefined; -1
#   is used here so that "1 + max of the children" works for every node.
#   (10_Binary_Tree.py counts nodes instead, so a leaf is 1 there.)

def is_bst(node, lower=None, upper=None):
    if node is None:
        return True
    if lower is not None and node.key <= lower:
        return False
    if upper is not None and node.key >= upper:
        return False
    return is_bst(node.left, lower, node.key) and is_bst(node.right, node.key, upper)


def parents_consistent(node):
    if node is None:
        return True
    for child in (node.left, node.right):
        if child is not None and child.parent is not node:
            return False
    return parents_consistent(node.left) and parents_consistent(node.right)


def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


# =====================================================================
# 9. TOP-DOWN ASCII PRINTER
# =====================================================================
# build_lines returns, for one subtree:
#   lines: the picture, one string per row, all the same width
#   width: that width
#   middle: the column where this subtree's root label sits
#
# Each node is drawn with its children's pictures side by side underneath,
# joined by "_" runs and "/" "\" strokes.

def build_lines(node):
    if node is None:
        return [], 0, 0
    label = str(node.key)
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


def show(tree, indent="    "):
    if tree.root is None:
        print(indent + "(empty)")
        return
    for line in build_lines(tree.root)[0]:
        print(indent + line.rstrip())


# =====================================================================
# 10. TESTS
# =====================================================================

def build(keys):
    tree = BinarySearchTree()
    for key in keys:
        insert(tree, key)
    return tree


def check(label, condition):
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    return condition


all_passed = True

print("=" * 72)
print("BINARY SEARCH TREE   -- Lecture 8, slides 3-13;  CLRS chapter 12")
print("=" * 72)

# --- slide 4: the example tree --------------------------------------
print("\nslide 4 example, inserted as 19, 3, 36, 17, 25, 100, 50, 200:\n")
slide_four = build([19, 3, 36, 17, 25, 100, 50, 200])
show(slide_four)
print()
all_passed &= check("in-order is sorted", in_order(slide_four.root, []) == [3, 17, 19, 25, 36, 50, 100, 200])
all_passed &= check("search(25) finds 25", search(slide_four, 25).key == 25)
all_passed &= check("search(26) is not found", search(slide_four, 26) is None)
all_passed &= check("minimum is 3", minimum(slide_four.root).key == 3)
all_passed &= check("successor(19) = 25 (has right subtree)", successor(search(slide_four, 19)).key == 25)
all_passed &= check("successor(17) = 19 (climbs up)", successor(search(slide_four, 17)).key == 19)
all_passed &= check("successor(200) = None (largest key)", successor(search(slide_four, 200)) is None)
insert(slide_four, 25)
all_passed &= check("inserting 25 again changes nothing (slide 5)", in_order(slide_four.root, []).count(25) == 1)

# --- slides 11-13: deleting the root 12 -----------------------------
slide_keys = [12, 7, 20, 5, 9, 15, 24, 19]
print("\nslides 11-13 example tree:\n")
show(build(slide_keys))

for method_name, method in (("delete", delete), ("delete_by_copy", delete_by_copy)):
    tree = build(slide_keys)
    method(tree, 12)
    print(f"\nafter {method_name}(12):\n")
    show(tree)
    print()
    all_passed &= check(f"{method_name}: new root is 15, as slide 13 says", tree.root.key == 15)
    all_passed &= check(f"{method_name}: 19 now hangs under 20", tree.root.right.left.key == 19)

# the three cases one at a time, on the same tree
leaf_tree = build(slide_keys)
delete(leaf_tree, 5)
all_passed &= check("delete leaf 5: 7 has no left child", leaf_tree.root.left.left is None)
one_child_tree = build(slide_keys)
delete(one_child_tree, 15)
all_passed &= check("delete 15 (one child): 19 takes its place", one_child_tree.root.right.left.key == 19)
missing_tree = build(slide_keys)
delete(missing_tree, 99)
all_passed &= check("delete missing key 99: tree unchanged", in_order(missing_tree.root, []) == sorted(slide_keys))

# --- randomized insert/delete ---------------------------------------
random.seed(8)
trial_count = 300
failures = 0
for _ in range(trial_count):
    for method in (delete, delete_by_copy):
        tree = BinarySearchTree()
        present = set()
        for _ in range(60):
            key = random.randint(0, 40)
            if random.random() < 0.6:
                insert(tree, key)
                present.add(key)
            else:
                method(tree, key)
                present.discard(key)
            if (not is_bst(tree.root) or not parents_consistent(tree.root)
                    or in_order(tree.root, []) != sorted(present)
                    or (tree.root is not None and tree.root.parent is not None)):
                failures += 1
                break
print()
all_passed &= check(f"random insert/delete, both delete methods: {2 * trial_count - failures}/{2 * trial_count} runs "
                    f"kept BST property, parent pointers, in-order == sorted(set)", failures == 0)

# both delete methods must build the SAME shape, not just the same keys
random.seed(13)
shape_mismatches = 0
for _ in range(trial_count):
    keys = random.sample(range(100), 30)
    transplant_tree = build(keys)
    copy_tree = build(keys)
    for key in random.sample(keys, 15):
        delete(transplant_tree, key)
        delete_by_copy(copy_tree, key)
    if build_lines(transplant_tree.root)[0] != build_lines(copy_tree.root)[0]:
        shape_mismatches += 1
all_passed &= check("transplant delete and copy delete give identical shapes", shape_mismatches == 0)

# successor agrees with the in-order list everywhere
random.seed(21)
tree = build(random.sample(range(1000), 200))
ordered = in_order(tree.root, [])
successor_ok = all(
    (successor(search(tree, key)).key if successor(search(tree, key)) else None)
    == (ordered[position + 1] if position + 1 < len(ordered) else None)
    for position, key in enumerate(ordered))
all_passed &= check("successor(k) is the next key in the in-order list, for all 200 keys", successor_ok)

# --- why the lecture moves on to AVL: sorted input is a path (slide 14) ---
sorted_tree = build(range(1, 101))
random_tree = build(random.sample(range(1, 101), 100))
print(f"\n  100 keys inserted in sorted order: height {height(sorted_tree.root)} (a path, slide 3 'linear')")
print(f"  100 keys inserted in random order: height {height(random_tree.root)}")
all_passed &= check("sorted insertion gives height n - 1 = 99", height(sorted_tree.root) == 99)

print("\n" + ("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"))

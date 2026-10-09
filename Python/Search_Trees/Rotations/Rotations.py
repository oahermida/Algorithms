r"""
ROTATIONS
Lecture 8, slides 18-22; CLRS 3rd ed., section 13.2 (p. 313).

Notes: [[Rotations — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Rotations — Code Notes.md

What is in this file:
    1. TreeNode and a small tree builder
    2. left_rotate / right_rotate, CLRS style      [slides 20-21, CLRS p. 313]
    3. rotate_left / rotate_right, subtree style   [slides 20-21]
    4. a top-down ASCII printer
    5. tests: slide picture, in-order kept, inverse, slide 22 claim

Run with:
    python3 Rotations.py
"""

import copy
import random


# =====================================================================
# 1. THE NODE AND A BUILDER
# =====================================================================
# key: the value stored here
# left / right: the children, or None
# parent: the node above, or None at the root (only the CLRS version uses it)

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class BinarySearchTree:
    def __init__(self):
        self.root = None


def insert(tree, key):
    # plain BST insert (see ../BST/BST.py), only here to build test trees
    trailing = None
    current = tree.root
    while current is not None:
        trailing = current
        if key == current.key:
            return
        current = current.left if key < current.key else current.right
    new_node = TreeNode(key)
    new_node.parent = trailing
    if trailing is None:
        tree.root = new_node
    elif key < trailing.key:
        trailing.left = new_node
    else:
        trailing.right = new_node


def in_order(node, visited):
    if node is not None:
        in_order(node.left, visited)
        visited.append(node.key)
        in_order(node.right, visited)
    return visited


def height(node):
    # slide 15: edges on the longest path down; a leaf is 0, empty is -1 here
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def disbalance(node):
    # slide 15: dis(v) = h(u1) - h(u2), taken as left minus right
    return height(node.left) - height(node.right)


# =====================================================================
# 2. CLRS STYLE, WITH PARENT POINTERS [CLRS 13.2 p. 313]
# =====================================================================
# CLRS LEFT-ROTATE(T, x), steps in the same order:
#   1. y = x.right
#   2. x.right = y.left              <- B moves across
#   3. if y.left != NIL: y.left.p = x
#   4. y.p = x.p                     <- y takes x's place under x's parent
#   5-9. fix the parent's child link (or T.root)
#  10. y.left = x
#  11. x.p = y
#
# Notes: [[Rotations — Code Notes#2. CLRS style, with parent pointers]] (variables, right_rotate)

def left_rotate(tree, lower_top):
    riser = lower_top.right
    middle = riser.left
    lower_top.right = middle  # B moves across
    if middle is not None:
        middle.parent = lower_top
    riser.parent = lower_top.parent  # riser takes lower_top's place
    if lower_top.parent is None:
        tree.root = riser
    elif lower_top is lower_top.parent.left:
        lower_top.parent.left = riser
    else:
        lower_top.parent.right = riser
    riser.left = lower_top
    lower_top.parent = riser


def right_rotate(tree, lower_top):
    riser = lower_top.left
    middle = riser.right
    lower_top.left = middle  # B moves across
    if middle is not None:
        middle.parent = lower_top
    riser.parent = lower_top.parent
    if lower_top.parent is None:
        tree.root = riser
    elif lower_top is lower_top.parent.right:
        lower_top.parent.right = riser
    else:
        lower_top.parent.left = riser
    riser.right = lower_top
    lower_top.parent = riser


# =====================================================================
# 3. SUBTREE STYLE, RETURNING THE NEW TOP [slides 20-21]
# =====================================================================
# Notes: [[Rotations — Code Notes#3. Subtree style, returning the new top]] (variables, how the caller uses it)

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
# 4. TOP-DOWN ASCII PRINTER
# =====================================================================
# build_lines returns, for one subtree:
#   lines: the picture, one string per row, all the same width
#   width: that width
#   middle: the column where this subtree's root label sits

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


def show(root, indent="    "):
    for line in build_lines(root)[0]:
        print(indent + line.rstrip())


def shape(node):
    # the tree as nested tuples, so two trees can be compared for equal SHAPE
    if node is None:
        return None
    return (node.key, shape(node.left), shape(node.right))


# =====================================================================
# 5. TESTS
# =====================================================================

def check(label, condition):
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    return condition


all_passed = True

print("=" * 72)
print("ROTATIONS   -- Lecture 8, slides 18-22;  CLRS 13.2")
print("=" * 72)

# --- the slide 20 picture, with numbers --------------------------------
# keys chosen so A < x < B < y < C:  A = 10, x = 20, B = 30, y = 40, C = 50
print("\nslide 20 with numbers: A = 10, x = 20, B = 30, y = 40, C = 50\n")
slide_tree = BinarySearchTree()
for key in (40, 20, 50, 10, 30):
    insert(slide_tree, key)
show(slide_tree.root)
before_order = in_order(slide_tree.root, [])

right_rotate(slide_tree, slide_tree.root)
print("\nafter right_rotate at y = 40:\n")
show(slide_tree.root)
print()
all_passed &= check("x = 20 is the new root", slide_tree.root.key == 20)
all_passed &= check("y = 40 is x's right child", slide_tree.root.right.key == 40)
all_passed &= check("B = 30 moved across to y's left", slide_tree.root.right.left.key == 30)
all_passed &= check("B's parent pointer now points at y", slide_tree.root.right.left.parent.key == 40)
all_passed &= check(f"in-order unchanged: {in_order(slide_tree.root, [])}",
                    in_order(slide_tree.root, []) == before_order)

left_rotate(slide_tree, slide_tree.root)
print("\nafter left_rotate at x = 20 (slide 21, back again):\n")
show(slide_tree.root)
print()
all_passed &= check("left rotation undoes the right rotation",
                    shape(slide_tree.root) == (40, (20, (10, None, None), (30, None, None)), (50, None, None)))

# --- rotation below the root: the parent's child link is updated --------
deep_tree = BinarySearchTree()
for key in (60, 40, 80, 20, 50, 10, 30):
    insert(deep_tree, key)
right_rotate(deep_tree, deep_tree.root.left)
all_passed &= check("rotating at a non-root node re-links its parent (60.left becomes 20)",
                    deep_tree.root.left.key == 20 and deep_tree.root.left.parent is deep_tree.root)

# --- random trees: many rotations, order never changes -------------------
random.seed(18)
order_failures = 0
parent_failures = 0
style_mismatches = 0
for _ in range(300):
    tree = BinarySearchTree()
    for key in random.sample(range(200), 40):
        insert(tree, key)
    expected = in_order(tree.root, [])
    for _ in range(50):
        # walk to a random node
        node = tree.root
        while random.random() < 0.7:
            next_node = random.choice((node.left, node.right))
            if next_node is None:
                break
            node = next_node

        # the subtree-style version on a copy of the same subtree must agree
        subtree_copy = copy.deepcopy(node)
        if random.random() < 0.5 and node.left is not None:
            right_rotate(tree, node)
            subtree_copy = rotate_right(subtree_copy)
            if shape(subtree_copy) != shape(node.parent):
                style_mismatches += 1
        elif node.right is not None:
            left_rotate(tree, node)
            subtree_copy = rotate_left(subtree_copy)
            if shape(subtree_copy) != shape(node.parent):
                style_mismatches += 1
    if in_order(tree.root, []) != expected:
        order_failures += 1
    stack = [tree.root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child is not None:
                if child.parent is not node:
                    parent_failures += 1
                stack.append(child)
    if tree.root.parent is not None:
        parent_failures += 1

print()
all_passed &= check("300 random trees x 50 random rotations: in-order never changed (slide 19)",
                    order_failures == 0)
all_passed &= check("parent pointers still consistent after every run", parent_failures == 0)
all_passed &= check("CLRS-style and subtree-style rotations build the same shape", style_mismatches == 0)

# --- slide 22: if A is the tallest, a right rotation reduces the disbalance --
random.seed(22)
cases_seen = 0
claim_failures = 0
for _ in range(3000):
    tree = BinarySearchTree()
    for key in random.sample(range(60), random.randint(3, 25)):
        insert(tree, key)
    stack = [tree.root]
    while stack:
        node = stack.pop()
        stack += [child for child in (node.left, node.right) if child is not None]
        if node.left is None:
            continue
        height_a = height(node.left.left)
        height_b = height(node.left.right)
        height_c = height(node.right)
        if height_a > height_b and height_a > height_c:
            cases_seen += 1
            before = disbalance(node)  # dis_T(y)
            after = disbalance(rotate_right(copy.deepcopy(node)))  # dis_T'(x)
            if not after <= before - 2:  # the docstring's 'smaller by at least 2'
                claim_failures += 1
all_passed &= check(f"slide 22: h(A) > h(B), h(C)  =>  dis_T'(x) < dis_T(y) (by >= 2), on {cases_seen} cases",
                    claim_failures == 0 and cases_seen > 0)

print("\n" + ("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"))

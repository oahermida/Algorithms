r"""
BINARY SEARCH TREE
Lecture 8, slides 3-13; CLRS 3rd ed., chapter 12 (pp. 288-299).

Notes: [[BST — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/BST — Code Notes.md

What is in this file:
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
# Notes: [[BST — Code Notes#1. The node]] (variables, why a parent pointer)

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
# Notes: [[BST — Code Notes#2. Insert]] (variables, how the walk works)

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
# Notes: [[BST — Code Notes#4. Minimum and successor]] (variables, the two successor cases)

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
# Notes: [[BST — Code Notes#6. Delete, CLRS transplant style]] (transplant, variables, the three cases)

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
# Notes: [[BST — Code Notes#8. Checks]] (is_bst, parents_consistent, height)

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
# Notes: [[BST — Code Notes#9. Top-down ASCII printer]] (what build_lines returns)

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

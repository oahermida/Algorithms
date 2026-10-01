# Binary tree: each node has a value and up to two children (left and right)
# Here, a binary search tree: smaller values go left, larger go right

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:  # empty spot found: the new node goes here
        return TreeNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def in_order(root, visited):
    # left subtree, then this node, then right subtree: gives sorted order
    if root is not None:
        in_order(root.left, visited)
        visited.append(root.value)
        in_order(root.right, visited)
    return visited

def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))

root = None
for value in [8, 3, 10, 1, 6, 14]:
    root = insert(root, value)

#        8
#       / \
#      3   10
#     / \    \
#    1   6    14
left_child = root.left.value  # 3
right_child = root.right.value  # 10
sorted_values = in_order(root, [])  # [1, 3, 6, 8, 10, 14]
tree_height = height(root)  # 3

# Linked list: a chain of nodes, each one holds a value and points to the next
# Python has no built-in one, so you make a small class
# Cost: adding at the front is fast; reaching item k means walking k steps

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node  # None marks the end of the chain

# Build 1 -> 2 -> 3 by adding at the front, last value first
head = None
for value in [3, 2, 1]:
    head = Node(value, head)

def chain_to_text(head):
    parts = []
    current = head
    while current is not None:  # walk until we fall off the end
        parts.append(str(current.value))
        current = current.next_node
    return " -> ".join(parts)

chain = chain_to_text(head)  # "1 -> 2 -> 3"

# Insert 99 after the first node: just re-point two arrows, nothing shifts
head.next_node = Node(99, head.next_node)  # 1 -> 99 -> 2 -> 3

# Remove the head: point head at the second node
head = head.next_node  # 99 -> 2 -> 3

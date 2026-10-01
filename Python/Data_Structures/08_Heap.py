# Heap (max-heap): a complete binary tree where every parent >= its children,
# so the largest value is always at the root (Lecture 6-7, slides 15-28)
# Stored in a plain list, no pointers (slide 22):
#   children of position i: 2i + 1 and 2i + 2
#   parent of position i:   (i - 1) // 2

def parent_of(position):
    return (position - 1) // 2

def upheap(heap, position):
    # move the value at position up while it is bigger than its parent
    while position > 0 and heap[position] > heap[parent_of(position)]:
        parent = parent_of(position)
        heap[position], heap[parent] = heap[parent], heap[position]  # swap
        position = parent

def downheap(heap, position, size):
    # move the value at position down while a child is bigger than it
    # size: how much of the list counts as heap (heap sort shrinks it)
    while True:
        left = 2 * position + 1
        right = 2 * position + 2
        largest = position
        if left < size and heap[left] > heap[largest]:
            largest = left
        if right < size and heap[right] > heap[largest]:
            largest = right
        if largest == position:  # both children are smaller: done
            return
        heap[position], heap[largest] = heap[largest], heap[position]  # swap with the bigger child
        position = largest

def add(heap, value):
    heap.append(value)  # new value goes in the next free spot at the bottom
    upheap(heap, len(heap) - 1)  # then climbs to where it belongs

def extract_max(heap):
    largest = heap[0]
    last = heap.pop()  # take the bottom-right value off
    if heap:  # if anything is left, put it at the root and let it sink
        heap[0] = last
        downheap(heap, 0, len(heap))
    return largest

def construct_heap(array):
    # turn any list into a heap in O(n) (slides 24-25)
    # leaves are already heaps, so start at the last parent and work back to the root
    for position in range(len(array) // 2 - 1, -1, -1):
        downheap(array, position, len(array))

def heap_sort(array):
    # in place, no extra list (slide 26): the largest goes to the end, then the heap shrinks by one
    construct_heap(array)
    for size in range(len(array) - 1, 0, -1):
        array[0], array[size] = array[size], array[0]
        downheap(array, 0, size)

# Building by adding one at a time
heap = []
for number in [5, 1, 8, 3, 2]:
    add(heap, number)
# heap is [8, 3, 5, 1, 2]
#        8
#       / \
#      3   5
#     / \
#    1   2
largest = heap[0]  # 8, look without removing

while heap:
    largest_item = extract_max(heap)  # 8, then 5, 3, 2, 1

# Turning a whole list into a heap at once
numbers = [3, 9, 2, 7, 4]
construct_heap(numbers)  # [9, 7, 2, 3, 4]

# Heap sort
unsorted = [5, 1, 8, 3, 2]
heap_sort(unsorted)  # [1, 2, 3, 5, 8]

# Priority queue (slide 28): tuples compare by their first item,
# so (priority, task) pairs come out highest priority first
tasks = []
add(tasks, (1, "wash up"))
add(tasks, (3, "hand in practical"))
add(tasks, (2, "revise logic"))
while tasks:
    priority, task = extract_max(tasks)  # "hand in practical", then "revise logic", then "wash up"

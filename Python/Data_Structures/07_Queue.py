# Queue: first in, first out (like a line at a till)
# Built by hand: a list plus the index of the front item
# Removing from the front just moves that index forward, so nothing shifts
# (list.pop(0) would work too, but it shifts every remaining item: O(n) per call)

class Queue:
    def __init__(self):
        self.items = []
        self.front = 0  # index of the next item to come out

    def enqueue(self, item):
        self.items.append(item)  # join at the back

    def dequeue(self):
        item = self.items[self.front]
        self.front += 1  # the old front stays in the list, but is never looked at again
        return item

    def peek(self):
        return self.items[self.front]

    def is_empty(self):
        return self.front == len(self.items)

queue = Queue()
queue.enqueue("first")
queue.enqueue("second")
queue.enqueue("third")
front_item = queue.peek()  # "first", look without removing

while not queue.is_empty():
    front_item = queue.dequeue()  # "first", then "second", then "third"

# Example: breadth-first search on a grid, distance from (0, 0) to every square
# 0 = open, 1 = wall; moves go up/down/left/right
grid = [
    [0, 0, 1],
    [1, 0, 0],
    [0, 0, 0],
]
rows, columns = len(grid), len(grid[0])
distance = [[None] * columns for _ in range(rows)]
distance[0][0] = 0
to_visit = Queue()
to_visit.enqueue((0, 0))
while not to_visit.is_empty():
    row, column = to_visit.dequeue()
    for row_step, column_step in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_row, next_column = row + row_step, column + column_step
        inside = 0 <= next_row < rows and 0 <= next_column < columns
        if inside and grid[next_row][next_column] == 0 and distance[next_row][next_column] is None:
            distance[next_row][next_column] = distance[row][column] + 1
            to_visit.enqueue((next_row, next_column))
# distance ends as (None = wall or unreachable):
# [[0,    1,    None],
#  [None, 2,    3   ],
#  [4,    3,    4   ]]

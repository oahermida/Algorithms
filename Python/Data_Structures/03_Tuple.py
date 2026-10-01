# Tuple: like a list, but it can't be changed after it's made
# Good for small fixed groups of values, like a grid coordinate (row, column)

position = (2, 3)
row_part = position[0]  # 2
column_part = position[1]  # 3

# Unpacking: give each part its own name in one line
row, column = position  # row = 2, column = 3

# Trying to change it fails
try:
    position[0] = 5
except TypeError as error:
    error_message = str(error)  # 'tuple' object does not support item assignment

# Because tuples can't change, they can be dict keys and set items (lists can't)
visited = {(0, 0), (0, 1), (1, 1)}
was_visited = (0, 1) in visited  # True

# A function returning two values is really returning one tuple (P3_3A line 113)
def smallest_and_largest(numbers):
    return min(numbers), max(numbers)

result = smallest_and_largest([4, 9, 1])  # (1, 9)
smallest, largest = result  # smallest = 1, largest = 9

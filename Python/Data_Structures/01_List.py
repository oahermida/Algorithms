# List: Python's dynamic array, an ordered row of items you reach by index
# Cost: index/append/pop-from-end are fast; insert/pop at the front shift every item

numbers = [10, -3, -2, 3]

# Reading
first_item = numbers[0]  # 10, indexes start at 0
last_item = numbers[-1]  # 3, negative indexes count from the end
length = len(numbers)  # 4

# Changing
numbers[1] = 99  # overwrite one slot -> [10, 99, -2, 3]
numbers.append(7)  # add to the end -> [10, 99, -2, 3, 7]
removed = numbers.pop()  # remove from the end and get it back: 7 -> [10, 99, -2, 3]
numbers.insert(0, 5)  # add at index 0, every other item shifts right -> [5, 10, 99, -2, 3]

# Slicing: numbers[start:stop] copies a piece, stop is not included
middle = numbers[1:3]  # [10, 99]

# Making a list of a fixed size up front (what P3_3A does with grid)
empty_slots = [None] * 4  # [None, None, None, None]

# Looping over just the values
total = 0
for number in numbers:
    total += number  # 115

# Looping over index and value together
for position, number in enumerate(numbers):
    if number == 99:
        position_of_99 = position  # 2

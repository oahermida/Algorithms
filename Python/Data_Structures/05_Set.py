# Set: an unordered collection with no duplicates
# Cost: "is x in it?" is fast on average (a list has to check every item)

seen = {3, 1, 4}
seen.add(1)  # already there: nothing happens
seen.add(5)  # {1, 3, 4, 5}
has_four = 4 in seen  # True

seen.discard(3)  # remove if present, no error if not -> {1, 4, 5}

# Removing duplicates from a list
numbers = [2, 2, 7, 1, 7]
unique_values = set(numbers)  # {1, 2, 7}

# Set maths
odd = {1, 3, 5, 7}
prime = {2, 3, 5, 7}
in_both = odd & prime  # {3, 5, 7}
in_either = odd | prime  # {1, 2, 3, 5, 7}
odd_not_prime = odd - prime  # {1}

# Note: {} makes an empty dict, not a set; use set()
empty_set = set()

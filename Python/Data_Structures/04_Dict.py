# Dict: a hash map from keys to values
# Cost: lookup, insert and delete by key are fast on average, no matter the size

ages = {"anna": 21, "ben": 19}

# Reading
anna_age = ages["anna"]  # 21
carl_age = ages.get("carl", "not there")  # "not there"; ages["carl"] would raise KeyError

# Adding, changing, removing
ages["carl"] = 23  # new key
ages["ben"] = 20  # existing key: overwrite
del ages["anna"]  # ages is now {"ben": 20, "carl": 23}
has_ben = "ben" in ages  # True, checks keys, not values

# Looping over keys and values together
total_age = 0
for name, age in ages.items():
    total_age += age  # 43

# Common use: counting
word_counts = {}
for word in "the cat and the hat".split():
    word_counts[word] = word_counts.get(word, 0) + 1
# {"the": 2, "cat": 1, "and": 1, "hat": 1}

# Tuples as keys: a sparse grid that only stores the squares that matter
sparse_grid = {(0, 0): 10, (3, 2): 3}
stored_square = sparse_grid[(3, 2)]  # 3
missing_square = sparse_grid.get((1, 1), 0)  # 0, not stored so the default is used

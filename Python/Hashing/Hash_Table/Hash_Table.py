r"""
HASH TABLE WITH CHAINING
Advanced Algorithms, Lecture 9 "Hashtables", slides 3-23; CLRS 3rd ed., 11.2-11.3 (pp. 256-268).

Notes: [[Hash Table — Code Notes]]
  ~/Documents/Obsidian/Uni/100 - Pre-Master/1A - Logic & Algorithms/
  Advanced Algorithms/Code Notes/Hash Table — Code Notes.md

What is in this file:
    1. division_hash             h(x) = x mod m                [slide 9, 20]
    2. draw_universal_hash       h(x) = ((ax + b) mod p) mod m [slide 14]
    3. ChainedHashTable          insert, search, delete        [slide 14]
    4. the lecture's example     x mod 7: 16 and 9, 4 and 18   [slide 11]
    5. hand cases
    6. slide 20's bad keys       one long list vs spread out
    7. slide 15's claim          counted over every (a, b)
    8. random checks against a Python dict

Not here: open addressing (slides 24-27) and string hashing (slides 28-29).

Run with:
    python3 Hash_Table.py
"""

import random

# The lecture's Example 2 [slide 11]: h(x) = x mod 7 makes two collisions.
SLIDE_KEYS = [4, 16, 9, 26, 18, 34]
SLIDE_SLOT_COUNT = 7


# =====================================================================
# 1. THE DIVISION METHOD [slide 9, slide 20; CLRS 11.3.1]
# =====================================================================
# Returns a hash function that maps a key to its remainder mod slot_count.
#
# slot_count: m, how many lists the table has
#
# Fast: one division. Not random, so a bad set of keys stays bad (section 6).

def division_hash(slot_count):
    def hash_function(key):
        return key % slot_count
    return hash_function


# =====================================================================
# 2. UNIVERSAL HASHING [slide 14; CLRS 11.3.3]
# =====================================================================
# Notes: [[Hash Table — Code Notes#2. Universal hashing]] (variables)

def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def next_prime_above(number):
    candidate = number + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def draw_universal_hash(slot_count, universe_limit, random_generator=random):
    prime = next_prime_above(universe_limit)  # p > U
    multiplier = random_generator.randint(1, prime - 1)  # 0 < a < p
    offset = random_generator.randint(0, prime - 1)  # 0 <= b < p

    def hash_function(key):
        return ((multiplier * key + offset) % prime) % slot_count

    hash_function.description = (
        f"(({multiplier}*x + {offset}) mod {prime}) mod {slot_count}")
    return hash_function


# =====================================================================
# 3. THE TABLE [slide 14; CLRS 11.2]
# =====================================================================
# Notes: [[Hash Table — Code Notes#3. The table]] (variables, the two steps, cost)

class ChainedHashTable:
    def __init__(self, slot_count, hash_function):
        self.buckets = [[] for _ in range(slot_count)]
        self.hash_function = hash_function
        self.item_count = 0

    def slot_of(self, key):
        return self.hash_function(key)

    # insert: put (key, value) in its list, or update the value if present.
    # slot_index: which list the key belongs in
    # chain: that list
    def insert(self, key, value=None):
        slot_index = self.slot_of(key)
        chain = self.buckets[slot_index]
        for position, (stored_key, _) in enumerate(chain):
            if stored_key == key:
                chain[position] = (key, value)  # already here: overwrite
                return
        chain.append((key, value))  # new key: add to the end of its list
        self.item_count += 1

    # search: return the value stored for key, or None if key is absent.
    # Only ONE list is looked at. Keys in the other lists cannot be the key.
    def search(self, key):
        chain = self.buckets[self.slot_of(key)]
        for stored_key, stored_value in chain:
            if stored_key == key:
                return stored_value
        return None

    def contains(self, key):
        chain = self.buckets[self.slot_of(key)]
        return any(stored_key == key for stored_key, _ in chain)

    # delete: remove key from its list. Returns True if it was there.
    # Deleting from a chained table is easy: the key just leaves its list.
    # (Open addressing makes this hard, slide 25. Not here.)
    def delete(self, key):
        chain = self.buckets[self.slot_of(key)]
        for position, (stored_key, _) in enumerate(chain):
            if stored_key == key:
                chain.pop(position)
                self.item_count -= 1
                return True
        return False

    # load_factor: alpha = n / m, the average list length [CLRS p. 258]
    def load_factor(self):
        return self.item_count / len(self.buckets)

    def longest_chain(self):
        return max(len(chain) for chain in self.buckets)

    def show(self, indent="    "):
        for slot_index, chain in enumerate(self.buckets):
            keys_here = [stored_key for stored_key, _ in chain]
            marker = "  <- collision" if len(chain) > 1 else ""
            print(f"{indent}[{slot_index}] {keys_here}{marker}")


# =====================================================================
# TEST HELPER
# =====================================================================

failure_count = 0


def check(description, condition):
    global failure_count
    status = "PASS" if condition else "FAIL"
    if not condition:
        failure_count += 1
    print(f"{status}  {description}")


# =====================================================================
# 4. THE LECTURE'S EXAMPLE [slides 9-11]
# =====================================================================
# Slide 10 (Example 1): A = 4, 16, 10, 26, 21, 34 with h(x) = x mod 7.
#   Every key gets its own cell. No collisions.
# Slide 11 (Example 2): A = 4, 16, 9, 26, 18, 34.
#   16 mod 7 = 2 and 9 mod 7 = 2   -> same cell
#   4 mod 7 = 4 and 18 mod 7 = 4   -> same cell
# The slide draws them as "16,9" and "4,18". Chaining keeps both.

print("=" * 78)
print("HASH TABLE WITH CHAINING   -- Lecture 9, slides 3-23;  CLRS 11.2-11.3")
print("=" * 78)

print("\nslide 10, Example 1: A = 4, 16, 10, 26, 21, 34,  h(x) = x mod 7\n")
example_one_table = ChainedHashTable(SLIDE_SLOT_COUNT, division_hash(SLIDE_SLOT_COUNT))
for key in [4, 16, 10, 26, 21, 34]:
    example_one_table.insert(key)
example_one_table.show()
check("Example 1 has no collisions", example_one_table.longest_chain() == 1)

print(f"\nslide 11, Example 2: A = {', '.join(map(str, SLIDE_KEYS))},  h(x) = x mod 7\n")
for key in SLIDE_KEYS:
    print(f"    {key:>2} mod 7 = {key % 7}")
print()
example_two_table = ChainedHashTable(SLIDE_SLOT_COUNT, division_hash(SLIDE_SLOT_COUNT))
for key in SLIDE_KEYS:
    example_two_table.insert(key, f"value of {key}")
example_two_table.show()
print(f"\n    load factor n/m = {example_two_table.item_count}/{SLIDE_SLOT_COUNT}"
      f" = {example_two_table.load_factor():.2f}")
print()

slot_two_keys = [stored_key for stored_key, _ in example_two_table.buckets[2]]
slot_four_keys = [stored_key for stored_key, _ in example_two_table.buckets[4]]
check("16 and 9 share slot 2", slot_two_keys == [16, 9])
check("4 and 18 share slot 4", slot_four_keys == [4, 18])
check("both colliding keys are still found",
      all(example_two_table.search(key) == f"value of {key}" for key in SLIDE_KEYS))
check("23 (also 2 mod 7) is not found, though its list is not empty",
      example_two_table.search(23) is None)


# =====================================================================
# 5. HAND CASES
# =====================================================================

print("\n" + "=" * 78)
print("HAND CASES")
print("=" * 78 + "\n")

hand_table = ChainedHashTable(SLIDE_SLOT_COUNT, division_hash(SLIDE_SLOT_COUNT))
check("search in an empty table finds nothing", hand_table.search(5) is None)
check("delete in an empty table returns False", hand_table.delete(5) is False)

for key in SLIDE_KEYS:
    hand_table.insert(key, key * 10)

hand_table.insert(16, "new value")
check("insert of an existing key overwrites, count stays 6",
      hand_table.search(16) == "new value" and hand_table.item_count == 6)

check("delete 16 (front of a chain) returns True", hand_table.delete(16) is True)
check("16 is gone, 9 in the same list is still there",
      hand_table.search(16) is None and hand_table.search(9) == 90)
check("delete 18 (back of a chain), 4 stays",
      hand_table.delete(18) and hand_table.search(4) == 40)
check("delete 18 again returns False", hand_table.delete(18) is False)
check("item count is now 4", hand_table.item_count == 4)
print("\n    after deleting 16 and 18:")
hand_table.show(indent="      ")
print()

# CLRS 11.3.3 (p. 267) worked example: p = 17, m = 6, a = 3, b = 4, key 8 -> 5.
clrs_value = ((3 * 8 + 4) % 17) % 6
check(f"CLRS p. 267 example: h_3,4(8) = ((3*8 + 4) mod 17) mod 6 = {clrs_value}",
      clrs_value == 5)

seeded_generator = random.Random(9)
universal_function = draw_universal_hash(SLIDE_SLOT_COUNT, 100, seeded_generator)
print(f"\n    universal table, drawn function: {universal_function.description}\n")
universal_table = ChainedHashTable(SLIDE_SLOT_COUNT, universal_function)
for key in SLIDE_KEYS:
    universal_table.insert(key)
universal_table.show()
print("\n    this draw collides MORE than x mod 7 did. that is allowed: the promise")
print("    is about the average over all draws, not about one draw on one set.\n")
check("the same keys in a universal table are all found",
      all(universal_table.contains(key) for key in SLIDE_KEYS))
check("the drawn function gives the same slot every time (slide 23)",
      all(universal_function(key) == universal_function(key) for key in SLIDE_KEYS))


# =====================================================================
# 6. SLIDE 20's BAD KEYS
# =====================================================================
# "if our set of keys contains the following values 1, m + 1, 2m + 1, 3m + 1,
#  ..., (n - 1)m + 1 everything end up in one list"
#
# With x mod m, every one of those keys has remainder 1. One list of length n:
# search is O(n), no better than a plain list. A random (a, b) breaks the
# pattern, because the attacker did not know a and b in advance.

print("\n" + "=" * 78)
print("SLIDE 20: keys 1, m+1, 2m+1, ...  under x mod m  vs  a random (a, b)")
print("=" * 78 + "\n")

bad_slot_count = 10
bad_key_count = 30
bad_keys = [step * bad_slot_count + 1 for step in range(bad_key_count)]
print(f"    m = {bad_slot_count}, keys = {bad_keys[:5]} ... {bad_keys[-1]}\n")

division_table = ChainedHashTable(bad_slot_count, division_hash(bad_slot_count))
for key in bad_keys:
    division_table.insert(key)
print("    x mod 10:")
division_table.show(indent="      ")

bad_generator = random.Random(20)
bad_universal_function = draw_universal_hash(bad_slot_count, max(bad_keys), bad_generator)
spread_table = ChainedHashTable(bad_slot_count, bad_universal_function)
for key in bad_keys:
    spread_table.insert(key)
print(f"\n    {bad_universal_function.description}:")
spread_table.show(indent="      ")
print(f"\n    load factor in both: {spread_table.load_factor():.1f}"
      f" -- the AVERAGE list is 3 long either way")
print(f"    longest list:  x mod m = {division_table.longest_chain()},"
      f"  random (a, b) = {spread_table.longest_chain()}\n")

check("x mod m puts all 30 keys in one list", division_table.longest_chain() == bad_key_count)
check("random (a, b) spreads them (longest list well under 30)",
      spread_table.longest_chain() <= 10)


# =====================================================================
# 7. SLIDE 15's CLAIM, COUNTED EXACTLY
# =====================================================================
# Notes: [[Hash Table — Code Notes#7. Slide 15's claim, counted exactly]] (variables)

print("\n" + "=" * 78)
print("SLIDE 15: Pr[x and y collide] over every (a, b)")
print("=" * 78 + "\n")

small_prime = 17
small_slot_count = 6
function_count = small_prime * (small_prime - 1)
worst_fraction = 0.0
worst_pair = None

for first_key in range(small_prime):
    for second_key in range(first_key + 1, small_prime):
        collision_count = 0
        for multiplier in range(1, small_prime):
            for offset in range(small_prime):
                first_slot = ((multiplier * first_key + offset) % small_prime) % small_slot_count
                second_slot = ((multiplier * second_key + offset) % small_prime) % small_slot_count
                if first_slot == second_slot:
                    collision_count += 1
        fraction = collision_count / function_count
        if fraction > worst_fraction:
            worst_fraction = fraction
            worst_pair = (first_key, second_key, collision_count)

print(f"    p = {small_prime}, m = {small_slot_count}, {function_count} functions in the family")
print(f"    worst pair: x = {worst_pair[0]}, y = {worst_pair[1]},"
      f" collide under {worst_pair[2]} of {function_count} functions"
      f" = {worst_fraction:.4f}")
print(f"    1/m = {1 / small_slot_count:.4f}\n")
check("no pair of keys collides more often than 1/m", worst_fraction <= 1 / small_slot_count)


# =====================================================================
# 8. RANDOM CHECKS AGAINST A PYTHON DICT
# =====================================================================
# A long random mix of insert / search / delete, done on both this table and a
# real dict. After every step they must agree. Small key range on purpose, so
# collisions, repeats and deletes of missing keys all happen often.

print("\n" + "=" * 78)
print("RANDOM CHECKS AGAINST dict")
print("=" * 78 + "\n")

random_generator = random.Random(52)
operation_count = 20000
key_limit = 200

for table_name in ("division", "universal"):
    random_slot_count = random_generator.randint(1, 30)
    if table_name == "division":
        chosen_function = division_hash(random_slot_count)
    else:
        chosen_function = draw_universal_hash(random_slot_count, key_limit, random_generator)
    random_table = ChainedHashTable(random_slot_count, chosen_function)
    reference_dict = {}
    mismatch_count = 0

    for _ in range(operation_count):
        operation = random_generator.choice(("insert", "search", "delete"))
        key = random_generator.randint(0, key_limit)
        if operation == "insert":
            value = random_generator.randint(0, 999)
            random_table.insert(key, value)
            reference_dict[key] = value
        elif operation == "search":
            if random_table.search(key) != reference_dict.get(key):
                mismatch_count += 1
        else:
            was_there = key in reference_dict
            reference_dict.pop(key, None)
            if random_table.delete(key) != was_there:
                mismatch_count += 1
        if random_table.item_count != len(reference_dict):
            mismatch_count += 1

    stored_pairs = sorted(pair for chain in random_table.buckets for pair in chain)
    check(f"{table_name}: {operation_count} random operations, m = {random_slot_count},"
          f" every step agrees with dict",
          mismatch_count == 0 and stored_pairs == sorted(reference_dict.items()))
    check(f"{table_name}: every key sits in the list its hash says",
          all(random_table.slot_of(stored_key) == slot_index
              for slot_index, chain in enumerate(random_table.buckets)
              for stored_key, _ in chain))

print(f"\n{'ALL PASS' if failure_count == 0 else f'{failure_count} FAILED'}")

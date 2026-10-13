"""

  6C — Volcano species
  1. Don't answer queries in the order they arrive. Sort them by distance d, but keep
     each query's original position so you can print the answers in input order at
     the end.
  2. Treat each species as two events: it appears at lo and disappears just after hi.
     Walk along the distances in increasing order, and the set of species "currently
     alive" is exactly what you need when you reach a query's d.
  3. Sort all the names alphabetically once at the start and give each one its rank
     (0, 1, 2…). After that the structure only stores numbers, and "the k-th name
     alphabetically" becomes "the k-th smallest rank that's alive", which you turn
     back into a name at the end.
balanced BST
"""
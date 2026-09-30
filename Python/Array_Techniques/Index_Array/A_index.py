calls = [("Ana", 3), ("Ben", 1), ("Cleo", 4), ("Dan", 2)]
n = len(calls)

# --- build the index array ---
board = [None] * n              # n empty slots, one per finishing place
for name, place in calls:
    board[place - 1] = name     # place 1 -> slot 0, place 2 -> slot 1, ...
#Instead of asking "where does this go relative to the others?" (a comparison), 
#you compute the address directly from the data.
print("board      :", board)
print("3rd place  :", board[2])

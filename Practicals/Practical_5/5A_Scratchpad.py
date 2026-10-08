"""
1[ 3 ]
2[ 3 ]
3[ 1 ]
4[ 5 ]
5[ 9 ]
6[ 8 ]
7[ 7 ]
8[ 1 ]


1 a[ x ]b[   ]
2 a[   ]b[ x ]
3 a[ x ]b[   ]
4 a[   ]b[ x ]
5 a[ x ]b[   ]
6 a[   ]b[ x ]
7 a[ x ]b[   ]
8 a[   ]b[ x ]

its not just a or b
because it might be that there is a row with a very high value that
might outweight maximizing the amount of taps

for example:
1[ 50]
2[ 3 ]
3[ 1 ]
4[ 50]
5[ 9 ]
6[ 8 ]
7[ 7 ]
8[ 1 ]

in this case it is still better to tap both 50s and not tap 3 or 1
that one would look something like this:
1[ x ]
2[   ]
3[   ]
4[ x ]
5[   ]
6[ x ]
7[   ]
8[ x ]
which would total 50 + 50 + 8 + 1 = 109
which is better than:
1 a[ x ]b[   ]
2 a[   ]b[ x ]
3 a[ x ]b[   ]
4 a[   ]b[ x ]
5 a[ x ]b[   ]
6 a[   ]b[ x ]
7 a[ x ]b[   ]
8 a[   ]b[ x ]
in which column a would total 50 + 1 + 9 + 7 = 67
and b would total 3 + 50 + 8 + 1 = 62

the rule dictates that no two taps can be adjecent
so for each value, i should store a value in case it was tapped and a value in case it was not tapped
the value in case it was tapped would be the value of the cell + the value of the best configuration of 
the previous row that does not have a tap in the same column the value in
the value in case it was not tapped would be the value of the best configuration of the previous row

i should start with the first row, and then for each row, calculate the best configuration for each column 
based on the previous row's best configurations

Formula for:
Tapped value = value of cell + max(previous row's best configurations that do not have a tap in the same column)
Not tapped value = max(previous row's best configurations)
maybe i could called taps x's and untapped cells o's
"""
print("==== CHECKERS APPROACH ====")
Array = [[50], [3], [1], [50], [9], [8], [7], [1]]
print(f"Array= {Array}")
A_x_o = [[0, 0] for _ in range(len(Array))]
for i in range(len(Array)):
    A_x_o[i][0] = Array[i][0]
    for k in range(i + 2, len(Array), 2):
        A_x_o[i][0] += Array[k][0]

for i in range(len(Array)):
    for k in range(i + 1, len(Array), 2):
        A_x_o[i][1] += Array[k][0]

print(f"A_x_o = {A_x_o}")
print("=======================")

"""
1[ 50]
2[ 3 ]
3[ 1 ]
4[ 50]
5[ 9 ]
6[ 8 ]
7[ 7 ]
8[ 1 ]

walk Array from the top row to the bottom, keeping two numbers per row:
    x: the best total so far if this row IS tapped
    o: the best total so far if this row is NOT tapped

row 1: nothing above it, so
       x = the cell's value
       o = 0

every row after that (using the formula above):
       x = cell's value + previous row's o   (tapped: the row above can't be tapped)
       o = max(previous row's x, previous row's o)   (not tapped: the row above can be either)

the answer is max(x, o) of the last row

the "three options" at row 2 are all covered by these two numbers:
    x row 1   -> row 2's o (it takes row 1's x)
    x row 2   -> row 2's x
    x neither -> row 2's o (it takes row 1's o), and max() only keeps it if it's the best

"""
def best_taps(Array):
    x = Array[0]  # row 1 tapped
    o = 0  # row 1 not tapped
    for i in range(1, len(Array)):  # row 1 is already done above
        new_x = Array[i] + o  # uses the old o
        if x > o:  # uses the old x, so x can't be overwritten yet
            o = x  # row above tapped was better
        # else: o stays the same, row above not tapped was better
        x = new_x
    return max(x, o)

Array = [50, 3, 1, 50, 9, 8, 7, 1]
# print(best_taps(Array))  # 109


tapped = Array[0]
untapped = 0
#following rows:
for i in range(1, len(Array)): #starts at the second row
    tapped_current = untapped + Array[i]
    # If this row isn't tapped, the row above can be either
    if tapped > untapped:
        untapped = tapped
    tapped = tapped_current
best_combo = max(tapped, untapped)

print(best_combo)


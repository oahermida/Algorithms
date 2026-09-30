A = [5, 1, 3, 7, 9, 2, 6]
v = 60
def insertion_sort(A):     
    n = len(A)
    for j in range(1, n):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
    return A

A = insertion_sort(A)
print(f"Sorted array: {A}")
# mid = len(A) // 2
low = 0
high = len(A) - 1
while low <= high:
    # low (the bottom of the section) + the half of the difference between high and low
    # equivalent to (low + high)//2
    # Example: low = 4, high = 9, (high - low) = 5
    # low + (high - low) // 2  =  4 + 5 // 2   =  4 + 2  =  6
    # (low + high) // 2        =  (4 + 9) // 2 =  13 // 2 =  6
    # HOWEVER: apparently (low + high)//2 has some edge cases in C where it fucks things up for the code
    mid = low + (high - low) // 2
    if A[mid] == v:
        print(f"Found {v} at index {mid}")
        break
    elif A[mid] < v:
        low = mid + 1
    else:
        high = mid - 1
else:
    print(f"{v} is not present.")

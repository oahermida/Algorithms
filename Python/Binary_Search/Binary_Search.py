A = [5, 1, 3, 7, 9, 2, 6]
v = 6
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
mid = len(A) // 2
low = 0
high = len(A) - 1
while low <= high:
    mid = low + (high - low) // 2 # This is the line that calculates the middle index of the current search range.
    if A[mid] == v:
        print(f"Found {v} at index {mid}")
        break
    elif A[mid] < v:
        low = mid + 1
    else:
        high = mid - 1
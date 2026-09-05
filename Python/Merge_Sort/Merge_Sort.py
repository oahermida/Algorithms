A = [5, 2, 4, 6, 1, 3]

def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge([2, 4, 5], [1, 3, 6]))  # [1, 2, 3, 4, 5, 6] — two sorted halves interleaved into one

def merge_sort(A):
    if len(A) <= 1:
        return A

    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])

    return merge(left, right)

print(merge_sort([]))  # [] — empty list, hits the base case immediately
print(merge_sort([7]))  # [7] — single element, already sorted, base case again
print(merge_sort([1, 2, 3, 4, 5]))  # [1, 2, 3, 4, 5] — already sorted, comes back unchanged
print(merge_sort([5, 4, 3, 2, 1]))  # [1, 2, 3, 4, 5] — reversed input, fully rebuilt in order
print(merge_sort([3, 1, 3, 2, 3]))  # [1, 2, 3, 3, 3] — duplicates kept, none lost or merged
print(merge_sort(A))  # [1, 2, 3, 4, 5, 6] — the sorted copy of A
print(A)  # [5, 2, 4, 6, 1, 3] — A itself, still unsorted: merge_sort returns a new list

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


def merge_sort(A):
    if len(A) <= 1:
        return A

    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])

    return merge(left, right)

# === How it Runs ===
# --- merge_sort ---
# merge sort is called (in this case in the print statements)
# checks if len(A) <= 1 (empty OR one element), IN WHICH CASE THIS ONE CALL RETURNS A IMMEDIATELY (no split, no merge)
# sets the midpoint of A floored
# defines left as the result of calling THIS SAME function (recursion) on A[:mid]. The part up to mid (not including mid)
# defines right as the result of calling THIS SAME function on A[mid:]. From mid (including mid)
# dont get confused, this is single threaded and sequential
# merge(left, right) can only run once both calls above have returned, so merging happens bottom-up: deepest pairs first, whole list last
#
# --- merge ---
# what reaches merge is TWO lists, each already in order within itself. The five merge calls arrive in this order:
#   out of Claude as an example A = [5, 2, 4, 6, 1, 3]:
    #   merge([2],     [4])     -> [2, 4]
    #   merge([5],     [2,4])   -> [2, 4, 5]            left half of A now fully sorted, line 26 returns here
    #   merge([1],     [3])     -> [1, 3]
    #   merge([6],     [1,3])   -> [1, 3, 6]            right half now fully sorted, line 27 returns here
    #   merge([2,4,5], [1,3,6]) -> [1, 2, 3, 4, 5, 6]   the final one, same as the merge() test at the bottom

# inside merge:
# i and j are the cursors: left[i] is the next element not yet taken from left, right[j] the same for right. only one advances per pass, so they move at different rates
# compare left[i] against right[j] and take the smaller (on a tie the <= takes left[i]), then advance only that side's cursor
# when one side runs out the while loop stops, so the rest of the other side gets extended all at once - no comparisons needed, it's already sorted and all of it is bigger
# that merged list becomes the left or right of the call one level up, WHICH WAS FROZEN WAITING FOR IT
# repeat up the stack until the outermost call returns the finished list. A itself is never touched, because the slices at lines 26-27 copied it


print(merge_sort([]))  # [] — empty list, hits the base case immediately
print(merge_sort([7]))  # [7] — single element, already sorted, base case again
print(merge_sort([1, 2, 3, 4, 5]))  # [1, 2, 3, 4, 5] — already sorted, comes back unchanged
print(merge_sort([5, 4, 3, 2, 1]))  # [1, 2, 3, 4, 5] — reversed input, fully rebuilt in order
print(merge_sort([3, 1, 3, 2, 3]))  # [1, 2, 3, 3, 3] — duplicates all kept, not deduplicated; the <= keeps equal elements in their original order (stable)
print(merge_sort(A))  # [1, 2, 3, 4, 5, 6] — the sorted copy of A
print(merge([2, 4, 5], [1, 3, 6]))  # [1, 2, 3, 4, 5, 6] — two sorted halves interleaved into one
print(A)  # [5, 2, 4, 6, 1, 3] — A itself, still unsorted: merge_sort returns a new list

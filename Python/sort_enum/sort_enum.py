array = [3,2,1,5,4]
def sort_enum(enum_A):
    temp_n = len(enum_A)
    final_array = [None] * temp_n

    for i in range(temp_n):
        final_array[enum_A[i]-1] = enum_A[i] 

    return final_array

print(sort_enum(array))
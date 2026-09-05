#include <stdio.h>

int main(void) {
    int A[] = {5, 2, 3, 1, 4, 6};
    int n = sizeof(A) / sizeof(A[0]); // this is necessary because otherwise you get the size in memory of all items combined

    /*
    For loops are a bit weird in C
    the first expression is the initialization, 
    the second is the condition, 
    and the third is executed (every time) after the code block has been executed
    */
    for (int j = 1; j < n; j++) {
        int key = A[j];
        int i = j - 1;

        while (i >= 0 && A[i] > key) {
            A[i + 1] = A[i];
            i--;
        }
        A[i + 1] = key;
    }
    
    // In C, you need a loop to print each element in an array
    printf("Sorted array: {%d", A[0]);
    for (int i = 1; i < n; i++) {
        printf(", %d", A[i]);
    }
    printf("}\n");
    return 0;
}
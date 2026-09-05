#include <stdio.h>

int main(void) {
    // --- INSERTION SORT ---
    int A[] = {5, 2, 3, 1, 4, 6};
    int n = sizeof(A) / sizeof(A[0]); // this is necessary because otherwise you get the size in memory of all items combined

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

    // --- BINARY SEARCH ---
    int v = 6; // value to search for
    int low = 0;
    int high = n - 1;

    while(low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] == v) {
            printf("Found %d at index %d\n", v, mid);
            break;
        } else if (A[mid] < v) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return 0;
}
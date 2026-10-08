// =============================================================================
// Based on my python version (previous submission, Themis/V1/5A/main.py)
// =============================================================================
#include <stdio.h>

// COMPILE: gcc -g -O2 -Wall -pedantic -std=c11 -o a.out P5_5A.c -lm
// RUN:     ./a.out < 5A_Sample.txt

// ===== python version =====
// n = int(input())
// mining_field = []
// for i in range(n):
//     row = input().split()
//     for j in range(len(row)):
//         row[j] = int(row[j])
//     mining_field.append(row)    
// print(f"mining_field = {mining_field}")
//
// #for three columns a row can take the following valid shapes:
// #none        [ ][ ][ ]
// #left        [x][ ][ ]
// #middle      [ ][x][ ]
// #right       [ ][ ][x]
// #left_right  [x][ ][x]
//
// none = 0
// left = mining_field[0][0]
// middle = mining_field[0][1]
// right = mining_field[0][2]
// left_right = mining_field[0][0] + mining_field[0][2]
//
// #compatible rows with the row above:
// #none: none, left, middle, right, left_right
// #left: none, middle, right
// #middle: none, left, right, left_right
// #right: none, left, middle
// #left_right: none, middle
//
// for i in range(1,len(mining_field)):
//     none_current = 0 + max(left, middle, right, left_right)
//     left_current = mining_field[i][0] + max(none, middle, right)
//     middle_current = mining_field[i][1] + max(none, left, right, left_right)
//     right_current = mining_field[i][2] + max(none, left, middle)
//     left_right_current = mining_field[i][0] + mining_field[i][2] + max(none, middle)
//     none = none_current
//     left = left_current
//     middle = middle_current
//     right = right_current
//     left_right = left_right_current
//
// best_combo = max(none, left, middle, right, left_right)
// print(best_combo)
// ==========================
//! fix code to show V2

int main(void) {
    //n can be up to 2mil, so int is fine
    int n;
    //i dont think the five totals will fit in a long long in most test cases
    //so unsigned long long
    unsigned long long none, left, middle, right, left_right;
    unsigned long long none_current, left_current, middle_current, right_current, left_right_current;
    // there is no mining_field in C
    return 0;
}

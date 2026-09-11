
#include <stdio.h> //printf and scanf
// also needed later: <stdlib.h> for qsort, <math.h> for llround


// =============================================================================
// 1. Variables the whole program uses
//    Python: they sat at the top of the file, so two_sum could see them.
//    C: same idea. Declared here, above the functions, every function sees them.
//       Declared inside main, two_sum could not.
// =============================================================================

// n = int(nk[0])
//   C: int


// k_scaled = round(float(nk[1]) * 100)   # x100
//   C: long long


// A1_E = []
// A2_A = []
// A3_M = []
//   C: three long long arrays of 20000 (the largest n). C arrays can't grow like lists.



// =============================================================================
// 2. Compare function for qsort
//    Python: sorted() needed none. C: qsort needs one, and it goes above main.
// =============================================================================



// =============================================================================
// 3. one_decimal
// =============================================================================

// def one_decimal(value_x10):
//     return f"{value_x10 // 10}.{value_x10 % 10}"
//   C: returning text is hard in C. Make it a function that PRINTS the grade instead.



// =============================================================================
// 4. two_sum
// =============================================================================

// def two_sum(target):
//     side_E = []
//     side_M = []
//       C: two long long arrays of 20000


//     for i in range(len(A2_A)):
//         chosen_A = A2_A[i]


//         if len(side_E) == n: #or side_m
//             side_E = []
//             side_M = []
//           C: not needed. Every pass overwrites indices 0 .. n-1.


//         for E in A1_E:
//             side_E.append((E**2)+(chosen_A*E))
//           C: there is no **, and ^ is XOR. E**2 is E * E.


//         for M in A3_M:
//             side_M.append((M**2)+(chosen_A*M))


//         E_low_index = 0
//         M_high_index = n -1
//           C: M_high_index must be a signed int. It has to reach -1 to stop.


//         while E_low_index < len(side_E) and M_high_index >= 0:
//             left_value = side_E[E_low_index]
//             right_value = side_M[M_high_index]
//             paired_total = left_value + right_value


//             if paired_total == target:
//                 # side_E was built from A1_E in order, so the same index gives back the grade
//                 E_text = one_decimal(A1_E[E_low_index])
//                 A_text = one_decimal(chosen_A)
//                 M_text = one_decimal(A3_M[M_high_index])
//                 # k from k_scaled (x100), not the raw text, so an input like "380" still prints "380.0"
//                 k_text = f"{k_scaled // 100}.{(k_scaled // 10) % 10}"
//                 print("POSSIBLE")
//                 print(f"{E_text}^2+{E_text}*{A_text}+{M_text}^2+{M_text}*{A_text}={k_text}")
//                 return
//               C: no E_text / A_text / M_text. Print the formula piece by piece,
//                  calling the print-a-grade function (section 3) for each number.
//                  return leaves the whole function, same as Python. break would only leave the while.


//             if paired_total < target:
//                 E_low_index += 1
//             else:
//                 M_high_index -= 1


//     print("IMPOSSIBLE")




int main(void) {

    // =========================================================================
    // 5. Read the input
    // =========================================================================

    // nk = input().split()
    // n = int(nk[0])
    // k = nk[1]
    // k_scaled = round(float(nk[1]) * 100)   # x100
    //   C: one scanf into n and a double k. Then k_scaled = llround(k * 100).
    //      k as text isn't needed: the output prints k from k_scaled.


    // StrA1_E = input().split()
    // for i in range (n):
    //     A1_E.append(round(float(StrA1_E[i]) * 10)) # x10


    // StrA2_A = input().split()
    // for i in range (n):
    //     A2_A.append(round(float(StrA2_A[i]) * 10))


    // StrA3_M = input().split()
    // for i in range (n):
    //     A3_M.append(round(float(StrA3_M[i]) * 10))


    // =========================================================================
    // 6. Sort
    // =========================================================================

    // A1_E = sorted(A1_E)
    // A3_M = sorted(A3_M)


    // =========================================================================
    // 7. Run the search
    // =========================================================================

    // two_sum(k_scaled)


    return 0;
}

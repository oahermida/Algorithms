
// =============================================================================
// Based on my python version (previous submission)
// =============================================================================
#include <stdio.h>      // scanf, printf
#include <limits.h>     //for LLONG_MAX
// main thing to watch out for is the type of variables and functions i use, and hope the memory doesnt do a backflip when i multiply things
// where each type I use runs out:
    // int = 2^31 - 1
    // long long = 2^63 - 1
    // unsigned long long = 2^64 - 1
    // __int128 the widest type GCC (couldnt find a precise source to trust, so lets just hope)

// Main sources: learn.microsoft.com/en-us/cpp/c-language/cpp-integer-limits and en.wikipedia.org/wiki/C_data_types
// __int128 is a GCC extension

// COMPILE: gcc -g -O2 -Wall -pedantic -std=c11 -o a.out main.c -lm

// k = int(input())
// k <= 2^63. long long stops at 2^63 - 1
// so unsigned long long
unsigned long long k;

// n = int(input())
// n < 10^6, well inside int
int n;

// m = []
// s = []
// C arrays have fixed size (no .append())
// n < 10^6 is strict, so the largest n is 999999
int m[1000000];
int s[1000000];

// def count(t):
//     total_requests = 0
//     for i in range(0, n):
//         total_requests += (t//s[i])*m[i]
//     return total_requests #the total number of requests sent from all sources by time t
// worst single term is t/s * m = 2^63 / 1 * 2^20 = 2^83,
// summed over n < 10^6 computers, it has to be int128 and hope it doesnt break
__int128 count(long long t) {
    __int128 total_requests = 0;
    for (int i = 0; i < n; i++)
        total_requests += (__int128)(t/s[i]) * m[i]; // widen before the multiply
    return total_requests;
}

// def binary_search():
//     low = 1
//     high = 2**63 - 1
//     while low != high:
//         mid = low + (high - low) // 2
//         if count(mid) >= k:
//             high = mid
//         else:
//             low = mid + 1
//     return low
long long binary_search(void) {
    long long low = 1;
    long long high = LLONG_MAX; // = 2^63 - 1. C has no **
    while (low != high) {
        long long mid = low + (high - low) / 2;
        if (count(mid) >= k) // no cast: k is promoted up to __int128
            high = mid;
        else
            low = mid + 1;
    }
    return low;
}


int main(void) {

    // k = int(input())
    scanf("%llu", &k); // %llu reaches 2^64 - 1. %lld stops at 2^63 - 1, and k can be 2^63

    // n = int(input())
    scanf("%d", &n);

    // for i in range(0, n):
    //     misi = input().split()
    //     m.append(int(misi[0]))
    //     s.append(int(misi[1]))
    for (int i = 0; i < n; i++)
        scanf("%d %d", &m[i], &s[i]); // scanf skips the newlines itself

    // print(binary_search())
    printf("%lld\n", binary_search());

    return 0;
}

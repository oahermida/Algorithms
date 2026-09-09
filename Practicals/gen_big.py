"""
Generates the performance test for P1_1A: Big_uniform.txt

n = 10^6 computers, every one m=1 s=1, so count(t) = 10^6 * t.
With k = 10^18 the answer is therefore exactly 10^12 -- known without
needing a solver, which is why every computer is identical here.

The point of this file is TIMING, not correctness:
  - 10^6 input lines, so it exposes a slow parser
  - ~60 binary search probes x 10^6 computers per probe

Run:  python3 gen_big.py
Then: time python3 P1_1A.py < Big_uniform.txt      (expect 1000000000000)
"""
N = 10**6
K = 10**18

with open("Big_uniform.txt", "w") as f:
    f.write(f"{K}\n{N}\n")
    f.write("1 1\n" * N)

print(f"wrote Big_uniform.txt  (k={K}, n={N}, expected answer = {K // N})")

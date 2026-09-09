# Test inputs for P1_1A ("Pizza warfare")

Run one:

    python3 P1_1A.py < T02_burst_gap_k9.txt

Every expected answer below was cross-checked against a brute-force reference.

| file | k | what it checks | expected |
|---|---|---|---|
| `Sample.txt` | 10 | the given sample | `12` |
| `T01_single_smallest.txt` | 1 | smallest legal k, single computer | `1` |
| `T02_burst_gap_k9.txt` | 9 | k lands in a burst gap (tally jumps 8 -> 13) | `12` |
| `T03_exact_jump_k13.txt` | 13 | k lands exactly on a jump value | `12` |
| `T04_just_past_k14.txt` | 14 | k one past a jump -- must move to the next burst | `14` |
| `T05_zero_m_present.txt` | 10 | a computer with m=0 mixed in; must be ignored, not crash | `12` |
| `T06_mostly_zero_m.txt` | 5 | all but one computer send nothing | `6` |
| `T07_max_answer.txt` | 2^63-1 | answer at signed-64-bit max -- catches a too-small `high` | `9223372036854775807` |
| `T08_overflow_probe.txt` | 1 | answer is 1, but early probes make count() ~2^92 | `1` |
| `T09_slow_single.txt` | 1 | slowest legal computer (s = 2^20) | `1048576` |
| `Big_uniform.txt` | 10^18 | performance: n = 10^6 (run `gen_big.py` first) | `1000000000000` |

## Why these particular cases

**T02/T03/T04 -- the atomic burst.** The tally jumps 5 -> 8 -> 13, so no t exists
where count(t) == 10. Any solution testing `== k` fails these. T04 is the one that
catches "returned the jump before the right one".

**T05/T06 -- m = 0.** The constraints say `0 <= mi`, and a lower bound of 0 is a
promise the setter WILL send it.

**T07 -- the ceiling.** Fails instantly if `high` was written `2^63` (XOR, = 60)
instead of `2**63`. The sample cannot catch this; its answer is 12.

**T08 -- intermediate overflow.** 1000 computers x 2^20 requests, probed at
t ~ 2^62, makes count() about 2^92. Python is fine. This is the case the problem
statement's `__int128` warning is about, so it matters on the C port, not here.

**Big_uniform.txt -- the two budgets.** 10^6 lines punishes `input()` in a loop
(use `sys.stdin.buffer.read().split()`), and 60 probes x 10^6 computers is the
O(n log answer) work the whole approach rests on. CPU limit is 2s.

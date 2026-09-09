#!/usr/bin/env bash
# Runs P1_1A.py against every test input and compares the LAST line of output
# to the expected answer. Comparing the last line only, so the debug prints
# still in the file don't break the check -- but Themis compares EVERYTHING,
# so this passing does not mean the hand-in is clean.

declare -A expected=(
  ["Sample.txt"]=12
  ["T01_single_smallest.txt"]=1
  ["T02_burst_gap_k9.txt"]=12
  ["T03_exact_jump_k13.txt"]=12
  ["T04_just_past_k14.txt"]=14
  ["T05_zero_m_present.txt"]=12
  ["T06_mostly_zero_m.txt"]=6
  ["T07_max_answer.txt"]=9223372036854775807
  ["T08_overflow_probe.txt"]=1
  ["T09_slow_single.txt"]=1048576
  ["Big_uniform.txt"]=1000000000000
)

pass=0; fail=0
for f in Sample.txt T0*.txt Big_uniform.txt; do
    [ -f "$f" ] || continue
    want=${expected[$f]}
    got=$(timeout 60 python3 P1_1A.py < "$f" 2>&1 | tail -n 1)
    if [ "$got" = "$want" ]; then
        printf '  PASS  %-28s %s\n' "$f" "$got"; pass=$((pass+1))
    else
        printf '  FAIL  %-28s got %-22s want %s\n' "$f" "$got" "$want"; fail=$((fail+1))
    fi
done
echo
echo "$pass passed, $fail failed"

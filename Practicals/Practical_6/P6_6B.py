"""
 6B — Marble sacks
  1. Don't store the marbles; store only how many there are of each weight. Index the
     counts by the exponent: weight 8 is 2³, so count[3]. That gives about 25 slots
     instead of 10 million numbers.
  2. Packing one sack means going through the exponents from heaviest to lightest and
     taking as many as fit. Get the sample (3 sacks) working this way, one sack at a
     time, before you think about speed.
  3. For speed, notice that consecutive sacks are often packed identically. Ask: "how
     many more sacks could I fill exactly like this one before some count runs out?"
     Then subtract that many in one step.
"""
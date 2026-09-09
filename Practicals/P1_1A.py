"""
PP - Rosa's Pizza palace

SP (competition) has n computers (numbered 1 to n)
Each of SP's computers (i) starts at t = 0
Then it starts sending their burst of m(i) DDos requests every s(i) seconds (Will send requests at every timestamp of t = ns(i) but not at 0)


Input:a line containing k, followed by a line containing n. Then follow n lines each describing one attack computer by the numbers m(i) and s(i)
    Example:
        10      (this is k)
        3       (this is n)
        13 20   (3(n=3) lines m(i) s(i))
        3 7 
        5 6
    Output: 12
    Explanation: the first *five requests* get sent by computer 3 at time t = 6. 
    The next three requests are sent at time t = 7 by computer 2. We have eight requests so far. 
    Then, at time t = 12, computer 3 again sends five requests. Thus, at time t = 12, thirteen messages have been sent in total. 
    Hence, the (k)th (as in ten*th*) request has also been sent at t = 12

Output: The timestamp at witch the (k)th DDoS will be sent

Question: Rosa wants to know at which timestamp the (k)th DDoS request will be sent.

Constraints:
• In each test case: 
    * 1 ≤ k ≤ 2^63 
    * 1 ≤ n < 10^6 the number of computers attacking is higher than 0, but is under 10^6
    * 0 ≤ mi ≤ 2^20 an individual computer may send 0 t/m 2^20 request
    * 1 ≤ s(i) ≤ 2^20 a computer might fire 1 t/m 2^20 times per second
    Takeaway: numbers can get astronomical very quickly

• Caution: in this problem, some values in the intermediate calculation may overflow, 
even if you use a 64-bit wide integer. Hence, please use the datatype __int128 for intermediate calculations.
a) It is given that the output will always fit within a (signed) 64-bit integer. • CPU time limit: 2 seconds per test case. 
• Memory limit: 256 MiB per test case. 
a) It is good to know that __int128 is not part of any C standard; it is a GCC extension. Other compilers may not support it, but we use GCC on Themis

Established variables:
    k: which *request* to look for
    n: how many computers are attacking
    i: stands for one individual computer
    m(i): how many requests computer i sends (they all go in an instant)
    s(i): how often computer i fires (seconds)
    t: time in seconds

What k is:
it can be read as k requests have been sent in total. 

run with:
cd /home/oscar/Documents/Code/Algorithms/Practicals/
python3 P1_1A.py < Sample.txt
"""
# === The input ===
k = int(input())
n = int(input())
m = []
s = []
for i in range(0, n):
    misi = input().split()
    m.append(int(misi[0]))
    s.append(int(misi[1]))

# === The solution ===
"""
given a specific timestamp, how many requests (k) have been sent by then?

if i do something every 10 seconds (s(i)) and every time i do it i do 2 things(m(i)), at the end there are 20 things(k), how many seconds (t) passed? 100
t = (k/m)*s

but need to run it backwards, assuming k, and i cant rearrange the equation
k = (t/s)*m
bingo



"""
t = 0


# === Debugging (DO NOT LEAVE IN THE HAND IN) ===
print(k)
print(n)
print(m)
print(s)
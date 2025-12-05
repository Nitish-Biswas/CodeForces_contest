import sys
import os
from collections import defaultdict, Counter, deque
from math import gcd, lcm, sqrt, ceil, floor
from bisect import bisect_left, bisect_right
from itertools import combinations, permutations, accumulate
import inspect, re, sys

# ================================== FAST I/O ==================================
def inp():
    return sys.stdin.readline().rstrip()

def intp():
    return int(inp())

def linp():
    return list(map(int, inp().split()))

def sinp():
    s = inp()
    return list(s)

def pinp():
    return map(int, inp().split())

# ================================== DEBUG SETUP ==================================
DEBUG_LOCAL = ("--debug" in sys.argv) or os.environ.get('DEBUG_LOCAL', 'False') == 'True' or sys.stdin.isatty()

if DEBUG_LOCAL:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "input.txt")
    error_file = os.path.join(current_dir, "Error.txt")

    # create files first
    open(input_file, "w").close()
    open(error_file, "w").close()

    sys.stderr = open(error_file, "a")
    print("--- DEBUG SESSION STARTED ---\n", file=sys.stderr)

    original_stdin = sys.stdin
    log = open(input_file, "a")

    class InputLogger:
        def readline(self):
            line = original_stdin.readline()
            if line:
                log.write(line)
                log.flush()
            return line

        def read(self, size=-1):
            data = original_stdin.read(size)
            if data:
                log.write(data)
                log.flush()
            return data

        def __iter__(self):
            return self

        def __next__(self):
            line = self.readline()
            if not line:
                raise StopIteration
            return line

        def __getattr__(self, attr):
            return getattr(original_stdin, attr)

    sys.stdin = InputLogger()

    def debug(*args):
        frame = inspect.currentframe().f_back
        code = frame.f_code
        line = open(code.co_filename).readlines()[frame.f_lineno - 1]
        name_part = re.search(r"debug\((.*)\)", line).group(1)
        names = [v.strip() for v in name_part.split(",")]
        for name, val in zip(names, args):
            print(f"{name} = {val}", file=sys.stderr)
else:
    def debug(*a): pass
# ================================== UTILITY FUNCTIONS ==================================
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def sieve(n):
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for i in range(2, int(sqrt(n)) + 1):
        if prime[i]:
            for j in range(i * i, n + 1, i):
                prime[j] = False
    return prime

def mod_pow(base, exp, mod=10**9+7):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def mod_inv(n, mod=10**9+7):
    return mod_pow(n, mod - 2, mod)
















# ================================== SOLUTION ==================================


def solve():
    n,q = pinp()
    s = inp()
    
    segments = []
    
    i = 0
    while i < n:
        if s[i] == '?':
            start = i
            while i < n and s[i] == '?':
                i += 1
            end = i # exclusive
            
            char_before = s[start-1] if start > 0 else None
            char_after = s[end] if end < n else None
            
            segments.append((end - start, char_before, char_after))
        else:
            i += 1
            
    fixed_transitions = 0
    
    fixed_sum = 0
    
    for k in range(n):
        if s[k] != '?':
            if s[k] == 'I': fixed_sum += 1
            elif s[k] == 'V': fixed_sum += 5
            elif s[k] == 'X': fixed_sum += 10
            

        if k + 1 < n and s[k] == 'I' and s[k+1] in ('V', 'X'):
            fixed_transitions += 1

    all_gains = []
    
    for length, left_char, right_char in segments:

        
        seg_scores = []
        
        for k in range(length + 1):
            cnt_I = k
            cnt_NI = length - k
            
            internal = min(cnt_I, cnt_NI)
            
    
    q_idx = [i for i, char in enumerate(s) if char == '?']
    
    i = 1
    
    
    
    m = len(q_idx)
    pairs=0
    while i<m:
        if q_idx[i]==q_idx[i-1]+1:
            pairs+=1
            i+=2
        else:
            i+=1
    
    base_total = 0
    
    for i in range(n):
        if s[i]=="X":
            base_total +=10
            
        if s[i]=="V":
            base_total +=5
            
        if s[i]=="I":
            
            if i+1<n and s[i+1] in "VX":
                base_total -=1
            else:
                base_total +=1
    
    total_I = [0]*(m)
    total_V = [0]*(m)
    total_X = [0]*(m)
    pre_I = [0] * (m + 1)
    pre_V = [0] * (m + 1)
    pre_X = [0] * (m + 1)
    
    for k in range(m):
        idx = q_idx[k]
        
        total_I[k] = 1
        total_V[k] = 5
        total_X[k] = 10
        
        if idx + 1 < n and (s[idx+1] == 'X' or s[idx+1] == 'V'):
            total_I[k] = -1
        if idx-1>=0 and s[idx-1]=="I":
            total_V[k] -=2
            total_X[k] -=2
            
        pre_I[k+1] = pre_I[k] + total_I[k]
        pre_V[k+1] = pre_V[k] + total_V[k]
        pre_X[k+1] = pre_X[k] + total_X[k]
        
        
    for _ in range(q):
        cx,cv,ci = pinp()
        
        num_I = min(m, ci)
        
        num_V = min(m - num_I, cv)
        num_X = m - num_I - num_V
        res = min(pairs, num_I)
        
        res = min(res, num_V+num_X)
        
        curr_I = pre_I[num_I]
        curr_V = pre_V[num_I + num_V] - pre_V[num_I]
        curr_X = pre_X[m] - pre_X[num_I + num_V]
        
        ans = base_total + curr_I + curr_V + curr_X-2*res
        
        # if num_I>0 and num_V>0:
            
        #     if q_idx[num_I]-1 == q_idx[num_I-1]:
        #         ans -=2   
        
        # if num_I>0 and num_V==0 and num_X>0:
        #     if q_idx[num_I]-1 == q_idx[num_I-1]:
        #         ans -=2
                
        print(ans)
        
    
    
    



















# ================================== MAIN ==================================
def main():
    t = int(inp())
    for _ in range(t):
        solve()

if __name__ == '__main__':
    main()
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
    n = intp()
    
    if n%2:
        print(0)
        return
    
    print((n//4)+1)
    
    



















# ================================== MAIN ==================================
def main():
    t = int(inp())
    for _ in range(t):
        solve()

if __name__ == '__main__':
    main()
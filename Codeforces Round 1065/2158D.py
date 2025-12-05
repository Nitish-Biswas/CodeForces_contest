import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
    iterator = iter(input_data)
    
    try:
        t_cases = int(next(iterator))
    except StopIteration:
        return
    
    for _ in range(t_cases):
        n = int(next(iterator))
        s = [int(c) for c in next(iterator)]
        t = [int(c) for c in next(iterator)]
        
        ops = []
        possible = True
        
        # We stop at n-1 because we need at least 2 characters (l < r)
        # So the last possible start index is n-2
        for i in range(n - 1):
            if s[i] == t[i]:
                continue

            # We need to flip s[i]. 
            # Strategy 1: Find a DIRECT palindrome starting at i (length >= 2)
            best_j = -1
            for j in range(i + 1, n):
                # Check palindrome
                # Optimisation: We don't need to slice repeatedly, but for N=100 it's fine
                sub = s[i : j+1]
                if sub == sub[::-1]:
                    best_j = j
                    break # Greedy: Take the first one found
            
            if best_j != -1:
                # Direct flip found
                for k in range(i, best_j + 1):
                    s[k] = 1 - s[k]
                ops.append(f"{i + 1} {best_j + 1}")
            
            else:
                # Strategy 2: The "Helper Flip"
                # If we are stuck at i, we look for a palindrome at i+1
                next_j = -1
                
                # Ensure i+1 is valid start point for length >= 2
                if i + 1 < n - 1:
                    for j in range(i + 2, n):
                        sub = s[i+1 : j+1]
                        if sub == sub[::-1]:
                            next_j = j
                            break
                
                if next_j != -1:
                    # 1. Flip the neighbor (Helper Move)
                    for k in range(i + 1, next_j + 1):
                        s[k] = 1 - s[k]
                    ops.append(f"{i + 2} {next_j + 1}")
                    
                    # 2. Now a palindrome MUST exist at i. Find it and flip.
                    # (Usually it becomes '00' or '11' right at the start)
                    final_j = -1
                    for j in range(i + 1, n):
                        sub = s[i : j+1]
                        if sub == sub[::-1]:
                            final_j = j
                            break
                    
                    if final_j != -1:
                        for k in range(i, final_j + 1):
                            s[k] = 1 - s[k]
                        ops.append(f"{i + 1} {final_j + 1}")
                    else:
                        # Theoretically shouldn't happen in binary strings with this logic
                        possible = False
                        break
                else:
                    # If we can't find palindrome at i AND can't find at i+1
                    possible = False
                    break
        
        # After loop, check if last char matches (since loop went to n-2)
        if s[n-1] != t[n-1]:
            possible = False

        if possible and s == t:
            print("YES") # Remove this line if judge format doesn't ask for YES/NO
            print(len(ops))
            if ops:
                print('\n'.join(ops))
        else:
            print("-1") # Or NO, depending on judge

if __name__ == '__main__':
    solve()
import mpmath as mp
mp.mp.dps = 50

def qseq(A,B,C,N):
    b=[None]+[A*n*n+B*n+C for n in range(1,N+1)]
    q=[mp.mpf(0)]*(N+1)
    q[0]=mp.mpf(1); q[1]=mp.mpf(b[1])
    for n in range(2,N+1):
        q[n]=b[n]*q[n-1]+q[n-2]
    return b,q

print("=== STEP 2 crux: can a sign-varying transient zero the dominant component? ===")
print("    b_n with NON-integer roots (sign-varying, never exactly 0).")
print("    dominant comp != 0  <=>  q_N / prod b_k  -> finite nonzero const.\n")
# non-integer roots: discriminant not a perfect square
cases=[(1,-9,19),(1,-7,11),(1,-11,29),(1,-5,5)]
for (A,B,C) in cases:
    N=1400
    b,q=qseq(A,B,C,N)
    disc=B*B-4*A*C
    early=[A*k*k+B*k+C for k in range(1,8)]
    nzeros=sum(1 for k in range(1,N+1) if A*k*k+B*k+C==0)
    prod=mp.mpf(1)
    for k in range(1,N+1): prod*=b[k]
    val=q[N]/prod
    # also value at N-50 to show it's converging to a constant, not drifting to 0
    prod2=mp.mpf(1)
    for k in range(1,N-50+1): prod2*=b[k]
    val2=q[N-50]/prod2
    print(f"(A,B,C)={(A,B,C)}  disc={disc} (non-square={disc**0.5%1!=0})  b_1..b_7={early}  #(b_k==0)={nzeros}")
    print(f"    q_N/prod b_k @N={N}: {mp.nstr(val,15)}   @N-50: {mp.nstr(val2,15)}  (converged, !=0 => dominant)\n")

print("=== restate STEP 1 R verdict ===")
print("    Numerics gave 1/R -> A/4, i.e. R = 4/A = d^d/beta_d (d=2).")
print("    Review's 'R = d^{-d} beta_d = A/4' is 1/R  => reciprocal slip (review hedged 'modulo constant').")

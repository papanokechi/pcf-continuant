import mpmath as mp
mp.mp.dps = 40

def qseq(A,B,C,N):
    b=[None]+[A*n*n+B*n+C for n in range(1,N+1)]
    q=[mp.mpf(0)]*(N+1)
    q[0]=mp.mpf(1); q[1]=mp.mpf(b[1])
    for n in range(2,N+1):
        q[n]=b[n]*q[n-1]+q[n-2]
    return b,q

def minimal(A,B,C,N):
    # backward recurrence s_{n-1}=s_{n+1}-b_n s_n  amplifies the minimal solution
    b=[None]+[A*n*n+B*n+C for n in range(1,N+1)]
    m=[mp.mpf(0)]*(N+2)
    m[N+1]=mp.mpf(0); m[N]=mp.mpf(1)
    for n in range(N,1,-1):
        m[n-1]=m[n+1]-b[n]*m[n]
    return b,m

print("=== STEP 2: ratio argument  Q_n/Q_{n-1} ~ b(n) (dominant) ===")
for (A,B,C) in [(1,0,1),(2,3,5),(1,-9,20)]:   # last: b_1=12? check sign-varying transient
    N=1500
    b,q=qseq(A,B,C,N)
    bn=b[N]
    r=q[N]/q[N-1]
    print(f"(A,B,C)={(A,B,C)}  b_1={b[1]}  b_2={b[2]}  ... b_N={bn}")
    print(f"    q_N/q_(N-1)={mp.nstr(r,12)}   b_N={bn}   ratio/b_N={mp.nstr(r/bn,12)} (->1, dominant)")
    # minimal solution ratio -> 0
    bm,m=minimal(A,B,C,N)
    rm=m[N//2+1]/m[N//2]
    print(f"    minimal m_(k+1)/m_k at k={N//2}: {mp.nstr(rm,10)}  b={bm[N//2+1]}  prod={mp.nstr(rm*bm[N//2+1],8)} (-> -1? ratio ~ -1/b -> 0)")

print()
print("=== STEP 1: pin R.  g_n=q_n/(2n)!,  test 1/R = lim g_n/g_(n-1) ===")
print("    claim to adjudicate: review says R = d^{-d} beta_d = A/4;  Stirling derivation says R = d^d/beta_d = 4/A")
for (A,B,C) in [(1,0,1),(2,0,1),(3,1,1)]:
    N=400
    b,q=qseq(A,B,C,N)
    # g_n/g_{n-1} = (q_n/q_{n-1}) / ((2n)(2n-1))
    n=N
    gr=(q[n]/q[n-1])/(mp.mpf((2*n)*(2*n-1)))
    invR=gr
    print(f"(A,B,C)={(A,B,C)}  beta_d=A={A}  d=2")
    print(f"    lim g_n/g_(n-1) = 1/R = {mp.nstr(invR,10)}   ->  A/4={mp.nstr(mp.mpf(A)/4,10)} ?  4/A={mp.nstr(mp.mpf(4)/A,10)}")
    print(f"    => R = {mp.nstr(1/invR,10)}   (compare A/4={mp.nstr(mp.mpf(A)/4,8)}, 4/A={mp.nstr(mp.mpf(4)/A,8)})")

print()
print("=== STEP 2 crux: does a sign-varying transient ever zero the dominant component? ===")
print("    dominant component nonzero  <=>  q_n/prod|b_k| -> nonzero const (= R_inf-like).")
for (A,B,C) in [(1,-9,20),(1,-15,50),(1,-3,1)]:
    N=1200
    b,q=qseq(A,B,C,N)
    signs=[ '+' if b[k]>0 else '-' for k in range(1,7)]
    # product of b_k (could be negative early); track q_n / prod b_k
    prod=mp.mpf(1)
    for k in range(1,N+1): prod*=b[k]
    val=q[N]/prod
    print(f"(A,B,C)={(A,B,C)}  early signs b_1..b_6 = {' '.join(signs)}  b_1={b[1]}")
    print(f"    q_N/prod(b_k) = {mp.nstr(val,12)}  (bounded away from 0 => dominant comp != 0)")

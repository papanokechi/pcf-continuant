import mpmath as mp
mp.mp.dps = 40

def Rinf(alpha, beta, N=1600):
    alpha=mp.mpf(alpha); beta=mp.mpf(beta)
    bs=[None]+[ (n-alpha)*(n-beta) for n in range(1,N+1) ]
    qm1=mp.mpf(1); qn=bs[1]; prod=mp.mpf(bs[1])
    for n in range(2,N+1):
        qn1=bs[n]*qn+qm1
        qm1=qn; qn=qn1
        prod*=bs[n]
        if prod==0:
            return mp.inf
    return qn/prod

g=mp.mpf('2.4')
print("="*78)
print("(2) CONTINUITY / POLE audit of R_inf(alpha), beta=alpha+2.4, alpha in [1.2,3.4]")
print("    R_inf = q_n/prod b  -> infinity wherever some b(k)=0, i.e. alpha=integer or beta=integer.")
print("    Predicted poles in range: alpha in {1.6 (beta=4), 2.0 (alpha=2), 2.6 (beta=5), 3.0 (alpha=3)}")
print("="*78)
alphas=[mp.mpf('1.23')+mp.mpf('0.05')*i for i in range(0,44)]  # offset off integers
prev=None; prevA=None
print(f"  {'alpha':>7} {'min dist to integer collision':>30} {'R_inf':>16} flag")
def coll_dist(a):
    b=a+g
    ds=[abs(a-round(a)), abs(b-round(b))]
    return min(ds)
for a in alphas:
    R=Rinf(a,a+g)
    cd=coll_dist(a)
    flag=""
    if abs(R)>30: flag="<-- POLE neighborhood (|R|>30)"
    if prev is not None and mp.sign(prev)!=mp.sign(R):
        # is the sign change near a collision (pole) or interior (zero)?
        kind="POLE-CROSSING" if min(coll_dist(prevA),cd)<0.12 or abs(prev)>30 or abs(R)>30 else "ZERO-CROSSING"
        flag+=f"  [sign change {mp.nstr(prev,4)}->{mp.nstr(R,4)}: {kind}]"
    print(f"  {mp.nstr(a,4):>7} {mp.nstr(cd,6):>30} {mp.nstr(R,6):>16} {flag}")
    prev=R; prevA=a

print()
print("="*78)
print("  WITNESS bracket [1.85,1.98] (alpha*~1.940): nearest collisions are 1.6 and 2.0,")
print("  both OUTSIDE -> R_inf continuous there. Fine scan to confirm a smooth single zero:")
print("="*78)
for i in range(0,14):
    a=mp.mpf('1.85')+mp.mpf('0.01')*i
    print(f"    alpha={mp.nstr(a,5)}:  R_inf={mp.nstr(Rinf(a,a+g),10)}")

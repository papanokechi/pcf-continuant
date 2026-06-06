import mpmath as mp
mp.mp.dps = 45

def Rinf(alpha, beta, N=1600):
    alpha=mp.mpf(alpha); beta=mp.mpf(beta)
    bs=[None]+[ (n-alpha)*(n-beta) for n in range(1,N+1) ]
    qm1=mp.mpf(1); qn=bs[1]; prod=mp.mpf(bs[1])
    for n in range(2,N+1):
        qn1=bs[n]*qn+qm1
        qm1=qn; qn=qn1
        prod*=bs[n]
    return qn/prod

g=mp.mpf('2.4')
lo=mp.mpf('1.85'); hi=mp.mpf('1.98')
flo=Rinf(lo,lo+g); fhi=Rinf(hi,hi+g)
print(f"bracket: f({mp.nstr(lo,4)})={mp.nstr(flo,6)}  f({mp.nstr(hi,4)})={mp.nstr(fhi,6)}")
for _ in range(60):
    mid=(lo+hi)/2
    fm=Rinf(mid,mid+g)
    if mp.sign(fm)==mp.sign(flo):
        lo=mid; flo=fm
    else:
        hi=mid; fhi=fm
astar=(lo+hi)/2; bstar=astar+g
print(f"\nLOCATED EXACT-CANCELLATION (C=0) seed:")
print(f"  alpha*={mp.nstr(astar,30)}  beta*={mp.nstr(bstar,30)}")
print(f"  b(n)=n^2-(alpha+beta)n+alpha*beta  =>  B=-(a+b)={mp.nstr(-(astar+bstar),20)}  C=ab={mp.nstr(astar*bstar,20)}")
print(f"  b(1)={mp.nstr((1-astar)*(1-bstar),12)}  b(2)={mp.nstr((2-astar)*(2-bstar),12)}  b(3)={mp.nstr((3-astar)*(3-bstar),12)}")

print("\nStability / genuineness check: R_inf at this (alpha*,beta*) for increasing N should -> 0 (minimal seed):")
for N in [400,800,1600,3200]:
    print(f"  N={N:5}:  q_N/prod b = {mp.nstr(Rinf(astar,bstar,N),10)}")

# Compare: a generic nearby alpha gives O(1) R_inf (dominant), confirming the zero is special
print("\nContrast at nearby generic alpha (NOT the zero):")
for da in ['-0.05','+0.05']:
    a=astar+mp.mpf(da)
    print(f"  alpha={mp.nstr(a,8)}:  R_inf(N=1600)={mp.nstr(Rinf(a,a+g),10)}   R_inf(N=3200)={mp.nstr(Rinf(a,a+g,3200),10)}")

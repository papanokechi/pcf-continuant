import mpmath as mp
mp.mp.dps = 40

# b(n) = (n-alpha)(n-beta) = n^2 - (alpha+beta) n + alpha*beta, leading coeff 1>0.
# Choose 1 < alpha < beta, non-integer => sign-varying transient (b<0 for integers in (alpha,beta)).
# C := R_inf = lim q_n / prod_{k=1}^n b(k)  is the dominant coefficient. C=0  <=> seed (1,b(1)) is minimal.
# FALSIFICATION: scan (alpha, beta); look for R_inf crossing 0.

def Rinf(alpha, beta, N=1600):
    alpha=mp.mpf(alpha); beta=mp.mpf(beta)
    bs=[None]+[ (n-alpha)*(n-beta) for n in range(1,N+1) ]
    q0=mp.mpf(1); q1=bs[1]
    prod=mp.mpf(bs[1])
    qm1=q0; qn=q1
    for n in range(2,N+1):
        qn1=bs[n]*qn+qm1
        qm1=qn; qn=qn1
        prod*=bs[n]
    return qn/prod

print("Falsification scan: min |R_inf| and sign changes over a grid of (alpha,beta), 1<alpha<beta.")
import itertools
alphas=[1.2+0.13*i for i in range(0,18)]   # 1.2 .. ~3.4
gaps=[0.3,0.6,0.9,1.4,1.9,2.4,3.1,4.2]
results=[]
prev=None
minabs=None; minat=None
signflips=0
for g in gaps:
    row=[]
    prevR=None
    for a in alphas:
        b=a+g
        R=Rinf(a,b)
        row.append(R)
        if minabs is None or abs(R)<minabs:
            minabs=abs(R); minat=(a,b,R)
        if prevR is not None and mp.sign(prevR)!=mp.sign(R):
            signflips+=1
            print(f"   *** SIGN CHANGE of R_inf between alpha={a-0.13:.3f} and {a:.3f} at gap={g}: {mp.nstr(prevR,6)} -> {mp.nstr(R,6)}")
        prevR=R
    # print summary of this row
    print(f"gap={g:4}: R_inf over alpha-grid  min={mp.nstr(min(row),6)}  max={mp.nstr(max(row),6)}")

print()
print(f"GLOBAL min |R_inf| over scan = {mp.nstr(minabs,8)}  at (alpha,beta,R)= ({minat[0]:.3f},{minat[1]:.3f}, {mp.nstr(minat[2],8)})")
print(f"total sign flips of R_inf detected: {signflips}")
print()
print("Interpretation: if R_inf never changes sign and stays bounded away from 0, the seed (1,b(1))")
print("never hits the minimal ray on this grid => no exact cancellation observed.")

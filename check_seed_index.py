"""
Seed-index leak check for the deposited family b(n)=A n^2 + B n + C0, A,B,C0>=1.

Safety chain under scrutiny:  b(n)>=3>0  =>  u_n=1/(b(n-1)b(n))>=0  =>  N0=1  =>  C=R_inf>=1.

The reviewer's worry: u_n references b(n-1); does any index reach b(0)=C0 in a
denominator with the wrong sign/zero? We verify, at dps=50:
  (1) the SCALED recurrence Q_n = Q_{n-1} + u_n Q_{n-2} holds with u_n=1/(b(n-1)b(n))
      and the SMALLEST b-index actually referenced is b(1) (so b(0) never appears);
  (2) Q_0=Q_1=1 are pure seeds, independent of b(0);
  (3) for the boundary family A=B=C0=1 and a few interior members, b(n)>=3, u_n>0,
      Q_n is nondecreasing and >=1.
"""
from mpmath import mp, mpf

mp.dps = 50

def run(A, B, C0, N=60):
    b = [None] * (N + 2)            # b[k] = A k^2 + B k + C0, we will track which indices we touch
    touched = set()
    def bb(k):
        touched.add(k)
        return A * mpf(k) ** 2 + B * mpf(k) + C0
    # raw denominators q
    q = [mpf(1), bb(1)]             # q_0=1, q_1=b(1)
    for n in range(2, N + 1):
        q.append(bb(n) * q[n - 1] + q[n - 2])
    # product P_n = prod_{k=1}^n b(k)
    P = [mpf(1)]                    # P_0 = empty product = 1
    for k in range(1, N + 1):
        P.append(P[k - 1] * bb(k))
    Q = [q[n] / P[n] for n in range(N + 1)]
    # check scaled recurrence and gather u-indices
    max_resid = mpf(0)
    u_min_index = None
    mono_ok = True
    ge1_ok = True
    for n in range(2, N + 1):
        u_n = mpf(1) / (bb(n - 1) * bb(n))
        # smallest b index used by u_n is (n-1); track the global minimum
        idx = n - 1
        u_min_index = idx if u_min_index is None else min(u_min_index, idx)
        resid = abs(Q[n] - (Q[n - 1] + u_n * Q[n - 2]))
        max_resid = max(max_resid, resid)
        if Q[n] < Q[n - 1] - mpf(10) ** (-40):
            mono_ok = False
        if Q[n] < 1 - mpf(10) ** (-40):
            ge1_ok = False
    bmin = min(A * mpf(k) ** 2 + B * mpf(k) + C0 for k in range(1, N + 1))
    return {
        "A": A, "B": B, "C0": C0,
        "b0_touched": (0 in touched),
        "min_b_index_used": u_min_index,        # over the u_n; should be 1
        "min_b_index_in_q": min(touched),       # over the whole computation; should be 1
        "b_min_over_tail": bmin,                # should be >= A+B+C0 (>=3)
        "max_recurrence_residual": max_resid,   # should be ~0 (machine)
        "Q_monotone": mono_ok,
        "Q_ge_1": ge1_ok,
        "C_estimate_Q_N": Q[N],
    }

cases = [(1, 1, 1), (1, 1, 5), (3, 1, 1), (1, 7, 1), (2, 5, 9), (1, 1, 1000)]
print(f"mp.dps = {mp.dps}")
print("=" * 96)
for (A, B, C0) in cases:
    r = run(A, B, C0)
    print(f"b(n)={A}n^2+{B}n+{C0}")
    print(f"   b(0) ever used as a value?         {r['b0_touched']}   "
          f"(min b-index touched anywhere = {r['min_b_index_in_q']})")
    print(f"   min b-index inside any u_n          {r['min_b_index_used']}   (must be 1, NOT 0)")
    print(f"   min b(k), k>=1  (>= A+B+C0)         {mp.nstr(r['b_min_over_tail'], 8)}")
    print(f"   scaled-recurrence max residual      {mp.nstr(r['max_recurrence_residual'], 4)}")
    print(f"   Q nondecreasing / Q>=1              {r['Q_monotone']} / {r['Q_ge_1']}")
    print(f"   C = R_inf estimate (Q_N)            {mp.nstr(r['C_estimate_Q_N'], 12)}  (>=1 expected)")
    print("-" * 96)

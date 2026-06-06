/-
Copyright (c) 2026 papanokechi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: papanokechi
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Finitary core for the quadratic-PCF growth law

Pure-algebra / order core underlying the two-solution (connection-constant) structure of the
quadratic polynomial continued fraction `V(A,B,C) = 1 + K_{n≥1} 1/(A n² + B n + C)`, whose
convergent numerators `p` and denominators `q` satisfy the same second-order recurrence
`s (n+2) = b (n+2) * s (n+1) + s n`.

Main results (all finitary; no analysis, no extra axioms beyond Mathlib defaults):

* `casoratian_step` — the Casoratian (discrete Wronskian) of two solutions of the SAME
  recurrence flips sign at each step.
* `casoratian_eq`   — hence it equals `(-1)^n` times its initial value.
* `pq_casoratian`   — for convergents (`p 0 = 1, p 1 = b 1 + 1, q 0 = 1, q 1 = b 1`),
  `p (n+1) * q n - p n * q (n+1) = (-1)^n`.  This is the exact Casoratian identity from
  `delta_characterization.md` (item 2), the source of the `(∏ b)⁻²` Wronskian decay.
* `rseq_ge_one`, `rseq_mono` — the scaled sequence `r (n+2) = r (n+1) + u (n+2) * r n`
  (with `u ≥ 0`) is `≥ 1` and monotone — the "monotone, bounded-below" half of the
  monotone-bounded convergence of `Rₙ → R∞` (item 3).  The *upper* bound `R∞ ≤ 1/(1-S)`
  and the existence of the limit are analytic and remain OUT OF SCOPE (labelled hypotheses).
-/

namespace PcfContinuant

/-! ## The algebraic Casoratian identity (over any commutative ring) -/

variable {R : Type*} [CommRing R]

/-- A second-order linear recurrence `s (n+2) = c (n+2) * s (n+1) + s n`. -/
def IsSol (c s : ℕ → R) : Prop := ∀ n, s (n + 2) = c (n + 2) * s (n + 1) + s n

/-- The Casoratian (discrete Wronskian) of two sequences. -/
def casoratian (y z : ℕ → R) (n : ℕ) : R := y (n + 1) * z n - y n * z (n + 1)

/-- The Casoratian of two solutions of the same recurrence flips sign at each step. -/
theorem casoratian_step {c y z : ℕ → R} (hy : IsSol c y) (hz : IsSol c z) (n : ℕ) :
    casoratian y z (n + 1) = -casoratian y z n := by
  have hyn : y (n + 1 + 1) = c (n + 1 + 1) * y (n + 1) + y n := hy n
  have hzn : z (n + 1 + 1) = c (n + 1 + 1) * z (n + 1) + z n := hz n
  simp only [casoratian, hyn, hzn]
  ring

/-- Hence the Casoratian equals `(-1)^n` times its value at `0`. -/
theorem casoratian_eq {c y z : ℕ → R} (hy : IsSol c y) (hz : IsSol c z) (n : ℕ) :
    casoratian y z n = (-1) ^ n * casoratian y z 0 := by
  induction n with
  | zero => simp
  | succ k ih =>
      rw [casoratian_step hy hz k, ih, pow_succ]
      ring

/-- The exact Casoratian identity for PCF convergents: with `p 0 = 1, p 1 = b 1 + 1`,
`q 0 = 1, q 1 = b 1`, both solving `s (n+2) = b (n+2) s (n+1) + s n`,
`p (n+1) * q n - p n * q (n+1) = (-1)^n`. -/
theorem pq_casoratian {b p q : ℕ → R}
    (hp : IsSol b p) (hq : IsSol b q)
    (hp0 : p 0 = 1) (hp1 : p 1 = b 1 + 1) (hq0 : q 0 = 1) (hq1 : q 1 = b 1) (n : ℕ) :
    p (n + 1) * q n - p n * q (n + 1) = (-1) ^ n := by
  have h := casoratian_eq hp hq n
  have h0 : casoratian p q 0 = 1 := by
    simp only [casoratian, hp0, hp1, hq0, hq1]; ring
  rw [h0, mul_one] at h
  simpa [casoratian] using h

/-! ## The convergence core: the scaled sequence is `≥ 1` and monotone

Specialized to `ℝ` (the application domain) to use its order instances directly. -/

section Order

/-- The scaled denominator-type sequence `r (n+2) = r (n+1) + u (n+2) * r n`,
`r 0 = r 1 = 1`. With `u = 1/(b_{n-1} b_n) ≥ 0` this is `Rₙ` of the note. -/
def rseq (u : ℕ → ℝ) : ℕ → ℝ
  | 0 => 1
  | 1 => 1
  | (n + 2) => rseq u (n + 1) + u (n + 2) * rseq u n

/-- `rseq` is bounded below by `1` (carrying two consecutive values through the induction). -/
theorem rseq_ge_one (u : ℕ → ℝ) (hu : ∀ n, 0 ≤ u n) :
    ∀ n, 1 ≤ rseq u n ∧ 1 ≤ rseq u (n + 1) := by
  intro n
  induction n with
  | zero => exact ⟨by simp [rseq], by simp [rseq]⟩
  | succ k ih =>
      obtain ⟨hk, hk1⟩ := ih
      refine ⟨hk1, ?_⟩
      change 1 ≤ rseq u (k + 2)
      have hpos : 0 ≤ u (k + 2) * rseq u k :=
        mul_nonneg (hu _) (le_trans zero_le_one hk)
      simp only [rseq]
      linarith

/-- `rseq` is monotone (nondecreasing) when all `u n ≥ 0`. -/
theorem rseq_mono (u : ℕ → ℝ) (hu : ∀ n, 0 ≤ u n) (n : ℕ) :
    rseq u n ≤ rseq u (n + 1) := by
  match n with
  | 0 => change rseq u 0 ≤ rseq u 1; simp [rseq]
  | (k + 1) =>
      change rseq u (k + 1) ≤ rseq u (k + 2)
      have hpos : 0 ≤ u (k + 2) * rseq u k :=
        mul_nonneg (hu _) (le_trans zero_le_one (rseq_ge_one u hu k).1)
      simp only [rseq]
      linarith

end Order

end PcfContinuant

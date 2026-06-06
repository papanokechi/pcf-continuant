# pcf-continuant

When does the dominant coefficient of a polynomial continued fraction vanish?
A monotone positivity criterion (machine-checked core), an unconditional bound for
a positive family, and an explicit vanishing witness.

## Contents

- **Paper:** `Cnonzero_classification.pdf` (source `Cnonzero_classification.tex`).
- **Numerical witnesses** (`mpmath`, 50-digit precision): `review_check_Cnonzero.py`,
  `review_check_transient.py`, `falsify_Czero.py`, `locate_Czero.py`,
  `verify_witness_precision.py`, `check_bracket_continuity.py`, `check_seed_index.py`.
- **Lean core:** `lean/pcf_continuant/` — `Check.lean` prints the axiom cones for
  `casoratian_step`, `casoratian_eq`, `pq_casoratian`, `rseq_ge_one`, `rseq_mono`,
  each a subset of `{propext, Classical.choice, Quot.sound}` with no `sorryAx`.

## Licensing (dual)

- **Paper, text, and prose** — the manuscript (`.tex`/`.pdf`) and this README — are
  licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**; see
  the top-level `LICENSE`.
- **Code** — the Lean project under `lean/pcf_continuant/` and the Python witness
  scripts — is licensed under the **Apache License 2.0**; see
  `lean/pcf_continuant/LICENSE`.

## Companion deposit

This work's all-positive corollary (`C >= 1`) is exactly the strict positivity
`delta = log R_inf > 0` of the quadratic growth-law deposit (Zenodo concept DOI
`10.5281/zenodo.20564681`); the Zenodo metadata records this as `isSupplementTo`.

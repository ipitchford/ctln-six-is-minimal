# Six Is Minimal
## Exact certification and infinite families of stable nonclique CTLNs

**Evidence Press research candidate — v1.1 — 1 October 2026**

The main result is an exact minimum: in a nondegenerate legal combinatorial threshold-linear network (CTLN), a stable nonclique fixed-point support needs **at least six neurons**, and six suffice.

This bundle contains a computer-assisted candidate proof, a manuscript, source code, finite certificates, all-size polynomial certificates, verification logs, and a bounded source/priority audit. It has not undergone independent external peer review or proof-assistant verification. Scholarly creator: Anonymous. Publication and archiving do not establish correctness or priority.

## Main results

1. **All supports through size five.** Across the entire legal parameter region, no nonzero zero-diagonal zero-one nonedge matrix of order at most five can satisfy both positivity and linear stability. The checker covers **9,846 isomorphism classes / 1,052,741 labelled graphs**. Thus stable supports of these sizes are exactly target-free cliques, in the usual nondegenerate dynamical setting.
2. **A rational six-neuron witness.** Geneson's existing six-neuron graph works at `epsilon = 1/12`, `delta = 11/120`. Exact fixed-point coordinates, characteristic polynomial, Hurwitz determinants, and global nondegeneracy checks are supplied. The graph and original counterexample are attributed to Geneson, not claimed as new here.
3. **An infinite family.** For every integer `r >= 0`, an explicitly defined graph on `5*r + 6` vertices has a globally nondegenerate stable nonclique full-support equilibrium at
   `D = 30*r + 31`, `epsilon = 1/(2*D + 1)`, `delta = (D+2)/(D*(2*D+1))`.
   A five-class weighted quotient reduces the proof to positive-coefficient integer polynomials. An identity modulo two proves nondegeneracy for all subsets at every size.
4. **Complete legal phase region of the seed.** Put `u = delta/epsilon - 1` and `t = (1-epsilon)/epsilon`. Full-support stability holds exactly when `0 < u < u_star` and `t > max(1/u, T(u))`, where `u_star` is a specified sextic root and `T(u)` the unique positive root of a specified quartic. Exact root isolators and the proof of uniqueness are included.
5. **Weighted embedding rule.** An outside neuron remains silent exactly when the sum of the active motif's missing-input weights exceeds one. The seed's complete ten-set minimal antichain is certified.

The manuscript distinguishes full-support stability from global nondegeneracy, positivity from stability, and active-support enlargement from adding inactive neurons. It does **not** claim a topology classification of all CTLNs, counterexamples at every integer size, global convergence, or biological validation.

## Read first

- `paper/six_is_minimal_ctln_v1_1.pdf` — revised manuscript.
- `AI_INDEX.md` — agent-readable navigation, exact claims and safe-reuse boundaries.
- `REVISION_RESPONSE.md` — disposition of the supplied review.
- `paper/main.tex` — complete editable LaTeX source, including proofs and references.
- `CLAIMS.md` — claim-by-claim evidence and scope.
- `research/source_audit.md` — attribution, primary sources, bounded novelty search.
- `research/referee_checklist.md` — adversarial review targets, with no invented referee report.
- `verification/verification_summary.json` — executed verification status.

## Reproduce every mathematical check

Requirements: **Python 3.9 or later, standard library only**. No package installation, network access, graph database, commercial solver, or floating-point arithmetic is needed.

From the release directory:

```sh
python3 code/verify_all.py --regenerate --read-only
```

This regenerates graph certificate instructions by Newton identities, checks them by direct signed-permutation determinant expansions, explicitly verifies the full labelled-graph cover, rebuilds the family certificate, validates the seed phase and witness, and runs implementation/mutation regressions. It prints a PASS line for each script. Every executed mathematical check passed in the supplied Python 3.13.5 run.

Without regeneration:

```sh
python3 code/verify_all.py --read-only
```

Do not run Python with `-O` or `PYTHONOPTIMIZE`: assertions are part of the checker. The programs reject disabled assertions. With `--read-only`, the suite runs in a temporary copy, requires byte-identical regenerated mathematical certificates, and leaves the release unchanged. Without that flag it writes certificates and logs in the release directory. Mathematical certificate outputs are deterministic; elapsed-time and interpreter-version fields in logs are operational metadata and may change. See `REPLAY_RECEIPT.md` for the publication replay boundary.

The only finite graph certificate consumed as instructions is `certificates/small_order_obstructions.json`. Polynomial coefficients are reconstructed, not trusted from that file. The family and phase scripts recompute their polynomial certificates from the displayed matrices and verify sign conditions; their JSON files are inspectable outputs, not an external oracle.

## Checker inventory

| File | Purpose |
|---|---|
| `code/exact_polys.py` | Integer-polynomial arithmetic, determinant formulae, substitutions, Hurwitz determinants, graph masks and orbits. |
| `code/generate_small_order.py` | Newton-identity generation of the finite obstruction instructions. |
| `code/verify_small_order.py` | Direct Leibniz/Cramer reconstruction and complete orbit coverage. |
| `code/verify_family.py` | Symbolic all-r proof, limiting-quartic mechanism, explicit parameters and quotient checks. |
| `code/verify_phase_and_witness.py` | Complete seed phase argument, rational root isolators, exact witness and external-neuron antichain. |
| `code/audit_regressions.py` | Three-method arithmetic cross-checks and rejection of nine corrupted certificates. |
| `code/verify_all.py` | Reproducible orchestration; any failure returns a nonzero exit status. |

## Certificate conventions

Matrices encode **missing** directed edges, not present ones: `N[i][j] = 1` means source `j` does not point to target `i`. Masks use row-major off-diagonal bits, least-significant first. Polynomial arrays in family/phase JSON files are in **ascending powers**; characteristic-polynomial arrays list descending powers of the characteristic variable, with each entry itself an ascending coefficient vector in `r`.

Legal parameter coordinates are `beta = 2+u`, `t = (1+v)/u`, `u>0`, `v>0`. The exclusion is over this entire open quadrant, including arbitrarily large or small legal values. A finite floating-point parameter scan is not used as a proof.

A matrix `K` is called positive stable when its eigenvalues have positive real parts. The polynomial `det(z I + K)` must therefore be Hurwitz stable, with roots in the **left** half-plane. The local active Jacobian is `-epsilon*K`.

## Build the paper

A standard LaTeX installation with the packages named in `paper/main.tex` is sufficient:

```sh
cd paper
pdflatex -interaction=nonstopmode -halt-on-error -jobname=six_is_minimal_ctln_v1_1 main.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=six_is_minimal_ctln_v1_1 main.tex
```

PDF production is not required for the mathematical checker. No fonts are separately distributed.

## Integrity and trust boundary

`MANIFEST.sha256` records SHA-256 checksums for every distributed file except the manifest itself. Check from the release root with:

```sh
sha256sum -c MANIFEST.sha256
```

On macOS, use `shasum -a 256 -c MANIFEST.sha256`.

The proof depends on the mathematical reductions, the Python interpreter, and this small exact implementation. The generator and verifier use different determinant constructions but share low-level utilities. The additional Bareiss and signed-product cross-checks reduce implementation risk; they do not amount to an independent human review, a proof-assistant proof, or an exhaustive guarantee of novelty.

## Provenance

Original prose, diagrams and data are dedicated under CC0-1.0; original software is MIT licensed. See `LICENSES.md`. Third-party literature and reviewer materials retain their own terms and are not redistributed here.

This is an AI-assisted research candidate prepared in response to the supplied problem commission. The six-neuron graph and prior counterexample are from J. Geneson (2026), arXiv:2607.21396v1; the previous at-most-four classification is from Curto, Geneson, and Morrison (2024), arXiv:1909.02947v3 / *Advances in Applied Mathematics* 154, 102652. Full references and explicit new-versus-prior attribution are in the manuscript and source audit. No third-party full-text papers are redistributed.

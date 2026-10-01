# Claim and evidence ledger

Release: v1.0, 1 October 2026. “Proved” below denotes the candidate proof and executed exact certificate, not completed peer review.

| ID | Claim | Exact evidence | Scope / status |
|---|---|---|---|
| C1 | No permitted positive-stable nonclique active matrix of order at most five exists at legal parameters. | Theorem 3.1; `small_order_obstructions.json`; `verify_small_order.py`; exact complete labelled orbit cover. | Computer-assisted proof. Covers the full legal continuum, not a parameter grid. No nondegeneracy needed for this algebraic statement. |
| C2 | Minimum stable nonclique support size is six. | C1 plus rational seed witness and all 255 global nondegeneracy determinant checks. | For local exponential stability in **nondegenerate** legal CTLNs, as in the source conjecture. |
| C3 | The seed graph is stable at epsilon=1/12, delta=11/120. | Integer matrix `10I+21N+110J`, exact equilibrium, quintic, four positive Hurwitz determinants, nonzero determinant enumerations. | Existing graph due to Geneson; new rational certificate in this candidate, not a new graph. |
| C4 | Stable nonclique full supports exist for every size 5r+6, integer r>=0, at explicit legal rational parameters. | Theorem 4.3; five-class quotient; full symbolic permission and Hurwitz polynomials; parity identity. | All-r theorem, not an extrapolation from the five regression sizes. Does not claim every integer size. |
| C5 | Global nondegeneracy of the family holds for all subsets and all sizes. | `D K = D I +(2D+2)N+2D^2 J = I (mod 2)`, with D odd; column-replacement argument. | Analytic all-size proof. The modular device is not claimed as a wholly new general method. |
| C6 | The seed's complete legal full-support stability region is 0<u<u_star and t>max(1/u,T(u)). | Theorem 5.1; coefficient bounds; unique roots of Hurwitz determinants; ordering t2<t3<T; exact rational isolators. | Necessary and sufficient for this **one graph**, all legal parameters. Does not assert that all other subsets are nondegenerate at every such point. |
| C7 | Every legal seed parameter with 1<delta/epsilon<=11/10 is stable. | Corollary 5.2; positive lower bound 2256/25 for the legal-boundary polynomial. | Whole cone, not just one parameter ray. |
| C8 | Outside-neuron activity is governed by the weighted missing-source inequality. | Proposition 6.1; exact substitution of the equilibrium into the outside input. | Direct reformulation of the standard off-neuron test. Not claimed as a previously unknown general criterion. |
| C9 | The rational seed has exactly ten inclusion-minimal missing-source sets that silence an outside neuron. | Exact 64-subset check of weights with common denominator 1613071. | Specific to beta=21/10; no equality cases at that beta. |
| C10 | All included verification scripts passed; nine intentionally invalid certificates were rejected. | `verification/verification_summary.json`, `regression_result.json`, script logs. | An executed software fact, not external peer review or a formal proof-assistant certificate. |

## New versus inherited

**Inherited and attributed:** the CTLN formulation and support criterion; target-free-clique sufficiency; classification through size four; Geneson's seed topology and its counterexample status; rank-one permission reduction; earlier modular nondegeneracy device and large-t spectral principle.

**Candidate new contributions:** all-parameter five-neuron exclusion and sharp six-neuron minimum; the explicit twin-cluster family and all-r rational parameter theorem; the complete seed stability region and whole-cone corollary; a compact rational witness and a computed external antichain.

**Standard tools, not novelty claims:** determinant multilinearity, Cramer's rule, rank-one identities, Routh–Hurwitz, Descartes' rule of signs, parity, and invariant-subspace factorization. The quintic square identity is used as a reusable elementary certificate; no unsupported claim that the algebraic identity itself is unprecedented is made.

## Explicit exclusions from the claim set

There is no claimed general graph-level classification of all CTLNs; no solution for every size-seven-and-up graph; no biological experimental validation; no assertion of global dynamical convergence or nonlinear Hopf bifurcation; no proof-assistant formalization; no external independent referee report; no guaranteed priority; no self-assigned REF rating; and no publication, authorship, or endorsement claim on behalf of the commissioning user or Evidence Press.

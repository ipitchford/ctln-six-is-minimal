# Agent index — Six Is Minimal

## Start here

- Exact claims and hypotheses: [CLAIMS.md](CLAIMS.md) and [manuscript](paper/main.tex).
- Assurance and nonclaims: [ASSURANCE.md](ASSURANCE.md).
- Antecedents and search boundary: [source audit](research/source_audit.md) and [SOURCES.md](SOURCES.md).
- [Revisions](REVISION_RESPONSE.md), [provenance](PROVENANCE.md) and [licences](LICENSES.md).

## Statement and scope

In nondegenerate legal CTLNs with uniform drive theta>0, delta>0 and 0<epsilon<delta/(1+delta), the smallest stable nonclique fixed-point support has cardinality six. Every stable support of size at most five is a target-free bidirected clique. Stable means local exponential stability; positivity alone is insufficient.

The family has full active support n=5r+6 for each integer r>=0, D=30r+31, epsilon=1/(2D+1), delta=(D+2)/(D(2D+1)). It does not prove every integer size or a common parameter pair. Its physical transverse eigenvalues tend to zero.

The seed phase theorem uses u=delta/epsilon-1 and t=(1-epsilon)/epsilon: 0<u<u_star and t>max(1/u,T(u)). See paper/main.tex and certificates/seed_phase_and_witness.json for the defining sextic, quartic and exact isolators.

## Replay

Python 3.9+ standard library, assertions enabled:

    python3 code/verify_all.py --regenerate --read-only

The release is copied to a temporary directory; outputs are regenerated and certificate bytes compared. Failure is nonzero. No network or proprietary solver is required. Without --read-only, outputs in the working copy are overwritten. Do not use -O; rejection is intentional, not a proof failure.

## Evidence map

- [small-order certificate](certificates/small_order_obstructions.json): finite instructions; [checker](code/verify_small_order.py) reconstructs coefficients and complete labelled orbit coverage.
- [family certificate](certificates/infinite_family.json): inspectable all-r polynomial outputs; [checker](code/verify_family.py) reconstructs them.
- [seed certificate](certificates/seed_phase_and_witness.json): rational witness, exact phase polynomials, determinant lists and ten-set external-neuron antichain; [checker](code/verify_phase_and_witness.py) reconstructs them.
- [regressions](code/audit_regressions.py): nine invalid-certificate controls and arithmetic cross-checks.
- [manifest](MANIFEST.sha256): payload integrity, not mathematical truth.

## Safe reuse

N[i][j]=1 means the edge j→i is missing. K is positive stable, det(zI+K) has left-half-plane roots, and the physical Jacobian is -epsilon K. Quotient matrices are weighted and are not ordinary smaller CTLNs. Preserve Geneson and CGM attribution. Candidate, formal-proof, reproduction, human-review and novelty statuses are separate; do not promote one based on DOI or CI success.

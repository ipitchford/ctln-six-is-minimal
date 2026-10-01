# Adversarial review checklist

This is a checklist for a future independent referee, **not** a report from one. The performed checks are identified below.

## Load-bearing mathematical steps

**1. Legal parameter region.** Confirm that delta>0 and 0<epsilon<delta/(1+delta) are equivalent to beta>2 and t(beta-2)>1, and that u>0,v>0 covers the entire region. Check that no sign certificate silently truncates an unbounded range.

**2. Permission is not optional.** Check the rank-one reduction, including the case in which I+beta N might initially be singular. Verify why stability plus permission forces positive determinant and every positive Cramer numerator. A stable matrix without a positive fixed point does not refute the theorem.

**3. Exact graph coverage.** Check bit orientation, permutation action, canonical representative checks, and completeness of the labelled cover. The proof does not assume a graph-database count. Counts were verified by the executed orbit-marking checker.

**4. Sign-certificate contracts.** Check that multiplying by u^k never changes sign; identically zero polynomials are legitimate obstructions to strict positivity; removing z+1 factors preserves the needed implication; and the directed-cycle quadratic really has a forbidden coefficient. The supplied independent determinant constructions and direct checker cover these steps.

**5. The three remaining quintics.** Derive the square identity, verify a1>0, inspect the printed polynomial vectors, and check that the two regions 0<u<=2 and u>=2 cover the whole domain. The generator's discovery is not being treated as proof: the checker reconstructs the polynomials.

**6. Seed witness.** Multiply the integer matrix by the fixed-point numerator, reproduce the characteristic factorization, verify the signs of the Hurwitz determinants, and inspect all 255 principal/Cramer checks. Remember that det(zI+B) roots are negatives of B's eigenvalues.

**7. All-r family.** Check the missing-source specification, twin classes, weighted quotient and transverse eigenvalues. Confirm that the quotient is not an ordinary five-neuron CTLN. Verify both the boundary-quartic mechanism and the explicit parameter certificate; the all-r theorem is not inferred from the five finite regression sizes.

**8. Global nondegeneracy.** Check the all-subsets identity modulo two, including column replacements by ones. Positive full-support determinant alone would not suffice. The parity method applies to arbitrary graphs at the displayed odd-D grid, but it does not prove their stability.

**9. Exact phase theorem.** Audit permission on 0<u<2/11; exclusion beyond that interval; convexity and root isolation of F; coefficient bounds for B0,...,B3; unique positive Hurwitz roots; and the strict ordering t2<t3<T. A large-t argument alone would not establish the necessary-and-sufficient finite-t result.

**10. External embedding.** Derive the weighted inequality from the actual off-neuron input. Confirm strictness and the ten-set antichain. This enlarges ambient network size, not active support size; the infinite family handles the latter separately.

## Performed implementation checks

- Exact full graph enumeration and certificate verification: PASS.
- Exact all-r polynomial inequalities and parity identities: PASS.
- Exact seed phase, rational witness, nondegeneracy, and external antichain: PASS.
- Newton / signed-product / Bareiss cross-checks on 149 graphs: PASS.
- Nine deliberately corrupted certificates: all rejected.
- One hundred exact integer instances of the generic quintic identity: PASS (supplementary only; the manuscript gives its algebraic derivation).
- No assertions-disabled execution permitted.

## Residual assurance limits

The checker is not formally verified and shares some primitives between generation and verification. The same research session produced the mathematics, code, and manuscript. No external referee or second independent agent has been represented as having reviewed it. A future independent implementation and domain review would strengthen assurance and check priority; the release does not invent either.

# Primary-source and priority audit

**Boundary:** public sources checked on 1 October 2026. This audit identifies direct antecedents and searches the specific gap; it is not an exhaustive bibliometric review or proof of novelty.

## Direct foundations

**Geneson, J. (2026).** *A six-neuron counterexample to the target-free clique conjecture* (arXiv:2607.21396v1, posted 23 July 2026).

- Version read: https://arxiv.org/html/2607.21396v1
- Metadata: https://arxiv.org/abs/2607.21396
- DOI: https://doi.org/10.48550/arXiv.2607.21396
- Source claims relevant here: a six-neuron nondegenerate legal counterexample along delta=29 epsilon/25 for sufficiently small epsilon; a complementary all-graph parameter bound; separate permission, stability, and external-input conditions.
- Precisely inherited: the seed nonedge matrix (equation 19 / Theorem 3.2), the permission reduction (Lemma 2.1), the rank-one large-t principle (Lemma 3.1), and the modular approach to global nondegeneracy.
- Candidate extension: minimality by a five-neuron exclusion; explicit stable twin-family supports of size 5r+6; a complete parameter region for the seed; a simpler rational seed certificate. The source's six-neuron topology is **not** claimed as new.
- The public author page still placed this paper under “Under review” when checked: https://sites.google.com/view/geneson/papers . That label does not establish acceptance or any status of this candidate.

**Curto, C., Geneson, J., & Morrison, K. (2024).** Stable fixed points of combinatorial threshold-linear networks. *Advances in Applied Mathematics, 154*, 102652.

- DOI: https://doi.org/10.1016/j.aam.2023.102652
- Open version read: https://arxiv.org/html/1909.02947v3
- Metadata: https://arxiv.org/abs/1909.02947
- Relevant result: Theorem 1.6 classifies supports of size at most four as target-free cliques. Theorem 1.8 rules out directed cliques or a nonclique support containing a clique of size one less than the support.
- The candidate independently checks the smaller orders as regressions, but claims the five-neuron step rather than rediscovery of the earlier cases.

**Curto, C., Geneson, J., & Morrison, K. (2019).** Fixed points of competitive threshold-linear networks. *Neural Computation, 31*(1), 94–155.

- DOI: https://doi.org/10.1162/neco_a_01151
- Open preprint metadata: https://arxiv.org/abs/1804.00794
- Role: foundational support equations and graph-based fixed-point analysis. Used as background attribution, not as evidence that this candidate's new theorem is already established.

**Gantmacher, F. R. (1959).** *The theory of matrices* (Vol. II). Chelsea.

- Role: classical Routh–Hurwitz criterion. Bibliographic metadata was checked against Geneson's reference list; this session did not independently read the complete book.
- The candidate defines the exact Hurwitz-determinant convention and computes every determinant it needs. It does not rely on a numerical stability solver.

## Bounded novelty searches

Queries included combinations of:

- `"target-free clique" "five"`
- `"stable nonclique" "five" CTLN`
- `"2607.21396"`
- `"A six-neuron counterexample" Geneson`
- `"threshold-linear" "5r" "clique"`

The direct preprints, their metadata, and the author's papers page were checked. Searches found the six-neuron source and the older at-most-four theorem, but did not reveal a later five-neuron resolution or the family/phase theorem proved in this candidate. The unusual 5r query also returned irrelevant results; those are not evidence either way and are not used scientifically.

**Interpretation:** absence from these results does not prove priority. Before submission, a human referee or domain expert should check related CTLN papers, equitable/twin reductions, and any later version or unpublished overlap. The arithmetic truth claims do not depend on the novelty search succeeding.

## Audit of the problem commission

The supplied commission requested: (i) the minimum size of a stable nonclique support, (ii) resolution of size five throughout the legal region, and (iii) a substantial structural or parameter-dependent extension. It explicitly warned that stability without positive active coordinates is insufficient.

The release answers (i) with six, (ii) by full exact exclusion, and (iii) with both an all-size constructive family and the exact legal phase region of the seed. Positivity, stability, legal parameters, external inputs, and nondegeneracy are handled separately. No unrelated problem from the six-project shortlist is included.

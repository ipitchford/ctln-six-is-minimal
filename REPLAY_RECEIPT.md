# Replay provenance

The supplied v1.0 package records a successful producer replay and a separately implemented model-generated referee audit. Their scope and limitations are retained in ASSURANCE.md and REVISION_RESPONSE.md. Neither is external human peer review.

The v1.1 publication adds a non-mutating replay wrapper and five wrapper/optimized-Python regression tests. Those lightweight tests passed during preparation. The mathematical checkers and three certificate JSON files are unchanged from the reviewed input.

The publication replay runs in GitHub Actions on Python 3.13 from a fresh `git archive` extraction of the exact commit. It checks the manifest before and after `python code/verify_all.py --regenerate --read-only`, then runs `python code/test_replay_guards.py`. The workflow retains a commit-labelled full log. Publication is conditional on that run succeeding; no local queue completion is claimed.

The immutable release's separate REPLAY_SUMMARY.json identifies the successful run, tested commit and archive digest. Consult that receipt and the linked canonical provider run for the publication outcome, not this pre-run description.

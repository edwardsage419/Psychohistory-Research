# R135 post-freeze audit: optimization-safe source amendment

Date: 2026-11-12. This addendum refers exclusively to the new manual R135 reputation-erasure sensitivity program. No change to the 2026-10-20 R135 frozen protocol, historical output, CI or evidence grade.

The original exploratory source in commit `5a648db8dd94236a6036c3a1aaa2d30434f2910a` used ordinary Python `assert` for internal checks, which Python removes under `-O`. The mathematical result had passed ordinary-mode tests, but the source could skip some invariants under optimization. Before treating the new artifact as ready for later reuse, we replaced those internal checks with explicit ValueError/AssertionError branches, without changing the payoff functions, bit enumeration or data schema. The GitHub source was updated by commit `81354feb8b4013b5cc7f3b839368e1ddeaf60123`, prior blob `ba7bfaa8defb621263c36e03a2368aab5c6b62da`, new blob `92ee7ffddee0a5601d0089e87454875b6c1d7d6a`.

Actual local execution of the revised program:

* `python r135_assignment_noise_boundary.py --test`: 7 tests, OK, 4.796 seconds.
* `python -O r135_assignment_noise_boundary.py --test`: 7 tests, OK, 5.333 seconds.
* `python r135_assignment_noise_boundary.py` and `python -O r135_assignment_noise_boundary.py`: 1623-byte JSON stdout was byte-identical in both modes, and identical to the previously committed results JSON. `sha256=5ad4a8a2eda8e286f7c0bd6eeb95461fcd1e1336c195e6e0789dfa7560f507b3`.
* Revised Python source SHA256: `eb0354b822c80ba0f376b4b0749ca91a692b7e69ed7f59013fdf6b1e97495237` (supersedes historical source digest `c17713a42aa4feb063751d5a2ba5734832e266bc6deb7c4250e78f2ed35e1158` in first research note).

This new fix was tested locally in two interpreter modes; GitHub Actions was NOT_RUN, outside-team replication NOT_RUN. The mathematical statement and original 4096-case R135 frozen scan remain unchanged. This addendum preserves both initial and revised source identities for auditability.
# B addendum: native R276 S72 archived Python byte replay

Date: 2026-10-30 Asia/Singapore. Additive correction to prior R276 S72 reports and handoff: the native R Python CLI gap is now CLOSED for this exact archived source and two receipts. Original scientific scope remains exploratory artificial E1, nonblind internal.

The complete R source `research/validation/r276_s72_auxiliary_z_sample_curve_20261030.py` was reread from GitHub, reconstructed locally byte-for-byte, and verified by Git blob before execution:
`e4742d63d3356a1ded01fad78dc3efbb119cf8f7` (local equals remote).

Actual commands executed with standard-library Python:
```
python r276_s72_auxiliary_z_sample_curve_20261030.py --output-dir generated
python r276_s72_auxiliary_z_sample_curve_20261030.py --check generated
python r276_s72_auxiliary_z_sample_curve_20261030.py --selftest
```
All commands returned without execution error. `--selftest` printed `Ran 8 tests`, `OK` (8 passed, 0 failed). The two in-program mutation checks rejected altered CSV and JSON. The `--check` command returned status PASS, 1533 source rows, and exact SHA256:
CSV `4e727cf2b7ec39bd9a201976282b6c5af265affa1d6d1657e8d68e308b20ad61`.
JSON `2c3b4d1d23513b9c385547563d417f34aa72ecde97c64903b2984aa6a868275f`.

Crucially, both independently regenerated local files were hashed with Git's blob algorithm and compared to the actual remote persisted file identities:
CSV local/remote `08dbd0c57ea2f18749d05fe953b2ed907de9cbdd`.
JSON local/remote `51eb669c9150b6c90ac81c3ab8cf5f91030f9d0b`.
Both exact byte identities PASS. No original research files were modified.

Earlier B independent Python count oracle and full remote V8 source checker remain separate methods; this addendum closes only the native R Python execution/byte-identity gap. Full original R276 acceptance stays unchanged. This does not create an external-team replication, real E2 prediction, E3 evidence, blind validation or scientific status upgrade. GitHub Actions NOT_RUN due unverified free quota; no chargeable operations. R073/PESEN frozen.

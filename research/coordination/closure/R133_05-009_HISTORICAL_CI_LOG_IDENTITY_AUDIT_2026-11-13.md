# R133 / 05-009 historical CI identity and execution log audit

Date: 2026-11-13. Independent closure track. Fixed starting main `c051a02d00ede4fb6e261a60cba1c12d927abcff`.

## Evidence directly retrieved

Read GitHub Actions REST run 39368129476 and jobs endpoint, then independently fetched the actual archived job logs for IDs 118449550882 (Python 3.11.17) and 118449550662 (Python 3.12.15). Run event push, attempt 1, completed/success, head SHA `a2c0ee1f5953de0fdce3b4fd0e62afa85a02d5bd`. Both job records show this same SHA and success.

Each job log contains `R133 archive and two source SHA256 hashes verified`, `Ran 36 tests`, and the six exact enumerated counts 625, 300, 300, 100, 200, 100, 25. Each log prints the constructed three-strategy mutant result (0,-1/9). Thus the historical receipt's CI identity, two-job execution and printed mathematical outputs are independently corroborated by GitHub's actual log records.

The logs show a ZIP SHA256 check and two extracted Python SHA256 comparisons. Claimed expected SHA256 values: ZIP `e5ffa574bcbc0cdd2013cbc5312e5fea2ce4e49263e6abc57e65102f88195007`; source `161aae1cbfc609494798ee5c6921c3a091a93b0dabcef70f24bf038870160e3f`; test `56e7e4801a592ee3bcba35d135bdc25bc5141cb9225a39acab13bcca253c6957`. Git blob of archive in main: `31b97e35f1eee5513d7aabae1fa2e8e1d4096e68`. These are historical CI-verified claims; this audit did not independently obtain the ZIP bytes and recompute the three SHA256 values.

Sources: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39368129476 and its job logs. Historical acceptance receipt Git blob `b91625e942a583051c21ad442ba45bc073c138ed`.

## Scientific disposition

This closes the specific historical CI run identity/log-reading evidence gap for R133 05-009. It does not close the original catalogue itemwise review. No original 1973 stochastic simulation was rerun; no new animal/human data, no E2/E3, no independent third-party execution. Maintain R133 CLOSED_BOUNDED and 05-009 provisional pending original-source and archive-byte assessment. Existing independent mathematical enumeration in the preceding closure report remains the numerical evidence; this audit avoids repeating it. No workflow was triggered, no freeze or R core code modified, and no paid resource invoked.

# S53 authenticated composition

User-authorized bounded continuation of the PR integration queue. Reuse the main-side original225 Node gate and pinned PR3 Python mathematical validator. No original files, mathematical algorithms, protocol interpretations or old PRs are changed.

- [x] Refresh main/open PRs; inspect source-link implementation and S53 protocol/deviation.
- [x] Write tests and observe the absent composition fail.
- [x] Authenticate exact bytes of 4 data/source inputs, the source-link gate, frozen protocol and historical deviation, plus the external PR3 validator. Run both original CLIs on the same temporary snapshot; require exact expected bounded success summaries.
- [x] Test normal/optimized execution, changed/missing inputs, changed executable code before execution, malformed child success and unchanged sources.
- [x] Review, record hashes/commands/results, and deliver separate draft PR without CI/merge.

The caller supplies --validator PATH from fixed PR3 head 97d5f74df5d84916917db943156120f08144f445; missing dependency is an error, never skipped or downloaded implicitly. Output is stdout only, so this tool cannot leave a stale on-disk success file. Snapshot identity authenticates the bytes consumed, not simultaneous filesystem state, author signatures or historical timing. No claim of new E2/E3/external replication.

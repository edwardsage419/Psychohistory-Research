# Psychohistory Platform v0.3 implementation plan

**Goal**  Provide separate, reproducible synthetic trajectories for the historical R123 and R132 mechanisms, strengthen execution and durable storage, and verify the new workflow on Linux and native macOS.

**Architecture**  Use the existing SQLite store, source registry and bounded scheduler. Introduce a distinct trajectory run kind with immutable inputs, content-addressed snapshots and mathematically compatible comparisons. Keep the v1 simulation and v2 prediction run contracts. Compute the trajectory in a sealed interpreter from the exact platform source bytes recorded at submission.

**Scope**  Base `dd05f32f79efc2f4f4f37117cc039dca1008ed76`. R132 source identity points to the v0.2 curated main pin, verified unchanged at the base commit. The #44 candidate remains browse-only. The only executed model inputs are synthetic.

- [x] Add a stdlib-only R132 plugin with exact Fraction equations, distinct generation and ODE clocks, reference trajectories, bounded input and numeric diagnostics.
- [x] Register both mechanisms under a shared v3 trajectory workflow. Bind the model, source blobs, code and checkpoint to every run. Require a fresh approval when creating an independent branch. Compare matched times and states using the same mechanism, versions, source and scientific parameters.
- [x] Test the shared scheduler under normal finish, cancellation, wall timeout and forced parent exit. Enforce and prove CPU limits with native POSIX tests. Record each effective control in the worker receipt.
- [x] Make audit and state commits consistent with SQLite backups. Flush object and directory metadata before a successful run may reference the object. Inject process interruption and verify historical backup restores.
- [x] Deliver authenticated v3 API, CLI and Chinese research panel using one model contract. Exercise source verification, approval, separate methods, snapshot branches, incompatible comparisons and persisted results in Chromium.
- [x] Run Linux and standard free GitHub macOS ARM64 from fresh checkouts. Independently review the code and retain command results, provenance and artifact comparisons in the Draft PR.

The most consequential review boundaries are wrong generation/ODE comparisons, invalid simplex excursions at RK4 intermediate stages, disguised scientific promotion of a candidate, sealed worker ownership after parent termination, and false success around object publication or SQLite commit.

运行结果与保留的限制见 [v0.3 验收](../reports/V03_ACCEPTANCE.md)。

# R127 local fail-closed gates

Spec: main's `R127_CI_P0_FAIL_CLOSED_HANDOFF_MATRIX_2026-11-10.md` and
`R127_STAGE2_E2_RECEIPT_MASKING_NEGATIVE_CONTROL_2026-11-10.md`.
Base: `b8b0ea2e2a45a6fb9c99e9a51302ab0f07e8c613`.

Implement only an independent Codex A module. The R mainline owns workflow
edits and final scientific acceptance. Do not change the workflow, original
program/tests/report, historical receipt, final status, R073 or PESEN v0.1.

1. Write failing unittest coverage for log failure markers, optimization,
   exact typed stage-two fields, upstream E2=7, missing fields, duplicate JSON,
   source/Git identity mismatch and preservation of the source files.
2. Implement a stdout-only local replay: authenticate the five fixed workflow,
   code/test/report/receipt byte snapshots; run the original 60 tests and original
   six stage-two computations in an isolated temporary tree. Explicitly compare
   all returned fields/types with the authenticated historical receipt sections.
3. Emit a separate local provenance sidecar, binding checkout, source identities,
   gate bytes, exact commands, exits and raw-stream SHA256. Derive its E2 count
   from validated upstream values. Do not claim historical CI/run/time identity.
4. Run unit tests and real native replay in normal/-O; verify protected source
   hashes before/after, archive RED/GREEN logs and hand off an independent draft.

Review focus: trailing fake OK; duplicate/zero/incorrect summary; failed child
with success-shaped output; bool/int confusion and hidden nested field changes;
upstream E2 masking; authenticated receipt versus supplied expectations; runtime
optimization propagation. No Git writes or receipt publication from the CLI.

The publishing no-op/rebase policy and production workflow wiring stay with R
mainline. This is a concrete candidate gate and execution receipt, not a claim
that the production P0 defects or scientific closure are already resolved.

Completed: explicit gate, all final normal/-O tests/replays, source preservation
and a fresh review. Review P2 provenance finding fixed in one RED/GREEN pass.
Production workflow ownership, publication and historical CI identity remain
mainline responsibilities, as specified above. Independent draft prepared.

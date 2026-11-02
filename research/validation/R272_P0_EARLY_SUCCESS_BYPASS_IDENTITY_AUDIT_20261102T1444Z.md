# R272 P0: successful early-exit bypass in proposed mandatory caller

Date: 2026-11-02T14:44Z. Track: R/B. Starting main: 10031b279977bb5e5d625261a632ee4eb960a9d8.
Status: COMPLETE_BOUNDED_STATIC_REPRODUCTION. Production acceptance: OPEN.
Scientific evidence: internal nonblind E1 engineering audit only. CI: NOT_RUN.

## Exact reviewed sources

* Candidate YAML: research/validation/r272_mandatory_acceptance_proposal_20261102.yml, Git blob fe7165cf0dfe1de12664ddfbcf4360b73c29a518.
* Prior checker: research/validation/r272_proposed_caller_structural_gate_20261102.py, Git blob 9121d9d873b364446e41e2dea5c765a9f1a2e827.
* Active workflow: .github/workflows/r272-exact-train-test-oos-e1.yml, Git blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d.
* Freeze: protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md, Git blob 9fbdb0078a58c4a9c0a548643227e30da5731119.
* original239 crosswalk v7.8 Git blob 36f24235901172642c46853298aebb421f1a3552; pending queue Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. Queue re-count: 154, P0 27, P1 82, P2 45.
* Open Codex PR count: 12. PR #1 and #3 remain open, concern R257 S53 and do not implement R272 caller adoption.

## New counterexample

The prior checker searches for required command substrings and disallows a small set of tokens. It does not prove the shell reaches the required commands. Insert an unconditional indented 'exit 0' immediately before the first mandatory preimage wrapper command in the preimage-first job, before the final mandatory wrapper in independent-sources-and-archive, or in both places. The literal command strings, dependency graph, ZIP hash, watched paths, permissions, and optimized-mode tokens remain unchanged.

A local reconstruction of the exact candidate YAML was checked against its Git blob and matched byte-for-byte. The previously archived check() function was reconstructed from the connected GitHub source for offline execution. CPython 3.13.5 and PyYAML 6.0.3: baseline checker PASS; mutated preimage step PASS; mutated final step PASS; combined bypass PASS. These are **three observed false accepts by the archived check() logic in the reconstructed local fixture**. The complete original remote checker CLI on a full checkout was NOT_RUN.

An independent local Bash experiment with errexit enabled, 'exit 0' before a failing command, returned process exit code 0. This shows why ordinary Bash fail-fast cannot protect unreachable checks.

With both wrappers bypassed, the proposed job can still run its generator unit tests and its native negative regression, which regenerates a separate disposable root. That regression does not authenticate the existing checkout's archived triplet. The final archive job's mandatory wrapper is also bypassed. Therefore the candidate's historical preimage acceptance is no longer guaranteed. A complete GitHub Actions false-green execution with corrupt archives was NOT_RUN and is not claimed.

## Additive guard and bounded tests

New executable: research/validation/r272_workflow_early_exit_identity_audit_20261102.py. It pins the reviewed candidate's exact Git blob, checks whether the active workflow is byte-identical to the reviewed candidate, and constructs three early-exit mutations for comparison with the archived checker. The strict byte-identity check rejects all three altered candidates. This is a conservative review gate, not a replacement for command reachability testing or an adopted workflow.

Local syntax compilation PASS. Local exact-candidate and reconstructed-checker execution: 3/3 mutated inputs incorrectly accepted by old check() logic. Independent identity gate: 3/3 correctly rejected. Local synthetic fixture end-to-end Python audit: PASS. No random seed. Native audit on a complete authentic checkout: NOT_RUN. The actual active workflow remains different from the proposal and retains the previously documented preimage overwrite risk.

## A source eligibility and scope

English official Kim 2023 openICPSR V1 DOI 10.3886/E152261V1 was rechecked. It explicitly says stage decisions were made all at once; the repository already documents this design as ineligible for unchanged R073 observed-opponent-history replication. Previously assessed DF2011, ON007822 and Grujic data are not counted again as newly qualified independent cohorts. New eligible R073 dataset: 0; new E2/E3 scores: 0.

## Closure conditions

1. Require exact reviewed candidate identity or a separately reviewed revised candidate. Install a genuinely mandatory check that detects early-success exits, unreachable commands, conditional skips, custom shell semantics and failure suppression. Do not treat substring-only static lint as execution proof.
2. Execute the negative mutations on the complete checkout and require every bypass to fail the mandatory adoption gate. Verify historical archive bytes before any generation, compare isolated regeneration, and preserve original failed preimages.
3. Confirm PR and push path coverage and actual no-charge Actions eligibility before owner-authorized production workflow adoption. Preserve frozen protocols and old failed evidence.
4. Keep R272 P0 OPEN until a production caller is adopted and independently verified. R257 S53 historical blind-order FAIL and R333 to R340 composite caller gaps remain open. R073 and PESEN v0.1 remain frozen.

No paid APIs, Actions runs, new subscriptions, cloud compute, or data purchases were initiated. Account billing and Actions quota are not independently verified. Formal original239 pending queue net change: 0.

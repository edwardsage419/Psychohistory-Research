# R272 P0: complete-checkout execution, false acceptance and quarantined v2

Date: 2026-11-17 UTC. Engineering integrity research for original239 item 12-002, priority P0. Scientific evidence scope: internal, nonblind, artificial E1 acceptance tooling. The original R272 frozen mathematical acceptance and historical records remain unchanged.

## Baseline, freeze and nonduplication

Research branch started at main f1761b89af48bc38f70c04b1369ce76ecb6492e9. During this research, main advanced to 073496bed7b0e1ab0bafef7739fc02f8a4a004c4 with a nonoverlapping theory-source commit. This branch changed only the new R272 audit workflow, the quarantined v2 candidate, and its evidence files.

Frozen original protocol: protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md, Git blob 9fbdb0078a58c4a9c0a548643227e30da5731119. The original R272 model comprises 4 independent training and 2 independent future Bernoulli bits for 9 synthetic worlds with 576 labelled source atoms. The original frozen acceptance required Python 3.11 and 3.12 tests, independent source replay and three successful workflow jobs. Its historical run 39903106107 and bounded E1 conclusion are immutable.

The current main production workflow .github/workflows/r272-exact-train-test-oos-e1.yml, blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d, retains prevalidation regeneration of archival evidence, optimizer-sensitive Python assert validation, contents:write and automated rebase/push to main. It does not call the unadopted candidate. Prior audits already identified these issues; this run does not reimplement the old production pipeline.

Unadopted archived candidate research/validation/r272_single_entrypoint_failclosed_20261102.py, blob f33e4e7e544560d65342a899606311d169e4d122, was previously evaluated locally. A November 3 audit flagged possible import-shadow of unpinned sibling Python modules. This round adds new real full GitHub checkout execution, an end-to-end false-success witness, and a directly tested quarantined v2 candidate.

## First actual GitHub native full checkout

A new separately named, read-only Actions workflow .github/workflows/r272-full-checkout-unadopted-candidate-20261117.yml executed the exact archived candidate in the actual full GitHub checkout under Python 3.11.18 and 3.12.16. The parent was invoked in Python isolated mode. Internally the candidate independently ran each of normal, optimized and double-optimized modes. For each mode it checked the original 83 scientific tests, 15 intentional preimage-mutation rejection checks, archived preimage integrity and isolated regeneration. All positive executions succeeded and both checkout trees had no tracked or untracked scientific changes.

This confirms the old candidate runs in a clean checkout. A clean-input pass does not establish resistance to untrusted import paths.

## New exact-source full false acceptance

A disposable directory was populated with the actual Git-blob-verified original R272 science source, historical freeze, archived CSV/JSON/receipt, wrapper, native negative tests and original ZIP checker. Exactly two additional, unpinned Python modules named json.py were injected into the disposable research/validation and research/R272 script directories.

The additional modules were configured for deterministic synthetic failure-control simulation. The validation directory module ended the real wrapper and negative tests early with process exit 0 after printing expected JSON claims. The R272 directory module ended the original generator/test command early with exit 0 after printing a forged unittest summary mentioning 83 tests. The original candidate itself was invoked with python -I -S, and all archived source and frozen identities remained authentic.

Observed result: the original top-level candidate returned status PASS, three accepted mode receipts, 83-test claims and 15 negative-check claims **although the real scientific wrapper, native negative suite and upstream tests had been bypassed**. The true reason is that the archived candidate invoked its children with sys.executable without propagating isolated import settings and relied on unpinned output text and JSON. The parent check never pinned or excluded the injected sibling modules.

Real GitHub log marker: R272_UNPINNED_SIBLING_IMPORTS_CAUSE_FULL_FALSE_ACCEPTANCE. This is an actual full candidate false-PASS demonstration in an isolated, synthetic attack fixture. There is no evidence of an actual historical production compromise. The original production workflow never adopted this candidate.

## Quarantined v2 engineering candidate

New code: research/validation/r272_quarantined_candidate_v2_20261117.py, Git blob e5143fe2e18f8acab5223f04a62cb4510ffbea57.

It first authenticates the archived candidate, original generator, freeze protocol, wrapper, native negative suite and three science artifacts using eight fixed original Git blob hashes. It independently checks the archive ZIP SHA256 f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151. It then copies **only these nine identified files** into a fresh private test directory and confirms their complete identity and filename allowlist. No unpinned original-neighboring Python module is copied. The subprocess runs the original pinned candidate under python -B -I -S with all inherited PYTHON-prefixed environment variables cleared, and PYTHONSAFEPATH, PYTHONNOUSERSITE and PYTHONDONTWRITEBYTECODE explicitly controlled. It validates all three mode receipts with unconditional exceptions and independently rechecks every original and private source byte afterward.

Actual native results: v2 passed clean full-checkout execution under Python 3.11.18 and 3.12.16. On the same poisoned fixture that produced the original candidate's false PASS, v2 excluded both modules and ran genuine science checks in the private fixed-input directory. A separate fixture with a corrupted original results JSON was rejected before any scientific process execution.

The v2 evidence is limited to the specific verified input paths, controlled Python interpreter and tested attacks. It is not a proof against arbitrary compromised system Python runtimes, untrusted executable binaries or all possible code-injection mechanisms. Historical source input bytes were preserved, and v2 is an unadopted candidate.

## Complete actual CI history

GitHub CI 44037432313: SUCCESS, clean native original candidate on two Pythons; parent-level import-shadow control.

GitHub CI 44037737795: SUCCESS, explicit full-candidate false-PASS proof using only disposable files.

GitHub CI 44038227060: FAILURE. The first v2 adversarial fixture omitted the old candidate file from its new v2 strict allowlist. v2 correctly rejected the missing file; test fixture was incomplete. This failed CI is retained.

GitHub CI 44038360525: SUCCESS, trigger SHA 9dad41695941d17b0754bd7eae93ebda4bde242b. All three real GitHub jobs completed success:
* Job 133886625843, Python 3.11.18: clean old candidate and quarantined v2 success.
* Job 133886625867, Python 3.12.16: clean old candidate and quarantined v2 success.
* Job 133886625473: old candidate full false-PASS reproduced, quarantined v2 excluded the injected modules, and v2 rejected corrupt archived evidence.

Observed log signatures:
R272_FULL_CHECKOUT_CANDIDATE_THREE_MODES_PASS;
R272_CHECKOUT_ARCHIVES_REMAIN_UNMODIFIED;
R272_QUARANTINED_V2_REAL_CHECKOUT_3_MODES_PASS;
R272_UNPINNED_SIBLING_IMPORTS_CAUSE_FULL_FALSE_ACCEPTANCE;
R272_QUARANTINED_V2_BLOCKS_TWO_MODULE_INJECTION;
R272_QUARANTINED_V2_CORRUPTED_PREIMAGE_REJECTED.

Run URL: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44038360525

The three success jobs above are jobs of this new read-only engineering audit workflow. Their numeric count must not be substituted for the frozen 2026-10-23 original three-job production acceptance contract.

## Production disposition and scientific evidence limits

Current main was independently verified protected=false, and GitHub rulesets returned no rules. This does not establish that validation checks are required before writing to main. The actual production R272 workflow still uses the old assert and writeback pattern and has not been changed.

Disposition: OLD_SINGLE_ENTRYPOINT_FALSE_SUCCESS_CONFIRMED; V2_BOUNDED_IMPORT_QUARANTINE_VERIFIED; CURRENT_PRODUCTION_GATE_P0_OPEN.

Production adoption requires independent owner authorization, a freeze-compatible three-job review, real mandatory-status enforcement, path-trigger coverage, dependency pinning, and a separate review of the proposed CI security boundary. No production workflow was installed or merged. No real-human E2, real-historical E3, R073 independent dataset, external-team replication or model fusion was performed. The R272 original CLOSED_BOUNDED_E1 research acceptance and 154-item P0 queue remain unchanged, as do R073 and PESEN v0.1.

No paid API, additional service or commercial runner was invoked. Standard GitHub-hosted Ubuntu was used on a public repository. Account billing records were not inspected.

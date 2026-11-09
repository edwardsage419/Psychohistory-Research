# Original239 05-007 / R131: independent SHA256 replay of three historical core files

Date: 2026-11-10 UTC. Track: closure. Baseline main HEAD: `f5e0f18bfc61eab88b8d53bc8fcb199970f7aade`. This note is additive and does not modify frozen protocols or earlier scientific conclusions.

## Method and evidence

Fetched the three exact UTF-8 files directly through the connected GitHub repository file reader on `main`. Independently computed SHA256 over their returned UTF-8 bytes using a self-contained JavaScript SHA256 implementation with no import from the R131 research implementation. The implementation was checked against the standard `abc` SHA256 vector `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`, which matched. Compared computed digests against `research/R131/R131_PHASE_A_1978_63_TEST_504_INVASION_SOURCE_FINITE_DRIFT_CI_ACCEPTANCE.json` on the same branch.

| File under research/R131/ | Git blob SHA1 | UTF-8 bytes | Independently computed SHA256 | Historical receipt match |
| --- | --- | ---: | --- | --- |
| R131_TAYLOR_JONKER_1978_ORIGINAL_ESS_DYNAMIC_COUNTEREXAMPLES_AND_FINITE_DRIFT_SCIENTIFIC_REPORT_2026-10-20.md | `22a0877501a525f780fc8e525f9b682c1cde9eef` | 10632 | `f37ab851ffe4cd196419668467c43d0e9f9374f1d9bf2c416d0faa7f46fc8ca5` | MATCH |
| r131_taylor_jonker_1978_evolutionary_game_exact.py | `3c61e0c3c0fe7a6d4458eccd8fc18e9714e7152f` | 17344 | `55f3006a3d1c23d82f30fff4aa6eda63efb537425035e471b180a031e0a282d3` | MATCH |
| test_r131_taylor_jonker_1978_evolutionary_game_exact.py | `de3391fa8252e17186616123d523942915aec9e7` | 15547 | `4e36571a3db3915d9effcd84ce0cef0897533ed8556ee6dd501d734040b2b7f2` | MATCH |

All three digests matched the historical machine receipt exactly. This closes the **three-file byte-digest verification subtask** left OPEN in the prior closure note `ORIGINAL239_05-007_R131_FROZEN_PROTOCOL_AND_CI_RUN_VERIFICATION_2026-11-10.md`.

## Scientific scope and remaining gates

This proves that the current main-branch UTF-8 file contents match the SHA256 digests in the historical receipt. It does not establish the historical commit's byte identity independently, prove source-paper page attribution, or independently rerun the R131 Python program and its 63 tests. Historical GitHub Actions job success was checked in the prior closure note. The original 1978 paper's selected witness attribution is already corrected by the R track, so no duplicate correction is made.

A03 historical receipt **file hash subgate: PASS**. A03 full native replay: OPEN. A02 original paper source inspection: PARTIAL (separate R-track provenance audit). A06 itemwise closure: OPEN. R131 existing `CLOSED_BOUNDED` remains unchanged. Original239 `05-007` provisional mapping remains unchanged; formal queue reduction: **0**. Evidence tier: **E1 only**; new E2/E3 scores: **0**. No Actions/CI triggered, no paid API or cloud resource invoked. GitHub account billing was not checked.

Next highest-value step: independently run the current original Python program and tests, compare actual output with the frozen protocol and receipt, then decide the A01–A06 itemwise gate without changing historical results.

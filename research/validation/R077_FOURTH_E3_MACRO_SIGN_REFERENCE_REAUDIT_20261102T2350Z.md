# R077 fourth independent human experiment: archived E3 macro consistency and conditional sign reference

UTC: 2026-11-02T23:50Z. Track: R/B. Baseline main: 0d02b35284b291c7f33398034e58844587ba5ddc. Target key: (R/B, R077 fourth original human study, Rev002 prescore freeze, independent archived macro and paired sign audit). Status: COMPLETE for the bounded nonblind archive audit; original individual scoring and external independent replication NOT_RUN.

## Pinned sources and exclusions

* Original anonymous archived R077 JSON: `research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json`, Git blob `13946754afc06e529f2d3a2072a7bae297453fa9`, 9,835 bytes.
* Original scoring protocol: `protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md`, with the historical Rev001 eligibility FAIL preserved. Rev002 eligibility amendment: `protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md`, commit `f79d59175098b4314c9c784394cfd5beb8083f2e`, frozen before first R077 seven-model target scores.
* First-party author data: Drouvelis and Pearce (2025), Zenodo v1 `https://zenodo.org/records/15462528`, original `cleandata.dta` MD5 `4cce04ea68b7a0492c242b206efebe53`. The published page was read on 2026-11-02 UTC; it lists the file and checksum. It displays a License heading without a visible license value. No data was downloaded or redistributed in this audit.
* New independent read-only program: `research/validation/r077_fourth_e3_macro_sign_reference_audit_20261103.js`, remote Git blob `030db517ed53a6b2e1208a8843cfae6539b75305`. It imports no R073/R077 original model or scoring code and has no random inputs.
* Original239 v7.8 crosswalk remains current. Queue `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv`, Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`, contains 154 rows: P0=27, P1=82, P2=45. Net closure 0. Open Codex PR count at inspection: 12; #1 and #3 still unmerged. Their R257 S53 work is distinct and was not repeated.

## Actual independent execution

The complete newly committed program was re-fetched from main and its exported `selftest` invoked in isolated JavaScript V8 against the complete re-fetched archived JSON. This is a genuine execution of the new algorithm over the historical anonymous macro receipt. It is not native Node CLI execution on a full checkout. All seven model identities, six prespecified contrast identities, 15 original sessions (treatment 0:7, treatment 1:8), and 1,040 scorable events were checked against the archive.

Fourteen model macro recomputations use the treatment-weighted formula `(7*m0 + 8*m1)/15` for Brier and log loss. For each of six frozen pairwise contrasts, the algorithm independently recomputes overall and treatment-specific Brier differences, treatment sign-count conservation, 15-session coverage, and treatment-weighted pair differences. Total numeric checks: **80/80 PASS**; maximum absolute floating-point difference **2.220446049250313e-16**. The program also rejected **7/7** mutations of macro score, treatment score, pair difference, sign count, treatment size, model coverage and pair coverage. These negatives were tested against the actual archived macro structure.

The result verifies algebraic consistency of the *reported aggregate receipt*. No original Stata data were re-read, no participant-level predictions were recomputed, and the original 15 session-level scores are intentionally absent from the public archive. The reported better/worse signs are therefore only checked for internal count consistency; their truth cannot be independently recovered from the released macro JSON.

## New exploratory exact sign-tail references

Using only the 15 already reported paired session signs, the code calculates `min(1, 2*sum_{k=0}^{min(better,worse)} C(15,k)/2^15)`. It also computes monotone Holm reference adjustments across the six originally specified contrasts. These are *post hoc mathematical reference values*, not part of the frozen R077 acceptance protocol. Independence of the 15 sessions is **NOT VERIFIED** because participant re-enrolment across sessions has not been independently excluded. No p-value below is claimed as a valid confirmatory inference.

| Prespecified Brier contrast | Better / worse | Two-sided sign-tail reference | Six-contrast Holm reference |
| --- | ---: | ---: | ---: |
| M3 versus M1 | 14 / 1 | 0.0009765625 | 0.005859375 |
| M6 versus M0 | 1 / 14 | 0.0009765625 | 0.005859375 |
| M2 versus M0 | 13 / 2 | 0.00738525390625 | 0.029541015625 |
| M1 versus M0 | 12 / 3 | 0.03515625 | 0.10546875 |
| M5 versus M0 | 10 / 5 | 0.3017578125 | 0.603515625 |
| M4 versus M3 | 8 / 7 | 1.0 | 1.0 |

The archived R077 macro Brier improvements are M3 minus M1 = **-0.030210760470721517**, and M4 minus M3 = **-0.001918699476466503**. The 14/15 versus 8/15 signs show that the stronger one-lag joint-history advantage and the weak two-lag increment have materially different session consistency. M6 performs worse than M0 in 14/15 sessions. These are descriptive archived observations. The test does not identify a causal effect of receiving opponent feedback.

## Status, constraints and next task

* R/B archived E3 macro re-audit: COMPLETE. Independent *algorithm* on a known same-team archive, nonblind.
* R077 original E3 frozen result: unchanged. New human E2/E3 scored events: 0. Original Rev001 failure: retained.
* Original participant/session-level replay, external-team independent replication, independence of session signs, and cluster-robust uncertainty: NOT_RUN / UNKNOWN. No scientific acceptance upgrade.
* R272 mandatory production P0 and R257 S53 historical blind-order FAIL: remain OPEN. R073 and PESEN v0.1 remain FROZEN. Original239 net closure 0.
* GitHub Actions: NOT_RUN. No workflow dispatch or new paid API, cloud service, subscription or data purchase. Account billing and Actions free quota: NOT_VERIFIED.

Next highest-value feasible research action: independently inspect R077 source-level session identity and participant re-enrolment only if the public author data and lawful processing are accessible, or execute the existing R272 preimage-first runner on a complete authentic checkout. The conditional sign-tail numbers should not be promoted to confirmatory p-values without the missing independence and session-level score evidence.

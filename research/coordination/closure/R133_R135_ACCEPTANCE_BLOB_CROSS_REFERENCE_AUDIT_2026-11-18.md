# R133 / R135 acceptance blob identity cross-reference audit

Date: 2026-11-18. Independent closure audit; candidate only. Main baseline: `7ea6eab94433e3669b6f492d802bb35316dc90d6` (confirmed identical to main by compare endpoint).

## Reproducible source identities

GitHub contents API at the same `main` ref returned:

| Path | Actual Git blob SHA-1 |
| --- | --- |
| `research/R133/R133_FINAL_ACCEPTANCE_STATUS.json` | `70d36423e87eca9a14f7b6f9f18177e66c9116d5` (previously independently recorded; re-fetch required before mutation) |
| `research/R135/R135_FINAL_ACCEPTANCE_STATUS.json` | `72e60d3e0fa8f131c6a4864d0d6cc89afbe350fc` (re-fetched this run) |
| `research/coordination/closure/R133_05-009_ITEMWISE_BOUNDED_DISPOSITION_2026-11-13.md` | `9ffb45fb632744fe40b3a027491d0983371871a9` (re-fetched this run) |

The R133 itemwise report's “Fixed evidence identities” section attributes `72e60d3e0fa8f131c6a4864d0d6cc89afbe350fc` to R133 final acceptance. Direct retrieval identifies this blob as **R135** final acceptance, whose content declares `research_id: R135`, `catalogue_id: 05-011`, and Ohtsuki/Iwasa 2004. The report itself addresses R133, `05-009`, Maynard Smith/Price 1973. This is a cross-model evidence pointer mismatch, not a newly demonstrated error in the R133 mathematical calculation.

## Scope and disposition

* Finding: P0 provenance integrity risk, one erroneous cross-model blob citation in a historical audit report. No proof of altered numerical outputs, checker acceptance, or additional affected reports.
* Proposed minimal remedy for R mainline: add a corrective addendum referencing the correct R133 acceptance blob after re-fetch; preserve the original erroneous string and the historical report as audit evidence. Do not silently rewrite historical identities.
* R133 research-level `CLOSED_BOUNDED` and catalogue `05-009 ACTIVE` unchanged.
* R135 research-level `CLOSED_BOUNDED`; catalogue `05-011` itemwise closure remains unadjudicated. Its existing acceptance records 4096 norms, 61440 invasion checks, five benefit counts 25/73/59/15/13, no original-author simulation code rerun, no new E2/E3. No new mathematical replay was performed in this audit.
* Crosswalk `docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json` has blob `36f24235901172642c46853298aebb421f1a3552`; the historical pending-154 queue is not a current unresolved-count measurement.
* No scientific grade upgrade, no formal itemwise closure, no frozen protocol changes, no CI triggered. Review and owner decision required before any formal catalogue mutation.

## Independent check recipe

Fetch the three named paths at a pinned commit, record each returned `sha`, compare the R133 report's claimed final acceptance blob with the actual R133 and R135 acceptance blobs, and inspect the JSON `research_id` and `catalogue_id`. No implementation import or computational result acceptance is needed for this provenance check.

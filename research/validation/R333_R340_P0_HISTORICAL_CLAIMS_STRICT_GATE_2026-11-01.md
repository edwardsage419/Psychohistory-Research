# R333 to R340 P0 historical scientific claim receipt gate

Date: 2026-11-01 UTC. Track: R / B. Baseline main: `4c0df1aec1db87dabddf97d4004d76bf91490a50`. Status: **PARTIAL_P0_OPEN**.

## Frozen scope and rationale

The pre-existing candidate `research/evidence_audit/r333_r340_acceptance_entry_20261101.py` authenticates model sources and finite E1 mathematical receipts, but does not inspect the eight historical `MACHINE_RECEIPT.json` and eight `FINAL_ACCEPTANCE_STATUS.json` files. The preceding source audit `research/validation/R333_R340_HISTORICAL_CLAIMS_COVERAGE_AUDIT_2026-11-01.md` documented this gap. This stage addresses exactly those 16 historical scientific claim files, without altering original data, protocols, scores, model calculations or old statuses.

## Added executable control

`research/evidence_audit/r333_r340_claim_receipt_gate_20261101.js` pins the full R333 through R340 model universe, all 16 historical Git blob SHA1 identities, the eight archived CI run IDs, each source commit and protocol commit. It rejects missing files, symlinks at file/model/root level, byte mismatches, source/protocol/model/catalogue mismatches, changed CI run or success claims, E1 grade inconsistencies, E2/E3 promotion and wrong machine receipt paths. Historical R334 `verified_source_commit` and `verification.run_id` fields are handled explicitly. This tool uses Node standard-library crypto and imports no original research implementation.

The gate's success output is deliberately `PASS_HISTORICAL_CLAIMS_E1_IDENTITY_ONLY`. It declares `mathematical_gate=NOT_RUN` and `production_adoption=NOT_ESTABLISHED`. The mathematical entrypoint and a trusted caller binding remain separate mandatory prerequisites. Historical CI success is a recorded claim, not a new CI run or scientific replication.

## Actually executed verification

* CPython 3.13.5 and Node.js v22.16.0 local environment. Executed `node /mnt/data/test_r333_r340_claim_receipt_gate_20261101.js`: **13/13 synthetic controls passed**, consisting of one complete eight-model positive fixture and twelve rejection cases. Controls cover machine CI tampering, E2 promotion, both file types missing, altered CI conclusion, source/protocol/grade mismatch even when the test fixture's blob pin is recomputed, model-universe shrink/expansion, a symlink receipt and wrong receipt path. Tests generate their own temporary fixtures and delete them. No randomness or external dependencies.
* The exact local tested source and test Git blobs are `add869ed3c8dc3f9eb39d91fb836ac9df5eb307f` and `a2654d42f74d9f22ebb3af0b10d35005c14cd034`. Remote GitHub file readback matched both hashes.
* Independently fetched all **16 actual historical GitHub JSON files** from main through the GitHub connector and checked their returned blob identities and 20 semantic/lineage conditions per model against the prior audit manifest. All eight model pairs passed. This was a connector-side semantic check, **not native execution of the new Node gate against a full real checkout**.
* Native full repository checkout execution of the claim gate: **NOT_RUN**. Native 16-child Python mathematical entrypoint: **NOT_RUN**. Original optimized-mode false-accept P0: **OPEN**. Production caller adoption: **NOT_ESTABLISHED**. External team replication: **NOT_RUN**.

## Queue and parallel tracks

The main crosswalk `docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json` has Git blob `36f24235901172642c46853298aebb421f1a3552`. The current itemwise pending queue `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv` has blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`, 154 entries with priority counts P0=27, P1=82, P2=45. Net closure this stage: 0. Codex PR #1 and #3 remain open and unmerged; PR #3's R257 S53 comparator problem is separate. No Codex files changed.

A-track source shortlist reviewed: the Cason/Riedl/Schram/Ule 2026 Dryad 100-round indirect-reciprocity source remains incompatible with the frozen R073 dyadic 100-round direct test because each round rematches and only one player chooses; original CSV remains unavailable per the prior source audit. DF2011 is already deduplicated against R074. No new source was promoted, downloaded or scored. New E2=0; new E3=0. R073 and PESEN v0.1 remain frozen.

## Remaining conditions and next work

1. Obtain a complete read-only repository checkout without paid infrastructure; run both this Node claim gate and the existing Python mathematical gate on all authentic archived files. Run a controlled mutation changing only historical claim fields, keeping mathematical source/CSV/JSON fixed.
2. Freeze and implement an authenticated composite acceptance caller that requires **both** gates; prove an old checker PASS cannot bypass the claim gate. Audit caller identity, coverage and invocation, including optimized Python.
3. Independently review the source-first R127 original239 protocol deviation and the R257 S53 open PR before any scientific closure. Preserve historical failures and E1/E2/E3 boundaries.

No GitHub Actions were dispatched; new CI **NOT_RUN**. No paid API, data purchase, runner, GPU or cloud provisioned. Actual GitHub billing and remaining free quota **NOT_VERIFIED**. No private data or keys were handled.

# R179 / original239 08-003 independent exact audit

Date: 2026-11-02 (Asia/Singapore). Track: R / B independent scientific audit. Status: COMPLETE for bounded E1 arithmetic, PARTIAL for itemwise scientific acceptance. Start main HEAD: `18136702699f6f602f35ed43eb92728d5179b02b`.

## Frozen subject and provenance

Original239 catalogue `08-003 Bayesian Posterior Inference` remains in `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv` as P0, provisional primary R179 link. Crosswalk v7.8 identifies R179 by README token and explicitly leaves scientific acceptance undetermined. Frozen protocol `protocols/R179_BETA_POSTERIOR_90_COUNT_WORLDS_PRESCORE_FREEZE_2026-10-21.md`, blob `6b807f3079eafcf9529c9ac3846c02d8f2f3cea6`, was committed as `25b17c232efe4902f9fd9ac39fde756d19294a98` before historical CI head `9e26807ec8a7e5876a7cd531a959e6ee9166fbfd` (ahead by three commits). The original R179 source blob is `d6fe1580fe9ab2e3eb0c344a1f614f86b4d07767`. The complete historical JSON blob is `bce1490a8178b996b5a7322c0f9a15257feb5187`, 527,917 UTF-8 characters.

The frozen grid comprises n=4/8/12, p=1/4 or 1/2, IID binomial, Beta-binomial with concentrations 2 and 8, zero-inflated binomial with zero masses 1/8 and 1/4, and Beta(1,1), Beta(2,2), Beta(1,3) working priors. Total: 90 worlds, 810 source count cells, 810 posterior count rows. No actual human or historical observations.

## New independently executed method

New self-contained JavaScript BigInt rational validator: `research/validation/r179_independent_exact_90world_receipt_gate_20261102.js`, final blob `94d528797304a7e28060d369821023536a4f81d6`. It imports neither the original R177 generator nor R179 implementation. The script independently reconstructs all source PMFs using binomial coefficients, Beta-binomial rising factorials and zero-inflated binomial mixtures. It then verifies every posterior mean, variance and true-p Beta CDF by binomial-tail identity, every 95% coverage flag, exact weighted means, bias, MSE, working posterior variance, MSE-to-variance ratio and coverage. It checks full world identity, 15 fixed examples against their complete world records, source identities, evidence labels, and expected future-event logloss via JavaScript floating point. The script's Node CLI additionally checks the complete input file's fixed Git blob before parsing.

Actual execution: connector-fetched original JSON was parsed in an isolated JavaScript V8 runtime and passed to the independent `audit` function. This is an internal nonblind cross-language calculation. No random seed is used. All 90 worlds and all 810 count cells passed; maximum absolute numerical logloss discrepancy across the 90 worlds was `3.3306690738754696e-16`. Six exact aggregate fields were independently checked per world, for 540 world-level aggregate comparisons. The 15 fixed illustrative worlds were checked for full content equality.

Thirteen isolated mutations were actually executed against copies of the full historical JSON, and all were rejected: duplicate world, duplicate prior world, source PMF, posterior mean, posterior variance, posterior CDF, coverage, numeric logloss, illustrative record, E2 evidence upgrade, missing count row, prior grid, and root verification flag. An earlier in-run draft omitted full illustrative-record comparison; that deficiency was detected before final acceptance, the checker was revised, and the final 13 controls were rerun successfully. Original archived data and protocols were untouched.

## Historical CI and limits

Historical GitHub Actions run `39555471118` completed successfully on 2026-10-21. Three jobs report success: Python 3.11 Beta conjugate/CDF tests, Python 3.12 Beta conjugate/CDF tests, and full frozen posterior evaluation/archive. These are historical CI receipts. This run did not trigger any new Actions. The new JavaScript file's standalone Node CLI was not executed against a native complete repository checkout in this environment. The R177 source code was not reexecuted here. Historical CI, connector source identity, and the independent V8 mathematical check are separate evidence types.

The finding supports the archived **bounded artificial E1** posterior mathematics and source-PMF construction. It does not establish real-data Bayesian calibration, general Bayesian inference validity, blind independent validation, external-team reproduction, or E2/E3. The 08-003 original239 itemwise status remains PARTIAL until its source scope and acceptance criteria are formally reviewed. No queue entry is silently closed.

## A data scout, bounded quick check

Rechecked original English publisher page for Romero and Rosokha (2023), *Mixed Strategies in the Indefinitely Repeated Prisoner's Dilemma*, DOI 10.3982/ECTA17482. Publisher reports 158 participants, 124 passing the comprehension quiz, six main-treatment sessions, 60 supergames per session, and direct-response/nonbinding/locked-response stages. Publisher lists a 197 MB data-and-programs ZIP. Original data bytes, file hash, reuse license, subject/group/round fields and R073 frozen-protocol compatibility remain UNVERIFIED. No download or E2 scoring occurred. This is a candidate for separately frozen strategy-elicitation work, not an admitted R073 independent validation set.

## Operations and next gate

Observed v7.8 index blob `36f24235901172642c46853298aebb421f1a3552`, pending queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`; pending rows 154 (P0 27, P1 82, P2 45). Net closed this run: zero. Codex PR #1 and #3 remained open and unmerged when checked; no work duplicated from their R257 S53 engineering path. R333..R340 composite production-caller and real native repository checks remain open P0 risks.

CI for this new audit: NOT_RUN. No new paid services, purchased datasets, metered APIs, or Actions were initiated. Actual GitHub billing and remaining free quota were not independently inspected. Next action: evaluate whether R179 can receive a formally bounded itemwise original239 decision after primary-literature scope review; separately prioritize the R333..R340 mandatory composite-caller defect and real native negative controls. Preserve R073 and PESEN v0.1 frozen. No classification, fusion, or decision product work.

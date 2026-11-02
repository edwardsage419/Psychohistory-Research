# R127 original239 05-003: original Table 2 second visual pass and balanced-error counterexample

track: R+B; A scout bounded
subflow: original239 itemwise primary-source and scientific receipt review
run_date_utc: 2026-11-02T21:40Z
target_key: (R+B,original239-05-003/R127,R127-2026-10-20-frozen,1990-AER-Table2-source-concordance-and-balanced-transcription-error)
observed_main_before_write: 684a413507fa53a5524c3240fc6252bddd05ff9d
status: COMPLETE_BOUNDED_SAME_AGENT_NONBLIND_SECOND_VISUAL_PASS; FORMAL_QUEUE_PARTIAL
new_R_E2: 0
new_R_E3: 0
external_independent_replication: NOT_RUN
CI: NOT_RUN
account_billing_and_Actions_free_quota: NOT_VERIFIED

## 1. Fixed primary source, frozen boundary and prior evidence

Original source: Van Huyck, Battalio and Beil (1990), *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, *American Economic Review* 80(1), pp. 234 to 248. Original published scan hosted at https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf . On 2026-11-03 Asia/Singapore, directly visually reread PDF image page indexes 6 and 7 (printed pp.240 and 241), Table 2, seven experiments, ten periods, seven effort categories. This was visual inspection; no OCR. Original PDF bytes and publisher master were not independently authenticated.

Frozen R127 protocol: `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md`, previously observed blob `4734ede5133701d622acfda76c4f9474bf660b21`. Prior source transcription: `research/validation/r127_primary_table2_70_periods_source_audit_20261103.js`, freshly fetched Git blob `aa575a803e5547afe24eabc1f232f2b539ef1709`. Prior report: `research/validation/R127_05_003_PRIMARY_1990_TABLE2_ALL_PERIODS_SOURCE_CHECK_20261102.md`, fetched Git blob `b394e696868172d85372f65d8db894ecc5cecd2d`.

## 2. Actual second visual comparison

The same research agent visually reread the two source images and manually entered a separate 7 by 7 by 10 integer matrix in a fresh JavaScript execution. This entry was then compared item by item with the freshly fetched archived JavaScript source, which was parsed separately. Exact results:

* 490/490 source-image-entered integers agreed with the archived transcription.
* Disagreements: 0.
* Seven experiment sizes [16,16,14,15,16,16,14] were checked across all ten periods; group-period sum errors: 0/70.
* Comparison used deterministic integer operations, random seed N/A. No Node CLI, GitHub Actions or independent external researcher was involved.
* The manual matrix was held only in the execution context and was not republished, to avoid redistributing the copyrighted Table 2. The matrix is therefore not a separately archived independent input; the recorded concordance is a bounded nonblind same-agent source reinspection. The agent had already viewed the prior code. This is **not** a blinded second reader or externally independent replication.

## 3. New exact counterexample against arithmetic-only source acceptance

Directly executed the archived JavaScript `audit` function, without modifying the GitHub file. Baseline returned `PASS_BOUNDED_SOURCE_TRANSCRIPTION_CONSISTENCY`. In an isolated in-memory copy of its Table 2 data, changed only experiment 1, period 2: count at effort 7 from 1 to 2, and count at effort 6 from 2 to 1. The altered table differs from the published scan in two cells. Column total remains 16, printed minimum remains 2, and frozen periods 1 and 10 remain unchanged.

**Actual mutated result:** the existing arithmetic-only `audit` also returned `PASS_BOUNDED_SOURCE_TRANSCRIPTION_CONSISTENCY`, retaining 70/70 column-sum checks, 70/70 minimum checks and 14 frozen endpoint vectors. This is a constructive counterexample showing that these three checks cannot independently authenticate intermediate-period cells. The earlier report explicitly warned of this limitation; therefore this result is an experimentally confirmed scope boundary, not evidence that the archived checker misrepresented its stated scope. The new direct image comparison checks the two altered cells against the printed source and rejects the mutation as a transcription.

## 4. Queue and related research status

Freshly fetched actual pending CSV Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`: 154 rows, P0=27, P1=82, P2=45. R127 05-003 remains `PROVISIONAL_PRIMARY_README_LINK` with `ITEMWISE_PRIMARY_SOURCE_AND_SCIENTIFIC_EVIDENCE_AUDIT_REQUIRED`. Freshly fetched original239 crosswalk Git blob `36f24235901172642c46853298aebb421f1a3552`. Neither was changed. Formal queue net reduction: 0. This reinspection improves source concordance but cannot alone settle all original model scientific acceptance or source identity.

Open Codex PR search returned 12 draft candidates at entry, including two R257 S53 PRs. No R127 second visual transcription PR was found. R272 production enforcement, R257 S53 blind-failure and R333 to R340 composite caller issues have no newly established closure in this run. R073 and PESEN v0.1 remain frozen.

## 5. A public data scout

Rechecked Kim, Jun and Nam (2026), *Data in Brief* 68:113064, DOI 10.1016/j.dib.2026.113064, open full text https://pmc.ncbi.nlm.nih.gov/articles/PMC13427532/ . The authors describe 11 triads (33 human participants), an iterated three-player Prisoner's Dilemma, 40 trials per triad, and trial-wise choice arrays of shape 40 by 3; dataset DOI 10.18112/openneuro.ds007822.v1.0.0. This improves field/time-structure evidence relative to the earlier catalogue-only scout. A published paper's CC BY license does not by itself establish the dataset's license. The dataset GitHub `LICENSE` file at https://github.com/OpenNeuroDatasets/ds007822/blob/main/LICENSE states license information was not provided with source files; some third-party catalogues say CC0. Dataset reuse permission remains UNKNOWN until authoritative dataset-version license is resolved. No participant-level files were downloaded or scored. Three-player histories do not directly meet a frozen two-player R073 mapping without an explicitly authorized adaptation. Candidate only; new eligible R073 dataset 0.

## 6. Scope, cost and next work

Evidence: internal same-agent nonblind published-source visual concordance and exact E1 arithmetic counterexample; no new predictive E2/E3, no raw individual histories, no blinded double entry, no independent team. GitHub Actions NOT_RUN, new paid operations 0, billing and Actions remaining free quota NOT_VERIFIED.

Next highest priority: obtain a complete authenticated checkout and execute the existing R272 fail-closed single-entrypoint end-to-end without activating unverified CI. If unavailable, seek a genuinely independent second human/algorithmic Table 2 transcription and formal R127 queue disposition review. Retain frozen R127, R073 and PESEN evidence unchanged.

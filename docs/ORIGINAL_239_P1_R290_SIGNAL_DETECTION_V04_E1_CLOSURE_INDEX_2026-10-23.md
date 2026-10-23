# Original 239 catalogue, P1 R290 signal detection and evidence crosswalk v0.4

Date: 2026-10-23 Asia/Taipei. Status: R290 **CLOSED_BOUNDED_E1_ARTIFICIAL_R290_SIGNAL_DETECTION_MATH**. Original 239 model candidate entries remain unchanged. The original 239-model scientific completion status remains **NOT_ESTABLISHED**; classification and fusion are deferred.

## Scientific scope (one independently scoped artificial E1 study)

Original catalogue 01-011 Signal Detection Theory (P1) -> [R290](../research/R290/README.md). Freeze before results [commit 696e86b0](https://github.com/edwardsage419/Psychohistory-Research/commit/696e86b029581d2b00dc79bdd2219c59427a7980). Core first-party source: Tanner & Swets (1954), *A decision-making theory of visual detection*, DOI https://doi.org/10.1037/h0058700. This work computes a *new discrete synthetic* detection example and does not reproduce original human experiments.

Three conditional evidence worlds x two priors x two error cost contracts yield 12 fully labeled artificial worlds and 120 original joint-probability source cells. Full likelihood Bayes model vs six ordered cutoffs, 72 ROC points and 384 arbitrary binary decision rules verified by separate model-independent audit. In CENTERED with equal prior and error costs Bayes selects evidence bins {1,2,3} and incurs risk 1/6; best single cutoff incurs 1/3. In IDENTICAL, equal signal/noise evidence distributions imply the hit and false alarm rates coincide. These are artificial E1 math results.

[Scientific report](../research/R290/R290_SCIENTIFIC_REPORT_2026-10-23.md) | [Formal scoped acceptance](../research/R290/R290_FINAL_ACCEPTANCE_STATUS.json) | [Original sources](../research/R290/R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv) | [source+result SHA256](../research/R290/R290_MACHINE_RECEIPT.json) | [independent audit](../research/catalogue_audit/independent_r290_source_audit.py).

Actual [R290 CI run39911797052](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39911797052) completed/success: 117 Python3.11 tests + 117 Python3.12 tests, third independent audit job completed/success; sources/results recovered into main at [b53ff9e2](https://github.com/edwardsage419/Psychohistory-Research/commit/b53ff9e2737c2911dce185ea14be8d45724931a8). Human E2=0, historical E3=0, original human paper replication=false.

## Metadata reconciliation, v0.3 to v0.4

| Original 239 classification | v0.3 | v0.4 | Scope |
|---|---:|---:|---|
| Candidate primary R research links | 177 | **178** | One new R290 link; does not imply all E2 validated |
| Shared earlier model mechanisms without separate R | 3 | **3** | Do not double-count |
| Earlier, bounded, scoped evidence only | 5 | **5** | Still lack one-to-one primary correspondence |
| No link found in checked metadata sets | 54 | **53** | Does not imply never studied |
| Total without confirmed primary link | 59 | **58** | P1 31, P2 27 |
| Immutable candidate catalogue | 239 | **239** | No addition, deletion or reprioritization |

[Machine-readable v0.4 239-row crosswalk](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.4_2026-10-23.json) is strictly a one-row change to [v0.3](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.3_2026-10-23.json) at 01-011. Its R290 README is bound by actual Git blob SHA1, its formal acceptance/CSV SHA256 are checked, and [remaining 58 queue](ORIGINAL_239_PENDING_58_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv) equals the previous [59 queue](ORIGINAL_239_PENDING_59_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv) minus precisely 01-011. No previous catalogue row is silently promoted.

[Independent complete v0.4 auditing code](../research/catalogue_audit/verify_p1_r290_crosswalk_v0_4.py) executes 13 true checks on both Python 3.11 and 3.12. [GitHub Actions run39911994710](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39911994710) completed/success for three jobs (two Python model-to-source metadata audits, one standalone third-party audit of the original R290 sources). **Catalogue evidence consistency and scientific model validity are explicitly separate claims.**

## Next bounded priority

Remaining first unresolved P1 is 01-013 Theory of Reasoned Action, followed by 01-014 Theory of Planned Behavior and 01-016 Schwartz Basic Human Values. Fishbein & Ajzen (1975) *Belief, Attitude, Intention, and Behavior*, authors' original [online book index](https://people.umass.edu/aizen/f%26a1975.html), is the first-party source for research planning. Before assigning R291, check older R001–R064 knowledge bundles and prior R mechanism content for an already established one-to-one model. TRA and TPB must stay distinct: perceived behavioral control in TPB must not be retrospectively inserted into the older TRA study.

Continue owner-mandated ordering: finish every original R-series learning/validation task, then catalog classification, finally model fusion. R073 and PESEN v0.1 remain frozen. Avoid treating the 178 mapping links as completed real human studies, and refrain from making any claim of historical forecasting performance from R290.

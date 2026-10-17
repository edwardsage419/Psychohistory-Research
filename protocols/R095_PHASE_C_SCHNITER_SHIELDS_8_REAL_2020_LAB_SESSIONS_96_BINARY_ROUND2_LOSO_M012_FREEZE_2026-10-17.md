# R095 Phase C — 8 TRUE original independent lab session holdouts: 96 human binary round-2 cooperation outcomes

**Frozen 2026-10-17 before ANY code-based evaluation of original 2020 experimental choices**, after publisher-original MD5, SHA256 and full group roster verified in [source-only CI 39020885386](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39020885386), with **25 synthetic tests success and the actual original source verified**.

Original creators Eric Schniter and Timothy Shields (Chapman University), Zenodo version 1 `4321821` (DOI `10.5281/zenodo.4321821`), source `Fields.csv` publisher MD5 `4c30ac1861e12f46e0b9847c9d1857a7`, file **22,312 bytes**, source verified full SHA256 `0678cc3d565d3a02e4766fedff211cc37b2e0e9d373e41c391466c6f84a56f4c`. Original full actual source rosters explicitly `session` and `group` verified: **8 real lab experimental sessions**, 12 different human participants per true session, 6 genuine fixed matched two-player groups per session, 96 distinct original participant identifiers total. Each actual 96 participates rounds 1 AND 2, 12 persons in exactly ONE original session also completed round3; total original actor-round rows **204 (96+96+12)**. Nobody merged/repeated between sessions, no source gender/age/PANAS/face/image read. **Source discovery preview displayed some source action row content prior to freeze**; therefore this is not full outcome-blinded pre-registration, but the fixed M0/M1/M2 were already used in R089–R094 and not selected using R095's losses. This limitation shall persist as an explicit scientific qualification.

## Immutable primary score and actual whole-session heldout group

Use only round t=2, source `option` action exactly `split` (code 1, cooperate) or `take all` (code0, defect), whitespace and case normalized. No third-round primary score or training; no `other_split` as predictive feature; optional source validation `other_split` should match real opposite partner action for each session×group×round 1 and 2, and be literal 0 or1; any mismatch FAIL CLOSED whole dataset. Require same 8 actual source sessions and 12 distinct participants each, same 48 fixed pairs and exact SHA; require original `option` is always recognized for rounds1&2 (any missing or other value FAIL CLOSED whole original, no subject deletion). Original 96 rows for each first two rounds.

For each target original person i in true experimental session S:
- `Y_{i,2}` person's second-round observed cooperation 0/1;
- `M0^{−S}` arithmetic mean of actual *all 84 participants from seven other ORIGINAL LAB SESSIONS* second-round actual cooperate 0/1. Target's entire S, BOTH rounds, including 12 other people, never enters training. Identical M0 for all 12 people in target S. **Cross-session original full-session holdout**, not chronological forward-time trial prediction.
- `M1_i` target person's first-round own observed cooperation 0/1; allowed because target's previous action is known at target prediction-time, but this is not “pure session holdout with zero target prior behavior”: distinction essential.
- `M2_i=(M0^{−S}+M1_i)/2` fixed 0.5, no fitted/tuned parameters.
- Binary Brier `(M_k-Y_{i,2})²` for ALL 96 humans, same target each model. Pairwise improvement M0−M1 and M0−M2 means averaged over true experimental session (12 persons each); report all 8 session gains via anonymous histogram/min/max and positive vs negative vs zero session counts, NOT 96 independent session claims. A source-reconstructed group pair action consistency audit is separate descriptive quality gate and must not be used to fit models.
- Complete-sample M0 baseline computed from others in target experiment. Thus all 84 training humans of other 7 sessions share independent experiment time but are no earlier calendar cohorts. Its score is genuine original-session-heldout **cross-session transfer** not a prospective E3 experiment. The target study is Friend-or-Foe binary split vs take all, NOT an identical game to R089 6-person public goods global investment or R094 social network wealth visibility.
- 8 true independent lab sessions, not 96 independent experiment units. No nominal individual-level p-values or confidence intervals. 8-session two-sided exact sign test may be computed **only** if separately frozen exact formula and zero-tie treatment before outcomes; otherwise report descriptive 8-unit signs and all true reversals.

## Quality and archive contracts

Original source was published with participant age, language, sex, mood and videos. Do not access demographic/MEDIA/restricted `MappingFile.csv`, never upload original Fields.csv, IDs, session or group labels, any unique participant trajectories or original partner pairs to GitHub. Keep only anonymous full-dataset MSE/gains and unsigned session count sign plus anonymized full 8 ordered numeric session gain vector? To avoid exact ID reconstruction, export **sorted values only** not indexed by true session. Also summary first/second-round cooperation only whole cohort, no detailed group trace; source raw identity verified with MD5 and SHA every run.
 
Synthetic tests ≥24 covering source official digest, 96 IDs×two rounds×8 true sessions, stable original 48 pairs, round3 excluded, option code eligibility, other_split consistency, M0 excludes ALL heldout original session, M1 exact prior, M2 exact half, positive and negative stable/alternating scenarios, full session sign positivity/negativity, no source ID/participant demographic output. First actual real run only after synthetic pass, then independent second full Zenodo refetch and aggregate JSON SHA byte-for-byte equality committed to Git, formal A01–A06 qualification.

PESEN v0.1=FROZEN; R095 R089/R090/R091/R093/R094 results and limits remain unchanged.

R095_SOURCE_ORIGINAL_REAL_INDEPENDENT_SESSIONS=8
R095_BINARY_ROUND2_TARGET_COUNT=96
R095_TRUE_SESSION_LOSO_CONTRACT_FROZEN_BEFORE_MACHINE_SCORING=YES
R095_FULLY_BLINDED_TO_SOURCE_PREVIEW=NO
R095_REAL_MODEL_SCORE=NOT_YET_CALCULATED

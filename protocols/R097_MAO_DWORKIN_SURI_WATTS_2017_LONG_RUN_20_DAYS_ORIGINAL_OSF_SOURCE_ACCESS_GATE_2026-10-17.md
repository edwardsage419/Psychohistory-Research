# R097 Phase A — independent Microsoft Research 2017 longitudinal IPD humans, OSF source access + original experiment code gate

**Frozen 2026-10-17 before reading original 2017 human cooperation microdata or creating model predictions.** New genuinely independent academic experimental team **Andrew Mao, Lili Dworkin, Siddharth Suri, Duncan J Watts**; original [Nature Communications (2017) DOI 10.1038/ncomms13800](https://doi.org/10.1038/ncomms13800) *Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*. Original article reports 94 analyzed human volunteers in a persistent population, up to **400 independent 10-round paired PD games**, played **20 days**, 20 games/day; total theoretical possible 4000 individual decisions each but attrition/uneven participation may reduce actual source observations. Real behavioral data publicly stated to be stored at **OSF https://osf.io/64z8u/** (original source node **64z8u**). Original experiment implementation code at **https://github.com/TurkServer/long-run-cooperation** (default master; observed source code Git tree `4d8ed83e7745e1ffe82ce9403064e3558fabfa6f`), no verified original CSV in the public code repository. Primary study original exact observed rows, session IDs, game partner identities and coding are NOT YET VERIFIED.

Scientific independence distinctions before source work:
- Independent from R096 author team and experiment; **YES independent experiment**, but the same 94 people may participate on 20 separate days. Thus 20 days are NOT 20 independent participant populations, cannot claim 20-session leave-one-experiment-out with independent participants.
- Original author 10-round game repeats up to 400 times with new opponents between games; **within a 10-round game partner remains fixed**, across games partner is randomly reassigned; cannot reinterpret 20×20 games as 400 entirely independent people/experiments. Additional 20-day dependence matters.
- Possible third-party automatic play if original platform permits automatic strategies unknown before verified logs; do not presume all recorded actions autonomous if no source audit.
- Published paper's cooperation curves are previously public, so any source-model scoring is retrospective E2 and definitely NOT outcome-blind preregistration or E3; no invented statistical significance from 400 games.

## Source access and eligible metadata-only protocol

Use only official publisher OSF exact project node endpoints:
`https://api.osf.io/v2/nodes/64z8u/`;
`https://api.osf.io/v2/nodes/64z8u/files/osfstorage/?page[size]=100`.
The OSF website page `https://osf.io/64z8u/` was not accessible to web reader (503); OSF JSON API accessibility must be tested on independent GitHub Actions runner. Follow links.next only if HTTPS host **api.osf.io**, OSF node **64z8u** provenance retained. For a listed original file, collect **only safe names and file sizes and OSF file IDs, MD5/SHA publisher metadata**; no direct original behavior file download or decode yet. File names must match ASCII basename whitelist `[A-Za-z0-9_. -]{1,90}`; otherwise redact; source may have folders or many file IDs. No original file contents, images, demographic records, subject-level logs or videos accessed this phase. Do not try network alternate mirrors without a separately frozen provenance protocol.
 
Discovery audit outputs coarse anonymous files metadata only; allow file names for original scientific data if generic, but never expose participant-specific naming, full original file URL with private tokens, per-person IDs or source microdata. If file listing fails from both API calls, issue access blocker not guessed file names; do not invent source rows or claimed successes. An OSF directory alone is insufficient for source dataset admission. After source metadata and codebook inspected in next frozen phase, require whole-file original cryptographic SHA256/MD5 and minimally distinct period/day, within-day/game, participant, round, action and opponent dimensions before any M0/M1/M2. Day is repeated measurements of same humans; consider **whole-person holdout** separately from **leave-one-day-out**, not interchangeable.

If original source unavailable, mark `R097=SOURCE_ACCESS_BLOCKED`; preserve negative access receipts and continue to another independent lab dataset in future research. Original 2017 model remains strict M0 same nonheldout cohort round index, M1 prior action *within same fixed partner 10round game*, M2 exact 50:50, Brier, but cannot freeze detailed score until eligible source context and study/codebook verified. R095 original 8 session M1 negative, R096 100 round FP vs SP heterogeneity retained, PESEN v0.1 FROZEN.

R097_PHASE_A_BEFORE_ANY_ORIGINAL_HUMAN_ACTION=FROZEN
R097_REAL_OSF_DATA_SOURCE_IDENTITY=NOT_YET_ESTABLISHED
R097_MULTIDAY_INDEPENDENT_HUMAN_SESSION_LOSO=NOT_ESTABLISHED
R097_NEW_HUMAN_E2_PREDICTIONS_SCORED=NO

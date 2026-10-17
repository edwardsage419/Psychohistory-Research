# R095 Phase A — original 2020 Schniter/Shields true session ID and stable matched-pair source gate

2026-10-17. Source research candidate is **Schniter, Eric; Shields, Timothy**, first-party `Participant Faces from a Repeated Prisoner's Dilemma`, Chapman University experiment, [Zenodo v1 record 4321821](https://zenodo.org/records/4321821), DOI **10.5281/zenodo.4321821**. The original lab ran 96 human subjects with an anonymous stable two-person match, using Friend-or-Foe binary action (Split vs Take All), mostly two rounds and sometimes three. Its original data file `Fields.csv` (22.3 kB) has publisher MD5 **4c30ac1861e12f46e0b9847c9d1857a7** and official codebook `Fields_codebook.csv` MD5 **832565bb440c08c328ac0db0f16a0aac** (1.5 kB). Direct fixed version URL `https://zenodo.org/records/4321821/files/Fields.csv?download=1` and codebook counterpart on same record, source absolute cap 100000 bytes, strict official MD5 then record full SHA256. No video, images, media file, identifiable demographic micro-record or original detailed rows in own public GitHub. Original `MappingFile.csv` is restricted and must **NEVER** be accessed or requested.

First-party original codebook explicitly defines columns `ID,round,option,session,group,other_split`. The true `session` provides *observed original independent lab sessions*; `group` identifies the matched pair within session. `option` means actor's binary Split vs Take All, `other_split` partner's realized game action (0 Take All,1 Split). No fabricated `session` inference needed as in R094.

**Evidence-contamination disclosure**: the publisher web Fields.csv preview was opened during R095 discovery and **part of actual choice rows were incidentally made visible** even though no formal model score was calculated, so it would be wrong to claim full blinded pre-outcome registration. This protocol is frozen **before computational source metadata audit and before any model scoring** but some publicly visible choices had been displayed. Model functional form M0/M1/M2, previously fixed across R089–R094, cannot be newly optimized. We will preserve this limitation in any science report.

## Phase A — genuine first-party file and source roster, no score

Read source byte only after official original MD5 and its SHA256, validate exact source header from official codebook; only process `ID,round,session,group` and source field count: unique participant IDs, total actor-round rows, source true number of different session codes, per-session number of unique source people, stable participant-to-session/group mapping, group 2-person membership, original rounds 1 and2 present for everyone, optional t3 only in complete true groups; all original duplicated ID×round fail closed. No original `option`, `other_split`, PANAS, age, language, sex or other source value accessed/extracted/logged. Anonymize all ID/session/group outputs: only session-level aggregate **number of humans** and **number of rounds**, and sorted histogram of numbers if any grouping smaller than 4 participants, avoid releasing original session codes or group IDs. Do not use original source value in public file names/hashes.

## Conditional Phase C freeze — no outcome scoring until after A roster confirmation

If ≥3 genuine source independent lab sessions and all source session rounds1/2 complete, freeze three unchanged models per original human source binary t=2 only:
- `y_{i,2}=1` if real `option` exactly source `split`, 0 if exactly `take all` (string case/whitespace canonical fixed).
- `M0` mean **other original entire sessions'** t=2 actions, excluding all people from target's session and all of target's own records. Because all candidate tests originate round2, session-heldout baseline truly untouched target session in training, but may not be forward-in-time across sessions.
- `M1` target's own previous first-round binary action; `M2=(M0+M1)/2` fixed. Same heldout binary Brier `(p-y)^2`, original t=2 only, at most 96 genuine source choices. Original third-round persons excluded for primary because no guarantee other sessions independently have t3; 3rd round not used for any training or scoring in this primary.
- Report strict per-session paired gain signs and all true sessions; never treat 96 individuals as independent experimental sessions. Since t=2 no partner historical variable, this is one-step binary own history transfer, not R073 self+opponent model or repeated group mean. No model fitting/tuning, no causality, no E3 future study.
- Stage A source sizes/session universe can imply fewer sessions and no scientific power; lack of session independent comparators fails source eligibility.

A synthetic test suite first, then real official Zenodo Actions source audit, then separate commit of C scoring protocol **before any program scores full genuine source**. At A or C unexpected original source -> fail closed and archive negative evidence. PESEN v0.1 FROZEN. R089+ R090− R091+ R093+ R094 visibility mixed remain unchanged.

R095_ORIGINAL_SOURCE_METADATA_PHASE_A=FROZEN
R095_REAL_SESSION_HELDOUT_E2=NOT_COMPUTED
R095_ORIGINAL_SOURCE_BLIND_PREVIEW=NOT_FULLY_BLIND

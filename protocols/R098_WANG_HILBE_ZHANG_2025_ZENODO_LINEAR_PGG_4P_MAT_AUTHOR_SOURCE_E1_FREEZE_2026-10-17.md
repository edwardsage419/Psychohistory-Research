# R098 Phase A: first-party 2025 four-person linear public-goods dataset — immutable source-only admission

Date 2026-10-17. **Frozen before any original source MAT read or human outcome inspection**.

New primary research team: Xiaomin Wang, Christian Hilbe, Boyu Zhang, *The dynamics of cooperation in asymmetric public goods games*, original-author public data and software Zenodo **v2** `10.5281/zenodo.16918146`, published 2025-08-21, [record](https://zenodo.org/records/16918146). Selected first-party source **`LinearPGG_4P_ExperimentalData.mat`**, official Zenodo publisher-listed **MD5 `42153952f8e6614d09c2d903fd97af62`**, publisher displayed size ~22.3 kB. Exact source URL only: `https://zenodo.org/records/16918146/files/LinearPGG_4P_ExperimentalData.mat?download=1`, HTTPS host must remain `zenodo.org` and path exact, maximum 100,000 bytes. After publisher MD5 passes, independently calculate FULL exact SHA256; subsequent stages must pin that hash.

Documented experiment: three four-person linear public good conditions **FE** (full equality, reported 100 human participants), **AI** (aligned inequality, 104), **MI** (misaligned inequality, 108); twenty rounds each session and **two sessions conducted sequentially within each treatment**. The same original humans play both sessions, with partner reshuffling; **different per-session GlobalPlayerID does not imply different original human being**. Groups of exactly four, `GroupID` globally unique across treatment/session; source public page describes `Treatment,Session,GroupID,PlayerID,GlobalPlayerID,Round,Contribution`. Published reported participant numbers are NOT yet verified from full MAT bytes. This is genuinely a new original experiment/laboratory versus 2017 Mao and 2022 Montero, **not equivalent behavior to R096's C/D binary Prisoner's Dilemma**.

A source-authenticity phase shall **not inspect even a single human contribution number**. First:
1. Fetch whole original MAT strictly publisher URL and verify official original MD5 as above, source cap, exact SHA256, and MAT version/type with SciPy in disposable CI (no microdata uploaded).
2. List ONLY top-level MAT variable names, shapes, dtypes, array dimensionalities and total bytes, and a BOOLEAN whether expected source field-name labels exist. Never print `Treatment` actual data values, `Session`/GroupID or any source individual, action/contribution values.
3. No gender/survey/other experimental workbooks or camera/person identities accessed.
4. No synthetic scores misrepresented as genuine human work. Source admission blocked if MD5, file schema, or data access fails.
5. One source-only synthetic test suite validates publisher checksum strict gate, URL pin and content privacy; one GitHub Actions actual publisher complete file audit.

A separate Phase B freeze will specify safe metadata `Treatment,Session,GroupID,PlayerID,GlobalPlayerID,Round` audit and **the actual distinction between source sessions and independently recruited subjects** before any contribution values are read. Phase C group holdout model would remain M0 other same-treatment + same-session groups' contemporaneous mean contribution fraction, M1 own target group previous round and M2 strict half, 20-round targets; if numeric contribution upper bounds differ by treatment/role, **must independently freeze valid normalization based on original experimental instructions not observed fit** before behavior scoring. Given repeated original people between Session 1 and Session 2, M0 must not pool sessions if claiming held-out unseen humans. One-session exclusion is NOT independent experimental-session holdout here.

Original published v2 file must be distinguished from other Zenodo v1 and other game types (`ThresholdPGG_4P`, two-player experiments, survey MATs). Source original raw file SHALL NOT be committed to project's public GitHub, only authenticated safe source receipt, protocols and source-only code. Any later A01–A06 result labels science-only according to actual source success; `R098_E3` not established. PESEN v0.1 remains frozen.

R098_PHASE_A_FROZEN_BEFORE_ORIGINAL_SOURCE_BYTES=YES
R098_SOURCE_SHA256=NOT_YET_VERIFIED
R098_REAL_HUMAN_E2_PREDICTIONS=ZERO
R098_INDEPENDENT_RECRUITED_SESSION_REPLICATION=NO

# R098 Phase A5 — independent non-decoding MATLAB 5 original variable directory metadata parser

2026-10-17. Authentic publisher file byte identity now **actually established** at [CI39025847448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025847448): original Zenodo v2 `LinearPGG_4P_ExperimentalData.mat` 22,347 bytes, official MD5 `42153952f8e6614d09c2d903fd97af62`, full SHA256 `dcdd23e709ce1c17fadddffb84d07b9cf2f37a0a206e4665317aed31fd4e790b`; 24 synthetic PASS. Actual original data `scipy.io.whosmat` failed source directory metadata with `TypeError`; **no human source row or contribution read/scored**. This preserves earlier three source failures and reports byte-validity NOT data-readability.

Freeze before next original source access: a pure stdlib MATLAB Level-5 **directory-only TLV tag parser** independent of SciPy:
1. Same exact publisher file + known SHA, not just MD5; total byte cap unchanged, no different source.
2. Read only MAT header [0..128], external TLV tags and the **first three metadata-only inner MI elements of each miMATRIX**: array flags, integer shape dimensions, variable name. DO NOT read/interpret human numeric data elements or actual actor/group/contribution identifiers, no `loadmat`, no row values.
3. Accept only little-endian MATLAB5 marker `IM` and version 0x0100, miMATRIX type14, optional miCOMPRESSED type15 with bounded zlib decompression max1MB; enforce exact element sizes/offsets, at most100 top-level objects. No arbitrary eval, file write or untrusted path.
4. Verify metadata-only variable names safe `[A-Za-z_][A-Za-z0-9_]{0,70}`, shapes integer 0..1000000 with at most5 dims, MATLAB class 1..18. Export only name/dims/named original type `struct/cell/double/...`, number of variables, source SHA and format; **no first party contribution data loaded or inspected**.
5. At least20 additional pure synthetic including scipy.savemat compressed and uncompressed, invalid endianness, tag truncation, non-MAT source, vector shapes, no data leakage and original MD5 mismatch. On source unexpected type reject.
6. Real CI first synthetic, then re-fetch verified SHA and run metadata-only parser. Commit only safe anonymized source receipt; do not claim E2 or repeated sessions independent recruitment.

If successful, Phase B must *separately freeze* decoding of the original structure's **nonbehavioral** `Treatment,Session,GroupID,PlayerID,GlobalPlayerID,Round` metadata, and subsequently Phase C freeze group-level score. The 2025 four-person linear public good contains same human subjects in both sequential sessions; do not conduct naive independent 2-session recruitment validation.

R098_ORIGINAL_MAT_FULL_BYTE_SOURCE_E1=ESTABLISHED
R098_UNREADABLE_BY_SCIPY_WHO_SMAT=TRUE
R098_NEW_TLV_SOURCE_DIRECTORY_E1=NOT_YET_EXECUTED
R098_REAL_HUMAN_MODEL_E2=ZERO
PESEN_v0.1=FROZEN

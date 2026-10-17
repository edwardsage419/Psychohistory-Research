# R098 Phase A5b — original source not accessed; correct compressed miCOMPRESSED alignment in synthetic TLV

2026-10-17. [CI run39026065160](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39026065160) **49 synthetic** source/metadata tests attempted, **47 PASS and 2 ERROR** in SciPy-generated `savemat(...,do_compression=True)` metadata-only fixtures; actual authentic 2025 Zenodo source test **SKIPPED**, so no new source values read. Failure `R098A5_MAT_TAG_LENGTH_OR_TYPE_INVALID` occurs on the second outer compressed miCOMPRESSED block because SciPy emits compressed top-level objects contiguous, without optional 8-byte padding between blocks.

Freeze only this narrow source-format accommodation: after a valid miCOMPRESSED outer tag and bounded zlib `eof`, advance to `offset+n` (next physical raw byte), not aligned `offset+ceil8(n)`. Keep legacy uncompressed miMATRIX 8-byte alignment and all bounds. Do not loosen known SHA256, publisher fullfile MD5, MAT version, number of variables, metadata-only first 3 tags, source ID, or individual/real contribution blindness. All previous 49 synthetic tests must pass before original file is read.

PESEN v0.1 FROZEN; R098 E2 no real scores.

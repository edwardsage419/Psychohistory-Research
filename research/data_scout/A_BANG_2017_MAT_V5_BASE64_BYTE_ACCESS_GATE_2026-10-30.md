# A: Bang et al. 2017 actual binary-byte access and MAT container gate

UTC audit date: 2026-10-29. Source: https://github.com/danbang/article-confidence-matching ; original publication https://doi.org/10.1038/s41562-017-0117 . No Chinese-language source used.

This follow-up adds a real byte-level access result to the previous A_BANG_2017 reports. The GitHub connector was asked to read the two public binary files using its explicit base64 encoding. The returned strings were decoded in memory by a separate JavaScript base64 decoder, and their MAT v5 outer headers were inspected without interpreting participant arrays.

| Source path at master | Git blob SHA1 | Decoded bytes | MAT v5 endian marker | First element type | First compressed element length |
| --- | --- | ---: | --- | ---: | ---: |
| Data/exp2-S.mat | fe5138ffc6625a3eda042cef133b9167ce0d7bac | 41674 | IM (little endian) | 15 (miCOMPRESSED) | 41538 |
| Data/exp3-S.mat | 604b3605a799a1b316c2e1fb7c0ef10b89f42ae8 | 80270 | IM (little endian) | 15 (miCOMPRESSED) | 80134 |

Both files begin with the exact ASCII signature `MATLAB 5.0 MAT-file`. The outer first element begins at offset 128. The binary data were read through the repository connector, without paid service, credentials, or re-publication. The Git blob IDs are content identities supplied by GitHub; this audit did not independently recalculate their Git SHA1.

The author README blob 0515aaa51c88f2f10c63e2658ec8d52df95c4793 documents 384 social trials for experiment 2 and 384 social trials for experiment 3, and lists group, sbjID, trial, sbjChoice, sbjConfidence, otherChoice, otherConfidence, dyadChoice and accuracy fields. This is author-described schema, not independently verified matrix dimensions. LICENSE blob 6c4b7f2dabab291c71346be66ff73ac8dea08db4 contains the MIT license; README calls the data anonymized and permissively licensed.

Access status: `BINARY_BYTES_OBTAINED`. Decode status: `COMPRESSED_MAT_ARRAYS_NOT_PARSED`. No individual trial count, subject count, missingness, partner identity continuity, or behavioral value distribution has been verified. A future free local SciPy or equivalent MAT v5 decompressor could check the arrays once the bytes are accessible in that runtime. The present GitHub connector cannot hand its returned binary bytes directly to the local Python runtime in this execution, so no unsupported reconstruction is claimed.

Replay suitability: potentially useful for longitudinal social perception and confidence research. Not eligible as a direct R073 frozen two-person 100-round prisoner's dilemma independent replication, because task structure differs. No E2 prediction was executed. No private data accessed. No paid API, cloud compute, data purchase or GitHub Actions dispatched.

Next: decode actual MAT arrays using a free authorized byte transport, then audit participant/trial keys, chronology, partner pairing, missingness, and permitted reuse. Keep this source separate from R073 frozen scoring.

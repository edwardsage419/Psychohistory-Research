# R275 S71: noisy pair observation and mechanism identification

Date 2026-10-30. Protocol committed before new numeric scores: 8c2964149055b7fa824bd9b10446ffd1e0613768. Original R275 prescore commit c29ff305375f8510137f3a50bf20005fd695768d and bounded E1 acceptance are unchanged.

## Research question
Under four observed pairs, how much can independent bit-flip measurement noise in the B coordinate erode MAP identification of the original three mechanisms? Original IID/COPY/FLIP pair generator, equal prior, exact tie rule and four-pair budget are preserved. The noise grid {0,1/8,1/4,1/2} was frozen before new scores. The earlier noiseless 23/24 result was already known, so the work is internally nonblind.

## Exact results
| flip probability epsilon | equal-prior average MAP accuracy | IID conditional accuracy | COPY conditional accuracy | FLIP conditional accuracy |
|---|---|---|---|---|
| 0 | 23/24 | 7/8 | 1 | 1 |
| 1/8 | 4541/6144 | 3/8 | 3773/4096 | 3773/4096 |
| 1/4 | 79/128 | 3/8 | 189/256 | 189/256 |
| 1/2 | 1/3 | 1 | 0 | 0 |

At epsilon=1/8, 4541/6144 is approximately 73.91%. At epsilon=1/4, 79/128=61.71875%. With epsilon=1/2 all three observed pair distributions coincide; the frozen tie rule selects IID for all observations. The average is 1/3 despite IID conditional accuracy of 1.

The four-pair relation count K is sufficient for this specific artificial classification problem. For epsilon=0, MAP labels for K=0..4 are FLIP, IID, IID, IID, COPY. At epsilon=1/8 and 1/4 they are FLIP, FLIP, IID, COPY, COPY. At epsilon=1/2 all labels are IID. This is a finite example of measurement noise destroying mechanism discrimination even though observed A marginals remain exactly identical.

## Executed methods and controls
R enumerator executed in V8: 4 epsilon settings × 3 true mechanisms × 256 observed four-pair strings = 3072 probability-labelled source rows including zero-probability placeholders. BigInt integer likelihood numerators and exact rational posteriors; normalization and original endpoint controls passed. Persisted CSV and JSON are new files. B independent Python standard-library combinatorial route was executed locally on separately generated equivalent full-source CSV/JSON: 3072 unique source keys, 36 confusion cells, 4 aggregate MAP values checked; result PASS. The B script has been archived, but byte-for-byte execution against the GitHub-persisted files and its exact archived blob has not yet been performed. Native Node execution and GitHub CI are NOT_RUN.

## Evidence and limitations
A01 PASS bounded artificial question; A02 PASS original R275 protocol and versioned new noise protocol; A03 PARTIAL native archived replay; A04 PASS endpoints and explicit tie behavior; A05 PASS E1-only nonblind statement; A06 PARTIAL external and CI gates remain open. This does not alter the original R275 formal bounded acceptance. No real behavioral or causal inference. New E2=0; new E3=0; external independent team=0; R073 and PESEN v0.1 frozen. No new paid service or Actions requested.

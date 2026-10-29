# B track: R267 S63 independent primitive-source tail risk audit

UTC date: 2026-10-29. Key: `(B,R267,S63,independent-primitive-tail-PMF)`. Prior knowledge: original R267 report and baseline means/variances were already read. Blindness: `NON_BLIND_INTERNAL`.

## Source and prescore

Original R267 results Git blob `310aa78c2e903cf8505856921c832bf6c73b04ca`; frozen S63 protocol commit `6b086febb09dcf5da854bad0e2e5cc256b2ca2a7`, protocol blob `fb154ad62cd7a725af3db855eb54f5071800e004`.

Persisted S63 R receipt blob `fde0bb6ca407c3633127c2a179a31e058b1697f3`. R program blob `9acb90a028ca72ae36eb0d1b0cbfd237d67941aa`. New independent B Python program blob `07ef871bc5ca2f5edd52b319d2afe02566a06267`.

## Actual independent execution

A separate V8 BigInt rational oracle independently encoded the nine frozen functions, enumerated every primitive IID three-gridpoint triple and every independent LHS pair of three-element permutations. This is `9*(729+36)=6885` primitive artificial design types. It did not call R267 source enumeration code, R267 archived PMFs, or the new R route algorithm. The original R267 source definitions were previously known, so the test is internal method independence.

The oracle recomputed all 18 world/design rows, including true mean, variance, both prespecified strict tail probabilities, expected absolute error and maximum absolute error. It compared 108 exact numeric fields, 18 source counts, 9 paired rankings and all 36 tail probabilities against the *persisted remote JSON receipt*. All matched exactly. A separate Python standard-library full primitive enumeration also produced all 18 exact rows, with the same 36 tail probabilities and absolute-error metrics.

The V8 strict receipt gate rejected six deliberately modified copies: duplicate world/design coverage, missing row, spurious real-human E2 count, tampered tail probability, E2 evidence upgrade and modified threshold. Result: `6/6 REJECTED`. These are executed in-memory mutation checks; the archived Python B CLI includes equivalent controls but has not yet been natively executed from its remote file.

## Key scientific check

In `CENTERED_INTERACTION`, IID versus LHS:
* Variance: `4/27` versus `2/9`.
* `P(|error|>1/3)`: `136/729` versus `1/3`; IID smaller.
* `P(|error|>2/3)`: `16/729` versus `0`; LHS smaller.

The strict ranking reversal is an exact finite-probability statement. Three paired worlds change ranking across thresholds when ties are included; only this world strictly reverses direction. The second tolerance is not selected post hoc; both were fixed before S63 results.

## Limits and next gate

B verification status `PASS_INTERNAL_EXACT_V8_AND_PYTHON_ORACLE`. Native execution of the two *archived* Python CLI entrypoints and byte-for-byte source CSV replay: `NOT_RUN`. External team independent replication: `0`. This audit does not establish empirical coverage, calibration, human causal mechanisms, or original paper replication. E1 only; new E2=0, new E3=0. R073 and PESEN v0.1 remain frozen. No GitHub Actions triggered or billed.

Next: execute both archived Python programs with exact fetched input bytes in a clean checkout and retain stdout, exit codes, input blob SHA and mutation logs. Treat any mismatch as an open gate, without modifying frozen original artifacts.

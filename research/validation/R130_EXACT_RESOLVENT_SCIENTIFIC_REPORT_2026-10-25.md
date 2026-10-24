# R130 independent exact state-resolvent scientific report

Date: 2026-10-25. Original239 item 05-006. Verdict: PASS_BOUNDED_INTERNAL_EXACT_STATE_RESOLVENT_E1.

## Provenance and prospective protocol

The new third-method protocol research/validation/R130_THIRD_METHOD_EXACT_RESOLVENT_PROTOCOL_FREEZE_2026-10-25.md was committed first at 8e50637f6da6747092d64eef39ab25b0f70db169. Frozen protocol Git blob 790f4b31494b4e56bb53bcc5d279a408064cceeb. The original R130 code, test and first-hand source report were reused unchanged. Original source Git blob acc82d15b23de015ca8e448cf622b077a4e8e6cd. The first-hand scientific sources are Axelrod and Hamilton (1981), Science DOI 10.1126/science.7466396, and Nowak and Sigmund (1993), Nature DOI 10.1038/364056a0.

## Actual third-method computation

The new source verify_r130_exact_resolvent.py independently constructs a deterministic state graph from prior realized actions and turn parity, then solves (I-wP)V=r by exact Fraction Gaussian elimination. It does not call the original strategy implementation to construct the new values. The original independent_infinite_state_cycle_value is imported only after construction for exact equality checks. There are 25 ordered strategy pairs from TFT, ALLD, ALLC, ALT_DC, WSLS and seven frozen discount factors, yielding 175 pair-discount cases and 350 scalar payoff comparisons. All matrix residuals are exactly zero; all new values equal the unchanged original cycle implementation. Two deliberately altered values are rejected.

Original-source controls at w=3/5: TFT/TFT 15/2, ALLD/TFT 13/2, ALT_DC/TFT 125/16. The ALLD payoff comparison is tied at w=1/2, and the alternating DC payoff comparison is tied at w=2/3. These are bounded pairwise comparisons; neither establishes a universal evolutionary stable strategy result.

The complete 175-row CSV has 5149 bytes, SHA256 7f9f44076ef039122e56d08b8c4d5cf5f42041cb90ee9a90b82f6b06d0a01ec3, Git blob 7332c9579bb82b474a3ea2020439de0e1c554e43. The raw CSV was generated locally before upload, and its Git blob identity was checked after the upload.

## Actual CI and scientific limitations

GitHub Actions final frozen replay https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40113779564, tested commit 69e2a21ca3f0f4aeb0e14100664d7d9b73ff68bc, completed/success. Both jobs 120930726572 and 120930727029 completed/success. Logs show the verifier ran with --verify-existing, compared the entire archived CSV byte-for-byte, printed 175 cases, 350 scalar values, two tamper controls and the pinned SHA256. Both jobs independently reran the original 65 unittest cases with OK. Earlier runs 40113684312 and 40113763950 also succeeded but the final run is the archived-byte verification gate.

Evidence is project-internal E1 synthetic finite-state mathematics. Original Axelrod tournament, original Nowak population mutation-selection simulation, real human behavior and historical events were not reproduced. No new E2 human prediction, E3 historical validation, out-of-sample calibration, confidence interval or external-team replication. Original R130, R073 and PESEN v0.1 were unchanged. No paid API, data, GPU, cloud or large runner was used. Standard Ubuntu runner on public repository is free under current GitHub documentation.

Original239 bounded E1 itemwise acceptance is justified for the precise mechanism above, leaving any broader theoretical and empirical claims open.

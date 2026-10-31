# B independent method audit: R325 S121 4116 exact weighted states

UTC 2026-10-31T22:50Z. Key (b,R325,S121_fff93b2a,nonblind_Fraction_all_row_and_mutation). Status: PASS_INTERNAL_NONBLIND_E1_EXACT; native archived Node CLI NOT_RUN; external team NOT_RUN.

Read parent R325 original README, report, code, exact JSON, original source and machine receipt. Prescore S121 protocol frozen at commit fff93b2a837d63be4047e932b1c6f66bfff9a0a7 before new outcome calculation. No import of R generator in the independent Python calculation.

Independent local Python Fraction implementation separately enumerated four fixed weight profiles, three kappa values and 343 ordered triples each. It reconstructed all 4116 CSV records and the complete JSON object with exact rational arithmetic. The resulting Git blob SHA1s were CSV `8df84f30ad1d680758aa526d3f8f05a911523bd0` (252327 bytes) and JSON `b1c4bf4d07f0479fdefb1dc22aa202b8e6526531` (6518 bytes), equal to both remote persisted Git blobs. Thus every archived byte, including row order, rational values, counts and scope labels, matched an independently implemented Python route.

The separate archived compact row checker `research/evidence_audit/b_r325_s121_row_checker.py` was actually executed against locally reconstructed copies with the same verified Git blob hashes. Normal Python and `python -O` each passed all 4116 row formula comparisons and all 12 aggregate summaries. Four live controls (CSV weight change, JSON E2 promotion, missing row, duplicate row) were rejected in both modes. The full local Fraction oracle also passed six separate live negative controls (missing row, duplicate row, weight, state/score, choice, E2 promotion) in both modes; these controls overlap in scope and must not be counted as ten distinct scientific failure classes. Both executed local scripts are internal nonblind checks. The archived compact checker is the reproducible persisted audit implementation.

Reproduce on a checked-out repository:
`python research/evidence_audit/b_r325_s121_row_checker.py --csv research/validation/R325_S121_ALL_4116_WEIGHTED_STATES.csv --json research/validation/R325_S121_EXACT_WEIGHT_RESULTS.json --selftest`
and repeat with `python -O`. The compact checker validates fixed source output blob identities and all mathematical rows; it does not independently reauthenticate original 1029-row source bytes. The primary R generator validated those source rows and fixed original Git blob through connector plus in-memory calculation.

Evidence: E1 project constructed mathematical identity only. No real data, independent participants, temporal holdout, baseline predictive comparison, empirical Brier/calibration, confidence intervals, or historical E3. The finite enumeration is exact and has no Monte Carlo uncertainty. Original R325 acceptance unchanged. PR #1 and #3 on R257 S53 remain unmerged, unrelated to this audit. No paid CI.

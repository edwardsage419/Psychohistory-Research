# B independent-method audit: R298 S94

Date 2026-10-30 UTC. Key (B,R298,S94-v1,independent full-branch exact oracle and mutations). Prescore freeze `479b96c37c53c4d5f62503f308ab2067daa26933`. This is an **internal nonblind** audit. R generator outputs were visible before B audit. It is not external laboratory replication.

## Inputs actually fetched and compared

Full GitHub persisted S94 CSV: 640 rows, 84,673 characters, blob `3d4d044817fb3b752f52f41d9e528532ca73b3ca`.
Full GitHub persisted S94 JSON: 80 worlds and 20 summaries, 97,918 characters, blob `bd908d7efd46dd69b2f07e5626d972c6e676f441`.
Original R298 64 action sources: blob `33611b20a9273754e4ed1fe800f3beab256b09cf`.

A separately written no-import JavaScript `b_r298_s94_independent_branch_oracle_20261031.js` directly reconstructs actual Q from each true scenario and predicted Q from the message or baseline cache. It checks exact fractions, each of 640 action sources, all 80 unique world probability masses/expected losses, 20 summaries and 64 original R298 decisions. The e=0 informed-planner/cache branches match the original source choices. All checks PASS in V8.

Controlled mutations tested against the full checker: duplicate source, omitted source, actual Q tamper, message probability tamper, chosen action tamper, regret tamper, aggregate summary tamper, and false E2 evidence promotion. **8 of 8 rejected**. A separate Python Fraction calculation (no R source import) reproduced 10 gamma/e paired expected regrets, including equality at e=3/4. This is exact E1 algebra, not independent human evidence.

## Scientific audit gates

Leakage: actual T is used for oracle evaluation only; predicted Q depends solely on message M for planner and baseline for cache. PASS for this frozen deterministic mechanism. Baselines: cached controller plus e=0 exact informed planner and BASELINE/BOTH negative controls PASS. Sample-outcome heldout: NOT_APPLICABLE to artificial complete enumeration. Calibration and resampling uncertainty: NOT_APPLICABLE for exact deterministic finite enumeration; cannot claim empirical calibration. Independent sample: NONE. External blind reproduction: NOT_RUN. Native Node CLI checkout: NOT_RUN. GitHub Actions: NOT_RUN pending verified no-cost runner availability. R281 S77 earlier freeze-assertion failure remains unresolved and was not modified.

A01 PASS, A02 PASS for fetched Git blob identities (full independent SHA256 computation of original bytes OPEN), A03 PASS for V8 internal oracle and mutation tests, native Node OPEN, A04 PASS for tested negative controls, A05 PASS E1-only scope, A06 PARTIAL. **B result = NONBLIND_INTERNAL_E1_PASS_WITH_OPEN_NATIVE_AND_EXTERNAL_GATES.** Original R298 scoped acceptance unchanged. R073 and PESEN v0.1 remain FROZEN.

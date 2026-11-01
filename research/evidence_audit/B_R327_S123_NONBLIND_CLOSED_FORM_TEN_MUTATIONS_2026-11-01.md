# B track R327 S123 independent-method internal audit
UTC date: 2026-11-01. Track: b. Baseline HEAD: 4fd2b79b7b8c3a0a017bd3b203a5504ffc445718.
Status: PASS_NONBLIND_INTERNAL_E1_MATHEMATICS; NATIVE_REMOTE_PYTHON_CLI_NOT_RUN; EXTERNAL_INDEPENDENT_NOT_RUN.

## Preregistered scope and seen evidence
Freeze: 5bfd3c13e4ee9d4b6af1defc17469c33bd538c4c. Before writing this audit, the auditor had seen the R327 original frozen one-sense protocol, original 18-world JSON, S123 grid, primary script and reported grid summary. This is explicitly nonblind same-operator checking. R original source was not modified.

Primary implementation uses direct enumeration of four hidden-state/observation joint probabilities in JavaScript BigInt. The independent auditor uses Python standard-library Fraction and the algebraic identity U=max(max(b,1-b),q) for q>=1/2. It imports no primary source. The auditor checks the exact expected 225 ordered identities and all six computed fields plus chosen action, fixed metadata, no extra fields, and E1 evidence tag.

## Actual execution and outcomes
The Python auditor was executed locally against an independently generated semantically identical 225-world receipt. Ordinary Python execution: PASS, 225/225 exact fields. Optimized Python (-O): PASS, 225/225. Ten deliberate receipt mutations were each rejected: omission, duplicate, belief identity, sensor accuracy identity, cost identity, reward, action, evidence-grade inflation, ordering and summary count. This was tested using the archived Python source bytes (Git blob 4bfab2edb3518db4f04d92fc3ec1fb3a2c904d9f).

Separately, the actual persisted GitHub primary JS source blob 17e4793ed2443a49670de94139dc7d8e660a6c14 was executed under a V8 adapter; its complete serialized 225-world result was byte-for-byte identical to the persisted GitHub JSON blob 0d5adcf7f518b78d730e34711cc08139f209ad8a. A separate BigInt closed-form calculation checked all 225 rows of the persisted remote JSON. All 18 overlapping original R327 worlds at cost 1/8 matched the original persisted result blob 71c696684555366c58140059ebd8947301300b48 across immediate, sense, optimal and action fields.

The original archived R327 three-job historical CI is distinct from S123 and is not counted as a new CI success. Native Node CLI execution of the archived S123 source and native Python audit against the actual remote receipt remain NOT_RUN. The local Python audit and V8 remote replay are complementary internal methods, not an external independent replication.

## Scientific evidence controls
No train/test split exists for this fully enumerated artificial model; therefore empirical leakage and out-of-sample predictive accuracy cannot be evaluated. The immediate-guess baseline is included in every world. Calibration and resampling uncertainty are not meaningful for deterministic exact E1 values; they are required for any later human E2 extension. The counterexamples include an uninformative q=1/2 sensor, strict tie boundaries, zero cost, perfect sensor and high-prior guesses. No independent human or historical data were used. E1 synthetic only; E2 human NOT_ESTABLISHED; E3 history NOT_ESTABLISHED.

## Remaining gates
1. Native Node command-line replay of the archived primary JS into a temporary receipt, byte-compare to GitHub blob.
2. Native archived Python auditor against the exact persisted GitHub receipt, with ten mutants.
3. Optional independent external reviewer and empirical pre-registration if a lawful human source becomes available.
4. Check that original239 and frozen R073/PESEN v0.1 identities remain unchanged. Do not infer formal S123 scientific acceptance from this report alone.

# B audit: R330 S126 independent coefficient oracle
Date 2026-11-01 UTC. Scope (B,R330,S126-v1,nonblind_full_192_world_exact_field_audit). Status PASS_INTERNAL_NONBLIND_E1.

Frozen protocol committed `4a7f9fa7d7ddf5cec19387e67750a9d7c792ee80` before any new result. Original R330 64-world source blob `c0ede1e2bedbd914cf5005c678370e0c8916466a`. Persisted extension JSON blob `34267384ea7bdcf9b39ffeb5983c650cf6ca4500` (66,169 bytes).

## Independent computation
Primary implementation uses four original memory records and exact BigInt weighted averages. Independent JS oracle `research/evidence_audit/b_r330_s126_independent_coeff_oracle.js` imports no primary source and uses explicit coefficient pairs:
d=0, z=0: A(1,1/2),B(1/2,1); z=1: A(1/2,1),B(1,1/2).
d=1, z=0: A(1/4,1/4),B(1/6,1); z=1: A(1/8,1/2),B(1/3,1/2).
The oracle independently forms conditional scores, posterior score averages and pooled weights. It read the **actual persisted remote JSON** and checked all 192 complete world objects, order, all fields, six group objects and identity. PASS. Primary persisted JS was re-executed in V8 and yielded byte-for-byte identical JSON. Original R330 64 e=0 rows separately compared with remote original JSON: PASS 64/64.

A third locally executed Python Fraction implementation generated the same 66,169 bytes and Git blob SHA1 `34267384ea7bdcf9b39ffeb5983c650cf6ca4500`; six Python unit tests passed. A second local Python coefficient oracle, not importing the primary, passed 2 tests and all 192 rows in ordinary and optimized Python modes. The remote JS and local Python source code are separate implementations; full remote receipt identity was verified by matching Git blob, stronger than a short summary hash.

## Eight active negative controls
The archived JS B oracle rejected each of: (1) removed world, (2) duplicated world, (3) altered posterior score, (4) altered pooled score, (5) flipped action, (6) altered error label, (7) altered original source identity, (8) changed evidence grade to E2. 8/8 rejected against persisted full receipt. The local Python B oracle separately rejected equivalent eight corruptions. No silent false positive observed in this limited set.

## Evidence review
Data leakage: no fitted model or real training data, N/A for synthetic enumeration. Baseline: naive observed-cue decision, original 64 worlds and normalize-after-pooling competitor explicitly reported. Sample-out prediction/calibration/cluster uncertainty: NOT_APPLICABLE to deterministic constructed universe; no E2. Null result preserved: 48 score differences with 0 action disagreements. Measurement prior uniform and symmetric noise are artificial assumptions. Independence: separate algorithms by the same research process, prior results and protocol read; **not blinded and not external replication**. Original native Node CLI and GitHub Actions NOT_RUN in this run. No E2/E3, R073/PESEN unchanged.

Next: run the archived native Node CLI only in a verified free environment; consider an independent external auditor and new empirical source only under a separately frozen E2 design. No upgrade to R330 original acceptance.

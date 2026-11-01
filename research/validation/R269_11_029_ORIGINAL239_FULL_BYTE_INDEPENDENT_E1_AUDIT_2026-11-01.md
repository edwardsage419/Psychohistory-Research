# R269 original239 11-029: independent full-byte finite-E1 cross-validation audit

UTC 2026-11-01. Track R with B method audit. Baseline main `3e800f3d2ad0ba7aaf99ad160818bee2f5ce50b2`. **Work COMPLETE; original239 formal itemwise disposition PENDING; queue net closure 0.**

## Scope and precommitted identity

P0 item `11-029 Cross Validation` is provisionally linked to R269 in the original239 v7.8 crosswalk (blob `36f24235901172642c46853298aebb421f1a3552`). Queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`, 154 rows, P0 27/P1 82/P2 45 at read. R269's historical research conclusion is bounded E1, not new human prediction.

Frozen protocol: `protocols/R269_GROUP_VS_ROW_CROSS_VALIDATION_576_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md`, blob `5c34e78a4a846786049a83348437c08eb82454a7`, prescore commit `1ba86be0a35b77c0d5e5f6a72bb102ba08c48795`. Fixed six independent Bernoulli groups, two identical rows per group, three p values, three predictors, 64 exact source configurations per world. LOOR holds out one row and retains its mate; LOGO holds out both rows of the group. Scores are Brier loss.

## Actual independent work

Two different implementation routes were used after reading the archived frozen protocol and original R269 implementation, so both are **same-operator nonblind**.

1. Connector-side JavaScript with a separately written BigInt rational CSV parser read the **complete 183253-byte original GitHub CSV**. It independently verified all 576 source configurations, group identities, duplicated outcomes, exact probability masses, 13824 row predictions, 13824 squared losses, 1152 per-source protocol averages and all nine weighted world results. Errors: **0**. It separately read the archived 3431-byte results JSON and checked all nine world expectations.
2. A standalone CPython 3.13.5 standard-library oracle, using a separate per-group algebraic calculation and `Fraction`, generated all 576 CSV source rows and the complete results JSON from the frozen design without importing R269's implementation. The **entire reconstructed CSV and JSON matched both original Git blobs and original SHA256 digests**. Normal and `python -O` executions returned identical PASS receipts. Two independent mutation controls changed one CSV byte and promoted E2 in the result JSON; both were rejected by the fixed Git blob identities.

Source CSV: Git blob `20b33f85a9408655cfbd7bdbfc1de15ec534571e`, SHA256 `6bc98c0c07c2a6d48184e6a8643dbd515dfa470ba626a10928d90614ce75155d`.
Results JSON: Git blob `4947ccb7a53de1343216e1b69773d0a5c4ea1f29`, SHA256 `d7dda54fdd07148713cd8acbaaafb06bc1282a005b48b09f570211e1a7d4193e`.

All nine archived scores match: memorizer LOOR 0 and LOGO 1/4; constant half both 1/4; global Laplace LOOR/LOGO 31/169 and 31/144 for p=1/4 or 3/4, and 41/169 and 41/144 for p=1/2. The row versus group training sample sizes differ; this audit does not attribute every loss difference uniquely to leakage.

Executable oracle: `research/validation/r269_exact_byte_rebuild_compact_20261101.py`, Git blob `1dfea84222c2b8cb3017eb5ff1bace8cd82e803e`. Independent machine receipt: `research/evidence_audit/B_R269_ORIGINAL239_11_029_FULLBYTE_RECONSTRUCTION_2026-11-01.json`.

## Disposition and limitations

**COMPLETE** for independent full-byte reproduction of the archived finite artificial E1 source and results. **PARTIAL** for original239 itemwise scientific adjudication: original primary-source reading, prior freeze compliance and actual scientific use beyond this bounded construction require a separate formal itemwise acceptance decision. Existing historical R269 acceptance remains untouched. No E2 human score, E3 historical score, out-of-experiment transfer or external-team replication was performed. The old R333 to R340 conditional false-accept risk remains OPEN; its composite candidate has not been natively executed on a complete authentic checkout or bound as a mandatory production caller.

A-track quick public-source scan found a 2017 long-run human repeated PD experiment (94 participants, up to 400 ten-round games over 20 weekdays; original publication PMC5241863, OSF `https://osf.io/64z8u/`). The games re-pair partners, so its ten-round game unit is structurally different from R073's frozen continuous-pair test. **Candidate only; no new download, permission audit, dataset qualification or scoring.** The already known Montero and DF2011/R074 sources remain deduplicated.

Codex open PRs #1 through #12 were read as pending PR evidence; #3 concerns R257 S53 and was not adopted into main. No overlap with the R269 oracle was identified. No frozen source, protocol, original receipt, queue or other track was edited. GitHub Actions: **NOT_RUN**. No paid API, cloud compute, new subscription or data purchase. GitHub account billing and remaining free quota: **NOT_VERIFIED**.

Next: complete authentic R333 to R340 composite native execution and separate claim/math corruption controls, then review mandatory production binding; pursue formal itemwise adjudication for R269 11-029 and R127 05-003 only after the relevant evidence scope is reviewed.

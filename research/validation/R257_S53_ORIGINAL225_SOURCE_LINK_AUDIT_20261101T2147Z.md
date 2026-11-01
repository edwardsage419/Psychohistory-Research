# R257 S53 original 225 source linkage audit

track: R+B
run_date_utc: 2026-11-01T21:47Z
observed_main_before_report: 5d646f695f740a1158558dbc2c2c660103540927
target_key: (R+B,R257/S53,2026-10-29-S53-prescore-freeze,original225-source-to-capacity-receipt-link)
status: COMPLETE_BOUNDED_SOURCE_LINK / FORMAL_S53_ACCEPTANCE_PARTIAL
original239_queue_change: 0
CI: NOT_RUN
billing_checked: NOT_VERIFIED

## Purpose and distinct work

Codex draft PR #3 (head `97d5f74df5d84916917db943156120f08144f445`) independently checks S53 mathematical KKT certificates and explicitly leaves source authentication unperformed. This R/B review independently connects the frozen R257 original 225-row source to the eight S53 convex-world inputs and the baseline receipts. It does not reimplement Codex's 40-capacity KKT or 32-secant validator, does not alter PR #3, and does not replace the frozen S53 protocol. PR #1 and PR #3 are draft/unmerged evidence when checked.

Independent JavaScript BigInt rational source checker:
`research/validation/r257_s53_original225_source_link_gate_20261102.js`
Git blob `a4dfac449371aa259bcdabf4cc73c88e7e014135`.

Four actual source inputs were fetched from GitHub main and their returned Git blob identities checked:

| Source | Git blob |
| --- | --- |
| `research/R257/R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv` | `63dc333cf4c4206fa466e0c0f33e3b079f4dc01b` |
| `research/R257/R257_EXACT_RESULTS.json` | `55c00defa893ba3ed36cc5d3a6b0144953f16301` |
| `research/validation/r257_s53_capacity_shadow_20261029.py` | `4026c2111eed6d64dd21d100ab9961c00a6fa71e` |
| `research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json` | `37f33083b45435e18c66641ef693c6f0c779a680` |

The standalone Node CLI authenticates these four exact blob identities before checking. In this run, the complete remote source code was re-read and its exported checker executed against the actual four fetched file contents in the connected JavaScript V8 runtime. The standalone Node CLI against a full local checkout remains NOT_RUN because Git network checkout is unavailable. This distinction is material.

## Actual independent checks

1. Original R257 universe: nine unique worlds, exactly 225 original grid candidates, 25 unique grid positions per world. All coordinates belong to the frozen five-by-five grid; capacity, feasibility, slack, uniform design mass, and convex/nonconvex flags agree with the original R257 result metadata. Exactly 145 of the 225 grid rows are feasible.
2. Eight strictly convex worlds: all 200 original source rows independently checked with BigInt rational arithmetic for exact gradients `2(x-a)`, `2(y-b)` and exact objective `(x-a)^2+(y-b)^2`, using the original archived R257 targets. All PASS.
3. S53 code binding: the eight world triples (baseline capacity, target a, target b) extracted from the original S53 Python source match the eight archived R257 world identities and parameters. All PASS.
4. S53 receipt binding: for each of the eight worlds, baseline capacity, objective minimum, capacity multiplier and zero-perturbation optimum point match the archived original R257 exact result. All PASS.
5. The ninth nonconvex original world is present with 25 unique grid rows and convex flag zero. Its nonconvex objective/gradient arithmetic was **not** independently recomputed here. It is excluded from the S53 convex-world source mapping.

Actual V8 executions: one authentic positive case PASS and six isolated mutation controls correctly rejected (7/7 expected outcomes). Mutations: corrupt source gradient, corrupt source capacity, duplicate one original grid candidate, corrupt original R257 target, corrupt S53 receipt baseline multiplier, corrupt S53 source parameter declaration. These were in-memory copies; original source and receipt bytes remained unchanged. No random seed is used.

Historical commit ancestry checked with GitHub compare: R257 source archive `e328edc4eff479b4453219e3b9c622f87968e4b8` is an ancestor of S53 protocol freeze `11a7300900888a3e668f462d7378f8683b35161a` (ahead 2149, behind 0); freeze precedes S53 code `f725b7b12c3d7fc6441943fcfae6a0d4333df8fb` (ahead 1, behind 0); S53 code precedes the receipt commit `49cd5356ef4291788960247de5fa3363800a9c03` (ahead 2, behind 0). This establishes Git commit ancestry, not blind execution order.

## Scientific disposition and limitations

`R257_S53_ORIGINAL_SOURCE_PARAMETER_LINK = PASS_BOUNDED_INTERNAL_E1`.
`S53_B_BLINDED_PRESCORE_ORDER = FAIL` remains as documented in the existing protocol-order addendum. The B reviewer had seen R results before running its independent algorithm. This new source linkage check cannot repair that historical sequence.
`PR3_STRICT_MATH_GATE = DRAFT_UNMERGED`; no adoption or production caller binding is inferred.
`S53_FORMAL_FROZEN_PROTOCOL_ACCEPTANCE = PARTIAL`.
`E2=0`; `E3=0`; `EXTERNAL_TEAM_REPLICATION=NOT_RUN`.

This is a source linkage and identity review. It does not rerun the original R257 Python program, does not independently calculate the 25 nonconvex objective values, does not prove actual blind prescore verification, and does not establish an external team's replication. The test code is stored as a separate R/B-owned file. Original frozen sources and Codex PRs were unchanged.

## A public data quick check

Rechecked the English original publisher record for Romero and Rosokha (2023), DOI 10.3982/ECTA17482, `https://onlinelibrary.wiley.com/doi/full/10.3982/ECTA17482`. The paper reports 158 participants, 124 quiz-qualified participants, six main sessions, and 60 supergames per session. A 197 MB data/program supplement is listed. Original bytes, license of the supplement, participant/session/round fields and unchanged R073 eligibility remain UNVERIFIED. No download, E2 scoring, or R073/PESEN parameter change occurred.

## Queue, CI, costs and next work

The main original239 crosswalk remains v7.8 (blob `36f24235901172642c46853298aebb421f1a3552`); the pending queue remains 154 (P0 27, P1 82, P2 45; blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`). This audit formally closes zero pending items.

No GitHub Actions dispatch, paid API, new service, data purchase, or cloud compute was initiated. The actual GitHub billing state and remaining free quota were not independently inspected. CI for this work: NOT_RUN.

Next priority: execute the R333 to R340 composite P0 gate in a trustworthy full checkout with authentic and independently mutated receipts, then bind it to a mandatory production caller only after review and no-charge CI confirmation. Separately, keep R257 S53 blind-order failure visible when evaluating PR #3, and obtain a true independent prescore procedure if formal protocol acceptance is sought.

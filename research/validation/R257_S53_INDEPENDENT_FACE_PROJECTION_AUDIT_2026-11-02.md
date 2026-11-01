# R257 S53: independent exact triangle-face projection audit

track: R/B
subflow: independent scientific verification
run_date_utc: 2026-11-01T22:52Z
initial_main: 119f6d1b5f57d98fb53a1463fd09af97c4d522ec
intermediate_code_commit: 6aba1f0f7b33c28d3c44d81e5893cd8eaa6da8c0
target_key: (R/B,R257 S53,2026-10-29 prescore freeze,independent face projection of 40 convex capacity optima)
status: COMPLETE_BOUNDED_NONBLIND_E1; FORMAL_S53_ACCEPTANCE_PARTIAL
CI: NOT_RUN
billing_checked: ACCOUNT_NOT_VERIFIED
original239_queue_change: 0

## Scope, fixed sources and independence

The current original239 v7.8 crosswalk has 239 rows (Git blob `36f24235901172642c46853298aebb421f1a3552`). The actual itemwise pending queue has 154 rows: P0 27, P1 82, P2 45 (blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`). Twelve Codex PRs remain open; R257 S53 PR #1 and PR #3 were inspected and are unmerged. PR #3 checks exact KKT certificates; it explicitly leaves source authentication unperformed. Earlier R/B source-link audit checks 225 original R257 atoms and the eight S53 source triples. The immediately preceding R/B audit separately verified the ninth nonconvex original world's 25 rows. These tasks are not repeated here.

Read the prescore freeze `protocols/R257_S53_CAPACITY_SHADOW_PRICE_PRESCORE_FREEZE_2026-10-29.md` (blob `2060b7423fed97dcd62f7a53aebea5220b969d2b`) and the complete archived `research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json` (blob `37f33083b45435e18c66641ef693c6f0c779a680`). Also read Codex PR #3 validator at head `97d5f74df5d84916917db943156120f08144f445` (validator blob `75c0870c49c26f175ab678a7600ae4d4b8a5c7f2`) to identify its method and avoid code reuse. This is a disclosed nonblind review.

New executable: `research/validation/r257_s53_independent_face_projection_20261102.js`, first committed at `6aba1f0f7b33c28d3c44d81e5893cd8eaa6da8c0`, remote Git blob `a3813551f3f5eb7a1d1da36f025346ef33506a47`.

## Independent method and actual computation

Used a newly written JavaScript V8 BigInt exact rational evaluator, with no import of the archived R257 Python optimizer, S53 Python code, or Codex PR #3 validator. For each fixed target (a,b) and capacity C>0, minimize `(x-a)^2+(y-b)^2` over the triangle `x>=0, y>=0, x+y<=C`. The independent candidate set comprises:

1. The `x=0` face: `(0, clamp(b,0,C))`.
2. The `y=0` face: `(clamp(a,0,C),0)`.
3. The `x+y=C` face: `(clamp((C+a-b)/2,0,C), C-x)`.
4. The unconstrained point `(a,b)`, only when feasible.

Every triangle optimum lies on one of these faces or in the interior. Strict convexity makes the minimum unique. Choose the smallest exact objective across these candidates. This route derives the solution by independent face minimization, whereas Codex PR #3 validates submitted KKT certificates.

Actually executed the pure verifier in the connected JavaScript V8 runtime against the complete real archived JSON content. Results: eight unique worlds, all 40 exact capacity points and objective minima matched; all 32 left/right secant values matched; all eight baseline multipliers and local derivatives matched. The supporting-line convex inequality was checked at all five capacities per world. Exact cross-multiplication was used; no float tolerance or random seed.

Eight isolated in-memory negative controls were correctly rejected: changed objective, changed optimum point, duplicate capacity delta, changed baseline multiplier, changed secant, removed world, E2 evidence promotion, and duplicated world identity. Positive outcome PASS; 8/8 negative controls REJECT. The source file includes a standalone Node.js CLI with pinned original receipt Git blob and `--selftest` option. That standalone CLI has NOT been executed on a full local checkout; the actual execution here was its pure mathematical core in V8. The code file was remotely reread after commit and the returned blob and byte length matched the uploaded source.

## Scientific disposition

`S53_FACE_PROJECTION_40_EXACT_CAPACITIES = PASS_BOUNDED_INTERNAL_E1`.
`S53_SECANTS_32_AND_BASELINE_MULTIPLIERS_8 = PASS_BOUNDED_INTERNAL_E1`.
`S53_EIGHT_MUTATIONS = ALL_REJECTED`.
`S53_NATIVE_NODE_CLI_ON_FULL_CHECKOUT = NOT_RUN`.
`S53_B_HISTORICAL_BLIND_ORDER = FAIL`, unchanged.
`S53_PR3_MATH_GATE = OPEN_UNMERGED`, unchanged.
`S53_FORMAL_FROZEN_SCIENTIFIC_ACCEPTANCE = PARTIAL`, unchanged.

The frozen protocol required B calculations before viewing the R receipt. This review is explicitly nonblind and cannot restore that historical ordering. The new geometry oracle adds an independent method for checking the eight convex worlds; it does not certify source authenticity of every future input, prove that the unmerged PR is adopted, or establish external team replication. E1 artificial only; new human E2 = 0, historical E3 = 0, external independent team replication = NOT_RUN.

## A source scan, deduplication and cost

Revisited Grujic and Lenaerts (2020), original paper DOI 10.1098/rsos.200618 and Dryad DOI 10.5061/dryad.7fq25s8. The original article confirms nine 16-person sessions, 50 rounds each, four fixed neighbors per participant, two information treatments. The official Dryad README download returned HTTP 403 in this runtime. A prior A-track report already records the same source, exact design, R073 frozen 100-round two-person incompatibility, and raw-access block: `research/data_scout/A_GRUJIC_LENAERTS_2020_SPATIAL_PD_DRYAD_50ROUND_SOURCE_GATE_2026-11-01.md` (blob `b77ead554923ad376f2ea459f2433c6e3625d676`). No duplicate A artifact was created. No raw dataset obtained, qualified, or scored.

No Actions, paid API, purchased data, GPU, cloud runner or subscription was initiated. Actual GitHub billing and remaining free quota were not independently verified. The next P0 target is the authentic full-checkout native R333 to R340 composite execution with independent mathematical and historical claim mutations, followed by authorized mandatory caller binding. R073 and PESEN v0.1 remain frozen.

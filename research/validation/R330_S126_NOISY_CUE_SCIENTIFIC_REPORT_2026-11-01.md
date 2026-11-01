# R330 S126 scientific report: noisy cue and normalization order
Date: 2026-11-01 UTC. Status: PARTIAL_E1_EXTENSION. Target (r,R330,S126-v1,noisy_cue_posterior_score_vs_pooled_weights). Original R330 bounded E1 acceptance remains unchanged.

## Freeze and provenance
New protocol `protocols/R330_S126_NOISY_CUE_POSTERIOR_SCORE_PRESCORE_FREEZE_2026-11-01.md` committed before the first new 192-world result at `4a7f9fa7d7ddf5cec19387e67750a9d7c792ee80`. Original R330 prescore protocol Git blob `fd73ccb03726c26b2db8a4b0e88b0258cb7c39f6`, source blob `a61f49f47f81ed12d89b856038e00f853d4156ce`, 64-world result blob `c0ede1e2bedbd914cf5005c678370e0c8916466a`. Original English paper: Gonzalez, Lerch, Lebiere (2003), DOI 10.1207/s15516709cog2704_2. Our four-instance scheme is a constructed teaching analogue; no original ACT-R replication.

## Exact design and results
Original four memory instances and all 16 binary utility histories held fixed. Cross decay d={0,1}, observed cue o={0,1}, symmetric observation error e={0,1/4,1/2}: 192 finite worlds. True cue prior is uniform. Score-average M_a=(1-e)S_a(o)+e S_a(1-o), compared with naive observed cue and normalize-after-pooling weights. Equal scores choose A.

| decay | error | worlds | M chooses A | M vs naive choice disagreements | pooled vs M choice disagreements | pooled vs M score differences |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 32 | 20 | 0 | 0 | 0 |
| 0 | 1/4 | 32 | 20 | 0 | 0 | 0 |
| 0 | 1/2 | 32 | 22 | 2 | 0 | 0 |
| 1 | 0 | 32 | 18 | 0 | 0 | 0 |
| 1 | 1/4 | 32 | 18 | 0 | 0 | 24 |
| 1 | 1/2 | 32 | 18 | 2 | 0 | 24 |

**Result 1.** At error 0, all 64 worlds match original R330 scores and choices exactly. At error 1/2, the posterior M action and score are independent of the observed cue. At decay 0, score averaging and pooled-weight normalization commute for every world.

**Result 2.** With recency d=1 and nonzero error, score averaging and pooling differ in 48 of 64 worlds, yet their chosen actions agree in all 192 worlds. This is a genuine null result for action disagreements in the frozen universe; it must not be converted into a claim of universal equivalence.

Concrete example history 0001, d=1, observed cue 0, e=1/4: B score under posterior averaging =111/140; under pooled-weight normalization =21/26. Both select B. This establishes a numerical difference in predicted utility while preserving the action in that world.

**Result 3.** At e=1/2, four of 64 worlds differ from the naive observed-cue decision. Example history 0011, d=0, observed cue 0: naive chooses B from A=1/3,B=2/3, posterior averaging ties A=B=1/2 and chooses A. At e=1/4 there are zero such decision changes.

## Reproducibility and negative evidence
Archived primary BigInt JavaScript: `research/validation/r330_s126_noisy_cue.js`. Complete exact JSON: `research/validation/R330_S126_EXACT_192_NOISY_CUE_WORLDS.json`, 66,169 UTF-8 bytes, Git blob `34267384ea7bdcf9b39ffeb5983c650cf6ca4500`. Primary JS executed in V8 and regenerated the actual persisted receipt with exact byte equality. Separate no-import JS oracle uses hardcoded coefficient pairs and compared every field in all 192 actual persisted worlds and all six group summaries. Eight distinct corruptions (missing/duplicate world, marginal/pooled score, action, error label, provenance, evidence grade) were all rejected. Original R330 persisted 64-world result was fetched and all 64 e=0 rows independently compared.

A third Python Fraction implementation and a separate Python coefficient oracle were executed locally with 6 and 2 unit tests respectively; normal and optimized Python B checks passed. The locally generated 66,169-byte JSON has exact Git blob `34267384ea7bdcf9b39ffeb5983c650cf6ca4500`, matching the GitHub persisted result. This is **internal, nonblind, procedural and mathematical verification**. The independent implementations saw the original model and new protocol. No external team replication. Original archived JS native Node CLI remains NOT_RUN in this run; GitHub Actions not dispatched because free billing quota was not verified.

## Scientific limitations and acceptance
No human observations, no likelihood fit, no heldout prediction, no empirical calibration, no causal manipulation, no R073 change, no PESEN v0.1 change, no historical E3. A01 PASS_BOUNDED, A02 PASS for constructed source identity, A03 PASS for V8 and local Python arithmetic, A04 PASS for frozen falsifiers and eight negative controls, A05 PASS for explicit E1-only limits, A06 PASS for versioned source and handoff after commit verification. **Extension status PARTIAL_E1_EXTENSION**; no upgrade of original R330 or external scientific claim.

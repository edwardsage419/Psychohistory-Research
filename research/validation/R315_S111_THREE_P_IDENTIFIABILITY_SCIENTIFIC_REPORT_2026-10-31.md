# R315 S111: exact three-class rewiring-probability identifiability in the frozen two-edge WS variant

Date: 2026-10-31 UTC. New S111 status: **PARTIAL_E1_EXTENSION**. Original R315 status **PASS_BOUNDED_E1_ONLY** unchanged.

## Freeze and evidence
Prescore protocol: `research/validation/R315_S111_WS_P_IDENTIFIABILITY_PRESCORE_FREEZE_2026-10-31.md`, frozen in commit `ec4fb603e3dccb1f35e8cf6b9d31f0c6e1ae5c40`, before inspecting S111 classification outcomes. Baseline HEAD `6934a919d8a790b20d886b6f3c4a7178de6694e6`. Original R315 180 complete path source Git blob `5abbcdbf01e8b31e54671e83d033ab0f1985bd78` and original 210 conditional source atoms Git blob `29f2774cfd56ad4ebd65beca9980900e250675af`. No original files changed.

Six original finite worlds: N=8/10, p=0,1/2,1; exactly two clockwise nearest-neighbor edge decisions. The task is to infer which of three equally likely p hypotheses produced one exact final graph. For each observation map O, the exact optimal zero-one classification accuracy is `(1/3) * sum_o max_p P(O=o | p)`. Five frozen observations: full labeled final graph; joint (C,L,components); C; L; components. No fitted p, no sample noise and no human observations.

## Exact results

| N | Full labeled graph | Joint C,L,components | C only | L only | Components only |
|---|---:|---:|---:|---:|---:|
| 8 | 5/6 | 13/16 | 13/16 | 1/3 | 1/3 |
| 10 | 5/6 | 5/6 | 5/6 | 89/120 | 1/3 |

For N=8, positive observation bins are respectively 19, 12, 12, 1 and 1. For N=10 they are 41, 27, 19, 5 and 1. All 10 accuracy cells satisfy the predeclared information coarsening inequalities. Full graph yields 5/6 for both sizes, C loses 1/48 accuracy relative to full graph at N=8 and loses none at N=10. This is a finite decision-theoretic equality under the specified prior and loss, not a universal sufficient-statistic result.

**Negative control:** For N=8 every possible two-event graph has the same mean shortest path `10/7`; L alone has only one bin and yields chance-level 1/3 classification. All 180 enumerated path outcomes are connected, so component count also has chance-level accuracy. At N=10, L has five positive bins and accuracy 89/120. Thus the same graph summary has very different identification value at these two small sizes.

## Exact expected graph metrics

| N | p | E[C] | Pr(connected) | E[L given connected] | Positive paths |
|---|---|---|---|---|---:|
| 8 | 0 | 1/2 | 1 | 10/7 | 1 |
| 8 | 1/2 | 611/1280 | 1 | 10/7 | 19 |
| 8 | 1 | 1403/2880 | 1 | 10/7 | 12 |
| 10 | 0 | 1/2 | 1 | 5/3 | 1 |
| 10 | 1/2 | 3259/7200 | 1 | 4411/2700 | 41 |
| 10 | 1 | 31/72 | 1 | 1084/675 | 30 |

At N=8 the mean clustering first falls from p=0 to p=1/2 and then rises slightly at p=1. This finite nonmonotonicity prohibits an unqualified claim that expected clustering must decrease in p. At N=10 mean clustering decreases at the three frozen p values. Neither result establishes a large-network trend.

## Verification and provenance
R scoring program: `research/validation/r315_s111_three_p_exact.js`; full exact machine output: `research/validation/R315_S111_THREE_P_CLASSIFICATION_EXACT.json`. B separate JS event enumeration and BFS graph oracle checked all 180 path graphs, six world summaries and 10 classification cells. Nine deliberate mutations rejected in direct JS function execution. Third local Python Fraction/BFS route independently reconstructed all 180 paths and agreed exactly with all 10 accuracies and six world summaries. Source CSV 210 rows was read and Git blob checked, but S111 does not claim to have rerun the original archived 210-row independent auditor. The archived Node and Python CLI programs have not been run in a clean repository checkout during this round. Details: `research/evidence_audit/B_R315_S111_NONBLIND_GRAPH_ORACLE_RECEIPT_2026-10-31.json`.

## Scientific limitations
This is complete arithmetic for a tiny, artificial, fully specified model. The original 1998 Watts–Strogatz study considered much larger networks and a full rewiring sweep. Here no unknown mechanism is estimated from human networks. The three-class prior is exactly uniform by design. No human sample, holdout, empirical calibration, confidence interval, external independent replication or causal attribution. The observed SocioPatterns student contacts lack a ring baseline and observable clockwise edge-rewiring event identity, so their published clustering and shortest paths cannot validate this S111 mechanism. E1 only; new E2=0; new E3=0. R073 scoring and PESEN v0.1 remain frozen.

## Reproduction (no paid services)
From a checkout containing this report and the immutable original R315 source:
```sh
node research/validation/r315_s111_three_p_exact.js --check
node research/evidence_audit/b_r315_s111_nonblind_independent_graph_oracle.js --mutations
python research/evidence_audit/r315_s111_local_fraction_third_route.py
```
These exact archived command lines are provided for future replay; they are **NOT_RUN** in a clean checkout in this round. No GitHub Actions dispatch.

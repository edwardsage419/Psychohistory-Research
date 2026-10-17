# R082 pre-result protocol: original 64-network human nonresponse sequences, original graph isolation and allocation source qualifications

Date: 2026-10-17. Scope: retrospective E2 descriptive source audit. This file is written **before any R082 real original source dropout classifications, degree/missingness contingency tables, or exceptional five-bot graph anomaly counts are calculated**. All R080 and R081 published arm outcomes and aggregate missingness bounds are known. Freeze does not undo that look-ahead.

## Provenance and source lock

Authors Shirado and Christakis (2020), *iScience*, DOI https://doi.org/10.1016/j.isci.2020.101438, main article at https://pmc.ncbi.nlm.nih.gov/articles/PMC7452167/; first-author original dataset Mendeley Data v1 DOI https://doi.org/10.17632/t963ktp6ft.1, metadata endpoint https://data.mendeley.com/public-api/datasets/t963ktp6ft . Original set fingerprint SHA256 of sorted 64 publisher SHA256 strings: `555e2127ac21f4532c33a2e0a08f2e081b5f970891bd772c9bac3155d1d53571`. R081 previously reconfirmed all 64 real original source files, 64 × 16 × 30 = 30720 human decision opportunities and 27656 observed C/D, 3064 unobserved. Its all16-human hypothetical round1-round30 change interval was [-0.2021484375,-0.0244140625].

All sixty-four original files must be downloaded and checked for **original publisher file SHA256 plus content length**, and all original R080 validations including the strictly limited zero-degree human graph node omission rule must pass before this study writes any E2 result. No reduction to valid sub-samples. Program must exactly reconstruct the frozen R080 first-last observed cooperation delta -0.11073225819319567 (tolerance 1e-12), as a source execution parity check. Read actual `players[].is_bot` status and `result_behaviors[].cooperation`, never treat humans absent from network.nodes as absent from the experimental 16-human roster.

## Frozen missingness history taxonomy (per original human slot over 30 behavior rounds)

Define observation x_t=1 if exactly one real `C` or `D` response appears for a human roster actor at round t; x_t=0 if no response. Following the source gates, each of the 1024 human identities is assigned exactly **one** disjoint category:
1. `full30_observed` if all 30 observed.
2. `never_observed` if all 30 unobserved.
3. `leading_only_missing` if a nonempty initial unobserved prefix followed by observed answers to t=30.
4. `trailing_only_missing` if nonempty observed prefix followed by missing answers to t=30.
5. `both_ends_missing_contiguous_middle` if nonempty initial missing prefix, one observed contiguous block and a nonempty missing suffix.
6. `interior_gap_with_return` for every other sequence with at least one observed response (an observed-missing-observed subsequence); this includes cases with both missing ends and intermittent reversals.

All human identities with an observed response must have a nonempty contiguous range between their first and last observed records; if any missing entry is inside this span, they are classified as `interior_gap_with_return`, taking precedence over the other partial cases. Verify all six bins sum to exactly 16 per original network and 1024 overall. Compute counts of missing human slots from those in the `trailing_only_missing` category only, as a **lower bound on what is consistent with possible permanent departures**, and separately count any final trailing missing suffix among all categories; such classifications do **not** prove departure, timeout, or nonparticipation. Report by original eight arms and full 64 network equal-roster aggregate.

## Frozen graph alignment and descriptive association

Original source has 30 action lists and 31 network snapshots but action/graph causal temporal alignment is **not independently validated**. Use two symmetric, explicitly labeled source positions: `snapshot_before_index` uses the graph at list index t; `snapshot_after_index` uses graph index t+1. Neither is asserted to be observed by actors before or after a specific decision, despite mnemonic labels.

For every human and every round, use the validated undirected graph's actual links (including zero-degree omitted humans) to count human-to-human degree and human-to-bot degree for BOTH positions. Two binary exposure classifications are frozen for both positions:
- `no_any_neighbor`: total degree zero versus at least one link;
- `no_human_neighbor`: human-human degree zero versus at least one human-human link.
For each exposure compute aggregate 2×2 tables of human action missing/observed within zero-degree vs nonzero-degree, separately for all64 and for each of eight original arms; release numerator/denominator and missing risk by degree status when denominator positive, else null. These are **joint observational associations**, not missingness causes. Crucially, isolated humans can retain a choice in experimental interface, so do not infer that isolation implies a missing choice.

Predeclare differences `missing_rate_zero_degree - missing_rate_nonzero_degree`; these are descriptive risk differences. Do not select one snapshot alignment by whichever has a larger association or a preferred treatment direction. Report both, all negative results, and null denominators honestly. No p-values, models, confidence intervals, clustering adjustment, causal inference, or missing-at-random assertions.

## Experiment 2 source five-node structural anomaly

For each of the eight original `single_mgmt_bot` JSONs, source `players.is_bot` has been previously shown to label five distinct bot **nodes** in a network; the primary article describes one logical bot with five ties. Per snapshot count HH/HB/BB edge **numbers** and histogram of source bot node degree. Export only across-all-eight-network aggregate frequencies of (a) number of bot-marked nodes with exactly one human neighbor, (b) snapshot HB total edge-count histogram and (c) count of snapshots that deviate from exactly five HB ties or five singleton bot nodes. With 248 graph snapshots expected, include all rather than dropping the anomalous snapshot; do not reveal any individual game/session, actor ID, edges, or single-network results. This is an observed structural fingerprint; the implementation map for the logical bot remains **UNVERIFIED** even if 247/248 states look compatible.

## Randomization and causal evidence gates

The 2020 primary article establishes Erdős–Rényi randomized **initial human-human ties**, random **rewiring opportunities/pair selection** and intervention algorithms, and that Experiment 2's single-bot strategy was **designed based on Experiment 1**. Neither the initial edge randomization nor the randomized rewiring opportunity alone establishes that sessions or networks were randomly assigned to each of the first experiment's seven treatment arms. The published 8-network balance is an outcome of design. Here `experiment1_treatment_assignment_randomized=NOT_INDEPENDENTLY_VERIFIED` until a specific reproducible allocation log or unambiguous source statement is available. `experiment2_vs_experiment1_randomized_comparison=NO`; no unobserved effect-estimation assumptions invented. A separately accessible supplementary PDF might contain further methods, but it must actually be opened before claiming what it says.

## Execution, audit and privacy

Implement pure synthetic tests before real data, at least 20 covering category boundaries, 30-round validity, source identities, all 8 arm names, omitted isolates, snapshot t/t+1 dual alignment, stratified missing-cell tallies, no bot actions counted as human, five-bot anomalous snapshot retained, complete all64 universe, no private identifiers emitted. Then real GitHub Actions fetch with full publisher SHA. Repeat independently with exactly frozen program and compare anonymous output exact SHA256 before permanent archiving in research/R082. No raw C/D, human IDs, experiment IDs, bot IDs, network edges, signed URLs or per-network metrics in repository, CI console or artifacts. Only group-level aggregate data and a full64 summary may be published.

If valid results exist, `R082_CLOSED_BOUNDED` is possible for this **source-limited E2 audit**, irrespective of whether dropout/isolation associations are present or absent. Do not claim independently identified human dropout, group assignment causal effect, peer contagion, robot intervention benefit, R073 mechanism validation, or societal historical forecast. PESEN v0.1 remains FROZEN.

R082_PROTOCOL=FROZEN_BEFORE_NEW_REAL_R082_CLASSIFICATIONS
R082_HISTORICAL_R080_R081_RESULTS=KNOWN_BEFORE_FREEZE
R082_RANDOM_TREATMENT_ASSIGNMENT=OPEN_SOURCE_GATE

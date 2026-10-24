# R341 original239 04-020 ERGM: prescore three-node finite exponential graph protocol v1

Date: 2026-10-24. Status: FROZEN_BEFORE_R341_SOURCE_GENERATION. All choices below must be fixed before the first R341 source commit.

## Sources and reuse
See docs/ORIGINAL_239_04-020_ERGM_REUSE_PREAUDIT_2026-10-24.md for Frank & Strauss (1986), Wasserman & Pattison (1996), R316 scope and unresolved early ZIP audit.

## Exact universe
Three labeled nodes 0,1,2. Undirected edge bits in fixed order (0,1), (0,2), (1,2). Graph strings ordered "000","001","010","011","100","101","110","111". Four worlds in order (a,b)=("1","1"),("1","2"),("2","1"),("2","2"). Edge count e is the number of ones. Triangle t=1 exactly when graph_bits=="111", otherwise 0. Unnormalized weight w=a**e * b**t using integer a,b. Partition function Z=sum over eight graphs of w. Exact graph probability Fraction(w,Z). All graph probability and weights serialized with Python str(Fraction).

## Frozen output formats
CSV research/R341/R341_ALL_32_ARTIFICIAL_GRAPH_ATOMS.csv, exact header a,b,graph_bits,edges,triangles,unnormalized_weight,probability. Emit 4*8=32 data rows in world and graph order. csv.writer lineterminator="\\n" interpreted as LF, UTF-8, final LF. All fields are strings.

JSON research/R341/R341_EXACT_4_GRAPH_WORLDS.json: top-level object insertion order schema,worlds,checks. Schema "R341_frozen_three_node_ergm_v1". Worlds array ordered as above. Each world object insertion order a,b,Z,edge_marginal,triangle_probability,closure_odds_ratio,graph_probabilities. edge_marginal is the probability edge (0,1) exists, summing graph probabilities for graph_bits[0]=="1". triangle_probability is P("111"). closure_odds_ratio is the conditional odds for bit 0 when bits 1 and 2 are both 1 divided by conditional odds for bit 0 when bits 1 and 2 are both 0; this equals b. graph_probabilities is an array of 8 canonical Fraction strings. Checks insertion order worlds,source_rows,normalization_worlds,expected_partition_functions,baseline_independent_worlds,closure_contrast_worlds. Checks values worlds=4,source_rows=32,normalization_worlds=4,expected_partition_functions=["8","9","27","35"],baseline_independent_worlds=2,closure_contrast_worlds=2. JSON dumps indent=2, ensure_ascii=True, final LF.

## Falsifiers and audit gates
F1: exactly four worlds, eight graphs, 32 source atoms.
F2: Z exactly 8,9,27,35 in world order and each world probability sums exactly to one.
F3: edge marginal exactly 1/2,5/9,2/3,26/35 in world order.
F4: triangle probability exactly 1/8,2/9,8/27,16/35 in world order.
F5: closure odds ratio exactly 1,2,1,2. For b=1 the three edges are independent Bernoulli with p=a/(1+a).
F6: all frozen checks values and byte formats exactly match.
F7: independent no-import Fraction auditor recreates CSV and JSON bytes, and rejects deliberate CSV and JSON tampering.
F8: Python 3.11, 3.12 and independent GitHub Actions jobs all success before formal E1 acceptance.
F9: source commit follows this protocol freeze; R073 and PESEN v0.1 unchanged.

## Evidence boundary
Potential grade PASS_BOUNDED_E1_CONSTRUCTED_THREE_NODE_EDGE_TRIANGLE_ERGM_ONLY. Three-node exact arithmetic does not establish parameter estimation, identifiability from real social networks, large-network degeneracy or mixing, human E2, historical E3, or original-author empirical replication. Catalogue linkage is provenance only. Personal decision system deferred.

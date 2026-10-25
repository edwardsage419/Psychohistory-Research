# R169 third method scientific report: observation-ladder identifiability

Date: 2026-10-26 Asia/Singapore. Research scope: original R169 four-node, labeled, artificial coevolving network. New protocol frozen in `protocols/R169_OBSERVATION_LADDER_72_WORLD_THIRD_METHOD_FREEZE_2026-10-26.md` at commit `e632cf3b5301589e55fb983fce11c27be7b29fd6` before writing the new code or obtaining results. Existing R169 original 72-world E1 result and scientific acceptance are unchanged.

## Research question and exact design

Twelve fixed starting configurations, comprising four network templates and three initial binary opinion vectors, each have six control choices: rewiring alpha in {0, 1/2, 1} and target rule in {same, any}. Within each fixed starting configuration, compare all 15 unordered pairs of controls at t=1,2,3. Observations are nested: O1 opinion-1 count; O2 joint count and number of discordant edges; O3 joint count, discordance and number of connected components; O4 full labeled network and four opinion values. Equality of probability laws is tested using exact Python Fraction, with no stochastic sampling or floating-point threshold. Twelve strata are compared separately to avoid trivial discrimination by different starting networks.

## New exact findings

The following totals sum within-stratum class counts and uniquely identified controls across all 12 strata. The six controls per stratum give 72 control worlds and 180 distinct within-stratum control pairs.

| Time | Observation | Classes summed | Unique worlds | Ambiguous worlds | Distinguishable pairs / 180 |
| --- | --- | ---: | ---: | ---: | ---: |
| t1 | O1 | 36 | 0 | 72 | 144 |
| t1 | O2 | 44 | 16 | 56 | 152 |
| t1 | O3 | 44 | 16 | 56 | 152 |
| t1 | O4 | 58 | 44 | 28 | 166 |
| t2 | O1 | 36 | 0 | 72 | 144 |
| t2 | O2 | 54 | 36 | 36 | 162 |
| t2 | O3 | 54 | 36 | 36 | 162 |
| t2 | O4 | 60 | 48 | 24 | 168 |
| t3 | O1 | 38 | 4 | 68 | 146 |
| t3 | O2 | 56 | 40 | 32 | 164 |
| t3 | O3 | 56 | 40 | 32 | 164 |
| t3 | O4 | 60 | 48 | 24 | 168 |

Exact witness: initial graph path {(0,1),(1,2),(2,3)}, opinions (0,0,1,1), alpha=1/2. At t=1 the 'same' and 'any' rewiring policies produce **identical distributions of opinion-1 count**, so O1 TV=0, but their complete labeled state distributions differ with **O4 TV=1/2**. This demonstrates an exact information-loss effect from observing only aggregate opinion. All 68 witness instances across the three timepoints were discovered only after the freeze. O3 yielded no additional control distinction over O2 in this frozen finite grid; this does not prove connected components are generally redundant.

For t2 and t3, O4 leaves 24 ambiguous worlds, corresponding to the 12 alpha=0 pairs (same and any target rule) across the 12 starting configurations. The target rule has no effect when rewiring never occurs. Observing additional timepoints of the same process cannot identify that inactive rule. All 12*3*3 nested observation comparisons satisfied refinement monotonicity.

## Execution, independent methods, negative controls

The main exact source `research/validation/r169_observation_ladder_20261026.py` locally executed 72 worlds, 288 full snapshots, 2829 nonzero-state snapshot entries. Deterministic serialization SHA256 of the complete computed paths: `8a7bddff1f100fb4736871906dac5b65cdf3b437a015731d1adbeb2aab07f177`. This digest is of the new script's serialization, **not** a claim of byte equality with original R169 JSON. The local compact machine receipt contains all 12 strata's classes and unique-world counts.

An executed mutation changing alpha=1/2 to 1/3 at the frozen path/block/same starting condition changed the t1 full-state law by exact TV=1/6, hence was detected. The previously archived original R169 t2 path/block/alpha=1 TV=1/2 between modes was independently recovered.

B's separately coded oriented-edge event enumerator recomputed 72 worlds and matched all 288 complete snapshots and 2829 reachable-state transition-kernel checks exactly. This is independent implementation inside the same project, not an independent external research-team replication. The first B local execution failed because its replacement edge tuple was not sorted canonically; the B script was corrected and then rerun successfully. The failed first attempt is disclosed rather than hidden.

## Scientific acceptance and boundaries

Status: `PASS_BOUNDED_INTERNAL_EXACT_E1` for this new finite mathematical observation experiment. R169's prior `CLOSED_BOUNDED_E1` remains unchanged. E2 newly scored human predictions = 0, E3 historical predictions = 0, external team replications = 0. No fitted parameters, independent human samples, out-of-sample scoring, probability calibration on real observations, causal identification or large-network phase transition is established. R073 and PESEN v0.1 remain frozen.

New CI was not triggered because zero-billing eligibility was not independently established. Local Python scripts executed; remote GitHub Actions status for new commits must be reported separately as NOT_RUN unless a later verified run exists. No new expense authorized.

Sources: [original R169 prescore](../../protocols/R169_FINITE_ADAPTIVE_NETWORK_72_LABELED_GRAPH_WORLDS_PRESCORE_FREEZE_2026-10-21.md), [original R169 report](../R169/R169_SCIENTIFIC_REPORT_2026-10-21.md), [new frozen protocol](../../protocols/R169_OBSERVATION_LADDER_72_WORLD_THIRD_METHOD_FREEZE_2026-10-26.md), [new source](r169_observation_ladder_20261026.py), [exact receipt](R169_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json), [B source](../evidence_audit/r169_b_oriented_event_independent_20261026.py).

# R340 original239 04-007 SIS Epidemic Model: prescore two-node CTMC protocol revision 2

Date: 2026-10-24. State: FROZEN_BEFORE_SOURCE_GENERATION. Revision 2 supersedes an earlier same-day prescore draft that left CSV formatting unspecified. No R340 source had been generated or committed at either revision.

## Sources and reuse

Pastor-Satorras and Vespignani (2001), DOI 10.1103/PhysRevLett.86.3200; Van Mieghem (2011), DOI 10.1007/s00607-011-0155-y. See docs/ORIGINAL_239_04-007_SIS_EPIDEMIC_REUSE_PREAUDIT_2026-10-24.md. Early R001–R064 ZIP strict reuse audit OPEN. No real epidemic data.

## Frozen exact universe and byte formats

Two undirected adjacent nodes. State strings ordered "00","01","10","11" with bits indicating infection. Recovery rate gamma=1 per infected node. Infection of a susceptible node occurs at rate beta times the number of infected neighbors. Beta worlds ordered "1/2","1","2". Construct the 4 by 4 continuous-time generator Q for each beta: for distinct states i,j, Q_ij is the rate of the single-node infection/recovery transition from i to j, or zero; Q_ii is minus the sum of off-diagonal rates.

Source path research/R340/R340_ALL_48_ARTIFICIAL_GENERATOR_ATOMS.csv. Exact CSV header: beta,origin,destination,rate. Emit rows in beta, origin, destination order, exactly 3*4*4=48 rows. All fields are strings. Rates use Python str(Fraction) canonical text, e.g. "0","1/2","1","2","-3/2","-2","-3". UTF-8, csv.writer lineterminator="\\n" interpreted as LF at runtime, final LF.

Results path research/R340/R340_EXACT_3_GENERATORS.json. JSON object insertion order exactly schema,worlds,checks. Schema string "R340_frozen_two_node_sis_generator_v1". Worlds array in beta order; each object insertion order exactly beta,matrix,first_event_infection,first_event_recovery. Matrix is four arrays of four canonical Fraction strings in state order. First-event values use canonical Fraction strings. Checks object insertion order exactly worlds,source_rows,absorbing_worlds,zero_sum_rows,nonnegative_offdiagonal_entries,correct_01_10_transitions,correct_11_recoveries. JSON dumps indent=2, ensure_ascii=True, final LF.

F1: 3 beta worlds, 4 states each, 48 original source entries.
F2: 00 is absorbing in all three worlds; its row is all zero.
F3: 01 and 10 each have one infection transition at beta and one recovery transition at 1; 11 has two distinct recovery transitions each rate 1.
F4: all 12 generator rows sum exactly zero; all 36 off-diagonal entries nonnegative.
F5: from 01, next event infection probability beta/(1+beta), giving 1/3,1/2,2/3 in beta order; complementary recovery 2/3,1/2,1/3.
F6: frozen checks dictionary values: worlds=3,source_rows=48,absorbing_worlds=3,zero_sum_rows=12,nonnegative_offdiagonal_entries=36,correct_01_10_transitions=6,correct_11_recoveries=3.
F7: independent no-import Fraction auditor recreates CSV and JSON exact bytes and rejects deliberate CSV and JSON tampering.
F8: GitHub Actions python311, python312, independent all success before formal E1 acceptance.
F9: source commit follows this final protocol revision commit. R073 and PESEN v0.1 unchanged.

## Scientific limits

Potential acceptance PASS_BOUNDED_E1_CONSTRUCTED_TWO_NODE_SIS_GENERATOR_ONLY. The finite two-node chain cannot establish scale-free epidemic thresholds, large-network persistence, endemic prevalence, real infection dynamics, human E2, historical E3 or original 2001 empirical replication. Catalogue linkage is provenance only. Complete R series and itemwise audits before taxonomy and fusion. Personal decision system deferred.

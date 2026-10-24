# R344 original239 04-024 heterogeneous typed meta-path: prescore 64 artificial pair atoms protocol v1

Date: 2026-10-24. State: FROZEN_BEFORE_R344_SOURCE_GENERATION.

## Sources and reuse
See docs/ORIGINAL_239_04-024_HETEROGENEOUS_NETWORK_REUSE_PREAUDIT_2026-10-24.md for Sun et al. 2011 PathSim, Sun and Han 2013, and R316/R343 strict reuse boundaries. Early ZIP strict reuse OPEN.

## Exact universe
Type-A nodes A0,A1, type-B nodes B0,B1. Four undirected bipartite edge bits ordered (A0,B0),(A0,B1),(A1,B0),(A1,B1). Network strings from "0000" through "1111". For each network and ordered A-source,target pair in order (A0,A0),(A0,A1),(A1,A0),(A1,A1), compute N_st=sum_{b in {B0,B1}} M[s,b]*M[t,b]. Self counts N_ss and N_tt are degrees of A nodes. PathSim-style value is Fraction(2*N_st,N_ss+N_tt) if denominator positive, else Fraction(0). Canonical Fraction strings.

## Frozen byte outputs
CSV research/R344/R344_ALL_64_ARTIFICIAL_TYPED_PATH_ATOMS.csv, header network_bits,source,target,path_count,self_source_count,self_target_count,pathsim. Emit exactly 16*4=64 data rows in network then ordered A-pair order. source/target strings A0 or A1, integer counts str(int), pathsim str(Fraction), csv.writer lineterminator="\\n" interpreted LF, UTF-8 final LF.

JSON research/R344/R344_EXACT_16_TYPED_NETWORKS.json, top-level insertion order schema,worlds,checks. Schema "R344_frozen_two_type_pathsim_v1". Worlds array in network order; each object insertion order network_bits,path_count_matrix,pathsim_matrix. Matrices are two rows of two entries, counts as integer values and PathSim as canonical Fraction strings. Checks object insertion order worlds,source_rows,symmetric_worlds,positive_cross_similarity_worlds,zero_graph_cross_similarity,layer_B_swap_invariant_worlds,projection_collision_witness. Exact values worlds=16,source_rows=64,symmetric_worlds=16,positive_cross_similarity_worlds=7,zero_graph_cross_similarity="0",layer_B_swap_invariant_worlds=16,projection_collision_witness=["1010","0101"].

## Falsifiers
F1: exactly 16 typed networks and 64 source atoms.
F2: path count and PathSim matrices symmetric for all 16.
F3: off-diagonal PathSim positive in exactly seven worlds.
F4: all PathSim values in [0,1]; diagonal is 1 for nonzero A degree and 0 for zero A degree.
F5: swapping B0 and B1 preserves path-count and PathSim matrices for all 16 worlds.
F6: "1010" and "0101" are distinct typed incidence networks with identical A-B-A path count matrices; frozen checks exact.
F7: independent no-import auditor recreates CSV and JSON bytes, rejecting deliberate CSV and JSON tampering.
F8: Python 3.11, 3.12 and independent CI jobs all success before formal E1 acceptance.
F9: source commit follows protocol freeze; R073 and PESEN v0.1 unchanged.

## Scientific boundaries
Potential grade PASS_BOUNDED_E1_CONSTRUCTED_TWO_TYPE_METAPATH_SIMILARITY_ONLY. This finite PathSim-style enumeration does not establish real-world network semantics, original empirical ranking performance, general heterogeneous embeddings, human E2, historical E3 or causal inference. Catalogue linkage is provenance only. Personal decision system deferred.

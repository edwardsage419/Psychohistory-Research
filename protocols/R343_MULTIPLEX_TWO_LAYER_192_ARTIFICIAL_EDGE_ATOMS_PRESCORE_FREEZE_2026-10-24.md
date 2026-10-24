# R343 original239 04-023 multiplex: prescore two-layer 192 artificial edge atoms protocol v1

Date: 2026-10-24. State: FROZEN_BEFORE_R343_SOURCE_GENERATION.

## Sources and reuse
See docs/ORIGINAL_239_04-023_MULTIPLEX_REUSE_PREAUDIT_2026-10-24.md for Kivelä et al. 2014 and Boccaletti et al. 2014, plus R316/R317/R341/R342 reuse boundaries. Early ZIP audit OPEN.

## Frozen exact universe
Three labeled nodes 0,1,2. Undirected edge positions ordered (0,1),(0,2),(1,2). Two labeled layers L0 and L1, each a 3-bit graph in order "000" through "111". Enumerate 8*8=64 configurations in L0 then L1 order. For each of three edge positions, union bit is OR(L0,L1), intersection bit is AND(L0,L1). Union and intersection aggregate graph strings preserve edge order.

## Frozen byte outputs
CSV research/R343/R343_ALL_192_ARTIFICIAL_LAYER_EDGE_ATOMS.csv. Header layer0_bits,layer1_bits,edge,layer0,layer1,union,intersection. Exactly 64*3=192 data rows ordered L0,L1,edge. Edge text "01","02","12". All bit fields text "0" or "1". csv.writer lineterminator="\\n" interpreted LF, UTF-8 final LF.

JSON research/R343/R343_EXACT_64_LAYER_PAIRS.json. Top-level insertion order schema,worlds,checks. Schema "R343_frozen_three_node_two_layer_projection_v1". Worlds array ordered L0 then L1, each object insertion order layer0_bits,layer1_bits,union_bits,intersection_bits. Checks object insertion order worlds,source_rows,unique_union_graphs,union_111_preimages,union_000_preimages,union_111_intersection_000_preimages,layer_swap_invariant_worlds. Exact values worlds=64,source_rows=192,unique_union_graphs=8,union_111_preimages=27,union_000_preimages=1,union_111_intersection_000_preimages=8,layer_swap_invariant_worlds=64. json.dumps indent=2, ensure_ascii=True, final LF.

## Frozen falsifiers
F1: 64 worlds and 192 source atoms.
F2: each union and intersection bit exactly OR and AND of layer bits.
F3: union graph has 8 distinct outcomes; union 111 has 27 preimages and union 000 has one.
F4: union 111 and intersection 000 has eight preimages, proving union alone loses layer identity.
F5: layer swap preserves union and intersection in all 64 worlds.
F6: exact frozen checks and byte formats.
F7: independent no-import enumerator recreates CSV and JSON exact bytes and rejects deliberate CSV and JSON tampering.
F8: Python 3.11, 3.12, independent CI jobs all success before formal E1 acceptance.
F9: source follows this protocol; R073 and PESEN v0.1 unchanged.

## Evidence boundary
Potential grade PASS_BOUNDED_E1_CONSTRUCTED_TWO_LAYER_PROJECTION_ONLY. This does not establish observed multilayer network, social meaning of layers, real network dynamics, human E2, historical E3 or original-author empirical replication. Catalogue association is provenance only. Personal decision system deferred.

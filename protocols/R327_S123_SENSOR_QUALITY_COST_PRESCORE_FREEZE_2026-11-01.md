# R327 S123: finite POMDP sensor quality and observation cost prescore freeze
UTC date: 2026-11-01. Track: r. Baseline main HEAD: b238923ec1a73ca985083b5f4a3c3706ee69c8b4.
Status at this commit: PROTOCOL_ONLY. No new S123 outcome is asserted here.

## Frozen upstream and boundary
Original R327 protocol: protocols/R327_TWO_STATE_ONE_SENSE_POMDP_72_PATHS_PRESCORE_FREEZE_2026-10-24.md, Git blob df46cf75cf0e0ae9e0e1eb4f94313de9130c7b2f. Original 72-path source and 18-world results remain immutable. R327 original acceptance is bounded E1, not transferable to this extension. R073 model/scoring and PESEN v0.1 remain frozen.

## Research question and exact finite universe
Quantify how the value of a single observation depends on known sensor quality q and fixed observation cost c, while keeping R327's hidden binary state H, reward 1 for a correct terminal guess, zero otherwise, and strict tie preference for an immediate guess. Predefine beliefs b=k/8 for k=0,...,8, sensor accuracies q in {1/2,5/8,3/4,7/8,1}, and observation costs c in {0,1/16,1/8,3/16,1/4}. Cartesian product: 225 distinct artificial worlds. This is a finite parameter sensitivity exercise, with no empirical fitting.

For each (b,q,c), calculate immediate reward M=max(b,1-b); four joint masses P(H=h,Y=y); uncosted information reward U=sum_y max_h P(H=h,Y=y); net sensing S=U-c; gross information value G=U-M; optimal reward V=max(M,S). Choose SENSE iff S>M; otherwise GUESS_0 when b<=1/2, GUESS_1 when b>1/2. Exact rational arithmetic only. Output fields and ordering are fixed: q ascending, c ascending, b ascending; each row has b,q,c,M,U,S,G,V,chosen_action. Use canonical Fraction strings and JSON serialization with sort_keys and compact separators plus terminal newline.

## Prespecified falsifiers and audit
1. Exactly 225 unique complete triples, rational fields exactly reconstructible, probability mass exactly one, all values finite.
2. For q=1/2, gross information value is zero for every belief, and SENSE is never chosen for nonnegative costs.
3. SENSE is chosen only when gross information value strictly exceeds c. Equality must choose an immediate guess.
4. At cost c=1/8 and q in {1/2,3/4}, all 18 original R327 worlds must have exactly the same immediate, sensing, optimal values and chosen actions.
5. Independently derive an algebraic closed form for U for binary symmetric observation, and compare every world using an auditor that imports no R production code. The auditor must check all output fields, complete coverage, ordering and metadata. At least eight deliberately mutated receipts must be rejected, including omission, duplicate, wrong identity, wrong value, wrong decision and E2 inflation.
6. Preserve all initial failures and scope boundaries. E1 mathematical check only; no E2, E3, out-of-sample human prediction, external replication or general POMDP solver claim. No CI launch without confirmed zero cost.

Sources: Smallwood and Sondik 1973 DOI 10.1287/opre.21.5.1071; Kaelbling, Littman and Cassandra 1998 DOI 10.1016/S0004-3702(98)00023-X. Original R327 frozen source and protocol are primary local inputs.

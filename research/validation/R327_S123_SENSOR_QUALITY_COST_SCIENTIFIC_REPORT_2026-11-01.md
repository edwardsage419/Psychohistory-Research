# R327 S123 scientific report: finite sensor quality and observation cost
Date: 2026-11-01 UTC. Track: r. Status: PARTIAL_E1_EXTENSION, INTERNAL_NONBLIND_EXACT_AUDIT_PASS. Baseline prior to freeze: b238923ec1a73ca985083b5f4a3c3706ee69c8b4.

## Freeze, sources and separation
The prescore protocol was committed at 5bfd3c13e4ee9d4b6af1defc17469c33bd538c4c before generating the S123 result. Original R327 source and its project-defined bounded E1 acceptance remain unchanged. Original R327 source protocol blob: df46cf75cf0e0ae9e0e1eb4f94313de9130c7b2f. The original 18-world result blob is 71c696684555366c58140059ebd8947301300b48.

Primary theory: Smallwood and Sondik (1973), DOI 10.1287/opre.21.5.1071; Kaelbling, Littman and Cassandra (1998), DOI 10.1016/S0004-3702(98)00023-X. This extension is a fully specified artificial one-observation decision world.

## Finite exact universe and method
The hidden state is binary and fixed. A terminal guess earns 1 if correct, zero otherwise. A symmetric binary sensor has known accuracy q. Nine frozen prior beliefs b=0/8,...,8/8, five q values {1/2,5/8,3/4,7/8,1}, and five nonnegative costs c {0,1/16,1/8,3/16,1/4} yield 225 complete worlds. No parameters were estimated from people.

Let M=max(b,1-b). The direct four-joint-mass enumeration yields the maximum terminal accuracy after sensing U=sum_y max_h P(H=h,Y=y). Net sense value S=U-c. Sensing is selected iff S>M, otherwise an immediate guess with the original R327 tie preference.

An independent algebraic method gives U=max(M,q) for q>=1/2. Thus gross information value G=max(0,q-M), and SENSE iff q>M+c. At equality, the original tie rule chooses an immediate guess.

## Complete results
Number of SENSE decisions across the nine prior beliefs for each (q,c):

| q / cost | 0 | 1/16 | 1/8 | 3/16 | 1/4 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1/2 | 0 | 0 | 0 | 0 | 0 |
| 5/8 | 1 | 1 | 0 | 0 | 0 |
| 3/4 | 3 | 3 | 1 | 1 | 0 |
| 7/8 | 5 | 5 | 3 | 3 | 1 |
| 1 | 7 | 7 | 5 | 5 | 3 |

Across 225 artificial worlds, 54 choose SENSE. These are deterministic grid counts, not empirical choice frequencies. Gross information values in this grid belong to {0,1/8,1/4,3/8,1/2}. Increasing q weakly increases the value of sensing; increasing c weakly decreases its selection region. Equality is a material boundary: e.g. q=3/4, b=3/8, c=1/8 has G=1/8 and therefore does not sense. At b=1/2, q=3/4, c=1/8, M=1/2, U=3/4, S=5/8 and SENSE is selected.

## Replay and internal audit
Primary JavaScript generator: research/validation/r327_s123_quality_cost.js (blob 17e4793ed2443a49670de94139dc7d8e660a6c14). Persisted full 225-row JSON: research/validation/R327_S123_ALL_225_SENSOR_QUALITY_COST_WORLDS.json (blob 0d5adcf7f518b78d730e34711cc08139f209ad8a). The V8-adapted execution of the persisted generator reproduced the remote JSON byte-for-byte. A separate exact BigInt closed-form comparison verified all 225 remote rows and all nine data fields; all 18 overlapping original R327 world values and decisions match the original persisted R327 JSON.

An independent Python Fraction no-import auditor was tested locally in normal and optimized modes on an independently generated, semantically identical 225-world receipt; all 225 worlds passed and ten deliberately corrupted receipts were rejected. Its archived source blob matches the locally tested bytes (4bfab2edb3518db4f04d92fc3ec1fb3a2c904d9f). The archived Python auditor has not yet been run natively against the actual remote JSON file. Native Node CLI replay is also NOT_RUN. These are execution gates, not claims of scientific validation.

## Scientific limits and acceptance
The extension supports only an exact conditional decision rule for this finite binary symmetric sensor world, grade E1_SYNTHETIC_ONLY. The full R327 project-defined E1 acceptance does not automatically transfer to S123. This S123 extension has no CI run, no external independent researcher, no human behavior, no held-out human prediction, no calibration, no historical E3 and no general POMDP solver validation. No human or historical result was inferred from the 54/225 grid count. R073 scoring and PESEN v0.1 remain frozen. Original239 v7.8 and the 154-item queue remain unchanged.

# R282 ODD 2020 — Complete seven-element agent-based model description

**Research ID:** R282 · **Model:** two interacting binary agents · **Frozen protocol:** [5447354b](https://github.com/edwardsage419/Psychohistory-Research/commit/5447354be84992df49810b59cd258405851d2eb9) · **Evidence:** finite artificial E1, no real participants.

This description follows the updated ODD model documentation framework of Grimm et al. (2020), *JASSS* 23(2):7, https://doi.org/10.18564/jasss.4259. It is a complete ODD documentation instance for an invented example, **not** an independent ODD standards certification or empirical replication of Grimm's model.

## 1. Purpose and patterns
Investigate reproducibility failures when two network-connected agents' activation schedule is undocumented. Given identical frozen primitive initial states and disturbance bits, compare synchronous and two sequential activation orders. Observable patterns: exact full sequence (t0,t1,t2), end-of-run joint state, joint end-state distribution, paired trajectory differences. It is not a model fitted to real human groups, and there is no historical prediction.

## 2. Entities, state variables, and scales
Two persistent agents **A and B** with binary state a,b∈{0,1}. A and B observe one another over a single permanent undirected dyadic interaction edge; there are no spatial coordinates or heterogeneous demographic attributes. Time is discrete t∈{0,1,2}, two transition epochs after initialization. Input bits a0,b0,eA0,eB0,eA1,eB1 are all 0/1. Source index ranges 0…63. All states, disturbances and transitions are exactly deterministic conditioned on sixbit source and schedule.

## 3. Process overview and scheduling
At t=0 assign a0,b0. At each epoch t=0,1, read the **next fixed disturbance pair** (eAt,eBt). The update map for each agent is its peer's state XOR its own disturbance bit. Precisely:
* **SYNC:** simultaneously compute a'=b XOR eA and b'=a XOR eB from the **old** time-t states.
* **A_THEN_B:** compute a'=b XOR eA, then compute b'=a' XOR eB using **new a**.
* **B_THEN_A:** compute b'=a XOR eB, then compute a'=b' XOR eA using **new b**.
Persist both newly computed states at t+1, for two epochs. No independent update order randomness exists: schedule is a mandatory experiment parameter. Execute all 64 primitive source indexes in ascending order per schedule; these source indexes are enumeration keys, not pseudorandom seeds. Record complete t0, t1, t2 traces.

## 4. Design concepts
Basic principles: two-site binary interaction with perturbation, intended only as an algorithmic reproducibility case. Emergence: joint-state probabilities and schedule-level distinctions emerge from repeated updates. Adaptation and learning: **none**, update rule stays fixed. Objectives and decision-making: **none**, binary states are not utilities, opinions or beliefs; XOR is synthetic. Prediction: exact final state conditional on primitive stream, and frequency across the full uniform stream. Sensing: each agent reads one peer state; in sequential policies, the latter agent can read updated peer value. Interaction: two-agent dyad. Stochasticity: solely the six equiprobable primitive source bits; the simulation transition is deterministic. Collectives: a fixed pair, no networks of more than two. Observation: sixbit source, schedule, all time states and final joint state. No real-world calibration or inference.

## 5. Initialization
Source ID i∈{0,…,63} maps bijectively to `format(i, '06b')` interpreted in exact positional order `a0 b0 eA0 eB0 eA1 eB1`. The exact complete primitive sample space contains 64 ordered sources per schedule, each probability mass **1/64**, regardless of which activation schedule is run. Initial state is the first two bits. All disturbance bits are fixed once by the source ID. There is **no runtime pseudo-random number generator**, so recording only a nominal integer seed without this mapping would be inadequate. Input source i=1 (000001) yields t0=00,t1=00; t2=01 for SYNC and A_THEN_B and t2=11 for B_THEN_A.

## 6. Input data
There is **no empirical or external input data**. All sixbit inputs are artificial, exhaustively enumerated and equiprobable. The complete ordered primitive source index, sixbit input and simulation policy are persisted verbatim in `R282_ALL_192_ORIGINAL_ODD_SCHEDULE_SOURCES.csv` (generated deterministically by `r282_exact_odd_replay.py --emit`). The result JSON and SHA256 receipt bind aggregate claims to archived source bytes. Neither the GitHub Actions runner nor Python global random state can change results. The numerical counter `source_index` is not a stochastic PRNG seed and should not be misdescribed as one.

## 7. Submodels
Exactly three mutually exclusive activation/scheduling submodels are defined in section 3; each reuses the deterministic social copying XOR update. No additional hidden agent rule, utility optimizer, learning component or death/birth process. Schedules have no fitted parameters. Compute `a_{t+1},b_{t+1}` with the formula applicable to the chosen schedule; never silently substitute one schedule for another. Versioned executable: `r282_exact_odd_replay.py`. The exact six-bit semantics, full time states, algorithmic update order, Python3.11/3.12 conformance, separate analytical checks and machine receipts are part of the complete reproducibility contract.

## Reproduction instructions and falsification boundaries
Run `python research/R282/r282_exact_odd_replay.py --test` and `python research/R282/r282_exact_odd_replay.py --emit` from repository root with Python 3.11 or 3.12; standard library only. Verify all 192 original-source rows, the result JSON and the SHA256 receipt. Frozen analytic prediction: each schedule's t2 state is uniform over 00,01,10,11 (16/64 each), but paired schedule disagreement vs SYNC appears in 32/64 sources at t1 and 48/64 at t2. Independent third CI audit recomputes every row **without importing the model implementation**. Negative cases must reject an incomplete ODD missing any of these seven sections. Evidence is self-consistency and source-complete software replay E1, not outside model validation or a real human behavioral mechanism.

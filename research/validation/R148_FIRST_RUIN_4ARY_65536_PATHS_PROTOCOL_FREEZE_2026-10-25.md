# R148 independent first-ruin path enumeration prescore freeze
Date: 2026-10-25. Parent main HEAD at freeze: 907b93e3b5ade0249f97d7e6bb21f3fc0256fb83.
Research class: E1 synthetic model only. This is an additive audit of existing bounded R148. R073 and PESEN v0.1 remain frozen.

## Exact frozen model
Use the already archived R148 original rules unchanged: S0=6, capacity 8, eight years, policies OPEN, QUOTA, ADAPT. OPEN requests 2; QUOTA 1; ADAPT requests 0 for S<=2, 1 for S=3..6, 2 for S>=7. Independent infrastructure failure F=1 with probability 1/4 overrides QUOTA/ADAPT to OPEN request 2, with annual fees still due. Independent climate shock D=2 with probability 1/4 follows extraction. H=min(S,request); B=max(0,S-H-D); S'=min(8,B+1) for 1<=B<=6, otherwise min(8,B). S=0 absorbing. Annual fees OPEN 0, QUOTA 1/8, ADAPT 1/4. These equations belong to this project's synthetic model and are not the published Ostrom equations.

## Prespecified independent experiment
At q=f=1/4 enumerate every ordered pair of eight-bit weather and failure histories: 2^16=65536 paths per policy, 196608 total. Assign exact integer numerator weights by multiplying 3 for each zero event and 1 for each one event; common denominator 4^16=4294967296. For each policy record the first year of stock zero, t=1..8, or SURVIVED_8. Record weighted mass, cumulative harvested units, and the exact eight-year fee ledger. Confirm 65536 paths per policy, total mass 4^16, ruin histogram sums to total mass, S=0 never recovers, and published R148 terminal survival numerators: OPEN 0, QUOTA 1330196823, ADAPT 1499549355. Confirm published expected net harvest as a second checksum using exact integer numerators.

## Independent checks
A second implementation must use state-mass dynamic programming with an explicit first-ruin accumulator rather than the 65536 path loop, and compare the nine first-ruin/survival masses exactly. Negative controls: (1) resurrect stock from 0 must fail; (2) remove the fee after collapse must change the frozen net ledger for fee-bearing policies. Label any policy rank or first-ruin timing patterns exploratory, not predeclared hypotheses. No human or historical inference, no external independent replication claim.

## Acceptance and reproducibility
Commit protocol before writing production computation. Preserve executable source, complete integer receipts, audit, scientific report in distinct additive paths. Local exact checks required. Remote CI only if free billing can be confirmed; otherwise NOT_RUN. Before each write recheck main HEAD, path absence, and permissions, never overwrite concurrent work.

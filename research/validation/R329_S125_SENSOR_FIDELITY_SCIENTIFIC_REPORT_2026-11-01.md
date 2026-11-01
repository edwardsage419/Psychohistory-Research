# R329 S125 sensor fidelity, observation preferences, and EFE
Date: 2026-11-01 UTC. Scientific status: PARTIAL_E1_EXTENSION. Target (r,R329,S125-v1,finite_sensor_fidelity_pragmatic_epistemic_tradeoff).

## Source and freeze
Original R329 bounded constructed E1 acceptance and all original files remain unchanged. Prescore freeze committed first at 84161eebcee14924d58df49874f21262f20525fb. Implementation and 720 source atoms / 90 worlds committed later at 22c453b744e1937becdbff1e385dcdd203fbe6b7. The original 18 q=3/4 worlds were independently matched on policy, both EFE scores and information values at nine-decimal precision.

The finite grid is belief b in {1/4,1/2,3/4}, observation preference c in {1/2,3/4}, candidate sensor accuracy q in {1/2,5/8,3/4,7/8,1}, and cost k in {0,1/8,1/4}. The baseline sensor accuracy is 1/2 and cost 0. Each world has two policies and four hidden-state/observation joint atoms. Total: 90 worlds and 720 atoms, including 36 zero-mass atoms for perfect sensors. 45 worlds choose PRECISE, 45 choose NOISY. Selection uses original NOISY-on-tie rule.

## Exact mechanism
G(a)=-E[ln C(O)]-I(S;O|a)+cost(a). Independent risk+ambiguity score equals G within 1e-12. Define A(q)=G(NOISY,k=0)-G(PRECISE,k=0). A positive advantage exceeding cost selects PRECISE, subject to frozen 1e-14 tie tolerance.

Since P(O=1|q)=1/2+(q-1/2)(2b-1), the exact analytic decomposition is
A(q)=I_b(q)+(q-1/2)(2b-1)ln[c/(1-c)].
Here I_b(q)=H(1/2+(q-1/2)(2b-1))-H(q), with binary Shannon entropy H and 0ln0=0. The second term reflects the expected preference for observation outcomes. Its sign can oppose the information gain. This observation preference is a feature of the constructed model and should not be mistaken for a general welfare claim.

## Six prespecified accuracy series
The five values in each row correspond to q=1/2,5/8,3/4,7/8,1 and represent A(q) at zero cost.

| belief | C(O=1) | A(q) sequence | shape |
|---|---|---|---|
| 1/4 | 1/2 | 0, 0.023750969, 0.099228094, 0.244316213, 0.562335145 | increasing |
| 1/4 | 3/4 | 0, -0.044912299, -0.038098443, 0.038326409, 0.287682072 | nonmonotonic |
| 1/2 | 1/2 | 0, 0.031583942, 0.130812036, 0.316377019, 0.693147181 | increasing |
| 1/2 | 3/4 | 0, 0.031583942, 0.130812036, 0.316377019, 0.693147181 | increasing |
| 3/4 | 1/2 | 0, 0.023750969, 0.099228094, 0.244316213, 0.562335145 | increasing |
| 3/4 | 3/4 | 0, 0.092414237, 0.236554630, 0.450306017, 0.836988217 | increasing |

The unique nonmonotonic series is b=1/4,c=3/4. Raising sensor fidelity from q=1/2 to 5/8 makes PRECISE worse under the frozen EFE objective even at zero cost. At q=7/8 and 1 the increased information gain eventually dominates the unfavorable observation-preference shift. This is a finite model counterexample to the blanket claim that a more accurate sensor always improves this particular EFE policy score.

| candidate sensor q | PRECISE chosen among 18 worlds | NOISY chosen |
|---|---:|---:|
| 1/2 | 0 | 18 |
| 5/8 | 5 | 13 |
| 3/4 | 8 | 10 |
| 7/8 | 14 | 4 |
| 1 | 18 | 0 |

## Checks and limitations
Primary pure JavaScript generator reproduced the persisted 720-row CSV and 90-world JSON exactly when executed from archived source in V8. Independently written no-import JavaScript auditor used the KL plus conditional-entropy expression, checked every rational source atom, 90 scores and choices, all six series, 18 original R329 worlds and 36 zero-mass atoms. Ten actual negative controls were rejected after correcting an initially ineffective policy mutation. Independent local Python Fraction-based marginal and entropy calculation reproduced all six advantage series and 45/45 decisions. This is internal nonblind programmatic and mathematical checking; external independent replication is NOT_RUN.

No human data, sample-out evaluation, calibration, empirical identification, historical event evidence, original author model reproduction, or new formal full-series acceptance. E1 constructed only; E2 and E3 unchanged. No Actions were triggered, CI status is separately checked. R073, PESEN v0.1, original239 v7.8, and pending154 remain frozen. No model fusion or personal product work.

# R309 S105: exact two-step artificial SIR, extinction and second-step infection

Date: 2026-10-31 UTC. Scientific state: **PARTIAL_E1_ARTIFICIAL_TWO_STEP**. Track: R. This is an additive finite mathematical investigation, not a change to the original R309 bounded E1 acceptance.

## Prescore protocol and source identity
S105 prescore protocol: `research/validation/R309_S105_TWO_STEP_SIR_PRESCORE_FREEZE_2026-10-31.md`, committed **a68643bcb79b49f1d96a491d63332a195175cad9** before computing S105 scores. The prior R309 one-step model and original results were read in advance, so this is **nonblind internal** work.

The underlying model is the project-defined discrete synchronous five-agent SIR approximation. It is distinct from Kermack and McKendrick's 1927 continuous mathematical theory (DOI 10.1098/rspa.1927.0118). Original R309 source: `research/R309/R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv`, remote Git blob **2d3034e02c83eeaaffeec7cfc704eb48047134f6**. The original-source byte reconstruction produced the same Git blob and SHA256 **9470c1e1c880f51da5c11377b6cc8be7f799542d0cebd1f82d4fc3539cabd134**. Original R309 21 states, 9 p/q combinations and 1,134 one-step source events were preserved without edits.

## Exact two-step design
Each step uses the original frozen rule. Every initially susceptible person has independent per-contact probability p of infection from each initially infectious person. Only initially infectious people may recover with probability q during that step. New infections become eligible for contacts and recovery at the **next** step. p,q stay fixed across both steps. Let K be the complete one-step transition matrix on 21 count states. The S105 two-step distribution is exactly `K²(start,final)=sum_mid K(start,mid)*K(mid,final)`.

All **189** artificial initial worlds were evaluated against all **21** final states, producing **3,969 exact rational probability cells**, including zeros; **459 cells have positive mass**. The producer enumerated **1,764** positive-first-step midpoint / second-step event evaluations for its additional second-step infection indicator. The output CSV and JSON are complete, deterministic and Git-blob verified. These worlds are correlated artificial parameter-state cases, not independent epidemics or human observations.

## Main numerical results
For initial (S,I,R)=(3,2,0) and p=q=1/2:

| Frozen metric | Exact result | Decimal approximation |
| --- | ---: | ---: |
| Extinction after step 1, P(I1=0) | 1/256 | 0.00390625 |
| Extinction after step 2, P(I2=0) | 6545/131072 | 0.0499344 |
| Extinction added at step 2 | 6033/131072 | 0.0460281 |
| At least one new infection at step 2 | 4097/8192 | 0.5001221 |
| E[S2] | 675/4096 | 0.1647949 |
| E[I2] | 9053/4096 | 2.2102051 |
| E[R2] | 21/8 | 2.625 |

The two-step extinction probability is larger than the single-step baseline in **65 of 189** artificial worlds. All 189 obey `P(I2=0)>=P(I1=0)`, because disease-free I=0 states are absorbing. **144 worlds** have positive two-step extinction probability, compared with **124** having positive one-step extinction probability. This is a finite mathematical observation, not a frequency of real outbreaks.

The frozen timing counterexample remains: start (3,2,0), p=q=1 yields deterministic step-one (0,3,2) and deterministic step-two (0,0,5). The three newly infected individuals recover at the second step, not the first. With q=0 and initial I>0, no extinction by time two; with p=0,q=1, all original infectives recover in the first step. All final distributions normalize exactly to one, conserve N=5, and respect monotone susceptible depletion and permanent recovery.

## Reproduction and independent audit
Producer: `research/validation/r309_s105_two_step.py`, run with `python research/validation/r309_s105_two_step.py`. It reconstructs and hashes the original source before generating output. Local environment: Python **3.13.5**. Actual local CSV SHA256 **e9734fbe7a9c9ae28431b20295c27cf3d8a860abf49d155f859489b39463d4f6**, JSON SHA256 **8404c0ed201a4b63340decd85d2ce6f1b4ab66413262fc8345021be41857d781**. Remote Git blobs: CSV **3aefbbc3b5042b6a93ed4e7b8017d9abb7ba9b53**, JSON **6a6c3853de4d557ec4e72ebc647e95272dd9e52d**, matching the independently generated local bytes.

B auditor `research/evidence_audit/B_R309_S105_MICROSTATE_AUDIT.py` enumerates independent binary contact and recovery assignments, importing neither producer nor original R309 module. Its complete two-step distributions and 189 world summaries match every S105 archived result. Eight mutation controls all rejected in ordinary Python and Python `-O`. B audit is nonblind, internal, artificial E1. The source-byte match and independent algorithm strengthen computational confidence; they do not create independent empirical replication.

## Limits and open acceptance gates
No observed pathogen transmissions, measured epidemic trajectory, empirical calibration, causal effect, social norm diffusion, opinion adoption, human E2 or historical E3 were evaluated. Two-step prediction is conditioned on known p,q; it is not held-out prediction with estimated parameters. No empirical calibration, uncertainty intervals or cross-site transport. No external independent research team. Original R309 `CLOSED_BOUNDED_E1_ARTIFICIAL_R309_FIVE_AGENT_SIR_ONE_STEP` remains unchanged. S105 remains PARTIAL. R073 and PESEN v0.1 remain frozen.

No paid data, API, cloud, GPU or GitHub Actions was used. Current-turn CI **NOT_RUN**; account billing and free runner quota **NOT_VERIFIED**. Continue R310 or a complementary R309 extension only after fresh HEAD, index/queue, other-track and PR checks. Global taxonomy, model fusion and personal decision product development remain deferred.

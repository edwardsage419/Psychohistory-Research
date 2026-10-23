# R303 prospectively frozen: observational acquisition versus imitative expression under vicarious consequence

Date 2026-10-23 Asia/Taipei. Original239 **03-001 Social Learning Theory** P1. Freeze **before** computational model/results. Scope **bounded synthetic E1 illustration**, not Bandura's original fitted equation, child experimental dataset recreation, human or animal E2 replication, or historical E3. R073/PESEN v0.1 frozen. Complete R-series before taxonomy and fusion.

## Primary first-hand author and earlier R063 scope

Bandura, A. (1965), **Influence of models' reinforcement contingencies on the acquisition of imitative responses**, *Journal of Personality and Social Psychology* 1(6):589–595, DOI https://doi.org/10.1037/h0022070. [Original 1965 paper reprint](https://www.psychologywizard.net/uploads/2/6/6/4/26640833/bandura_1965.pdf), NLM PubMed PMID14300234 https://pubmed.ncbi.nlm.nih.gov/14300234/. The actual human experiment studied film-mediated model rewarded / punished / neither, imitation spontaneous vs subsequent reward-incentivized reproduction. Original description: punishment lowered first imitation, but later direct incentives removed the between-treatment performance gap. This manuscript is an empirical **motivation and target qualitative distinction**, NOT the source of the numerical gate equation below. Bandura, Ross & Ross (1961), *Transmission of aggression through imitation of aggressive models*, *Journal of Abnormal and Social Psychology* 63:575–582 DOI https://doi.org/10.1037/h0045925, relates to observational imitation but is not rereplicated here.

Historical [R063 Najar et al. 2020 social imitation metaVS/VS2 audit](../research/R063/R063_EVIDENCE_AUDIT.md) read original fixed MATLAB code, social learning rates and author Figure6 summary and did **not** obtain complete locally verified human trial CSV with full out-of-sample model validation. That original source and earlier scoped empirical claims **stay as R063**. R303 does NOT use Q values, pseudo-rewards, social-rate adjustment, learned demonstrator reliability, or Najar trial-level data. Instead it tests the logical divergence of **acquired observational trace** and **currently expressed copying response** after observed reward/punishment. This is a new illustrative E1 form, not another independent Bandura real experiment. No original Bandura 1965 raw behavior CSV, child IDs, effect sizes or original model-fit estimates available in this study.

## Precisely defined **new original-to-project toy formalization** (never attributed to Bandura)

Four independent scalar synthetic gates for each demonstration:
- attention A∈{0,1/2,1}
- retention R∈{0,1/2,1}
- motor reproduction P∈{0,1/2,1}
- baseline motivation M∈{0,1/2,1}

Product formalization is **solely an explicitly posited mathematical mechanism of this project**, not a Bandura (1965) statistical specification. Define acquired trace probability Q_acquired=A*R, potential producible response Q_available=Q_acquired*P. There is no direct learner reinforcement in the toy world.

Observable consequence to the demonstrated model C∈{REWARDED,NO_CONSEQUENCE,PUNISHED} with fixed **invented, prospectively frozen** spontaneous expression scaling c(C)=1,1/2,1/4 respectively. The output has two stage sources:
1. SPONTANEOUS: conditional expression factor e=M*c(C); response probability p_spont=Q_available*e.
2. INCENTIVIZED: universal subsequent positive incentive intervention sets **expression factor e=1**, irrespective of C and M, response probability p_inc=Q_available. It does *not* change Q_acquired, P, observational training or direct learner experiences.

This structure **assumes** observational acquisition unaffected by observed model consequences. A discovered equality of incentivized imitation across consequence worlds follows algebraically from this assumption and cannot independently confirm Bandura's causal result or show equal true acquired learning in actual children.

Complete grid: 3^4=81 factor quadruples ×3 vicarious consequences = **243 unique artificial worlds** ×2 time/test phases = **486 fully labeled original source rows**. Sources do not represent human participants, trials, fit parameters or repeated independent evidence. All numbers exact Python Fraction.

Every original source contains world ID, gates A,R,P,M; C and consequence factor; phase; latent acquisition probability, availability probability, expression factor, response probability, counterfactual no-observation response baseline0, and difference between incentive and spontaneous expressions (the difference is computed at world level and repeated in both phase rows). We explicitly do **not** interpret Q_acquired as an observed independently identifiable psychological state.

## Frozen exact comparisons and negative controls

Across each of 81 gate tuples, all three C settings must have exactly the **same acquisition trace** A*R and the **same incentivized response** A*R*P. Under M>0 and Q_available>0, spontaneous response probabilities ordered REWARDED > NO_CONSEQUENCE > PUNISHED; if any required stage gate is zero, ordering can be weak/equality.

For every fixed world, incentivized response probability >= spontaneous. Rewarded spontaneous=Q_available*M, no-consequence spontaneous=Q_available*M/2, punished spontaneous=Q_available*M/4; incentivized probability=Q_available. Acquired trace zero when A=0 or R=0; potential response zero when P=0 even if acquired trace positive; M=0 blocks **spontaneous** response regardless of consequence while INCENTIVIZED output can remain positive if A,R,P>0. Explicitly, later incentive cannot undo A=0,R=0 or P=0.

Frozen positive case A=R=P=1,M=1/2: acquisition=1, availability=1; spontaneous rewarded1/2, neutral1/4, punished1/8; incentivized any consequence1; the spontaneous/incentive performance gaps =1/2,3/4,7/8. At A=0,R=P=1,M=1: acquisition0 and both phases expression0; A=R=1,P=0,M=1: acquisition1 but both expressed0; A=R=P=1,M=0: spontaneous0 across all C, incentivized1. For every phase probability in [0,1] and all 486 rows unique.

No claim of real-world violence imitation, Bandura treatment effect size, observational learning rate, probability calibration, generalization to groups or original Najar human results. Individual phase counts and world ratios **do not** establish empirical 1965 learning mechanisms or 2026 human reproduction.

## Reproducible and evidence gates

Require executable Python3.11/3.12 --test/--emit, exact original 486 source CSV and full 243-world dual-phase JSON, SHA256 receipt. Require independent no-import reconstruction with separate expression procedure and adversarial tampering for C mapping, phase, nonexistent world, source duplication, Q acquisition/performance conflation, and SHA/JSON. Three real GitHub Actions success jobs Python3.11+3.12 and independent 3rd archiver permanent main original sources. Only then declare **CLOSED_BOUNDED_E1_ARTIFICIAL_R303_ACQUISITION_EXPRESSION** and update original239 v1.7 one row **03-001** only, pending46→45, primary190→191, preserve R063 social-learning historical evidence at its own location and do not promote Bandura/Najar human data. R073/PESEN v0.1 remain frozen.

# R299 prescore freeze: Model-Free Reinforcement Learning, TD(0) delayed credit and Monte Carlo return

Date 2026-10-23 Asia/Taipei. Original 239 item **02-005 Model Free Reinforcement Learning**, P1. Freeze before any new R299 executable or computed output. Accept only exact bounded synthetic E1. No human/animal E2 or historical E3. Historical R073 and PESEN v0.1 remain frozen; all R-series original-candidate research before taxonomy and model fusion.

## Original first-hand sources and non-duplication

Sutton, R. S. (1988), "Learning to Predict by the Methods of Temporal Differences", *Machine Learning* 3:9–44, DOI https://doi.org/10.1007/BF00115009. Original author PDF https://jmvidal.cse.sc.edu/library/sutton88a.pdf and original bibliographic record https://mlanthology.org/mlj/1988/sutton1988mlj-learning/. Sutton & Barto (2018), *Reinforcement Learning: An Introduction*, 2nd ed., Chapter 6 temporal-difference prediction distinguishes TD bootstrap from Monte Carlo full returns; book original authors' web mirror https://incompleteideas.net/book/RLbook2020.pdf. Neither original source's human/animal experimental data nor broad convergence assumptions are verified here.

Historical R063 authored Najar et al. (2020) metaVS / VS2 social imitation Q shaping and Fig6 source review, not independent Sutton (1988) finite single-agent TD prediction. Preserve R063 original author commit 554ee8007ff6fd1c51cd68d7d254f22a34e6dab1 and `research/R063/R063_EVIDENCE_AUDIT.md` as scoped historical evidence for 02-005. R297 Q Learning off-policy MAX *control* (original 02-003) is structurally related but not identical to R299 fixed-policy state-value *prediction*. R298 uses supplied transition model planning (02-004), whereas R299 receives a fixed observed sequence with no transition probability estimation or planning. Do not equate mathematical overlap with new independent human replication.

## Frozen deterministic episodic reward prediction task

A fixed-policy episodic two-step sequence per episode S0 --(r=0)--> S1 --(r=R)--> terminal; R ∈ {0,2}. Every state value starts 0. Model-free TD0_ONLINE and MC_FULL_RETURN independently observe precisely the **same complete return** in each episode; no random state transitions, not a distribution over 120 independent people. Discount γ∈{0,1/2,1}; step α∈{1/2,1}; algorithm ∈{TD0_ONLINE,MC_FULL_RETURN}; training epoch n=0..4. Total **2 rewards ×3 gammas ×2 alphas ×2 algorithms=24 worlds**, exactly **120 labeled original epoch state rows** (one original world × epoch each).

Online TD0 update order each new episode: before observing the terminal step, S0 value update uses **previous episode's** V(S1):
δ0=γV_old(S1)−V_old(S0); V_new(S0)=V_old(S0)+αδ0.
Then S1 sees terminal reward R:
δ1=R−V_old(S1); V_new(S1)=V_old(S1)+αδ1.
No same-episode look-ahead from reward to S0's TD target; if α=1 then n=1 TD value(S0)=0, and n=2 TD value(S0)=γR.

Monte Carlo full-return comparator waits until the entire episode has ended and then uses G(S0)=γR, G(S1)=R:
δ0=γR−V_old(S0); V_new(S0)=V_old(S0)+αδ0.
δ1=R−V_old(S1); V_new(S1)=V_old(S1)+αδ1.
These are **two model-free policy evaluation updates**, not two action-control policies. There is no action selection, Bellman optimality MAX, transition-model learning or oracle leakage into updates.

Frozen source fields: model family, fixed true terminal reward R, gamma, alpha, epoch, old/start-of-episode V(S0), old V(S1), S0 TD error δ0, S1 terminal TD error δ1, S0 target, S1 target, V(S0) after episode, V(S1) after episode, true expected policy values gamma R and R, absolute errors. At epoch0 pre-training all V=0 and errors/targets recorded as zero with no training event. All exact Fraction, complete 120 rows.

## Pre-registered closed-form predictions, negative controls and failure boundaries

Let q=1−α and n≥0.
- Both models V_n(S1)=R[1−q^n].
- Monte Carlo V_n(S0)=γR[1−q^n].
- TD0_ONLINE V_0(S0)=0. For n>=1, V_n(S0)=γR[1−q^n−α n q^(n−1)], where 0^0=1 at n=1 in this algebraic formula. In particular n1 TD0(S0)=0 even with positive reward, and MC(S0)=αγR. Under 0<α≤1, 0≤γ≤1, R>=0, MC V(S0) >= TD0 V(S0) within the fixed task. Equality for R=0 or γ=0 or n=0, not a claim of global predictive dominance.
- At γ=α=1/2,R=2,n4: true S0 policy value=1, TD0 V(S0)=**11/16**, Monte Carlo V(S0)=**15/16**, both V(S1)=15/8.
- At α=1, γ=1/2,R=2: TD0 S0 after first episode 0, after second 1; MC S0 after first 1.
- For R=0, all values and errors remain zero; for γ=0, S0 cannot learn terminal reward and both S0 predictions remain zero while S1 can learn R. These are negative controls, not evidence for psychological insensitivity.
- All 120 source records must agree via direct simulation and separate exact closed form. Source order and initial zero handling fixed; every world has 5 consecutive epochs. Preserve state-episode target ordering. Independent third-party auditor must not import main module and must reconstruct each update, epoch-level errors, reward/discount labels, all source records, and stored results; reject tampered sources, missing/misordered epoch, wrong target, swapped TD update order, incorrect recorded output, digest tampering.
- Both algorithms are bootstrapping vs full-return forms of **model-free evaluation**; do not claim that MC requires a model. Neither finite training exact ratio is a real-human learning-rate estimate or original paper replication.

## Acceptance and versioning gate

Ship executable --test/--emit compatible Python>=3.11, original 120-source CSV, 24-world full result JSON, source/result SHA256 machine receipt, independent no-import audit tests and scientific report. Run real GitHub Actions 3 successful jobs (Python3.11 and Python3.12 plus separate independent source audit/archiver) to permanently commit all source bytes to main. Only after checked CI success may mark R299 CLOSED_BOUNDED_E1 and update original239 provenance crosswalk v1.3 changing **only original 02-005**, retaining R063 scoped evidence paths and explicit non-equivalence to R063 human results; pending50→49. Original catalogue itself remains untouched. R073/PESEN v0.1 frozen.

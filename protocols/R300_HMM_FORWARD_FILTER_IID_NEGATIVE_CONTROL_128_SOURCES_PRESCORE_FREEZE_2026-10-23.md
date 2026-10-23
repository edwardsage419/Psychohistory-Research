# R300 prospective protocol freeze: Hidden Markov Model (02-008) forward filtering vs i.i.d. hidden-state negative control

2026-10-23 Asia/Taipei. Original 239-candidate P1 ID **02-008 Hidden Markov Model**. This protocol is frozen **before** model source/results. Study is exactly bounded synthetic mathematical E1, **not** trained HMM on humans, animal data, speech, historical events, or new E2/E3. Original R073 and PESEN v0.1 remain frozen. All R-series first, then taxonomy, then fusion.

## Primary scientific source and previous evidence boundary

Rabiner, L. R. (1989), *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, *Proceedings of the IEEE* 77(2):257–286, DOI https://doi.org/10.1109/5.18626, original paper PDF https://web.mit.edu/6.435/www/Rabiner89.pdf. This review describes HMM hidden state probabilities, observable emissions, the forward procedure and decoding/estimation tasks. Earlier Baum and Petrie (1966) mathematical foundations motivated Markov-dependent latent-state inference. R300 only covers **known-parameter filtering and predictive likelihood**, and does not implement Baum–Welch, Viterbi decoding or identify transition/emission parameters from human data.

The 2026-10-18 original239 candidate overlay and crosswalk v1.3 have **no verified itemwise primary R research for 02-008**. Related Q-learning and model-free RL (R297/R299) are distinct from hidden-state probabilistic inference, and neither R063 Najar metaVS nor R073 held-out human experiment may be reassigned as original 02-008 human E2 evidence.

## All synthetic source cells

Latent state H_t∈{0,1}, observed symbol Y_t∈{0,1}. Initial P(H_1=0)=P(H_1=1)=1/2. Emission P(Y_t=H_t | H_t)=3/4; P(Y_t ≠ H_t | H_t)=1/4, conditionally independent across time given states.

Two **known-parameter** worlds:
1. PERSISTENT_HMM: P(H_t=H_{t-1})=3/4, P(switch)=1/4.
2. IID_HIDDEN_NEGATIVE_CONTROL: P(H_t=H_{t-1})=1/2, P(switch)=1/2 independent of previous state. This remains a valid HMM but the latent sequence is actually i.i.d., eliminating hidden-state memory.

For **each** world, exhaust all 2^4=16 full four-symbol observation strings in binary lexicographic order. For each full string, record time-prefix lengths t=1,2,3,4. Thus **2×16×4=128 complete labeled original artificial source rows**; each row is a (world, full four-symbol observation string, prefix length), not a real participant or independently sampled trajectory. It is intentional that the same t-prefix is repeated under different complete length4 strings in order to make the entire source provenance explicit; probability normalization across t must deduplicate prefixes.

Every source row stores world, assumed stay probability, full observation string, current prefix, prefix length, emission accuracy 3/4, unnormalized forward α_t(H_t=0/1), likelihood P(Y_{1:t}=prefix), posterior P(H_t=1|prefix), predictive P(Y_{t+1}=1|prefix), and conditional latent prediction P(H_{t+1}=1|prefix). All Fraction exact, no floating point, random seeds, samples, or estimates. At t=4 next-observation prediction is out-of-prefix forecast only and **not scored on a subsequently observed sample**.

## Frozen recursion and independent enumerative proof

Forward recursion for prefix y_1..y_t: at t1 α_1(h)=1/2 * emission(y1|h). At t>=2 α_t(h)=emission(y_t|h) × Σ_{hprev} α_{t-1}(hprev) T(h|hprev). Normalization L_t=α_t(0)+α_t(1), posterior p_t=α_t(1)/L_t.

One-step prior hidden probability pnext = pstay*p_t + (1-pstay)*(1-p_t). Predictive observation P(Ynext=1)=pnext*(3/4)+(1-pnext)*(1/4)=1/4+(1/2)*pnext.

Mandatory independent original-source auditor **does not import model code** and for every prefix enumerates all 2^t hidden paths to sum **full joint H and Y probabilities**, obtaining independent evidence and posterior. For next observation prediction, independently enumerate all paths length t+1 with required Y_next=1 and divide by evidence. Therefore 128 original source rows must exactly match independent brute-force enumeration. For each t=1..4 and both worlds, the sum of exact evidence across the 2^t distinct prefixes must be exactly 1; don't sum repeated rows across different 4-symbol suffixes.

Pre-specified negative controls:
* IID hidden world: for every t, posterior p_t=3/4 if last observed bit is 1, else 1/4; next-symbol predictive P(Ynext=1)=1/2 independent of all observed history, and prefix evidence=(1/2)^t.
* PERSISTENT world: two histories of equal length with same final observed bit but different earlier observations, e.g. 1110 and 0000, must have **different** posterior H4 and different next-symbol probability. Same latest observation is not sufficient when latent state persists.
* Both worlds: all hidden and observation probabilities in [0,1]; α0+α1=likelihood; positive evidence; exact probabilities sum to one over unique observation strings per length. Permuting hidden state names together with appropriately redefined parameters would preserve observable distributions; present results **do not prove real psychological hidden state labels or identifiability**.
* Both worlds share the same observations and marginal one-symbol distribution P(Y_t=1)=1/2, so one-symbol count alone cannot establish persistent latent dependence.

No fit to empirical speech/cognition and no claim Rabiner 1989 original application reproduced. Independent auditor must reject manipulated emission, transition, source likelihood, posterior, prediction, duplicate/missing row, result JSON or SHA receipt.

## Acceptance criteria

Python>=3.11 --test/--emit produces 128-source CSV, all exact forward result JSON and SHA256 receipt. Third-party independent original source program and genuine adversarial unit tests. GitHub Actions matrix Python3.11/3.12 plus independent third archive job all completed/success, generated source/result original bytes permanently committed to main. Only then formal R300 E1 acceptance and crosswalk v1.4 updating **only original 02-008**, preserving earlier R299/R063 and 239 original candidate identities. Pending original P1/P2 primary links 49→48. No added human/animal E2 or history E3.

# R329 S125 sensor fidelity and pragmatic preference: prospective E1 protocol
UTC freeze date: 2026-11-01. Baseline main: 1c032711eaa3cfb99b5e0526922a7bde0a87054a.
STATUS: PROTOCOL_ONLY. No S125 scores or results computed at freeze.
Target key: (r,R329,S125-v1,finite_sensor_fidelity_pragmatic_epistemic_tradeoff).
Preserve original R329 2026-10-24 protocol, source, E1 acceptance, R073 frozen scorer and PESEN v0.1. No R329 original file modifications.

## Model and universe
Use original constructed binary one-step EFE score and two policies. Hidden S in {0,1}; belief b in {1/4,1/2,3/4}; observation preference C(O=1)=c in {1/2,3/4}; PRECISE sensor accuracy q in {1/2,5/8,3/4,7/8,1}; NOISY accuracy fixed 1/2; PRECISE cost k in {0,1/8,1/4}, NOISY cost 0. Ordered Cartesian product b,c,q,k yields 90 worlds, each with 2 policies, 2 hidden states, 2 observations = 720 full joint atoms including zero mass at q=1. All state and observation probabilities use exact rational arithmetic. A zero mass atom remains present. This is an artificial E1 extension only.

## Frozen score and acceptance
For each policy a, joint j(s,o)=P(S=s)P(O=o|S=s,a), observation marginal m(o)=sum_s j(s,o).
Direct G(a)=-sum_o m(o)ln C(o) - sum_{s,o:j>0}j(s,o)ln[P(o|s,a)/m(o)] + cost(a).
Independent equivalent G(a)=KL(m||C)+sum_s P(S=s) H(P(O|s,a))+cost(a).
Zero terms use continuous extension 0 ln 0=0. Natural logs. Choose PRECISE only if G(PRECISE)<G(NOISY)-1e-14, else NOISY. Scores formatted to 9 decimals; score identity tolerance 1e-12; stored score comparison tolerance 5.1e-10.
For each b,c,q, define net advantage A(q)=G(NOISY,k=0)-G(PRECISE,k=0). Compare its sign, the cost threshold, and possible nonmonotonicity of A(q) over ordered q. Report all six b,c series, all 90 decisions, exact atom normalization, and 18 old R329 cases at q=3/4 with their frozen 9-decimal scores and policy labels. Do not presuppose the direction or number of any nonmonotonic series.

## Falsifiers and evidence gates
A new primary deterministic standard-library generator, 720-atom CSV and 90-world JSON, with executable tests. A separately written no-import B auditor must derive the alternative KL plus ambiguity formula, check complete unique universe, row identities, 90 choices, scores, all six advantage series and source replay; test deletion, duplication, probability alteration, policy alteration and metadata evidence-grade alteration as negative controls. Any failed check remains recorded and blocks extension acceptance. Freeze commit must precede scoring and implementation commit. Existing original R329 data and its Git blobs remain unchanged. External independent replication is NOT_RUN until actually performed; CI status must be queried and no GitHub Actions launched without verified free quota. Bounded E1 arithmetic success cannot promote E2 human or E3 historical claims. Original239 v7.8 and pending154 queue remain unchanged. Other tracks may write their own paths only. No extra cost.

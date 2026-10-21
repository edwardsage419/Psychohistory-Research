# R164 precode freeze: synthetic content-salience copying with finite copying weight and symmetric innovation

Date: 2026-10-21. Original catalog **P1 / 07-006 Content Biased Transmission**, verified from `docs/MODEL_CANDIDATE_CATALOG_v0.1.json`. R163 closed E1 and indexed on main at commit `e520ed420e5b3a33dcf2537df277952ef7a2f329`. The original priority/order stays fixed. This protocol is committed **before** the experiment's program, data and tests.

## Source inspection and external validity boundaries
Justin L. Barrett and Melanie A. Nyhof (2001), *Spreading Non-natural Concepts: The Role of Intuitive Conceptual Structures in Memory and Transmission of Cultural Materials*, *Journal of Cognition and Culture* 1(1):69–100, DOI [10.1163/156853701300063589](https://doi.org/10.1163/156853701300063589). [Oxford University research record](https://ora.ox.ac.uk/objects/uuid%3Aa6ed93bb-3ba0-4934-adec-9bb827cf8e9f) and English source abstract reviewed: expectation-violating items may have memory/transmission advantage in specific experimental settings. Original participant-level recall/serial transmission data and detailed trials are not replicated here.
Pascal Boyer and Charles Ramble (2001), *Cognitive templates for religious concepts: cross-cultural evidence for recall of counter-intuitive representations*, *Cognitive Science* 25(4):535–564 DOI [10.1016/S0364-0213(01)00045-3](https://doi.org/10.1016/S0364-0213%2801%2900045-3), original Elsevier research article and abstract checked. Authors found selective effects associated with specific kinds of expectation violations and inference potential in recall experiments in France, Gabon and Nepal. The article does not license treating every bizarre or salient item as maximally transmissible. We have not replicated any author recall percentages, materials, or cross-cultural sampling.
J. M. Stubbersfield, J. J. Tehrani and E. G. Flynn (2015), *Serial killers, spiders and cybersex: Social and survival information bias in the transmission of urban legends*, *British Journal of Psychology* 106:288–307 DOI [10.1111/bjop.12073](https://doi.org/10.1111/bjop.12073), [Wiley original abstract](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjop.12073) inspected, distinguishes choosing to receive, encoding/retrieval and choosing to transmit. The original 60-person chain and story datasets are not obtained.

Our experiment below is **new synthetic content A/B copying arithmetic** only, not memory psychology, religious belief modeling, emotional contagion or source-paper equation/experiment replay. Exactly **E1 synthetic math** and **E2/E3=0**. Synthetic labels A/B have no religious/political/ethnic or real-person meaning.

## Freeze 72 exact content-selection scenarios
Artificial binary cultural trait A has initial frequency p0∈{1/5,2/5,3/5,4/5}; an exogenously assigned content-attention multiplier r∈{1,2,4}; copy-by-content opportunity h∈{0,1/2,1}; symmetric replacement fraction e∈{0,1/4}. **4×3×3×2=72 distinct complete 5-observation trajectories t=0,1,2,3,4.**
At each generation:
S(p,r)=r*p/[r*p+(1-p)], which is a normalized *artificial content sampling weight*, not an actual cognitive recall probability.
q=(1-h)*p+h*S(p,r)
p[t+1]=(1-e)*q+e/2.
All arithmetic must be exact Python Fraction. Record every p[t], within-time S(p,r), q and next p[t+1]. No true efficacy, memorability, salience measurement or psychological parameter estimates. The multiplier is imposed solely as an arithmetic experiment.

## Separate exact oracles
1. Direct rational S and recurrence.
2. Independently construct a two-symbol *weighted urn* (unnormalized weights A=r*p and B=1-p), compute chance by explicit sum of weighted A and B masses (not call method1), then separately mix faithful/copy channels and an independent symmetric replacement coin. Must agree on all 72×5 p states with strict Fraction, including full state retention and boundedness.

## Frozen mathematical controls
1. If r=1, S(p,r)=p; for every h, when e=0, p is exactly constant.
2. If h=0, r is completely irrelevant to the full trajectory, so one content prevalence trajectory cannot identify r under h=0.
3. If e>0,h=0, p(t)=1/2+(1-e)^t(p0-1/2), confirmed for all four initial p0 values.
4. For r=4,p=1/5, S=1/2 (artificially favored minority catches up to unbiased half under *full sampling*), whereas under random copying p=1/5. This does not claim universal minority resurgence.
5. For all 0<p<1 and r>1, S>p; when r=1 S=p. For e=0,h>0,r>1, every p(t) strictly increases, but never crosses or reaches exactly 1 in finite time from p0<1.
6. For full content selection h=1,e=0, odds O_t=p_t/(1-p_t) grow by factor r per period, so \(p_t=r^t p_0/[1-p_0+r^t p_0]\) exact. This also shows symmetric content B complement under reversing which variant is assigned salience.
7. Positive symmetric replacement e can oppose a content advantage above one half; never claim content copying monotonically increases A when replacement is present.
8. Equal one-period output can be produced by different combinations of p, r, h, e (construct predeclared example r1,e0 vs h0,e0 at same initial p). A constant observed trajectory cannot identify whether content salience multiplier is neutral or no one uses content information.
9. An externally *hypothetical* statement that A is correct versus incorrect reverses the interpretation of higher A-copy probability; content prevalence alone does not establish true quality or advantage.
10. Unit interval exact, reject negative/out-of-bound p/h/e, unsupported multiplier r, floats, booleans and invalid horizons. No human or historical evidence.

## Acceptance
At least 72 uniquely identified full worlds and >=20 additional edge cases, two exact independent oracles, full immutable JSON, source+tests+JSON ZIP, Python3.11 and 3.12, pinned SHA256 of four original artifacts, GitHub Actions and permanent main archive with readback. Report sources' access limitations, explain that content attractiveness is imposed, and close E1 only if all tests and archive succeed. R073/PESEN v0.1 remain frozen. Verify following original catalog R165 independently after this model.

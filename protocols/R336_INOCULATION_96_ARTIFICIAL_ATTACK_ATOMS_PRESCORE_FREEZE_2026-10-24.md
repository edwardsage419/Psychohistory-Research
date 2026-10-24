# R336 prescore protocol freeze: constructed inoculation and transfer contrast

Date: 2026-10-24. Catalogue: original239 03-014 Inoculation Theory. State: FROZEN_BEFORE_SOURCE_OR_RESULT. E1 artificial mathematical mechanism only.

## Original English sources and strict reuse

McGuire (1961), *Resistance to Persuasion Conferred by Active and Passive Prior Refutation of the Same and Alternative Counterarguments*, Journal of Abnormal and Social Psychology 63:326–332, DOI 10.1037/h0048344. McGuire and Papageorgis (1961), *The Relative Efficacy of Various Types of Prior Belief-Defense in Producing Immunity Against Persuasion*, 62:327–337, DOI 10.1037/h0042026. Papageorgis and McGuire (1961), *The Generality of Immunity to Persuasion Produced by Pre-exposure to Weakened Counterarguments*, 62:475–481, DOI 10.1037/h0048430. Original human experiments exhibit conditional patterns; this study makes no claim to reproduce their parameters or data.

Existing R291 and R292 attitude/intention, R303 observational learning, R307 private/public influence, R334 induced compliance, and R335 public pressure have adjacent constructs. Their inspected summaries and the original239 03-014 preaudit do not verify a strict existing implementation of the present frozen weak exposure/refutation, later attack, same/novel transfer, and explicit competing mechanism. Early R001 to R064 ZIP full-content reuse remains OPEN due to binary retrieval. Do not assert exhaustive novelty.

## Frozen finite universe and model

Enumerate every combination of mode m in {0 NONE, 1 PASSIVE, 2 ACTIVE}, weak preview w in {0,1}, refutation r in {0,1}, same-topic indicator s in {0 novel, 1 same}, and subsequent attack intensity a in {1,2}. Exactly 3 x 2 x 2 x 2 x 2 = 48 worlds. The original artificial source CSV stores exactly two policy records per world, 96 records, one for INOCULATION_TRANSFER and one for TOPIC_SPECIFIC_SUPPORT. No human observations.

Prior belief score B=6. Unprotected attack loss L0=2a. Inoculation defense d=0 when m=0 or w=0 or r=0. Otherwise, when s=1, d=2 for passive and d=3 for active; when s=0, d=1 for passive and d=2 for active. Countermodel defense c=d when s=1, and c=0 when s=0. For policy defense q in {d,c}, post belief is B minus max(0,L0-q). All integer arithmetic, no randomness, no fitted parameters. A score increase relative to the unprotected baseline is defined by this assigned rule, and is not an observed psychological benefit.

## Frozen falsifiers and acceptance gates

F1: exactly 48 distinct complete worlds, 96 CSV rows, 2 models per world, no missing or extra worlds.
F2: when s=1, both policies have identical post scores in all 24 worlds.
F3: when s=0, the transfer policy exceeds the topic-specific countermodel in exactly 4 of 24 worlds, all with m>0, w=1 and r=1.
F4: for all 24 worlds with w=0 and all 24 worlds with r=0, both policies equal the unprotected baseline.
F5: for m=2, w=r=s=1, a=2, post score is 5; corresponding passive post score is 4. For a=1, both are 6 due to saturation. Thus active is not strictly superior in every world.
F6: independent auditor shall not import production module; it shall independently enumerate all 48 worlds, reconstruct exact CSV and JSON byte contents, and reject a tampered CSV score and a tampered JSON condition score.
F7: run production tests under Python 3.11 and 3.12, independent auditor as separate GitHub Actions job; require all three jobs success before formal E1 acceptance.
F8: source and results must be committed after this protocol commit. The original239 crosswalk can only change after source, independent audit and successful CI. No E2, E3 or original author empirical replication can be claimed.

## Scope

The two functions are constructed contrast mechanisms. They do not identify human inoculation, motivation, persuasion dynamics, causal transfer, or the original experiments. R073 and PESEN v0.1 remain frozen. Complete R-series and itemwise audit before classification and model fusion. Personal decision system remains deferred.

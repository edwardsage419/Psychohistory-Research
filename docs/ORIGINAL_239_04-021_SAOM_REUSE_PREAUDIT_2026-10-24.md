# Original239 04-021 SAOM: source and strict reuse preaudit

Date: 2026-10-24. State: OPEN_STRICT_REUSE_SCOPE. Next item after original239 04-020 ERGM. No E1 acceptance claimed here.

## Original non-Chinese sources
Snijders (2001), *The Statistical Evaluation of Social Network Dynamics*, *Sociological Methodology* 31:361–395, DOI 10.1111/0081-1750.00099, https://doi.org/10.1111/0081-1750.00099 . Snijders, van de Bunt and Steglich (2010), *Introduction to stochastic actor-based models for network dynamics*, *Social Networks* 32:44–60, DOI 10.1016/j.socnet.2009.02.004, https://doi.org/10.1016/j.socnet.2009.02.004 . These describe actor-driven continuous-time network change, actor choice among outgoing ties, and longitudinal estimation.

## Reuse audit
R341 provides a static undirected graph exponential-family distribution, with no actor-specific transition clock. R317 provides time-ordered exogenous contacts and reachability, with no endogenous tie-choice mechanism. R314 provides degree-weighted arrivals without fixed-actor tie toggling. Existing README inspection and GitHub indexed searches have not verified a strict SAOM finite actor-choice implementation. Full early R001–R064 binary ZIP member-level audit remains OPEN. This is a bounded reuse conclusion.

## Proposed bounded R342
Enumerate all 64 directed networks on three labeled actors, each of three actors, and the three choices stay or toggle one of two outgoing ties. Compare uniform and reciprocity-weighted local choices. Exact finite transition weights and normalization only. This is a constructed local actor-choice analogue, not the full Snijders model, longitudinal estimation, social causality, human E2 or historical E3. R073/PESEN v0.1 frozen. Complete R series and itemwise evidence audit before classification and fusion.

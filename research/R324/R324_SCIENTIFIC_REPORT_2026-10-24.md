# R324 scientific report: bounded artificial psychometric risk two-axis geometry

Date 2026-10-24. Original239 **01-017**, P2. Final grade **PASS_BOUNDED_E1_CONSTRUCTED_RISK_COMPOSITE_ONLY**.

## Primary English sources and reuse review
Fischhoff, Slovic, Lichtenstein, Read & Combs (1978), *How Safe Is Safe Enough? A Psychometric Study of Attitudes Towards Technological Risks and Benefits*, Policy Sciences 9:127–152, DOI 10.1007/BF00143739. The original research elicited judgments from 76 participants across 30 activities/technologies. Slovic (1987), *Perception of Risk*, Science 236:280–285, DOI 10.1126/science.3563507. Both concern measured human judgments and hazard characteristics.

Crosswalk v4.1 gave original 01-017 no primary R. R288/R318 evaluate constructed prospect valuations, R319 discrete mixed logit, R323 Boolean norm mediation. None establishes an original risk psychometric attribute/factor estimation. Earlier historical ZIPs have not been exhaustively content-audited. The R324 D/U axes and deterministic score are deliberately **project-created**, with no claim that they are the original authors' estimated model.

## Prescore frozen protocol and data provenance
[Prescore protocol commit 854fc11f](https://github.com/edwardsage419/Psychohistory-Research/commit/854fc11f1be6e902de753a919b9594884241ee8d) preceded [first source and 64-row data commit ae9568f0](https://github.com/edwardsage419/Psychohistory-Research/commit/ae9568f0d5c04f9973db6e2b7f9883d5ba8333f5). The initial source commit failed unit CI from a Python test assertion parenthesis syntax error, then [repair commit 6ebdfed1](https://github.com/edwardsage419/Psychohistory-Research/commit/6ebdfed14ef01a897533dfe09fcfd0853e0edd3d) changed the test line only. No frozen hypothesis, model rule, artificial data or JSON result changed.

Four scoring worlds: W0=(3,1), W1=(1,3), W2=(1,1), W3=(2,2). Exhaustively enumerate all 16 binary hazard-descriptor quadruples in each world, 64 original artificial rows. D=dread1+dread2, U=unknown1+unknown2, score=aD+bU, each source weight 1/16. No sampling randomness or fitted parameters.

## Exact results and falsification
Dread-only state 1100 has W0 score 6 and W1 score 2; unknown-only 0011 has W0 score 2 and W1 score 6. Thus changing a priori dimension weights reverses their rank. W2 assigns both score 2 although D,U differ; scalar rating alone cannot uniquely reconstruct the two dimensions in this finite universe. W3 is exactly twice W2 on every one of 16 states, preserving weak ranking. World mean scores are 4,4,2,4, with min zero in all four worlds. These statements follow from exact constructed arithmetic and are reproducible from the 64 committed source records.

## CI, audit and acceptance
[Initial CI run 40021221413](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021221413) **failure**, specifically syntax error in one test. [Corrected CI run 40021287400](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021287400) **success**, three jobs: Python 3.11 unit, Python 3.12 unit, independent Python 3.11 no-import source reconstruction. Each unit job executed 26 tests plus source byte replay. Independent auditor reconstructed 64 rows, four world summaries and exact witness without importing generator. Original source blob SHA1 and protocol blob SHA1 are recorded in the machine receipt.

## Evidence limits and open gates
No real psychometric ratings, original 1978 data, PCA/factor extraction, validated dread/unknown loadings, behavioral risk forecast, new human E2 or historical E3. The result tests a project-defined finite geometric analogy only. There are 173 provisional README links requiring itemwise evidence review and unresolved historical ZIP reuse audit. R073/PESEN v0.1 untouched. Complete R-series work before classification, then fusion. Personal decision system deferred.

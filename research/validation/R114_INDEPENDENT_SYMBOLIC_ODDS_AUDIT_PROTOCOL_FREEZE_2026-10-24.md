# R114 independent symbolic odds audit, frozen protocol

Date: 2026-10-24. Catalogue 03-008 Conditional Norm Compliance. Observed main HEAD before freeze: `599058887aa8e51017835afb4e4d12d187fa4169`.

## Source and existing evidence

Original R114 source blob SHA1 `468d41849c360be061944c0dfafa6e5df866da67`, test source blob SHA1 `c2bab5350d97705b95601f9cfae3bf3d6f615fa1`, existing bounded acceptance `research/R114/R114_FINAL_ACCEPTANCE_STATUS.json`. Original 30 synthetic tests passed in historical CI 39236924459. Strict reuse only. Primary sources: Bicchieri and Xiao (2009), DOI 10.1002/bdm.621, publisher abstract; Bicchieri, Lindemans and Jiang (2014), DOI 10.3389/fpsyg.2014.01418, open full text. No original individual-level data or fitted estimates are available in this audit.

## Preregistered falsifiers

1. Independently enumerate four models with frozen integer coefficients DESCRIPTIVE=(-1,2,0,0), NORMATIVE_ONLY=(-1,0,2,0), BOTH_ADDITIVE=(-1,1,1,0), INTERACTION=(-1,1,1,1). Four cells E0N0, E1N0, E0N1, E1N1. Build expected integer log odds and high precision Decimal probabilities from exp, without invoking the original logistic or logit functions to construct expected results.
2. For each model verify exact symbolic log odds interaction contrast equals the frozen fourth coefficient. Compare 16 independently calculated probabilities to the existing source grid with absolute error below 1e-14. Check four cell identities per model.
3. DESCRIPTIVE and NORMATIVE_ONLY must be identical on E0N0 and E1N1, and different on both discordant cells, with reversed ordering.
4. The first three factorial cells must leave the fourth cell and interaction coefficient unidentified. Exhibit two completions with the same first three cells and different E1N1 logits.
5. Independently reject two deliberate negative controls: a 0.01 perturbation to one reported probability and a +1 perturbation to the interaction cell log odds.
6. If any condition fails, original source cannot be imported, or source identity changes unexpectedly, fail closed. Report no new human E2 or historical E3, no real held out prediction, no external independent replication. The maximum grade is PASS_BOUNDED_INTERNAL_SYMBOLIC_E1.

## Execution and safety

Write a separate script under research/validation; never modify R114 source, R073, PESEN v0.1 or old acceptance. First verify source blob and current HEAD. Standard Python only. GitHub Actions may run only on a confirmed public repository with standard runners and zero incremental billing; otherwise report NOT_RUN. Update original239 crosswalk only after audit and CI success. Retain all failed runs. Do not interpret directory links as scientific validation.

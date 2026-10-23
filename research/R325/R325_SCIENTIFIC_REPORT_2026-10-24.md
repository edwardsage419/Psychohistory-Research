# R325 scientific report: exact finite statewise regret comparison

Date 2026-10-24. Original239 **01-020 Regret Theory** (P2). Formal scientific grade **PASS_BOUNDED_E1_PROJECT_CONSTRUCTED_CUBIC_REGRET_ONLY**.

## Primary English sources and reuse decision
Loomes and Sugden (1982), *Regret Theory: An Alternative Theory of Rational Choice Under Uncertainty*, Economic Journal 92(368):805–824, DOI 10.2307/2232669. Bell (1982), *Regret in Decision Making under Uncertainty*, Operations Research 30(5):961–981, DOI 10.1287/opre.30.5.961. The original work models counterfactual regret under uncertainty; the cubic function below is a **project-created illustration**. It is not an original author-estimated parameterization.

Existing R287 supplies a finite EU comparison baseline; R288 and R318 study prospect valuation and cumulative rank; R324 constructs risk descriptor composites. Their formulas cannot establish an itemwise primary regret model. Original239 v4.2 listed 01-020 pending. Earlier ZIP content has not been exhaustively reviewed.

## Protocol, source and exact mechanism
[Prescore protocol commit 2d4fec87](https://github.com/edwardsage419/Psychohistory-Research/commit/2d4fec87becfc46b6f66da1db5187b557afdcb53) predates [source and data commit 73c847c4](https://github.com/edwardsage419/Psychohistory-Research/commit/73c847c4be895b806621d929f80f20439b166c11). Enumerated 343 ordered statewise payoff-difference triples from {-3,-2,-1,0,1,2,3}^3 for each of kappa 0, 1/4 and 1, giving **1029 complete original artificial CSV rows**, each vector mass 1/343 per world. States are equiprobable within a vector. Exact Fraction arithmetic calculates EU advantage E=(d1+d2+d3)/3 and regret comparison F=(sum[d+kappa*d^3])/3.

Q(d)=d+kappa*d^3 is odd and has derivative 1+3*kappa*d^2>0 for kappa>=0. This monotone nonlinear comparator is a constructed submodel for investigating counterfactual statewise comparisons. No empirical estimation or participant observations.

## Frozen results
For vector (3,-2,-2), EU and kappa=0 advantage are -1/3 (strict B); kappa=1/4 gives 7/12 and kappa=1 gives 10/3 (strict A). Thus a strictly monotone nonlinear statewise comparison can reverse an EU ordering in this exact finite example.

Across 343 vectors, kappa=0 yields A=153, B=153, ties=37, strict EU/regret reversals=0. Kappa=1/4 and kappa=1 each yield A=162, B=162, ties=19, strict EU/regret reversals=6. The entire state universe obeys F(-d)=-F(d). Counts are artificial exhaustive enumerations; they are not empirical rates.

## CI and independent audit
[GitHub Actions run 40021709853](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021709853) completed **success** with three successful jobs: Python 3.11 unit (26 tests), Python 3.12 unit (26 tests), and independent no-import Python 3.11 audit. The independent auditor separately enumerated all 1029 records and recomputed rational scores, choice counts, six strict reversals in each nonlinear world and the prespecified witness. Source identities are recorded in the machine receipt.

## Evidence limitations
Artificial mathematical E1 only. No original 1982 fitted model, no actual regret elicitation, no human E2, no historical E3, no real behavior prediction, and no general proof of intransitive preferences. The cubic comparison may behave differently from other regret-theory functions. Prior early ZIP reuse scan and 173 provisional README itemwise reviews remain open. R073/PESEN v0.1 frozen; classification, fusion and personal decision system deferred.

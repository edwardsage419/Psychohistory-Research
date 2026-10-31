# R304 S100 prospective prescore freeze: noisy observed ingroup label and predictive Brier risk

Freeze timestamp UTC: 2026-10-31T01:44Z. Baseline main observed: b9ad55aca840977e004890bda5930565128a1a8d. Target key: (r,R304,S100-v1,noisy-observed-label-calibration-and-forecast-risk). Original R304 frozen at 60f6406cede7eb5bb7cea9dc622835d8fe3f4c41; original 216 worlds and 432 option rows, exact utility, tie rule, acceptance, original239 v7.8, and pending154 remain unchanged. New result is a bounded E1 synthetic extension only.

## Prespecified generator and question

For each fixed (s,d,e,menu) in {0,1/2,1}^3 times the four original R304 menus, assign the true ingroup label L uniformly over A_INGROUP and B_INGROUP. The true deterministic action Y(L) is the frozen R304 ALTERNATIVE=1, BASE=0. An external analyst observes a noisy label O, with symmetric misclassification probability epsilon in {0,1/4,1/2}, independently conditional on L and the fixed tuple. The analyst is given the exact artificial preference tuple and menu. This is a theoretical known-parameter forecasting task, not fitted data or a real intervention. Do not reinterpret the noisy label as a change in the agent's real group identity.

Compare three prespecified predictions for Y: PRIOR=(Y(A)+Y(B))/2; NAIVE=Y(O) assuming O is true; BAYES=(1-epsilon)Y(O)+epsilon Y(other). For each of 108 label-free tuples, two true labels, three epsilon levels, and two observed labels, enumerate 1296 atomic rows including zero-probability atoms. Atom probability conditional on tuple is P(L)=1/2 times P(O|L). For each predictor use Brier squared error (q-Y)^2; report exact expected risks across 108 equally weighted tuples, and separately the label-sensitive and label-invariant strata. Record exact source identities, true and observed labels, channel mass, all three probabilities and all three losses. The source row universe is 108*2*3*2=1296; zero-mass rows must remain in the source universe.

## Frozen comparisons and negative controls

Report count of label-sensitive tuples, number of label-invariant tuples, the original 216-world choice parity, and exact risks for each epsilon. Evaluate whether BAYES risk <= PRIOR risk and BAYES risk <= NAIVE risk for each epsilon. At epsilon=0, BAYES=NAIVE on positive-mass atoms; at epsilon=1/2, BAYES=PRIOR for every atom. If both true-label actions are equal, all three predictors coincide and their risks are zero. Do not infer real discrimination prevalence or causal effects. No parameter fitting, no post-score adjustment, no human E2, no historical E3.

## Independent audit requirements

B audit must use an algebraically separate route: derive the exact stratum risk using whether Y(A) differs from Y(B), then compare against the fully enumerated source row risk, verify the 216 original R304 decisions and the complete 1296 atom universe, and test at least eight corruptions: duplicate atom, missing atom, changed action, changed posterior probability, changed channel weight, changed Brier loss, changed aggregate, and false E2 evidence promotion. Preserve any failing controls and label the check scope as internal nonblind. Exact arithmetic only, no stochastic simulation. Any missing native script execution or external reproduction stays NOT_RUN. No CI execution without verified zero-cost quota. R073 and PESEN v0.1 remain frozen.

## A independent data scout

Inspect one publicly listed real human allocation/group-identity study. Record DOI, study task and temporal unit, access/file/field/participant/independent-unit/license status, explicit blockers, and whether it can test this toy model. Public metadata alone cannot be upgraded to trial-level E2 evidence.

This freeze is a design and scoring commitment only. Results, scripts, audits and scientific acceptance remain NOT_RUN at freeze. All future outputs must be additive, and other tracks' files must remain untouched.

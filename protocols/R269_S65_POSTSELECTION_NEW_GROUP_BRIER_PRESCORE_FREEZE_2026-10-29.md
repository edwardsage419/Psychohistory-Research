# R269 S65: Cross validation selection and new group risk, prescore freeze

Date: 2026-10-29 UTC. Track R. Base main HEAD observed before protocol: `831ead1aff9cd873db59a41ff1f83102ab3ac010`.
Status: PROSPECTIVE_FOR_S65_ENDPOINTS_ONLY. Researcher has read R269 original results and formulas. This is nonblind with respect to original R269.

## Fixed source and model universe
Keep R269's six independent Bernoulli(p) group labels, each repeated twice, with p in {1/4,1/2,3/4}. Enumerate all 64 six-bit sources for each p and weight each source by p^K(1-p)^(6-K). The three candidate predictors are exactly R269 GROUP_ID_MEMORIZER, GLOBAL_LAPLACE, CONSTANT_HALF. No new tuning or changed source distributions.

## New independent endpoint
For each complete six-group training source, calculate the original per-source LOOR and LOGO average Brier scores for all three models. Select one model under each CV policy using the smallest score and a prespecified tie order: GROUP_ID_MEMORIZER first, GLOBAL_LAPLACE second, CONSTANT_HALF third. Refit the selected predictor on all 12 training rows. Evaluate a seventh, unseen, independent Bernoulli(p) group, with two perfectly replicated rows. The group ID is new. Future risk is exact expectation over the independent seventh group's label. Thus the memorizer predicts 1/2 and has risk 1/4; constant predicts 1/2 and has risk 1/4; Laplace predicts q=(2K+1)/14 and has risk p(1-q)^2+(1-p)q^2. Average this future risk over the 64 original training sources, separately for LOOR-selected and LOGO-selected models and each p.

## Prespecified outputs and controls
Report six policy by p expected future Brier risks, six selection count distributions across three models, three paired LOGO-minus-LOOR risk differences, and the expected future risk of each fixed model at each p. Report exact Fraction arithmetic, no decimal-only results. Also report selection optimism as expected selected CV score minus expected future risk, with its sign stated explicitly. Count ties before tie-breaking.

Primary independent route A: direct full six-bit enumeration and explicit CV training fold reconstruction. Independent route B: K=0,...,6 binomial weights and closed-form CV formulas, with an independently coded tie rule and future risk. Compare all six risks, selection frequencies, and optimism. Negative controls: altered future risk, duplicated source, missing p, evidence E2 substitution, and Boolean count masquerading as integer must fail validation. Preserve failures.

## Scope and acceptance
All calculations are E1 artificial mathematical demonstrations. No real human E2, historical E3, or external-team independent replication. R269 original acceptance remains unchanged. R073 and PESEN v0.1 remain frozen. New native script and persisted receipt must be verified; no GitHub Actions without confirmed zero additional cost. All writes use new R track paths, no existing file replacement. If protocol commit is after any S65 score calculation, explicitly downgrade to exploratory.

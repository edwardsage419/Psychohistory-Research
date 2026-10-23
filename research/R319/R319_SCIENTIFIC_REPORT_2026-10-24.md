# R319 Mixed Logit: exact finite random coefficient mixture (E1)

Date 2026-10-24. Original239 01-007, P2. **Scientific status: PASS_BOUNDED_E1_ONLY**, after independently verified [GitHub Actions run 40005442471](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40005442471), all 3 jobs success, Python 3.11/3.12 each 35 tests and independent no-import source reconstruction. Git blob identities pinned in [machine receipt](R319_MACHINE_RECEIPT.json).

## Sources and strict reuse

Kenneth Train (2009), *Discrete Choice Methods with Simulation*, ch. 6, pp. 134–150, author-hosted https://eml.berkeley.edu/books/choice2nd/Ch06_p134-150.pdf , eq. 6.1 and finite discrete mixing, and McFadden & Train (2000), *Mixed MNL models for discrete response*, *Journal of Applied Econometrics* 15:447–470, DOI 10.1002/1099-1255(200009/10)15:5<447::AID-JAE570>3.0.CO;2-1. The exact finite support case is permitted by Train's chapter. No continuous random-coefficient density or simulation-based estimator is reproduced.

R111 is a shared fixed-logit formula only. R192/R193 provide other finite mixture kernels, not this mixed random-utility choice mechanism. No duplicate exact mixed-logit study was found in the checked GitHub search, but exhaustive historic ZIP content inspection is not claimed. [Frozen protocol](../../protocols/R319_MIXED_LOGIT_TWO_POINT_84_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed first at `93c0c409c0a33f478eaa6942e211a2b0a3baecb0`.

## Frozen source and exact result

Five ordered artificial choice sets, three predeclared q mixing masses and two coefficient values yield **15 worlds, 84 complete conditional source atoms, 42 marginal alternative probabilities**. Every rational component and marginal probability is retained, with zero estimation and zero real subjects.

For S0=(0,1) with q=1/2, the mixed probabilities are (1/2,1/2), A/B odds=1. Add a third alternative with feature 2, S1=(0,1,2): the same mixing mass yields (5/14,2/7,5/14), A/B odds=5/4. Each fixed coefficient separately preserves the A/B odds when C is introduced. The finite mixture does not preserve IIA in this constructed example. This is a mathematical counterexample to universal IIA under mixing; other mixture designs can still exhibit IIA.

Full artificial original source: [84 source rows](R319_ALL_84_ORIGINAL_CONDITIONAL_MIXTURE_SOURCE_ATOMS.csv), [15-world result](R319_EXACT_15_MIXED_LOGIT_WORLDS.json), [stdlib generator and 35 tests](r319_exact_finite_mixed_logit.py), [independent no-import source audit](../catalogue_audit/independent_r319_mixed_logit_audit.py), [workflow](../../.github/workflows/r319-mixed-logit-84-atom-e1.yml).

## Scientific and archival boundaries

Finite discrete support, one feature, fixed coefficients and known mixing masses only. No original respondent data, continuous integration, estimation of taste heterogeneity, observed substitution elasticities, real-world heldout prediction, or general consistency proof. E1 artificial mathematical mechanism only; human E2=0; historical E3=0. CI success certifies reproducibility of the exact finite computation, not empirical external validity. R073 and PESEN v0.1 remain frozen. Complete the R series before classification or fusion.

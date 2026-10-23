# R327 scientific report: finite two-state POMDP with costly information
Date: 2026-10-24. Original239 02-009, P2. Scientific grade: **PASS_BOUNDED_E1_FINITE_ONE_SENSE_POMDP_ONLY**.

## Source provenance and strict reuse review
Primary English literature: Smallwood & Sondik (1973), *The Optimal Control of Partially Observable Markov Processes over a Finite Horizon*, Operations Research 21(5):1071-1088, DOI 10.1287/opre.21.5.1071; Kaelbling, Littman & Cassandra (1998), *Planning and Acting in Partially Observable Stochastic Domains*, Artificial Intelligence 101:99-134, DOI 10.1016/S0004-3702(98)00023-X, author-hosted copy https://www.cassandra.org/arc/papers/aij98.pdf. Original theory covers general belief-state planning. This study checks a deliberately small one-sensing-step example.

Checked existing repository work: R300 provides a fixed-parameter HMM filter, R298 provides known fully observed model-based revaluation, R112 provides Bayesian updating, R326 provides finite hierarchical Bayesian borrowing. Their checked reports do not establish this costly contingent sensing decision. No existing E2 or E3 is transferred. Exhaustive older ZIP itemwise scan remains OPEN.

## Prescore freeze and complete original artificial sources
The falsifiable protocol was committed first as [e40b9f4252afb2b31efc9977091057fa1480ff15](https://github.com/edwardsage419/Psychohistory-Research/commit/e40b9f4252afb2b31efc9977091057fa1480ff15). The model, all 72 original source rows, exact results, independent auditor and CI workflow were committed later as [62f73f8a3cddb86c7d838283cac35c105e60669d](https://github.com/edwardsage419/Psychohistory-Research/commit/62f73f8a3cddb86c7d838283cac35c105e60669d).

The hidden binary state stays fixed. Nine priors b=0/8 through 8/8 cross two sensor accuracies q=1/2 and q=3/4. Each of the 18 worlds contains four exhaustive hidden-state/observation outcomes, including zero-probability counterfactual labels: 72 artificial source rows. Guessing a state yields 1 for a correct guess and 0 otherwise. A single sensor observation costs 1/8, then the agent must guess. Exact Fraction arithmetic is used throughout. Every row records joint mass, observation mass, posterior or NULL for impossible observations, terminal choice, values and optimal first action.

## Exact prespecified falsifiers and findings
At b=1/2 and q=3/4, immediate best guess value is **1/2**; sensing value is **5/8**. The optimal first action is SENSE. At b=1/2 and q=1/2, sensing value is **3/8** and immediate guess value **1/2**, so GUESS_0 wins the frozen tie break. At b=3/4 and q=3/4, sensing value is **5/8** versus immediate GUESS_1 value **3/4**, so sensing is rejected. Across the 18 investigator-specified worlds, first actions are 1 SENSE, 9 GUESS_0 and 8 GUESS_1. These are model-grid counts, never human behavior frequencies.

The independent auditor imports no production code. It independently constructs the 72 joint masses and enumerates all four terminal contingent policies after sensing for each world, matching the 18 exact value calculations and every source field. It also deliberately changes one CSV row and verifies rejection. Production rerun verifies exact CSV and JSON bytes.

## Verified CI and scope
[GitHub Actions run 40029054228](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40029054228) completed SUCCESS with three successful jobs: Python 3.11 unit and byte replay, Python 3.12 unit and byte replay, independent no-import auditor. Eight production unittest methods ran per Python version. [Machine receipt](R327_MACHINE_RECEIPT.json) pins source Git blob identities and job IDs. The formal acceptance is [R327_FINAL_ACCEPTANCE_STATUS.json](R327_FINAL_ACCEPTANCE_STATUS.json).

This E1 finding proves arithmetic consistency and a conditional value-of-information example under deliberately fixed model assumptions. It does not validate any actual psychological latent state, learned transition/observation probabilities, general POMDP algorithms, continuous belief optimality, real human E2, historical E3, original paper empirical replication, or external forecasting. R073 and PESEN v0.1 remain frozen. Original239 provisional mappings, taxonomy, fusion and personal decision system remain outside this study.

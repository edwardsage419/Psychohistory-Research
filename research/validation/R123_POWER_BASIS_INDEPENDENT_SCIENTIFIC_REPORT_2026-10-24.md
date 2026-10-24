# R123 DeGroot consensus third-method scientific audit

Date: 2026-10-24. Original239 04-009. Scope: constructed E1 exact finite matrix calculation, internal independent method. Original R123 remains unchanged.

## Sources, prior work, frozen protocol

Primary sources: DeGroot (1974), *Reaching a Consensus*, JASA 69:118–121, DOI 10.1080/01621459.1974.10480137; Berger (1981), *A Necessary and Sufficient Condition for Reaching a Consensus Using DeGroot's Method*, JASA 76:415–418. Original project R123 already reviewed both printed papers, the Berger correction, and original 58 tests. The third-method protocol was separately frozen in `research/validation/R123_THIRD_METHOD_EXACT_POWER_BASIS_PROTOCOL_FREEZE_2026-10-24.md`, Git blob `5cb01102d9792f6503e7897a5b4eb6276d7c69ef`, before new script or generated data.

Prior source, test, scientific report blobs independently checked in CI:
* source `c4dfe0ba8b5778440676dd1bf3fa01bbc4bf440e`
* test `c34b9617ec569d5ef7f459dba347b85a70665074`
* original scientific report `f2dfc14370fb437380ef7b10260f73dc5ede689d`

## Methods and raw evidence

An independent standard-library Python Fraction script calculates W^256 by 256 repeated exact matrix multiplications. The original R123 power routine and structural classifier are not used for the numerical matrix powers. Each column is the response to one basis initial opinion. Its max-minus-min spread is compared to the frozen tolerance 2^-24. An independently implemented reachability, recurrent-class and period classifier is compared against the unchanged original R123 graph classifier in verification mode.

The exhaustive predeclared row set has one-hot rows or two equal one-half weights: 1 one-node matrix, 9 two-node matrices, 216 three-node matrices. Total 226. Exact agreement between the frozen finite-horizon classifier and both graph classifiers: **226/226**. Universally consensus-guaranteed: **176/226**; other matrices: **50/226**. The largest observed basis spread among structurally universal cases is `46369903846391485115931664756875249686221522272598763/14474011154664524427946373126085988481658748083205070504932198000989141204992`, approximately 3.204e-24, below the frozen 2^-24 tolerance. This number is a deterministic property of this constructed roster, not an empirical estimate.

All 226 raw rows, including every matrix, each basis spread, maximum spread, and both classifier outputs, are archived at `research/validation/R123_POWER_BASIS_226_CONSTRUCTED_MATRICES_2026-10-24.csv`. Git blob `c3dc289d997dd80d1a3c1c3e962a30229c7d4962`; SHA256 `ec7700258254fcfc27eff46619f50a931f0fdf1c53a60a76f1db71f313a79e55`. Exact byte-for-byte regeneration is mandatory in CI.

Four controls: periodic two-person swap fails universal consensus despite a fixed equal initial opinion; identity with two absorbing nodes fails universal consensus while each opinion converges; a one-absorbing-leader non-strongly-connected graph has universal consensus; DeGroot's printed two-person example approaches the 1/3, 2/3 influence weights and the project-selected initial (0,1) approaches 2/3. A false original source SHA and a modified CSV are rejected.

## Executed GitHub Actions

Workflow `.github/workflows/r123-independent-power-basis-audit.yml`, run [40090970105](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40090970105), commit `f9cf9a8b62da0468e7a80985ea0d64988d6205de`, completed **success**.

Python 3.11 job `120863372067` and Python 3.12 job `120863371872` both completed success. Directly read both job logs: `R123_AUDIT_PASS total=226 universal=176 controls=4 csv_sha256=ec7700258254fcfc27eff46619f50a931f0fdf1c53a60a76f1db71f313a79e55 verify=True`; `Ran 58 tests`; `OK`. These are two runtime environments of the same project code, not two external independent research replications.

## Scope and scientific judgement

**PASS_BOUNDED_INTERNAL_FINITE_POWER_BASIS_E1**. The exact finite W^256 experiment agrees with the prior graph-theoretic classification for the specified 226 matrices. Finite-horizon numerical closeness alone does not establish convergence for arbitrary row-stochastic matrices. Universal consensus is a structural statement for all initial opinions, distinct from a particular initial opinion already agreeing and from individual convergence without agreement. Berger's 1981 correction remains essential.

No original human opinion time series, fitted influence matrix, out-of-sample E2 prediction, real-data calibration, causal inference, historical E3 test, or independent external research-team replication. No modifications to R073 or PESEN v0.1. The original239 directory crosswalk is metadata provenance, not evidence of additional real-world validity. Free public standard GitHub runner, no GPU, paid API, data purchase, or new expense.

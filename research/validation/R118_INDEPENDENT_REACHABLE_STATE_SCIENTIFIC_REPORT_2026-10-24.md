# R118: independent reachable-state graph audit and bounded scientific acceptance

Date: 2026-10-24. original239 item 03-019 Threshold Participation. Original study R118 is strictly reused. No new R number was assigned.

## Provenance and prospective protocol

Primary original-language paper: Mark Granovetter (1978), *Threshold Models of Collective Behavior*, American Journal of Sociology 83(6), 1420–1443, DOI 10.1086/226707. Source record: https://sociology.stanford.edu/publications/threshold-models-collective-behavior ; original publication: https://www.journals.uchicago.edu/doi/10.1086/226707 ; archived original PDF: https://snap.stanford.edu/class/cs224w-readings/granovetter78threshold.pdf . The original R118 report records direct reading of printed pages 1422 and 1424–1426. This audit independently verified the official original-source abstract and publication identity, and directly reused the repository's existing mathematical reconstruction. It does not claim a fresh page-by-page reread of the PDF in this audit.

Prospective independent audit protocol: `research/validation/R118_BFS_REACHABILITY_AUDIT_PROTOCOL_FREEZE_2026-10-24.md`, frozen at commit `6480045c34a195c113ca831521956e67976e13b7`, before any new audit implementation or constructed CSV. Original source and test Git blob SHA1 were fixed there.

## Actual independently executed checks

The original R118 uses synchronous irreversible group entry and a sorted threshold closure. This audit instead constructs a directed graph of *all reachable individual entry orders*, using bitmask states and breadth-first search. From the empty state, a previously inactive actor may enter when their fixed threshold is at most the current number active. No original solver is called during independent graph construction.

The finite census covers n=1..4, with (n+1)^n ordered threshold vectors per n: 2, 9, 64 and 625, **700 constructed mathematical worlds**. All 700 have one terminal reachable subset and agree with the original synchronous and sorted solvers. The independently generated 700-row CSV was checked byte-consistently against the Python reconstruction in both CI jobs, with SHA256 `5a7f5cc06ff6cd1f244b4f64fb4febc46c01ab4c5c79689e9f22b6637ab5a172`.

For the original 100-person theoretical example, thresholds 0..99 yield 100 participants. Changing threshold 1 to 2 yields 1 participant. The project's additional compensated example changes thresholds 1 to 2 and 99 to 98; both 100-person populations have threshold sum 4950 and mean 49.5, with final participation 100 versus 1. The original paper's one-change example and the project's own two-change example remain separately attributed.

Two negative mechanism checks passed: thresholds (1,1) have a possible all-active static configuration but zero reachable participants from no seeds; (0,2,2) reaches exactly one participant. Two deliberate perturbations, of the expected outcome and of the threshold vector, were detected. The original 44 unit tests were also rerun in both Python versions.

CI run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40079060024 finished `completed/success`. Both jobs, Python 3.11 (120828594682) and Python 3.12 (120828594494), succeeded. Actual job logs report 700 solver comparisons, two rejected tamper controls, and `Ran 44 tests` followed by `OK`. Machine identity receipt: `research/validation/R118_BFS_REACHABILITY_CI_RECEIPT_2026-10-24.json`.

## Independent method B audit and limitations

**Mechanism identification.** Reproducing the same mathematical closure with a third algorithm strengthens internal implementation confidence. It does not identify any actual participant's threshold or its causal origin. The reachable closure from an empty state cannot be substituted for all possible equilibria, nonzero seed states, or a dynamic network with limited neighborhood observations.

**Data leakage, baseline and generalization.** The entire dataset here is deterministic artificial enumeration, with no trained parameters, sampled participants, or train/test partition. Leakage, out-of-sample prediction, calibration, empirical baseline performance, bootstrap uncertainty, and independent human sampling cannot be estimated from this material. The zero-seed versus static-equilibrium control is a mathematical negative case, not an empirical predictive baseline.

**Evidence grade.** `PASS_BOUNDED_INTERNAL_INDEPENDENT_REACHABILITY_E1`. This is an internal methodological audit using a different algorithm and a different implementation language for archived CSV construction. No external independent research group performed replication. New human E2 prediction score = 0; new historical E3 score = 0. No causal effect, real riot, protest, social network, policy, or historical forecast is supported by this run.

## Repository and cost safeguards

Original R118 research source, original test, R073 and PESEN v0.1 were not modified by this audit. The workflow uses standard public `ubuntu-latest` runners, with no GPU, paid API, paid data, or larger runner. Official GitHub billing documentation states standard hosted runners in public repositories are free: https://docs.github.com/en/actions/concepts/billing-and-usage . No artifact upload, cache storage or external paid service was added.

Pending early ZIP strict reuse checks and real human transfer validation remain open. This bounded result can justify only the specific original239 03-019 E1 link upgrade, after independent catalogue consistency CI.

# R127 integer tent payoff independent third-method audit: interim scientific report

Date: 2026-10-24. Original239 05-003. Status: **EXECUTION_AND_CI_VERIFICATION_PENDING**. No formal new acceptance or catalogue decrement.

## Provenance and reuse

The existing R127 original source was read directly at Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`. Its 60-test suite is at blob `1e9338c5a8504d86d3032b139ab3f9546907d1ec`. The previously frozen third-method protocol is `research/validation/R127_THIRD_METHOD_INTEGER_TENT_BEST_RESPONSE_PROTOCOL_FREEZE_2026-10-24.md`. Original publication: Van Huyck, Battalio and Beil (1990), AER 80(1), 234–248. Existing R127 contains source paper Table 2 aggregate data, not original individual microdata.

## Archived new materials

* `R127_INTEGER_TENT_2793_PROFILES_2026-10-24.csv`: all 2,793 constructed effort profiles, ordered group sizes 2 to 4, original minimum and independent integer payoff numerators. Independently generated and checked with a separate local Python enumeration. Exactly 10,731 person-payoff cells. Canonical CSV UTF-8 SHA256: `821f785bf21a96eae5b65d1200389a5a2baa45ad63e5a115e48505051a2e9df4`.
* `verify_r127_integer_tent_best_response.py`: independently computes expected numerators `6 + 2*min(profile) - own_effort`, compares them with unchanged original `payoff_vector(..., experimental=True)`, and checks 399 opponent profiles with 2,793 own-effort alternatives and unique best response `min(opponents)`.
* `.github/workflows/r127-independent-integer-tent-audit.yml`: public standard Ubuntu runner, Python 3.11 and 3.12, original 60-test suite, source Git blob check, CSV byte identity and two negative tamper controls.

A local, separate Python enumeration reproduced 2,793 profile counts, 10,731 payoff cells, 399 opponent profiles, unique best-response claims and the archived CSV SHA256. This local check did **not** execute the original R127 source import, the archived verifier or the GitHub CI job. Those are explicitly pending machine confirmation.

Frozen positive controls: (1,1) -> (7,7) numerator; (7,7) -> (13,13); (7,1) -> (1,7); (1,7,7,7) -> (7,1,1,1). Original published 107 people and 7 experimental groups are published aggregate observations, with no newly re-estimated individual behavior.

## Audit and scientific boundaries

Programmatic internal method comparison, E1 constructed. Independent external replication absent. No new E2 human out-of-sample score, no E3 historical validation. No predictive calibration, independent experimental session holdout, confidence interval, or causal equilibrium-selection estimate. R073 and PESEN v0.1 remain untouched. A passing workflow, independently checked logs and formal acceptance are required before moving 05-003 out of the pending queue.

## CI verification status

Three commits archived the data, verifier and workflow, with latest known workflow commit `d58f71bceacc08fba2ae8b0ce478dc51e54900e3`. The available GitHub connector's commit-workflow-run method only lists pull-request-triggered runs and returned no runs for this push commit. Combined commit statuses were empty. **CI success has not been verified.** Do not infer success from absence of a status. The pending count stays 157.

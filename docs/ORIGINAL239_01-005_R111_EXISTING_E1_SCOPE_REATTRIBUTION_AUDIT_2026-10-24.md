# Original239 01-005 Random Utility Model: R111 existing evidence reattribution audit

Date: 2026-10-24. Scientific grade **PASS_EXISTING_BOUNDED_E1_IID_EV1_CONDITIONAL_LOGIT_ONLY**. This is an itemwise audit of an existing R111 result, with no new R number and no new human E2 or historical E3.

## Original literature and model boundary
McFadden (1974), *Conditional Logit Analysis of Qualitative Choice Behavior*, https://eml.berkeley.edu/reprints/mcfadden/zarembka.pdf . Train (2009), *Discrete Choice Methods with Simulation*, https://eml.berkeley.edu/books/choice2.html . R111 implements the conditional logit consequence of iid type-I extreme-value utility shocks. The broader random utility model family includes error structures and dependence beyond this special case. R111 does not validate the whole family.

## Frozen audit and source identities
[Prescore evidence audit freeze](../protocols/ORIGINAL239_01-005_R111_EXISTING_E1_REATTRIBUTION_AUDIT_FREEZE_2026-10-24.md) committed at [b58da05f](https://github.com/edwardsage419/Psychohistory-Research/commit/b58da05f13c83cd6b50d6a6e97e42d9a34fae00a), before the new independent audit source commit [70eca1e6](https://github.com/edwardsage419/Psychohistory-Research/commit/70eca1e6ac1aa46120ed8d801da6eb95e4bee99b). The existing R111 report, production code and 18-test source match their original archived SHA256 identities. Original R111 CI [39224159791](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39224159791) concluded success with one job.

## Independent replay
New [GitHub Actions run 40064119855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40064119855) concluded success. Python 3.11 and 3.12 each replayed the original 18 unit tests; an independent job verified the three original file SHA256 hashes, exact 18 test definitions, formal status and zero real-human observations. Two negative hash-tamper controls were included.

| Frozen gate | Result |
|---|---|
| A1 three source/report/test SHA256 identities | PASS |
| A2 McFadden iid EV1 conditional logit scope | PASS |
| A3 18 existing synthetic tests on Python 3.11 and 3.12 | PASS |
| A4 independent source and scope auditor | PASS |
| A5 three-job new CI | PASS |
| A6 strictly bounded existing-R E1 reattribution | PASS |
| A7 R073 and PESEN v0.1 unchanged | PASS |

## Scientific boundary
The tests establish mathematical and numerical properties of the existing conditional logit implementation, including probability normalization, IIA under iid EV1 assumptions, scale/translation invariance, red-bus/blue-bus limitations and seeded synthetic Monte Carlo behavior. No real human data was loaded or scored. No original 1974 empirical dataset replication, cross-population generalization, E2 or E3. The original239 link now has a checked bounded mechanism scope; catalogue association alone would have been insufficient. Early ZIP member-level audit OPEN. Remaining provisional items must be individually audited before classification and fusion.

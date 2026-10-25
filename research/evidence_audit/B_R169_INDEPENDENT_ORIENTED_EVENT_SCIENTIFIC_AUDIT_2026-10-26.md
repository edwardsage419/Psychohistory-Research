# B scientific audit: R169 exact oriented-event independent replay

Date: 2026-10-26 Asia/Singapore. Original frozen design: `protocols/R169_OBSERVATION_LADDER_72_WORLD_THIRD_METHOD_FREEZE_2026-10-26.md`, commit e632cf3b5301589e55fb983fce11c27be7b29fd6. Audit scope is artificial E1 only.

## Independent implementation and execution

Main route iterates discordant undirected edges and both orientations; B route builds a flat list of all oriented discordant edges, assigns each an exact Fraction probability, separately computes adoption and eligible rewiring branches and independently propagates complete state probability distributions for three transitions. B does not invoke main `step` or `trajectory` to calculate its own outputs. B imports the main module only for input templates and strict comparison of results.

Local execution of `research/evidence_audit/r169_b_oriented_event_independent_20261026.py` returned:

* 72 of 72 worlds with exact complete path equality.
* 288 of 288 full snapshot probability laws equal.
* 2829 of 2829 reachable-state transition kernels equal.
* Independent recomputation of archived R169 path/block/alpha=1 t2 target-rule total variation: exactly 1/2.
* Executed negative control replacing the real alpha=1/any rewiring kernel with an all-no-op kernel at the path/block start: exact total variation 1, detected.
* Main-script alpha=1/2 to 1/3 mutation changed t1 kernel TV by 1/6, detected.

Machine receipt: `B_R169_INDEPENDENT_ORIENTED_EVENT_RECEIPT_2026-10-26.json`.

## Correction disclosure

The first local B execution **failed** on a reachable state. B constructed a replacement graph by sorting retained edges and then appending the new edge, which produced a noncanonical tuple ordering even when the mathematical graph was identical. The main implementation uses canonical globally sorted edge tuples. B was corrected to sort the full edge set, and the final full audit then passed. This was a representation defect in the initial independent implementation. The first failure is retained as a disclosed local audit event; no original R169 frozen protocol or existing research file was edited.

## Evidence validity

The check confirms two independent coding routes agree on the same project-authored model. It does not provide independent real participants, separate study personnel, blind prospective human evaluation, probability calibration, external replication, or historical evidence. No statistical confidence interval is meaningful for the exact finite enumeration itself; predictive uncertainty on real networks remains unmeasured. Source access and scientific acceptance are separate. E1 internal replay PASS; E2 new 0; E3 new 0; external replication 0.

New remote CI was deliberately skipped because free billing entitlement could not be independently established. The archived script is runnable with standard Python; do not call the local run a GitHub Actions success. R073 and PESEN v0.1 are unchanged.

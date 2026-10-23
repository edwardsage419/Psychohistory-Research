# R297 Original 239 item 02-003 Q Learning: finite exact off-policy and coverage E1

Primary: Watkins & Dayan (1992), *Q-learning*, https://doi.org/10.1007/BF00992698. **Finite fully artificial deterministic Q-learning mechanism**, not human/animal experiments or proof of Watkins–Dayan asymptotic convergence conditions.

[Prescore prospective freeze fd66badd](https://github.com/edwardsage419/Psychohistory-Research/commit/fd66badd5a110b36cc97564f7e1a29daba4298ba) | [Complete frozen original protocol](../../protocols/R297_Q_LEARNING_OFF_POLICY_COVERAGE_24_WORLDS_120_SOURCE_PRESCORE_FREEZE_2026-10-23.md).

* [Executable exact Q-value replay, full 611 tests](r297_exact_q_learning.py)
* [120 original complete artificial Q-vector source states](R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv)
* [24 worlds ×5 epochs and oracle result JSON](R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json)
* [Original sources/results SHA256 receipt](R297_MACHINE_RECEIPT.json)
* [Independent no-import source audit (16 tests)](../catalogue_audit/independent_r297_source_audit.py)
* [Formal scoped E1 machine acceptance](R297_FINAL_ACCEPTANCE_STATUS.json)
* [Scientific report on coverage, behavior backup and exact learning limits](R297_SCIENTIFIC_REPORT_2026-10-23.md)

GitHub Actions run [39924889538](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39924889538) 3/3 completed/success, source/results archived permanently at [commit6d3b0496](https://github.com/edwardsage419/Psychohistory-Research/commit/6d3b0496111d58c03983941480398c1fd4bff85f).

At γ=α=1/2 FULL+MAX, epoch4 Q_SAFE=15/16, Q_EXPLORE=39/32, Q_GOOD=45/16, learned EXPLORE. Across 24 worlds 12 agree with unconstrained optimal policy; 12 fixed behavior or coverage worlds disagree. The fixed BAD behavior-policy comparator has a **different downstream objective** and should not be called suboptimal relative to its own restricted continuation. Counts are artificial grids only. R063 social learning, R073 and PESEN v0.1 remain separately scoped/frozen, original 239 model catalogue untouched.

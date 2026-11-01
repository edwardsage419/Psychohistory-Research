# B track nonblind independent audit: R328 S124

Date 2026-11-01 UTC. Baseline main before report: 796983a93d130a00a939488666d47e7c0c9be3fb.
Audit key: (b, R328, S124-v1, full receipt closed-form and five mutation gates).
Source read before audit: original R328 prescore freeze, original R328 120-row CSV and report; S124 freeze `b9838d4052c9632d950cffd2e22a9fa3e1ae47b5`; newly persisted JS, CSV and JSON. This is **informed/nonblind internal mathematical reproduction**, not independent external replication.

## Independent route and actual execution
The R generator uses a BigInt rational gradient recurrence. The B auditor independently computes the closed form using Python `fractions.Fraction`, with no R generator import. For every world and t, it recomputes `x[t]=x*+(m-x*)*lambda^t`, energy, residuals, analytic optimum and energy gap. It reconstructs the exact CSV and JSON bytes from independently computed values.

The exact archived Python B source was run locally in ordinary Python and `python -O` optimized mode, each with `--check` against locally reconstructed receipts. Both runs returned PASS, 480 rows, 96 worlds, and five rejected mutations. The tested local B source Git blob was `2fab93657611aa70e57e241f06e662adfe09ded0`, identical to the committed `research/evidence_audit/b_r328_s124_independent_fraction.py`.

The B output computed the following full-file Git blob identities, then these were compared with the **actual remote** GitHub blob SHA identities using separate GitHub reads:
* CSV: 18,220 bytes, `c2343a241f5389071eb1c8cdaf8c9e955f7daca2`, PASS.
* JSON: 34,439 bytes, `9e06c249036ebe09316e9952017b043afe96df73`, PASS.

The archived R JS source was independently fetched from the remote repository and executed in a V8 adapter. Its generated CSV and JSON strings matched the full persisted remote file contents byte for byte. The first 120 alpha=1/4 rows also matched the 120 original R328 source rows field by field. These checks jointly cover the persisted bytes and the distinct closed-form mathematics, subject to the usual Git SHA collision assumptions.

## Predeclared falsifiers and observed negatives
Five controlled mutations were rejected:
1. Omit one of 480 rows.
2. Duplicate a source row while dropping another.
3. Alter one row's energy to 999.
4. Alter one row's alpha label.
5. Add a spurious `evidence_grade=E2` to a world receipt.

The structural checker requires exact coverage, unique six-field row identities, all exact oracle fields, and exact world metadata. These five mutations share the same oracle, so they are five tested fault classes rather than five independent research replications.

Observed genuine negative scientific results: 24 nonzero-residual worlds have strictly increasing energy at one or more updates, and eight have neutral, non-improving dynamics. The source generator correctly retains them. No failure was reclassified as success.

## Evidence boundary and remaining gates
Data leakage, empirical baselines, human sample-out prediction, calibration, resampling and confidence intervals: NOT_APPLICABLE_TO_DETERMINISTIC_E1, with no E2 inference made. Original R328 finite alpha=1/4 serves as a frozen algebraic overlap control. Distinct subject count 0. E1 480 synthetic rows, E2 0, E3 0. External independent team: NOT_RUN. Native Node CLI replay of the exact committed R source: NOT_RUN. The Python `--check` used locally reconstructed byte-identical inputs, while the remote identity was checked by independent Git blob comparison; direct Python reading of the remote file from disk: NOT_RUN. GitHub Actions S124: NOT_RUN. Do not cite historical R328 CI as S124 acceptance.

Result: **PASS_NONBLIND_INTERNAL_E1_EXACT_MATH_WITH_OPEN_NATIVE_CLI_AND_CI**. S124 scientific status remains PARTIAL_E1_EXTENSION. No original R328 acceptance promotion, no R073/PESEN change. No paid service used; billing/free Actions quota not independently inspected.

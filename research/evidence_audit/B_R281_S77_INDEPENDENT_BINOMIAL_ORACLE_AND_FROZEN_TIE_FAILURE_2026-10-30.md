# B轨：R281 S77 独立计数与冻结断言失败审计

date_utc: 2026-10-30
target_key: (B,R281,original-cbf8eec7+S77-v1,binomial-oracle-frozen-tie-negative-evidence)
source_read: original R281 protocol/report and new S77 freeze, including prior known log-score expressions. Internal nonblind, not an external blind replication.
method: independent Python standard-library Fraction, comb(4,k), 12 worlds x 5 counts = 60 count cells. Analytic one-step expected loss coefficients in ln2/ln3/ln5, strict-win comparison via exact rational likelihoods, tie mass via equality. No ordered-source enumeration in the B oracle.
native_python_local: PASS (12 worlds, 60 count cells; independently checked four fixed controls and two mirror symmetries).
specific_checks: p=1/4, q=1/16, wrong model strict-win mass 81/256; p=1/2, q=1/4 mass 5/16; p=1/4, q=3/4 strict-win 13/256 and tie 27/128.
frozen_test: FAIL, “zero tie whenever q!=p” disproved by exact 27/128 counterexample; preserve as negative evidence. No threshold redefinition.
R_V8: 192 ordered source atoms, 12 world sums, analytic risk coefficients and symmetry checked in execution.
B_persisted_csv_json_native_cli: NOT_RUN in this cycle; archived Python checker is available for a later exact remote receipt replay. No claims of byte-identical remote source replay or external independent replication.
status: PARTIAL, FROZEN_TEST_FAIL; E1 internal nonblind only; E2 predictive=0; E3=0.
remaining: native B CLI on full remote CSV/JSON, mutation tests on persisted receipt, native Node CLI, external research replication. CI NOT_RUN because free billing eligibility not confirmed.

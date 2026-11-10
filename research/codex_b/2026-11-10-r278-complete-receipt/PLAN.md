# R278 S74 complete persisted receipt verification

Main baseline e5f2baa7f6b13b1a2bf95f48ed49571f732e7611. User authorizes continued
independent engineering PRs, preserving frozen research and no new human scoring.
Scope is only this Codex B directory, branch codex-b/r278-s74-complete-receipt-20261110.

Observed actual CLI blind spot: old B checker still returns PASS after deleting
conditional_forecasts, setting covariance/delta to999, changing R073 toMODIFIED,
or replacing numeric new_E2_predictions=0 with boolFalse. Existing fifteen-risk
and960-row protection is real; historical manual3-delta checks are not denied.

Design: reuse fixed archived B analytic/CSV verification rather than reimplement
its fifteen risks/960 atoms. Independently derive five conditional forecasts by
Bernoulli likelihoods and covariance via total covariance w(1-w)(qH-qL)^2. Add
complete key/type/unique-identity coverage for all21 receipt root fields and all
conditional/delta fields. Exact rational numeric strings, strict counts/bools,
duplicate JSON key and NaN/Inf refusal. Accept collection reordering and exact
equivalent fractions; reject missing/extra records/fields. Both input files are
read once and materialized to a temporary immutable snapshot for archived check.
CSV wire shape also checks the exact13-field header and every row width before
DictReader can fold duplicate column names or ignore surplus cells.

Native replay: execute original Node CLI to a disposable directory; compare both
CSV and JSON bytes with actual archived files, verify generated SHA receipt, then
run old B and new full gate on archive/replay. No original files written.
Actual old/new CLI mutation controls must distinguish unprotected fields from a
wrong-risk control that old B already rejects. Input/code/metadata hashes recorded.

Alternatives: changing the archived checker alters historical coverage; merely
authenticating JSON bytes would not independently verify the omitted mathematics.
Use a separate complete numeric gate and preserve originals. This is neither
generic PR integration nor Codex A source-authentication composition work.

Review focus: conditional forecasts/covariance and comparison signs; missing
fields/duplicate records; False vs0 and numeric strings; duplicate JSON keys;
snapshot consistency and no stale output. Standard library Python plus existing
Node; no installation, CI dispatch, paid APIs/resources or automatic merge.

- [ ] Write RED regressions for exact K2/central delta, schema/type/JSON mutations.
- [ ] Implement full logical receipt and conditional math supplement; GREEN/-O.
- [ ] Exact original Node/B CLI replay, byte identities, old/new mutation runs,
  source hashes and raw command logs.
- [ ] Fresh engineering review, necessary corrections and final verification;
  refresh main/PR scopes, publish/attach independent draft PR with [skip ci].

Evidence: artificial nonblind internal program replay plus independent analytic
verification. New human E2/E3/external replication0. Production adoption NOT_RUN.

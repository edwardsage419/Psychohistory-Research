# R180 / original239 08-004 Bootstrap: cross-source exact-moment itemwise audit

track: R+B
subflow: original239 P0 itemwise source and scientific evidence
run_date_utc: 2026-11-02T10:42Z
starting_main_head: cb93f132f113f4557836aaa7e5c4b5664365d4c6
analysis_code_commit: 57dbfa63757e09a2c923bf6834aaaad824f51fa0
target_key: (R+B,R180,2026-10-21 prescore freeze,original239 08-004 upstream PMF and bootstrap moments)
status: COMPLETE_BOUNDED_ITEMWISE_ANALYTIC_AUDIT / PARTIAL_FORMAL_ACCEPTANCE
evidence_scope: INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1
ci_status: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED

## Question, original model and fixed sources

Review original239 P0 08-004 Bootstrap (R180) for source identity and independently derivable moment claims. Preserve the existing frozen experiment and historical results. This is an internal nonblind scientific check, not a new experiment or external-team replication.

Primary theory reference: Efron (1979), *Bootstrap Methods: Another Look at the Jackknife*, Annals of Statistics 7(1), DOI 10.1214/aos/1176344552. The paper's publication identity and abstract were checked using English-language bibliographic records on 2026-11-02. R180's clustered finite experiment is a project-defined artificial construction, not a reproduction of Efron's empirical examples. Related original R180 protocol references Davison and Hinkley (1997) and Cameron, Gelbach and Miller (2008). No original author dataset was downloaded or replayed.

Source files read from main:
* protocols/R180_CLUSTER_BOOTSTRAP_30_WORLDS_7750_SAMPLES_PRESCORE_FREEZE_2026-10-21.md, Git blob 96fc3fd28ca61719231a33cf5f6507b751ea1ecd.
* research/R177/r177_four_finite_count_families_exact.py, Git blob 2d032513ce84141214b6b3f84df9c0ed9976a02b.
* research/R177/R177_EXACT_RESULTS.json, Git blob 8a8819e4d85989b518b9152cfc98336457c76a9c, historical SHA256 57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535.
* research/R180/R180_EXACT_RESULTS.json, Git blob b30bc0964a8ce89df6d723e32daad10521c538c5.
* research/R180/README.md and prior B_R180_FULL_CARTESIAN_INTEGER_SCIENTIFIC_AUDIT_2026-10-26.md; earlier audits were read before deciding the complementary scope.
* docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json, blob 36f24235901172642c46853298aebb421f1a3552.
* docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv, blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f.
* .github/workflows/r180-exact-cluster-bootstrap.yml was identified by path but not run.

GitHub path history places the frozen protocol at commit f2e935da4a3c3b478c619c86ca721d3e1de73948 (2026-10-21 06:46:58 UTC) and archived result at 52a54fc2df5efd96f1c967dfc368c42c0f2ead17 (2026-10-21 06:51:45 UTC). The ordering is supported by these path histories. Historical CI claims in README are retained as historical records, without rerunning Actions.

## Independent algorithm and executed checks

New code: research/validation/r180_original239_cross_source_exact_moment_gate_20261102.js. A pure JavaScript BigInt rational implementation was evaluated against both actual remote JSON documents in the tool V8 runtime, without importing R177 or R180 model code. Deterministic, no random seed.

The audit fixes the Cartesian identity of m={2,3,4}, p={1/4,1/2}, five source mechanisms. It checks exact 30-world uniqueness, expected 5^m ordered-sample cardinality, upstream R177 n=4 family/regime/p PMF identity, full mass and mean, then computes seven exact result fields per world.

For a group count K with source probabilities q_k and independent m groups:
* mu_K = sum(k q_k) = 4p, sigma_K^2 = sum(k^2 q_k) - mu_K^2.
* Var(p_hat) = sigma_K^2/(16m), equal to MSE because E(p_hat)=p.
* E[V_cluster*] = ((m-1)/m) Var(p_hat).
* E[V_cluster_corrected] = Var(p_hat).
* E[V_iid*] = [p(1-p) - Var(p_hat)]/(4m).
* P(all group counts identical) = sum_k q_k^m.
* The IID variance ratio is E[V_iid*]/Var(p_hat).

Observed: 30/30 R177 PMF cross-source identities PASS; 210/210 exact moment-field comparisons PASS; complete 30-world key set PASS. Seven negative controls correctly rejected duplicate world, missing world, altered source PMF, altered variance, changed R177 source identity, false E2 and changed source regime. Each negative control modifies one copy of the already inspected result; this is internal nonblind mutation testing.

For the frozen m=4, p=1/4, CLUSTERED_BB_C2 example, the independent formula confirms Var(p_hat)=3/128, E[V_iid*]=21/2048 and ratio=7/16 (43.75%). These quantities are finite artificial design properties. The archived group corrected Wald coverage of 108521749/134217728 was read but NOT_RECOMPUTED in this run.

The JavaScript audit and mutations ran inside tool V8 on fetched source JSON. Full Node.js CLI invocation with a native complete checkout, verification of CLI byte pins, complete 7,750-row CSV replay, full conditional bootstrap PMF and four coverage intervals are NOT_RUN. Prior project B audits addressed several of those quantities; this run does not duplicate or claim to reperform them. The new code includes a Node.js CLI entry that checks the fixed R177 source blob, R180 freeze blob, R177 result SHA256 and R180 result Git blob before the same audit; this CLI path awaits native execution.

## Scientific conclusion and unresolved conditions

The new cross-source audit supports **bounded itemwise acceptance of R180's 30-world artificial E1 bootstrap moment and provenance claims**. It adds a reproducible upstream R177-to-R180 identity check and a compact independent moment oracle. The R180 archived interval coverages, 7,750 sample rows and 120 conditional PMFs were not revalidated here; earlier audit records must be evaluated separately before formal acceptance. It does not establish general coverage properties for human social groups or causal effects.

original239 queue still has 154 pending (P0=27, P1=82, P2=45); R180 08-004 remains PROVISIONAL_PRIMARY_README_LINK. Formal queue reduction this run: 0. Do not silently change crosswalk, historical acceptance, freeze or the original model. R272 production P0 and R257 S53 blind-order P0 remain open. R073 and PESEN v0.1 remain frozen.

A public data: quick English-source scan found the 2026 triadic Prisoner's Dilemma EEG dataset, already present in earlier R-track OpenNeuro ds007822 scouting. It was not downloaded or newly qualified as an independent R073 experiment. New qualified independent data 0; new E2/E3 scores 0.

B evidence: internal nonblind E1 rational oracle and source identity check; no independent real dataset, no external team, no new E2 or E3. Other track and Codex overlap was checked: all 12 Codex PRs remain open, including #1/#3 for R257 S53; none targeted R180. No duplicate R180 validator was built for the previously audited full interval calculations.

No paid paper, API, cloud compute, service, or GitHub Actions was used or initiated. GitHub connector writes only R-owned research/validation files. Account billing and free Actions quota were not independently verified.

Next: run the new CLI on an authentic full checkout when available; then independently review original239 R180 bounded acceptance with the prior full-sample and coverage receipts. P0 production closure for R272 remains the highest risk and should resume before lower-value artificial expansion.

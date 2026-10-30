# B轨 R281 S77 远端完整收据及八项错误注入补充

date_utc: 2026-10-30
baseline_main_head: 702e81e1cd9d02f2964ba7f3be32e124937663e8
target_key: (B,R281,S77-v1,remote-persisted-exact-source-and-eight-mutations)
read: GitHub main archived full R CSV and JSON, original S77 freeze and original R281 report. Nonblind internal programmatic audit.
execution: independent V8 BigInt rational verifier executed directly on remote-fetched full 192-row CSV and 12-world JSON. 192 distinct source keys, 16 per world, exact source mass and 3 symbolic loss coefficients per row, 12 world risk coefficient triples, 60 independent Binomial(4,p) count cells, original unclipped infinity mass and metadata all PASS. R archived source also reexecuted separately and its full regenerated CSV/JSON were byte-equal to persisted remote bytes.
mutation_controls: duplicate atom, missing atom, altered source mass, altered ln2 coefficient, E1 upgraded to E2, original infinity replaced by finite, strict-win probability tampered, frozen test FAIL relabeled PASS. 8 of 8 were actually rejected by the verifier.
frozen_negative_evidence: remains FAIL; p=1/4 versus q=3/4 tie mass 27/128.
native_python_on_remote: NOT_RUN; native_node_on_remote: NOT_RUN; external independent team: NOT_RUN.
evidence: E1 internal nonblind; E2 predictive=0, E3=0. These controls establish internal receipt integrity, not a scientific claim about human behavior.
ci_status: NOT_RUN; billing eligibility not checked; no Actions triggered or paid API used.

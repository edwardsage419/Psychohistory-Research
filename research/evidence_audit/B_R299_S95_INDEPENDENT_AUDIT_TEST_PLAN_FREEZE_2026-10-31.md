# B R299 S95 independent nonblind audit test plan
UTC date: 2026-10-30. Track B under R automation. Baseline main HEAD: 0a7768ed4f05b8d037c69a0823f64d22b107ed03.
Subject key: (B,R299,S95-v1,independent-polynomial-weights-and-full-400-source-audit).
This plan is fixed before running the B auditor. The R S95 prescore freeze commit is 6a84026ee32039b1e4b256ae46370aee1add11de. R source and results are already available and visible to the auditor. This is therefore explicitly NONBLIND within the same research project.

Read scope: original R299 freeze/report/acceptance; S95 prescore freeze; R S95 archived generator, 400 source rows and 40 group results; current original239 v7.8 and pending154; 12 unmerged Codex PR summaries. No external team.

Independent mathematical route: derive each final S0 as a weighted sum of the n terminal rewards. For MC, coefficient at reward j (zero-index) is gamma*alpha*q^(n-1-j). For online TD, coefficient is gamma*alpha^2*(n-1-j)*q^(n-2-j) when j<n-1 and zero for j=n-1, q=1-alpha and alpha=1/2. S1 coefficients are alpha*q^(n-1-j) for both. Use Bernoulli independence to derive mean, variance, squared bias, estimation MSE, and independent holdout risk, rather than importing the R generator or reusing its recursion. Validate every row's source identity, history, probability, final S0/S1, mean, squared error, conditional holdout risk. Validate all 40 group summaries and all 20 MC minus TD comparisons with exact rational arithmetic.

Mutation cases, each expected REJECT: (1) duplicate a source row, (2) delete a source row, (3) corrupt source probability, (4) corrupt S0 estimate, (5) corrupt S1 estimate, (6) corrupt per-row holdout risk, (7) corrupt group aggregate risk, (8) falsely promote E1 scope to E2. Positive original archive must PASS. Negative controls p=0, gamma=0, p=1 deterministic original checkpoint, full mass including zero-weight histories. No assumption that TD or MC always wins.

Scope: mathematical/programmatic nonblind internal E1 audit only. No real E2/E3, probability calibration on real outcomes, or external replication. If execution fails, record exact failure and retain negative evidence. No Actions or paid services.

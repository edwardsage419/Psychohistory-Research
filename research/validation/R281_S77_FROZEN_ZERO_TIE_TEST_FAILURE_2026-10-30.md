# R281 S77 事前冻结负例登记

freeze_commit: aab1a46ebf6ec9b14d904c1625411e90e15c0b28
date_utc: 2026-10-30
frozen_assertion: "zero score-tie when q!=p"
status: FAIL
counterexample: p=1/4, boundary=ONE, epsilon=1/4, q=3/4, four observations exactly two successes
proof: (1/4)^2(3/4)^2=(3/4)^2(1/4)^2, hence identical four-observation likelihood and log score.
mass: C(4,2)(1/4)^2(3/4)^2=27/128
mirror: p=3/4, boundary=ZERO, epsilon=1/4, q=1/4; same mass 27/128
effect: the frozen "no ties for distinct q" negative control is invalid. Keep the frozen document unchanged, report the failure in all results. Strict-win probabilities do not include ties.
evidence: internal nonblind artificial E1; no external replication.

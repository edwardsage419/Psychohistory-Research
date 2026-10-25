# R155 third method prescore freeze: initial adoption jet identification

Date: 2026-10-25 UTC+08. Scope: bounded synthetic E1 mathematical identification audit of the existing R155 Bass (1969) continuous model. Original R155 CLOSED_BOUNDED_E1, its archived results, R073, and PESEN v0.1 remain unchanged.

## Fixed source and model
Original R155 source `research/R155/r155_bass_continuous.py` Git blob `60a296dfdb870c2a49994217d155d0a0387e7e20`, original 75-world grid p in {0,1/200,1/50,2/25,1/5}, q in {0,1/50,1/10,2/5,4/5}, market m in {100,1000,10000}. Use exact Python fractions for p,q,m and no empirical sales data. Fixed ODE F'=(p+qF)(1-F), F(0)=0; count sales S=mF'.

## Preregistered hypotheses and checks
Compute exact time-zero jet J=(S(0),S'(0),S''(0)) independently from the Riccati equation: S0=mp, S1=mp(q-p), S2=mp((q-p)^2-2pq). For p>0, let d=S1/S0 and h=(d^2-S2/S0)/2=pq. The nonnegative p is the unique positive solution of p(p+d)=h with q=p+d and m=S0/p. When q=0, h=0 and d=-p; use p=-d, q=0. For p=0 all three derivatives are zero, regardless of q,m. Compare the resulting exact jet keys across all 75 worlds. No fitting or grid-dependent parameter selection is permitted.

Check: 75 worlds enumerated; 60 positive-p worlds are uniquely distinguished by three jet components and 15 zero-p worlds form one indistinguishable class; exact rational inversion identities hold for every positive-p world. Record two-component jet equivalence classes and any collisions without assuming their counts. Verify invariance under changing market m for the normalized derivatives S1/S0, S2/S0, and scale sensitivity of S0. Negative controls: p=0 cannot be inverted; intentionally discard S2 and report collisions; if a p>0 world is reconstructed with q<0 or m<=0, fail. The independent B audit must derive S2 by polynomial series multiplication or an alternative calculation rather than import the main result or main program.

## Boundaries and acceptance
This is ideal continuous-time local-derivative structural identification with noise-free observation. Finite annual sales, unknown time origin, sample noise, finite differences, changing market size and empirical out-of-sample forecasts are excluded. All 75 rows, exact fractions, collision class counts, source blob and negative controls must be preserved. Classify as E1 only; E2=0 and E3=0. Keep previous R155 closure untouched. Never interpret internal independent implementations as external independent reproduction.

## Concurrency and cost
Write new files under research/validation and research/evidence_audit only. Recheck HEAD, target paths and write rights before each write; never overwrite a concurrent file. Do not trigger paid GitHub Actions or other paid resources. Record CI as NOT_RUN unless actually observed.

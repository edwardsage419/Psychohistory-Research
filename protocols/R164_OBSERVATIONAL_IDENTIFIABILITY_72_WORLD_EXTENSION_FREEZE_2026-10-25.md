# R164 observational identifiability extension, prospective freeze

Date 2026-10-25 (Asia/Singapore). Scope: new internal E1 extension of existing R164, no alteration of its original frozen 72-world protocol, original JSON, R073, or PESEN v0.1.

## Source identity
Use research/R164/R164_EXACT_RESULTS.json (Git blob 087686b629cba4d0b94492d360893a47e334ecb2) and research/R164/r164_content_salience_exact.py (blob b5ab1235bd7355fd2de55431c889580092085312). Original 72 worlds: p0 in {1/5,2/5,3/5,4/5}; r in {1,2,4}; h in {0,1/2,1}; e in {0,1/4}; t=0..4. Original recurrence p_next=(1-e)*(p+h*(r-1)*p*(1-p)/(1+(r-1)*p))+e/2.

## Frozen evaluation plan
1. For each fixed known p0, compare the 18 possible (r,h,e) worlds using three observation regimes: (p0,p1), (p0,p1,p2), and all five p0..p4. Group worlds by exact Fraction trajectory prefixes; record class counts, singleton worlds, ambiguous worlds, largest class, and whether different mechanism parameters are observationally indistinguishable. Report both pooled across four p0 and per p0. No parameter fitting, optimization, or real data.
2. Compare these regimes to a fourth observation regime where e is externally known: group only within the same (p0,e). This is a different information set; never combine its identification counts with unknown-e results.
3. Prove structural nonidentifiability for h=0 regardless of r and r=1 regardless of h. Identify whether nontrivial collisions (r>1,h>0) persist at 1, 2 or 4 transition observations. A collision is only a collision under the stated finite grid.
4. B audit: independent implementation using separate algebraic numerator/denominator arithmetic, grouping the frozen original JSON records without importing the main script, and comparing exact class-membership signatures for all 72 worlds. At least two mutation checks must actually execute: replace salience r with 1 and omit symmetric replacement e, then detect changed trajectory predictions on applicable worlds.
5. Require strict rational equality, 72 distinct world IDs, 360 observed states, all probabilities in [0,1], 4*18 factorial count, and full original frozen JSON replay. All results tagged internal synthetic E1; E2=0, E3=0, external independent replication=0.

## Boundaries
No human behavior evidence, no prediction skill or calibration claim, no E2/E3 promotion. The precomputation protocol must be committed before calculating or reporting class counts. If any check fails, preserve failure and do not claim acceptance. Do not trigger GitHub Actions unless free usage is positively verified. Add only new files in research/validation and research/evidence_audit; A scout is lower priority and may be deferred.

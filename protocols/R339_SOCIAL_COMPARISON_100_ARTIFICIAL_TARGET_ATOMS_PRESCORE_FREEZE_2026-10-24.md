# R339 original239 03-020 Social Comparison Theory: prescore frozen finite target-selection protocol

Date: 2026-10-24. State: FROZEN_BEFORE_SOURCE_GENERATION. Scope: constructed target selection E1 only.

## Provenance and reuse

Festinger 1954, *Human Relations* 7(2):117–140, DOI 10.1177/001872675400700202. Wood 1989, *Psychological Bulletin* 106(2):231–248, DOI 10.1037/0033-2909.106.2.231. See docs/ORIGINAL_239_03-020_SOCIAL_COMPARISON_REUSE_PREAUDIT_2026-10-24.md. R338 reference-gap arithmetic does not cover selection of a comparison target. Complete R001–R064 binary ZIP reuse remains open.

## Frozen universe and rules

Fix the artificial actor's self score to 2. Enumerate in lexicographic order objective_available in {0,1}, candidate A score in {0,1,2,3,4}, candidate B score in {0,1,2,3,4}, total 50 worlds. For each world record two artificial policies in fixed order SIMILARITY then HIGH_SCORE, total 100 source rows.

When objective_available=1, both policies choose target NONE and report estimate 2. When objective_available=0, SIMILARITY chooses the target minimizing absolute score distance to self=2; ties choose A. HIGH_SCORE chooses the target with larger score; ties choose A. Estimate equals chosen target's score. There are no fitted psychological parameters. CSV header exactly objective_available,candidate_a,candidate_b,policy,target,estimate,absolute_error. Store complete JSON conditions in same order, Python json indent 2 ensure_ascii True with final LF; CSV LF. Python 3.11 and 3.12 standard library.

F1: 50 worlds, 100 source rows; 25 objective and 25 no-objective worlds.
F2: 25 objective worlds choose NONE for both, estimate=2, error=0.
F3: 40 agreement worlds and 10 disagreement worlds; all disagreements occur without objective feedback.
F4: no-objective similarity chooses A in 17 worlds and B in 8; high-score chooses A in 15 and B in 10.
F5: among 25 no-objective worlds, similarity absolute error strictly improves over high-score in 8, ties in 17, worsens in zero.
F6: no-objective witness A=2,B=4 chooses A under SIMILARITY and B under HIGH_SCORE; reversed A=4,B=2 chooses B vs A.
F7: independent no-import byte replay and two intentional tamper rejections.
F8: GitHub Actions python311, python312 and independent all success before E1 acceptance. Source commit must follow this protocol freeze. Preserve R073 and PESEN v0.1.

## Boundary

Possible grade PASS_BOUNDED_E1_CONSTRUCTED_TWO_TARGET_SIMILARITY_ONLY. The superiority in error is mechanically guaranteed by minimization of distance to fixed self score; it cannot validate Festinger's human target selection, psychological motivation, objective feedback effects, or original experiment. No real human E2 or historical E3. Original239 primary link is provenance only. Complete R series and itemwise audits before classification or fusion. Personal decision system deferred.

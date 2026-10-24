# R338 original239 03-017 Relative Deprivation Theory: prescore protocol freeze

Date: 2026-10-24. State: FROZEN_BEFORE_SOURCE_GENERATION. Scope: finite investigator-created Boolean mechanism E1 only.

## Provenance and strict reuse gate

Original English sources: W. G. Runciman (1966), *Relative Deprivation and Social Justice* (Routledge), https://www.routledge.com/Relative-Deprivation-and-Social-Justice-A-Study-of-Attitudes-to-Social/Runciman/p/book/9781042033027 ; F. J. Crosby (1976), *A Model of Egoistical Relative Deprivation*, *Psychological Review* 83(2), 85–113, DOI 10.1037/0033-295X.83.2.85. R338 is a deliberately simplified illustration of Crosby's five antecedent conditions. No original participant data recovered.

Existing scope preaudit: docs/ORIGINAL_239_03-017_RELATIVE_DEPRIVATION_REUSE_PREAUDIT_2026-10-24.md. R047 inequality CPR, R293 values, R306 polarization, R307 private/public minority expression, R334 induced compliance do not establish exact joint reference comparison, desire, entitlement, feasibility, attribution. Early R001–R064 ZIP member-level reuse review OPEN_BINARY_ACCESS_BLOCKER. Therefore novelty against all archives is NOT_ESTABLISHED.

## Exhaustive universe, models, and exact falsifiers

Enumerate the lexicographic Cartesian product of six binary input bits, in this order: own resource x, reference resource r, desire d, perceived entitlement e, perceived feasibility f, external attribution a. Each bit is 0 or 1. Total 2^6=64 unique constructed worlds. The bit a=1 means the actor does not blame themselves. Define comparison gap g=1 exactly when x=0 and r=1, else g=0.

Conjunctive model C=g*d*e*f*a. Gap-only countermodel G=g. Store two original artificial CSV atoms per world in fixed order CONJUNCTIVE then GAP_ONLY, total 128 rows. CSV header exactly own,reference,desire,entitlement,feasibility,external_attribution,policy,gap,grievance. CSV line endings LF, UTF-8. Store JSON conditions in the same enumeration order, indent=2, ensure_ascii=True, final LF. Python 3.11 and 3.12 standard library only.

F1: 64 worlds, 128 rows, 16 worlds with g=1 and 48 with g=0.
F2: C positive in exactly one world, G positive in exactly 16 worlds.
F3: C and G agree in 49 worlds and disagree in 15 worlds.
F4: for x=0,r=1, setting all d,e,f,a=1 gives C=1; changing any one of these four bits to zero gives C=0 while G remains 1.
F5: every zero-gap world yields C=G=0, including x=r=0 and x=r=1.
F6: independent no-import enumerator must reproduce CSV and JSON exact bytes and reject one altered CSV output and one altered JSON condition.
F7: GitHub Actions python311, python312 and independent jobs must all finish success before any formal E1 PASS.
F8: source generation commit must strictly follow this protocol freeze commit. Preserve R073 and PESEN v0.1.

## Scientific grade and blockers

A successful result permits PASS_BOUNDED_E1_CONSTRUCTED_REFERENCE_GAP_AND_FOUR_GATES_ONLY. The rules and expected counts are algebraically imposed. This is no empirical evidence that Crosby's five conditions cause resentment, no independent original survey replication, no real human E2, no historical E3 and no causal identification. Formal acceptance must remain PENDING until source, audit and CI are verified. Original239 link is provenance and never scientific validation. Complete R series and itemwise audits before classification and fusion. Personal decision system deferred.

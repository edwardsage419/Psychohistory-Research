# R322 scientific report: finite Type 1 default and Type 2 intervention schematic

Date 2026-10-24. Original239 **01-012 Dual Process Accounts (P2)**. Scientific grade: **PASS_BOUNDED_E1_SCHEMATIC_DEFAULT_INTERVENTION_IDENTIFICATION_ONLY**.

## Original English literature and strict reuse

Evans and Stanovich (2013), *Dual-Process Theories of Higher Cognition: Advancing the Debate*, Perspectives on Psychological Science 8(3):223–241, DOI 10.1177/1745691612460685. The authors emphasize autonomous Type 1 defaults and higher-order Type 2 intervention with working-memory demands; they warn against a universal two-system stereotype or assuming Type 1 is always erroneous. The original source is a conceptual family rather than one uniquely parameterized original empirical model.

R295 habit, R289 sequential satisficing and R303 Bandura observational expression offer finite binary gating or selection components. They do not establish an equivalent dual-process intervention model; only generic gate arithmetic was reusable. Repository code search found no exact dual-process file. Early ZIP and knowledge-card content completeness remains unverified.

## Prospective source and complete artificial universe

Prescore protocol [98cd2788](https://github.com/edwardsage419/Psychohistory-Research/commit/98cd278861258cfa1697bca9a8eb122ebafbb74b) preceded all generated source data [87ddd735](https://github.com/edwardsage419/Psychohistory-Research/commit/87ddd735890286f7117757b95b9a7b31277c674d). All 64 six-bit exogenous states (default h, analytic proposal a, designated correct response y, conflict detection d, resource r, willingness w) are enumerated under four project-defined policy worlds: default only, gated intervention, analytic only, and single-stage Boolean lookup observationally equivalent to gated intervention. Total **256 artificial original source rows**, weight 1/64 each per world.

The gated rule overrides default h only when h differs from a and all three gate bits d=r=w=1. The lookup computes the identical output directly and carries no intervention label. This is a mathematical identification counterexample, without a claim that real cognition uses such a lookup.

## Frozen results and negative controls

The gated rule changes the default output on **4/64** states, compared with **32/64** for analytic-only and zero for default-only. Gated and lookup outputs agree on all **64/64** states despite different internal intervention labels (4 vs 0). This shows that complete response mappings under this artificial input set do not identify the hypothesized internal process labels. Across the fully independent uniform truth y, all four policies have accuracy **1/2**. Deliberation or overriding is therefore not inherently more accurate in this constructed universe. Conditional on a=y and h!=a, the gated override fires in 2 of 16 possible states, exactly **1/8**, and yields the correct answer when it fires.

## Reproducibility and CI

[GitHub Actions run 40014627376](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40014627376) completed three jobs successfully: Python 3.11 and 3.12 each 32 stdlib tests, plus independent no-import truth-table and aggregate audit. [Source generator](r322_dual_process.py) checks full CSV bytes and JSON; [independent audit](../catalogue_audit/independent_r322_dual_process_audit.py) recomputes all 256 rows without importing it. Git blob identity and CI job IDs are recorded in [receipt](R322_MACHINE_RECEIPT.json).

## Strict scope

The mechanism and parameter distribution are project-constructed. The uniform truth variable deliberately prevents a built-in accuracy advantage. No original 2013 human study replication, real working-memory intervention, psychological process identification, causal inference, human E2 or historical E3 is established. The one-process lookup is a proof of observational equivalence within the specified finite mapping, not a general rejection of dual-process theories. The 173 provisional catalogue links remain provisional. R073/PESEN v0.1 frozen; no classification or fusion.

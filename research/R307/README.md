# R307 — Minority Influence: consistency, private belief and public expression

Original239 **03-016 Minority Influence Models**, P1. Original Moscovici, Lage & Naffrechoux (1969), *Influence of a consistent minority on the responses of a majority in a color perception task*, Sociometry 32(4):365–380, https://doi.org/10.2307/2786541; 1994 Wood et al. *Minority influence: a meta-analytic review of social influence processes* https://doi.org/10.1037/0033-2909.115.3.323. **No original blue-green participant judgments, 1994 meta effect sizes or author-fitted quantitative models were used.**

Prospectively frozen [pre-score protocol](../../protocols/R307_MINORITY_INFLUENCE_CONSISTENCY_PRIVATE_PUBLIC_864_SOURCE_PRESCORE_FREEZE_2026-10-23.md) at [commit4f74448e](https://github.com/edwardsage419/Psychohistory-Research/commit/4f74448e261ac61c65cd60926a056d6916a84e34), BEFORE model/source calculation.

This original-to-project **artificial E1 model** posits O_after = [p0/(1−p0)](1+c*k)^t, private=b=O_after/(1+O_after), public=p0+[1−n*(6−m)/6]*(b−p0), with consistency c, credibility k, normative pressure n, minority m∈{1,2} of six, repeated evidence t∈{0,1,2,3}. These likelihood ratios and pressure factors were **invented in the project**, not measured in humans or supplied by Moscovici/Wood. Exact grid 2 prior probabilities ×4 exposures ×3 consistency ×3 credibility ×3 normative pressure ×2 minority sizes = **432 synthetic worlds, 864 complete private/public original source rows**.

* [Native exact model, 2607 unittest cases per Python interpreter](r307_exact_minority_consistency_private_public.py)
* [All 864 original fully labeled synthetic source rows](R307_ALL_864_ORIGINAL_MINORITY_PRIVATE_PUBLIC_SOURCES.csv)
* [All 432 private/public worlds and posterior trajectories JSON](R307_EXACT_MINORITY_INFLUENCE_RESULTS.json)
* [Original CSV and JSON byte SHA256 receipt](R307_MACHINE_RECEIPT.json)
* [Independent no-import normalized sequential Bayes audit, 18 adversarial tests](../catalogue_audit/independent_r307_source_audit.py)
* [Full scientific report and identifiability/empirical limitations](R307_SCIENTIFIC_REPORT_2026-10-23.md)
* [Final machine-scoped E1 acceptance](R307_FINAL_ACCEPTANCE_STATUS.json)

Example: p0=1/4, 3 repeated exposures, c=k=1 -> **private 8/11**. With full normative pressure, m=2/6 -> **public 9/22**; m=1/6 -> **public 29/88**. With no normative pressure, public=private=8/11. The independent counterexample (c,k)=(1/2,1) vs (1,1/2) gives the same private 9/17: **consistency and credibility not identified separately from final output**. Zero evidence strength or no exposure leaves original prior unchanged.

[Science CI run39953705822](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953705822) all 3 jobs completed/success. Python3.11 and3.12 each ran2607 model tests plus18 independent tests, third independently verified all rows and permanent archives [commit d4ebc9cb](https://github.com/edwardsage419/Psychohistory-Research/commit/d4ebc9cbbffe550a61aa2d602fc3bceb79fb4850).

No new human/animal E2, historical E3 or model prediction validity. Related R115 informational cascades / R116 normative public/private effects have separate original research paths. R073/PESEN v0.1 remain frozen, R-series completed before taxonomy and fusion.

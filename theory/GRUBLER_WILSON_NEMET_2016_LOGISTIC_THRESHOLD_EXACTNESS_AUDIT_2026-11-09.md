# Grubler, Wilson 与 Nemet（2016）Logistic 时间阈值原文核查及精确勘误候选

track: theory
subflow: theory / D-source-support
run_date: 2026-11-09 (Asia/Singapore)
observed_head: 9b150cb032d1ba2b2045a7eec305a2c5440ff609
target_key: (theory,Grubler-Wilson-Nemet-2016,UEA-accepted-manuscript-2016-06-30,logistic_threshold_duration_exactness)
status: PRIMARY_TEXT_BOUNDED; EXACT_ALGEBRA; NO_HISTORICAL_REESTIMATION
source: Arnulf Grubler, Charlie Wilson, Gregory Nemet (2016), *Apples, oranges, and consistent comparisons of the temporal dynamics of energy transitions*, Energy Research & Social Science 22:18–25. DOI 10.1016/j.erss.2016.08.015. University of East Anglia deposited accepted manuscript: https://ueaeprints.uea.ac.uk/id/eprint/60764/1/grubler_etal_apples_oranges_ERSS_preprint_clean_30June2016.pdf . Repository record states CC BY-NC-ND for deposited manuscript; no source text reproduced here.
reading_scope: Accepted manuscript PDF physical pages 2–3 (PDF indices 1–2), section 1, including its footnotes; physical pages 7–9 (indices 6–8), sections 4 and formative phase. Published journal layout and any journal erratum NOT_READ.

## 原文核查

The accepted manuscript at PDF page index 1 states that the duration from 1% to 50% (also 50% to 99%) is **identical** to the duration from 10% to 90% for a symmetric logistic curve. The same assertion recurs in the table caption at PDF index 5 and discussion at index 11. This is an exact-wording finding in the author manuscript, not merely a previous assistant paraphrase. Whether the journal's final typeset text repeats it is NOT_VERIFIED.

## 严格代数核查

For the ordinary logistic share p(t)=1/(1+exp(-k(t-t0))), k>0, the elapsed time from a to b is [ln(b/(1-b))-ln(a/(1-a))]/k.

* 1% to 50%: ln(99)/k = 4.59511985013459/k.
* 50% to 99%: ln(99)/k = 4.59511985013459/k.
* 10% to 90%: 2 ln(9)/k = ln(81)/k = 4.39444915467244/k.
* Ratio: ln(99)/ln(81)=1.04566458 approximately. Thus the first interval is about 4.566% longer than the 10–90% interval.

The equalities 1–50 = 50–99 and 10–90 = 2 times 10–50 are exact for this symmetric logistic. The manuscript's cross-threshold identity is an approximation (difference about 4.6%), unless a nonstandard threshold convention is intended. This correction does not establish which empirical diffusion curve is logistic, and cannot validate or invalidate historical transition durations.

## Separate historical-measurement issue

PDF index 1 footnote reports doubling the rapid-transition durations to 6–32 years after excluding the Brazil Flexfuel sales/stock mismatch and Kuwait scale mismatch. The doubling is a rough threshold harmonization heuristic, not an exact logistic conversion. At PDF index 2 the manuscript distinguishes annual new-vehicle sales from total vehicle stock; its reported 2010 Brazil 40% registered Flexfuel cars and 18% ethanol road transport energy are secondary historical numbers cited by the authors, not independently recomputed here. PDF index 7 reports Bento and Wilson's 16 technologies averaging 22 years in formative phases, with threshold definitions specified; underlying series NOT_READ.

## Evidence, competition, and boundaries

Original author manuscript text: directly inspected specified pages. Algebra: independently derived from a stipulated function, with no real historical data. The manuscript critiques Sovacool (2016) on threshold, system boundary, stock/flow, formative phase and leading/late market differences. Its own exact logistic identity requires the qualification above. Alternative asymmetric diffusion curves or different saturation levels invalidate any unqualified universal conversion. The present finding is an author-manuscript mathematical precision issue; final published text, formal corrigendum, and original data remain unchecked. No R E1/E2/E3 upgrade, no D weekly completion, no C daily completion.

tests: Symbolic algebra checked manually; executable tests NOT_RUN.
CI: NOT_RUN; no CI dispatch.
billing: no new paid service requested; account billing NOT_VERIFIED.
next_action: verify published final journal text or erratum if freely accessible; keep this source audit separate from D004 historical case reconstruction and C-track methods.

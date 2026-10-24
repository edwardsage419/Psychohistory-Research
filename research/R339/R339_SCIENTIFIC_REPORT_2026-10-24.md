# R339 scientific report: constructed two-target similarity selection

Date: 2026-10-24. Original239 **03-020 Social Comparison Theory**. Scientific grade **PASS_BOUNDED_E1_CONSTRUCTED_TWO_TARGET_SIMILARITY_ONLY**.

## Original English sources and strict reuse

Festinger (1954), *A Theory of Social Comparison Processes*, *Human Relations* 7(2):117–140, DOI 10.1177/001872675400700202, publisher https://journals.sagepub.com/doi/10.1177/001872675400700202 . Wood (1989), *Theory and Research Concerning Social Comparisons of Personal Attributes*, *Psychological Bulletin* 106(2):231–248, DOI 10.1037/0033-2909.106.2.231. The literature concerns human self-evaluation and target selection; R339 uses no human observations.

[Strict reuse preaudit](../../docs/ORIGINAL_239_03-020_SOCIAL_COMPARISON_REUSE_PREAUDIT_2026-10-24.md) checked R338 reference-gap arithmetic, R293 value centering, R303 observational learning and R334 induced compliance. Exact target selection was not verified. Early R001–R064 binary ZIP itemwise reuse remains open, so exhaustive novelty is not established.

## Frozen protocol and source

Prescore protocol [dba0ded5](https://github.com/edwardsage419/Psychohistory-Research/commit/dba0ded506b85e7c938a2c97d9478c2cd1daf120) precedes original artificial source commit [9152132d](https://github.com/edwardsage419/Psychohistory-Research/commit/9152132df26ecfb9a09aaa6ce09f12aedd3658e9). Fix self score 2, candidate A/B scores 0 through 4, objective availability binary. Complete 50 constructed worlds, 100 source rows. With objective feedback both policies choose NONE and use self score. Otherwise SIMILARITY chooses the closest target to self score with A ties; HIGH_SCORE chooses the larger candidate score with A ties.

| Frozen falsifier | Exact result | Assessment |
|---|---:|---|
| F1: worlds and original artificial atoms | 50 / 100 | PASS |
| F2: objective feedback worlds choosing NONE | 25 | PASS |
| F3: policy agreement and disagreement | 40 / 10 | PASS |
| F4: no-objective SIMILARITY A/B choices | 17 / 8 | PASS |
| F4: no-objective HIGH_SCORE A/B choices | 15 / 10 | PASS |
| F5: similarity strictly lower / equal / higher absolute error | 8 / 17 / 0 | PASS |
| F6: A=2 B=4 and reversed A=4 B=2 | opposite targets | PASS |
| F7: independent no-import byte replay and two tamper rejections | PASS | PASS |
| F8: Python 3.11, 3.12, independent CI | 3 successful jobs | PASS |

The error advantage follows the imposed nearest-score optimization against the fixed self score. It is an algebraic consequence of the constructed policy. The objective-standard branch was also assigned directly. Neither effect identifies human motivation or target selection.

## Independent audit and provenance

[GitHub Actions run 40059401269](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40059401269) finished success, with python311, python312 and independent jobs all success. Each production interpreter passed six tests and byte replay. The independent enumerator decomposed world indices into objective flag and two base-five scores, recreated CSV and JSON bytes without importing production code, and rejected altered CSV and JSON. Original source blob fe06c06c7f158ab174251f1a14d184a4317b3371, result blob 817389e331f07dda90ae291daef9b20df1f65363.

## Evidence boundary

Human E2: NOT_ESTABLISHED. Historical E3: NOT_ESTABLISHED. Festinger original human experiment replication: NOT_ESTABLISHED. No inference about the actual frequency of upward/downward comparison, emotional consequences, or subjective ability judgments. Full early ZIP reuse audit OPEN. Catalogue linkage is provenance only. R073 and PESEN v0.1 frozen. R series and itemwise audits precede taxonomy and fusion. Personal decision system deferred.

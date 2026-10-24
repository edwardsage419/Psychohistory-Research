# R337 scientific report: constructed argument-quality and source-cue gating

Date 2026-10-24. Original239 **03-015 Elaboration Likelihood Model**. Formal scientific grade **PASS_BOUNDED_E1_CONSTRUCTED_BINARY_ELM_GATE_ONLY**.

## Original English research and existing R reuse

Petty and Cacioppo (1986), *The Elaboration Likelihood Model of Persuasion*, *Advances in Experimental Social Psychology* 19:123–205, DOI 10.1016/S0065-2601(08)60214-2, [original author PDF](https://richardepetty.com/wp-content/uploads/2019/01/1986-advances-pettycacioppo.pdf). Petty, Cacioppo and Schumann (1983), *Central and Peripheral Routes to Advertising Effectiveness: The Moderating Role of Involvement*, *Journal of Consumer Research* 10(2):135–146, DOI 10.1086/208954. Petty, Cacioppo and Goldman (1981), *Personal Involvement as a Determinant of Argument-Based Persuasion*, *Journal of Personality and Social Psychology* 41(5):847–855, DOI 10.1037/0022-3514.41.5.847. The original human experiments crossed involvement with argument and source cues. R337 has no original participant-level data.

[Strict reuse preaudit](../../docs/ORIGINAL_239_03-015_ELABORATION_LIKELIHOOD_REUSE_PREAUDIT_2026-10-24.md) examined R322 generic default/override, R291/R292 attitudes and intentions, R307 source consistency/private expression, and R336 prior refutation transfer. Their inspected reports do not contain the exact R337 factorial model. Early R001–R064 ZIP itemwise audit remains open. No claim of exhaustive novelty.

## Frozen protocol and complete artificial source

[Protocol freeze c26ded95a844908d692f069c1a11ac1934b15487](https://github.com/edwardsage419/Psychohistory-Research/commit/c26ded95a844908d692f069c1a11ac1934b15487) preceded [source commit 7f7a44f9596acb5d06ffe4d51677e59d75a5f357](https://github.com/edwardsage419/Psychohistory-Research/commit/7f7a44f9596acb5d06ffe4d51677e59d75a5f357). Five binary variables were exhaustively enumerated: involvement, ability, signed argument quality, signed source cue, and cue visibility. **32** complete constructed conditions, two policies per condition, **64** original artificial CSV records.

The ROUTE_GATE policy assigns central gate g=involvement*ability. When g=1, score=2*argument quality; when g=0, score=cue visibility*source cue. FIXED_ADDITIVE assigns score=argument quality+cue visibility*source cue in every condition. All coefficients, scores and binary gate are investigator-created. They do not represent fitted persuasion probabilities or the original ELM's full elaboration continuum.

## Frozen exact tests

| Falsifier | Result | Assessment |
|---|---|---|
| F1 | 32 complete worlds, 64 artificial records | PASS |
| F2 | 8 central worlds, 24 other worlds, 12 no-cue low worlds score zero | PASS |
| F3 | Argument-quality flip: central 4 pairs change by 4, low 12 pairs by 0 | PASS |
| F4 | Source-cue flip with cue visible: central 2 pairs change by 0, low 6 pairs by 2 | PASS |
| F5 | Route gate and fixed additive agree 2/32, disagree 30/32 | PASS |
| F6 | Independent no-import replay, two deliberate tamper rejections | PASS |
| F7 | Python 3.11, Python 3.12 and independent CI all success | PASS |

The two agreeing conditions require g=1, cue visible and source cue equal to argument valence. These agreements are deterministic algebraic coincidences. The contrast's direction is imposed by the gated weights, so the results cannot independently confirm the original human experimental moderation effects.

## Independent audit and verification

[GitHub Actions 40055959491](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40055959491) completed with three successful jobs: python311, python312 and independent. Each production interpreter ran six tests and byte replay. The independent auditor uses integer-index enumeration rather than importing the production module, recreates complete CSV and JSON bytes, and rejects one tampered CSV policy and one tampered JSON score. The checks establish arithmetic replay integrity for the frozen constructed universe only.

## Evidence limits

Real human E2 **NOT_ESTABLISHED**. Historical E3 **NOT_ESTABLISHED**. Original 1981/1983 experimental replication **NOT_ESTABLISHED**. This study neither identifies central/peripheral psychological processing nor tests persistence of attitude change. The binary route gate is a schematic that excludes mixed and biased elaboration. Early ZIP reuse audit and 173 provisional README relations remain OPEN. Catalogue linkage is provenance only. R073 and PESEN v0.1 frozen. Finish R series and evidence audits before classification and fusion; personal decision system deferred.

# R342 scientific report: finite three-actor local choice analogue

Date: 2026-10-24. Original239 **04-021 Stochastic Actor Oriented Model**. Grade **PASS_BOUNDED_E1_CONSTRUCTED_THREE_ACTOR_LOCAL_CHOICE_ONLY**.

## Original sources and reuse
Snijders (2001), *The Statistical Evaluation of Social Network Dynamics*, *Sociological Methodology* 31:361–395, DOI 10.1111/0081-1750.00099. Snijders, van de Bunt and Steglich (2010), *Introduction to stochastic actor-based models for network dynamics*, *Social Networks* 32:44–60, DOI 10.1016/j.socnet.2009.02.004. [Preaudit](../../docs/ORIGINAL_239_04-021_SAOM_REUSE_PREAUDIT_2026-10-24.md) distinguishes static R341 ERGM, exogenous R317 contacts, and R314 preferential attachment. Early binary ZIP strict reuse remains OPEN.

## Frozen protocol and source
[Prescore protocol](../../protocols/R342_SAOM_THREE_ACTOR_1152_ARTIFICIAL_CHOICE_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed at [a18daa73](https://github.com/edwardsage419/Psychohistory-Research/commit/a18daa73d3fc2db9f01b2a50ef70a7094bdb6e9f), before [source commit e3b94a89](https://github.com/edwardsage419/Psychohistory-Research/commit/e3b94a895e16a578dbcedeaf21b4a0806a25518f).

Three labeled actors, six directed ties, all 64 possible directed networks. Each actor chooses stay or toggles one outgoing tie. Two artificial reciprocity-weight regimes r=1 and r=2. Choice weight is r^(number of reciprocated outgoing ties in candidate resulting network). Each three-choice local probability is normalized exactly.

| Frozen test | Exact result | Status |
|---|---:|---|
| F1: worlds, networks, actors, local decisions, source atoms | 2, 64, 3, 384, 1152 | PASS |
| F2: nonnegative weights and normalized local probabilities | 384/384 | PASS |
| F3: r=1 uniform decisions | 192/192 | PASS |
| F4: stay and exactly one outgoing-tie toggle | 384/384 | PASS |
| F5: reciprocity-weight odds ratios | all 384 decisions | PASS |
| Additional descriptive: r=2 nonuniform decisions | 144/192 | VERIFIED |
| F6: frozen output formats and checks | exact | PASS |
| F7: independent no-import replay and two tamper rejections | PASS | PASS |
| F8: Python 3.11, 3.12, independent jobs | 3 success | PASS |
| F9: protocol predates source; frozen assets preserved | PASS | PASS |

The local-choice contrast follows investigator-imposed weights. It supplies no evidence that human actors optimize reciprocity. The model omits the stochastic actor opportunity clock, longitudinal inference and other SAOM effects.

## CI and provenance
[GitHub Actions run 40063626962](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40063626962) concluded success. Jobs python311, python312 and independent all success. Seven unit tests per interpreter. The independent enumerator reconstructs the full 1152-row CSV and 384-decision JSON without importing production and rejects two deliberate corruptions.

Protocol blob 5b62289a71d9a3893aac0b57108eb51852ebc582. Source blob d3899536531c7bc708f7ee603116b6002573e951. Results blob c11012e3d4857e7a9c175b2abe9191bdc0b38f59. Production blob e54b2e3fa76a794d5feb71c4b9ba6e81bcb46ce9. Independent blob c967bca36bdb7baefd35752981db51888979bb91.

## Scientific limits
Human E2: NOT_ESTABLISHED. Historical E3: NOT_ESTABLISHED. Full stochastic actor-oriented model estimation, real longitudinal social networks, network/behavior coevolution, causal identification and original author replication remain untested. Catalogue linkage is provenance only. R073 and PESEN v0.1 frozen. R-series research and evidence audit before classification and fusion. Personal decision system deferred.

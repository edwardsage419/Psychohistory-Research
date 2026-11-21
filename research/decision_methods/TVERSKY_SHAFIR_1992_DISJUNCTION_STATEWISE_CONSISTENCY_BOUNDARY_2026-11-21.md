# Tversky and Shafir (1992): disjunction effect and statewise consistency boundary

Date actually reviewed: 2026-11-21. Track: personal decision theory. Status: source abstract reviewed; candidate acceptance preparation only.

## Primary sources and actual scope
1. Amos Tversky and Eldar Shafir (1992), *The Disjunction Effect in Choice under Uncertainty*, Psychological Science 3(5), 305–310 (publisher listing; Princeton lists 305–309, bibliographic discrepancy unresolved). DOI: https://doi.org/10.1111/j.1467-9280.1992.tb00678.x . Read publisher and Princeton institutional **abstracts**, not complete experiments, tables, or original participant data.
2. Eldar Shafir and Amos Tversky (1992), *Thinking through Uncertainty: Nonconsequential Reasoning and Choice*, Cognitive Psychology 24, 449–474, DOI https://doi.org/10.1016/0010-0285(92)90015-T . Read first page of Carnegie Mellon-hosted original PDF: https://iiif.library.cmu.edu/file/Simon_box00035_fld02674_bdl0001_doc0001/Simon_box00035_fld02674_bdl0001_doc0001.pdf . Remaining pages not independently inspected.

## Finding, assumptions, competing explanations
Publisher abstract reports cases in which a person prefers X to Y if A occurs and also if A does not occur, yet hesitates or selects Y when A is unknown. Making preferences under both branches salient may restore consistency. This is evidence for a possible branch-integration failure, not a quantified effect size or a universal normative command.

The statewise dominance check requires the **same feasible actions**, exhaustive mutually exclusive A / not-A branches, comparable consequences, fixed relevant preferences and constraints, and no additional value of waiting, learning, or timing. If these conditions fail, apparent reversal may be rational. Competing explanations: information value, action timing, state-dependent utility, different choice sets, missing branches, measurement framing, and attention or reasoning failures.

## Candidate user question and explanation rule
When the user hesitates because an uncertain event is unresolved, ask: “If event A happens, which option would you choose? If A does not happen, which would you choose? Would waiting reveal useful information or change your options, costs, deadlines, or preferences?” Preserve the three answers with their question framing and timestamps.

If X is preferred in every genuinely exhaustive branch under unchanged conditions, flag the unconditional preference for Y or delay as **a consistency question to clarify**, not an automatically corrected choice. If probabilities are missing, do not invent them. If waiting changes available actions, treat it as a distinct option and evaluate its costs and information value separately. Never override user hard constraints or value weights.

## Six synthetic acceptance counterexamples (not executed)
1. Branch A favors X, branch not-A favors X, unconditional response Y: request clarification and retain all three original answers.
2. A / not-A are not exhaustive because a third outcome exists: refuse a dominance claim.
3. X is unavailable in one branch: reject the statewise comparison.
4. Waiting produces a useful diagnostic signal and permits contingent action: preserve wait as a separate candidate; do not label it irrational.
5. User changes a value weight or deadline between branch and unconditional questions: version the preferences and withhold consistency judgment.
6. Branch probabilities are unknown: never turn the observed experimental pattern into a personal probability or numeric expected utility.

## Deduplication and handoff
Checked decision_methods directory (86 entries at inspection); existing TVERSKY_SHAFIR_1992_CONFLICT_DEFERRAL_OPTION_SET_BOUNDARY_2026-11-21.md concerns conflict and deferral. This record is restricted to **statewise consistency with explicit branch completeness and value-of-information exceptions**. Full semantic cross-track dedup remains pending.

Independent acceptance track: construct held-out cases for all six counterexamples. Model track: consider a non-coercive branchwise clarification step. Data track: verify whether branch outcomes, signal timing and available actions are observable. No code, tests, reanalysis, independent replication, or scientific acceptance claimed. No changes to R073, PESEN v0.1, or frozen protocols. Zero additional cost.

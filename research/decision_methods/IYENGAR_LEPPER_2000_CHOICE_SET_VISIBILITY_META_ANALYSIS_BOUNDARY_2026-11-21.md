# Choice-set visibility and overload: evidence boundary (2026-11-21)

## Scope and provenance
Decision capability: natural-language option elicitation, candidate shortlisting, explanation, and user control. Research track only; no product implementation or scientific acceptance.

Primary publication: Sheena S. Iyengar and Mark R. Lepper (2000), *When Choice Is Demotivating: Can One Desire Too Much of a Good Thing?*, Journal of Personality and Social Psychology 79(6):995–1006, DOI 10.1037/0022-3514.79.6.995. Actually reviewed: Columbia Business School author-affiliated abstract (https://business.columbia.edu/faculty/research/when-choice-demotivating-can-one-desire-too-much-good-thing) and PubMed bibliographic abstract (https://pubmed.ncbi.nlm.nih.gov/11138768/). Full methods and tables were not independently checked.

Competing original research: Benjamin Scheibehenne, Rainer Greifeneder and Peter M. Todd (2010), *Can There Ever Be Too Many Options? A Meta-Analytic Review of Choice Overload*, Journal of Consumer Research 37(3):409–425, DOI 10.1086/651235. Actually reviewed: journal publisher abstract (https://doi.org/10.1086/651235) and author-hosted opening text (https://www.scheibehenne.de/ScheibehenneGreifenederTodd2010.pdf). Meta-analysis reports 63 conditions from 50 experiments, N=5,036, average effect virtually zero and considerable heterogeneity. This is a literature synthesis, not independent replication of the specific jam experiment.

Competing explanation: Alexander Chernev, Ulf Böckenholt and Joseph Goodman (2010), *Commentary on Scheibehenne, Greifeneder, and Todd*, Journal of Consumer Research 37(3):426–428, DOI 10.1086/655200. Actually reviewed: publisher abstract. Argues conditional moderators and underlying mechanisms matter; does not establish a universal number of options.

## Findings and limits
Iyengar and Lepper's three studies report lower action rates or satisfaction under larger option sets (6 versus 24/30 in their tasks). This is task-specific experimental evidence. The 2010 meta-analysis found near-zero mean effect across heterogeneous studies. Neither establishes that a personal life-decision tool should cap all option sets at six or that removing alternatives improves objective decision quality.

The number of options, their comparability, prior preferences, cognitive effort, decision urgency and exposure to omitted options can all change outcomes. Shortlisting may ease presentation while hiding a feasible alternative. Existing work on conflict-induced deferral (Tversky/Shafir 1992), status quo framing (Samuelson/Zeckhauser 1988) and multi-objective feasibility is adjacent; this record concerns the **visibility and auditability of the candidate set**, rather than automatic preference scoring or deferral probability.

## Candidate elicitation and explanation rule
When the user reports too many alternatives, ask: “你希望先按哪些由你确认的底线筛选或分组？需要保留查看全部方案和恢复被隐藏方案的入口吗？”

Maintain the full user-supplied candidate inventory and immutable eligibility evidence. Distinguish user-authorized hard-constraint exclusion from reversible display-only grouping or shortlisting. Explain why each item is hidden and which user-confirmed condition or preference produced that view. Do not infer a universal optimal count, silently delete options, or treat shortlisting as evidence that an option is objectively inferior. Keep status quo and time-sensitive options visible when applicable.

## Synthetic acceptance counterexamples, proposed only
1. Ten feasible career options are provided; the system silently keeps the top six and deletes the remaining four. FAIL: display reduction changed the feasible set.
2. User changes a weight; a previously hidden option should reappear, but cached shortlist prevents its comparison. FAIL: view is stale.
3. One option violates a confirmed licensing requirement; system presents it as merely “low ranked” rather than hard-infeasible. FAIL: exclusion reason is lost.
4. The user requests all options; the interface refuses because the 2000 experiment supposedly proves that six is optimal. FAIL: unsupported generalization and loss of agency.
5. A deadline-bound option is grouped out of sight without an expiration warning. FAIL: omission hides a material timing constraint.
6. User is shown six options and chooses one; system reports that choice overload was causally reduced without a controlled comparison. FAIL: unsupported causal inference.

## Status and handoff
Completed: source abstracts, targeted directory de-duplication, concrete question, competing evidence, six synthetic cases, research write. Not run: original participant-level replication, software tests, independent held-out acceptance, personal longitudinal validation. This document is a research candidate, not an approved product requirement.

Independent acceptance track: design held-out cases for hidden option recovery, view changes after weights and deadlines. Model track: assess reversible view-only shortlisting with transparent rationale after owner authorization. Data track: investigate legal evidence for choice-set effects in real decision interfaces, avoiding private personal data.

No paid API, CI, PR merge, or change to R073/PESEN frozen records.

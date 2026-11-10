# F011 | Commitment contracts: behavioral effect, welfare and reversibility | 2026 W46

Status: COMPLETE_BOUNDED_PRIMARY_RESEARCH_REVIEW
Track: F privacy, ethics and decision safety. Research only. No deployment, personal data, paid resources, or product development.
Baseline main at prewrite read: 0d1c1154c37624f477535719848e74a302002803 (2026-11-10 06:19:01 UTC). This note does not modify R protocols or scientific grades.

## Primary evidence

1. Carrera, Royer, Stehr, Sydnor and Taubinsky, *Who Chooses Commitment? Evidence and Welfare Implications*, Review of Economic Studies 89(3), 2022, DOI 10.1093/restud/rdab056; free NBER working paper w26161, revised August 2021, https://www.nber.org/papers/w26161 . Randomized gym experiment N=1,248. Offering contracts for greater attendance increased exercise. About half of people accepting an increased-attendance commitment also accepted a decreased-attendance commitment. The authors' structural welfare model estimates negative consumer surplus for their offered contracts and greater efficiency of linear exercise subsidies for the same mean behavior change. Welfare estimates are model dependent; this is not a product-specific Beeminder or StepBet trial.

2. Spika, Wickström Östervall, Gerdtham and Wengström, *Put a bet on it: Can self-funded commitment contracts curb fitness procrastination?*, Journal of Health Economics 98 (2024), abstract at https://econpapers.repec.org/article/eeejhecon/v_3a98_3ay_3a2024_3ai_3ac_3as0167629624000882.htm ; free university working-paper abstract https://www.lusem.lu.se/ulf-gerdtham/publication/fdf4c5f0-dfee-4bea-ba81-565c5145852b . Randomized offers to 1,629 Stockholm gym members: hard financial-stake contracts increased visits 21% relative to control, soft contracts 8%. This measures attendance under an offer; no independently established long-term welfare gain follows from the abstract.

## Evidence boundaries

The two studies differ in setting, incentive, selection, treatment, and outcome. Their numerical effects are not pooled. They establish that behavior can change under contracts, while contract choice and welfare can diverge. Neither establishes effectiveness or welfare for any named commercial product. The structural welfare estimates are assumptions-sensitive and should not be treated as directly observed utility. No original raw dataset was downloaded or reanalyzed in this review.

## Bounded future-system safety questions

* Record the user's initial goal, anticipated benefit, acceptable loss, and explicitly revocable authorization separately from behavioral completion.
* Evaluate realized target completion, penalty burden, changes after incentive removal, and postdecision preference or regret as separate endpoints.
* If a user selects conflicting commitments, surface the conflict and ask for review in any future design; never interpret take-up alone as informed long-term preference.
* Research whether withdrawal, adjustment, data export and deletion can be implemented without corrupting historical evidence, and distinguish voluntary goal revision from data tampering.
* Any recommendation with financial penalties needs heightened uncertainty disclosure and final human control. These are candidate requirements, not tested protections.

## Audit and scope

Evidence: published peer-reviewed paper abstract, NBER author working paper, and university working-paper abstract. Research design and abstract results inspected; full-paper statistical reproduction NOT_RUN. No synthetic experiment was represented as real-user evidence. No commercial product algorithm, pricing or data processing claims are certified here. F011 is one weekly bounded topic; further numbered extensions require new independent evidence or an actual safety need.

Scientific sequence remains all planned R studies, unified classification, conditional synthesis, then potential personal decision application.

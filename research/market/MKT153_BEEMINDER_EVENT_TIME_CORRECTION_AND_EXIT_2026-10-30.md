# MKT153 Beeminder event-time correction, commitment exit and evidence limits

UTC 2026-10-30. Track market. Target key (market,Beeminder,official-help-2026-10-30,deadline-asof-correction-and-exit). Baseline main 1c5086b63085b04360f8186ebb774dfe416a8350. Status COMPLETE_BOUNDED_OFFICIAL_DOC_PLUS_ARTIFICIAL_E1. Read MKT152 and market handoff first. This is the first Beeminder-specific deep dive after Dcider and Exist.

## Primary English product evidence read on 2026-10-30

* Beeminder official red-line and 7-day akrasia horizon: https://help.beeminder.com/article/17-what-is-the-akrasia-horizon ; easing goal rates, scheduling breaks, archiving and reducing pledges normally take seven days.
* Data correction: https://help.beeminder.com/article/39-how-do-i-fix-incorrect-data ; correcting or deleting past data can trigger a derailment, and connected auto-data can refetch source truth and overwrite local edits.
* Derailment and legitimacy review: https://help.beeminder.com/article/17-what-happens-when-i-derail and https://help.beeminder.com/article/324-when-do-i-pay ; official help describes an email legitimacy check and generally a 24-hour delay before ordinary derailment charges, with exceptions for certain immediate actions. The support process can correct non-legitimate charges. The service's internal charge decision code is unavailable.
* Goal exit: https://help.beeminder.com/article/44-how-do-i-quit-a-goal ; standard archiving has a seven-day countdown, with limited exceptions and support contact for urgent issues.
* Data export and sync: https://help.beeminder.com/article/41-can-i-export-my-data ; CSV/TSV export and API datapoints are documented, webhook delivery may fail silently and reconciliation fetches are advised.
* Privacy: https://help.beeminder.com/article/102-privacy ; new goals default to public graphs with private datapoint values. https://help.beeminder.com/article/48-how-do-i-delete-my-account ; active-account deletion requires support confirmation, and past payment metadata and support emails may remain with the payment processor or service after account deletion.
* Cost: https://help.beeminder.com/article/19-how-much-does-beeminder-cost ; up to three active goals without a subscription, a stated $5 charge if no goal is created during the first week, derailment pledges and optional premium tiers. No account, payment method, pledge or subscription was created.

## Mechanism inventory and boundaries

Documented input: user-entered or connected-source dated datapoints, goal type, rate/road, deadline, pledge and account preferences. State: cumulative graph relative to the bright red line, safety buffer, scheduled future road edits and goal archival. Feedback: reminders, deadline assessment, derailment/road reset, legitimacy check and possible financial pledge. Self-correction: manual edits or source-side automatic refetch, support-mediated dispute. Explainability: graph, visible target line and documented deadline rules. Privacy: graph visibility controls and account deletion route; actual internal data access and deletion effects have not been independently audited. Cost: potentially real financial charges even without a premium subscription. Scientific validation: these help pages establish product behavior claims, not controlled causal evidence that long-term personal outcomes improve.

## Actually executed finite synthetic counterexample

The archived script `research/market/mkt153_beeminder_asof_20261030.js` ran in local Node 22.16.0: 16 assertions PASS. It models a fictional Do More goal with deadline threshold 2 at event-time 1. World A records value 2 at time 0, later revises to 1 at time 2 and restores 2 at time 3. World B records value 1 at time 0 and revises to 2 at time 2.

At deadline time 1, A is SAFE (2) and B SHORT (1). At time 2, the historical values are reversed. At time 3, both current snapshots equal 2 and display SAFE. Thus the identical current datapoint cannot reconstruct the deadline-time state or whether an appeal may be relevant. The experiment records a simple as-of ledger; it does not emulate Beeminder's billing algorithm, graph reset, grace periods, support judgment or monetary charges. The seven-day rule is recorded as official policy, not derived from this toy.

Candidate future knowledge reserve: store event-time and effective-time versions, source identity, goal/road version, deadline/timezone, correction reason, alert/charge review status, explicit user withdrawal and independent appeal evidence. Distinguish recorded event state from corrected state and billing legitimacy. Any future personal decision application should support a no-money path, immediate emergency safety suspension and human override subject to legal review. Those are design proposals, not Beeminder features or validated interventions.

Evidence labels: PRODUCT_OFFICIAL_HELP, INTERNAL_NONBLIND_ARTIFICIAL_E1; vendor product claims and privacy assurances are not third-party verified. New human E2=0, historical E3=0. No real user data or payment activity. Next: evaluate whether a free/open-source non-financial commitment design can preserve correction provenance and voluntary exit without introducing coercive penalties.

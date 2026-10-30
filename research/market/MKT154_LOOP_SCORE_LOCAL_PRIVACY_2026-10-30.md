# MKT154 Loop Habit Tracker: local-first habit scoring and missingness

UTC 2026-10-30. Track market. Target (market,Loop-Habit-Tracker,Score.kt-blob-9b26f3486c2a51b2ed0188195af5d1e2e1a09084,score-order-skip-local-privacy). Baseline main adcb1a703a6fe1fb3b18cd5930764d77de616e20. Status COMPLETE_BOUNDED_SOURCE_CODE_AND_SYNTHETIC_E1.

## Original English sources read 2026-10-30

* Maintainer repository README and license: https://github.com/iSoron/uhabits ; source branch dev. GPLv3, no ads, in-app purchases or subscription, offline operation, CSV/SQLite export, reminders, habit score, flexible schedules. No user account required.
* Actual core scoring implementation: https://github.com/iSoron/uhabits/blob/82c1ff287a8ac05321bfa95b61399fa8a2d1da5b/uhabits-core/src/commonMain/kotlin/org/isoron/uhabits/core/models/Score.kt ; Git blob 9b26f3486c2a51b2ed0188195af5d1e2e1a09084.
* Actual recomputation implementation: https://github.com/iSoron/uhabits/blob/82c1ff287a8ac05321bfa95b61399fa8a2d1da5b/uhabits-core/src/commonMain/kotlin/org/isoron/uhabits/core/models/ScoreList.kt ; Git blob 2ef4f4d49c92626a0126e0928196f142d7848356.
* Official privacy statement: https://loophabits.org/privacy.html ; developer says app data remain local and notes Android OS backup may upload phone data to Google if enabled. App privacy policy is a vendor assertion, not an independent device audit.
* Official product site: https://loophabits.org/ . No installation, registration, subscription or purchase performed.

## Mechanism and evidence boundary

Documented inputs: dated habit checkmarks, schedule/frequency, numeric target, reminders and locally stored history. Core Score.compute is precisely m=0.5^(sqrt(frequency)/13), new_score=m*previous_score+(1-m)*checkmarkValue. ScoreList.recompute clears its cached score map, recomputes from entries, treats Entry.SKIP by preserving previous score, and for non-daily boolean habits smooths a rolling schedule window. Numeric AT_MOST and AT_LEAST have separate normalization. The experiment below only models the daily boolean case with normalized YES=1, NO=0 and SKIP unchanged; it does not assert exact app behavior for every habit type or uninspected app release.

State: per-day rolling habit score and locally retained checkmarks. Feedback: charts, score, reminders and widgets; user edits can change recomputed historical scores. No financial derailment penalty in the documented product. User can export CSV/SQLite, but export provenance and backup deletion were not independently tested. Explainability: the exact score function is source-visible, while the score is a smoothed descriptive metric rather than a causal estimate of life outcomes. Privacy: local-first with an Android backup caveat. Cost: free/open source; zero new fees incurred. Scientific outcome validation: NOT_FOUND_IN_READ_SCOPE.

## Actually executed synthetic test

Archived Node 22.16.0 program `research/market/mkt154_loop_score_20261030.js` executed with 8 assertions PASS. With daily frequency, m=0.9480775143391714. After 13 YES days score is 0.5. On day 14, SKIP leaves 0.5; NO lowers it to 0.47403875716958593; YES raises it to 0.5259612428304146. Two 14-day histories each contain seven YES and seven NO: seven YES then seven NO ends at 0.21446596842754906; seven NO then seven YES ends at 0.3114952744028655. Changing a past YES to NO and recomputing changes the final score from 0.21446596842754906 to 0.1787170916853191.

This demonstrates order sensitivity and different handling of explicit SKIP versus NO in a synthetic reproduction of the pinned source formula. The score cannot independently identify a causal habit benefit or distinguish an unobserved event from an explicitly skipped event without a missingness policy. A locally recomputed current score alone is insufficient to attest to an earlier historical score after an edit. The app source itself is direct implementation evidence; this run did not execute the Kotlin app, run Android instrumentation, or inspect private data.

Candidate future controls: record event time, edit time, schedule version, explicit SKIP/missing/NO semantics, score algorithm version, and local backup permissions. Avoid mandatory monetary penalties and retain voluntary opt-out. These are proposals for later synthesis, not present product requirements.

Evidence: PRIMARY_OPEN_SOURCE_CODE plus PRODUCT_OFFICIAL_DOCUMENTATION plus INTERNAL_NONBLIND_ARTIFICIAL_E1. No external behavioral effect replication. New human E2=0, historical E3=0. No CI; no paid activity. Next MKT155: compare versioned score replay with missingness/skip and actual export schema, subject to latest repo changes.

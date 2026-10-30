# MKT155: Loop Habit Tracker CSV export and historical score provenance

UTC 2026-10-30. Track market. Target (market,Loop-Habit-Tracker,exporter-eb56a6794d8567240f0e0af5aacff52fb3d9c062,CSV-asof-version). Status COMPLETE_BOUNDED_PRIMARY_CODE_FIXTURE_E1. Baseline main 37a5f525a0a6c67499a09840bc7513db57fa3c6e.

## Pinned English primary evidence

Upstream iSoron/uhabits commit 82c1ff287a8ac05321bfa95b61399fa8a2d1da5b (2026-10-22): https://github.com/iSoron/uhabits . Exact exporter https://github.com/iSoron/uhabits/blob/82c1ff287a8ac05321bfa95b61399fa8a2d1da5b/uhabits-core/src/commonMain/kotlin/org/isoron/uhabits/core/io/HabitsCSVExporter.kt , Git blob eb56a6794d8567240f0e0af5aacff52fb3d9c062. Export task blob c04d9c105a4c20e5888c7475509fe92d2584b855. Upstream unit test blob 6716b567670d735e517a3f614098fc0fded9b860. Fixture blobs Habits.csv 37f40d4198b4ba3fd36b49123f4da3dbf5ce3711, Checkmarks.csv 3d443f4b53a7e9ef5908feb877bbb97595d0e973, Scores.csv 97637fb5b866e77daac6db7fe07a43011afa05d7, empty per-habit Checkmarks.csv af193ea33ff4ca3588d4a16cfe8afdb210842fcd. All five original source/fixture files were read via GitHub connector. Official privacy https://loophabits.org/privacy.html .

## Mechanism and actual audit

Exporter writes ZIP with Habits.csv, combined Scores.csv and Checkmarks.csv and selected-habit subdirectories containing each Scores.csv and Checkmarks.csv. Habits.csv fixture has 13 columns (position, name, type, question, description, frequency, color, target, archived, category and related fields), six habit rows. Combined checkmarks fixture has 13 dated rows with UNKNOWN, NO, YES_AUTO and YES_MANUAL. Combined scores fixture has 13 dated rows. The exporter writes computedEntries and formats score values to four decimal places. The examined CSV columns do not include event edit time, score algorithm version, provenance of revisions or a signed export identity. Export task names ZIP using current date; this is not a complete historical receipt.

Original pinned code and fixtures were inspected and 19 assertions executed in V8, all PASS. Two artificial values 0.123440 and 0.123449 both format to 0.1234. Two artificial edit histories have different earlier states [1,0] and [0,0] and identical final [0,0]; a final-only snapshot cannot distinguish their earlier records. This is a constructed information-loss example. It does not prove a defect in the actual app. Upstream Kotlin/Android app and exported ZIP were not run. Reproduction script research/market/mkt155_loop_export_schema_20261030.js requires a pinned local upstream checkout; native Node execution NOT_RUN.

## Product assessment and candidate controls

Inputs: dated habits, frequency, checkmark states, local history. State: computed entries and smoothed scores. Feedback: scores, charts, reminders. Export: CSV/SQLite per official README. Privacy: local-first developer assertion; Android OS backup may upload device data. Cost: GPLv3, free, no in-app purchases or subscription per official README; no purchase made. Explainability: source-visible scoring and exporter; empirical behavior improvement NOT_VALIDATED. Candidate future controls: explicit event/edit times, source and score algorithm version, snapshot time/digest, permission context, original-as-recorded versus recomputed-current scores, and UNKNOWN versus NO semantics.

Evidence PRIMARY_PINNED_SOURCE_AND_FIXTURES + INTERNAL_NONBLIND_SYNTHETIC_E1. New E2=0, E3=0. No CI or paid operations. Next MKT156: compare pinned SQLite backup schema and CSV revision provenance.

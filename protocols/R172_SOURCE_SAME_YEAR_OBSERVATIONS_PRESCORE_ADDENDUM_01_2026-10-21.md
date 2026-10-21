# R172 source-observation-year correction | pre-score protocol addendum 01

Date 2026-10-21. This **addendum does not alter** original locked protocol [R172 prescore freeze](../../protocols/R172_REAL_HISTORICAL_EPISODE_TEMPORAL_HOLDOUT_3_HAZARD_MODELS_PRESCORE_FREEZE_2026-10-21.md) commit 099b7a50924c86fdaecb6254eca2748836ae0c64, any model formula, duration bins, smoothing weights, outcome exclusions, train/test cohort cutoffs or scoring methods.

First actual remote model CI [run39545470112](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545470112) **failed before fitting/scoring** because its input validator required `year >= transition + 1`, an assumption from original source summary rather than every input row. A direct read-only scan of the authentic Dataverse table (official published TSV SHA256 `ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba`) identified **exactly 19** source rows with `year == transition`. These include 1975 Greece, 1984 Argentina, 1990 Chile, 1997 Taiwan, 2000 Croatia and 2002 Fiji. They are all labeled y=0, and source variable `t` is 0 while `t0` equals the original source `year`.

**Revised source admissibility invariant, before any scores exist**:
- For each source observation `year >= transition` is required, not `year >= transition+1`; `age == year-t0` must remain exact. Do **not** fabricate missing years or shift the source event date. Record number of same-year rows and protect as an explicit regression guard.
- A same-year record with `age=0` is precisely treated as **first observed year**; model M2 still falls back to M1 and does not use the initial index before the first observation.
- Year 1999 inclusive training-data cap, new transition cohort >=1999 test, test year>=2000, whole NGA2011 6-row exclusion, 45 source breakdown events, and original proper-score/512 cluster bootstrap remain **unchanged**.
- Original author narrative "first full year after transition" is not applied as an absolute row-level truth: the source contains same-year observations. No subsequent heldout scores have been examined, since first CI terminated in `parse_rows` before model fitting.

Document this source adjustment transparently in R172 scientific report and machine acceptance. The previous failed first CI **must not be presented as a successful scientific test**. Follow-up dual Python CI must pass with the explicit 19-row source consistency assertion. This is a data-eligibility correction, not model selection or hyperparameter tuning.

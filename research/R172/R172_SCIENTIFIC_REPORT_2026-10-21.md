# R172 Scientific Report — Real Historical Event-History Retrospective Holdout

Date 2026-10-21. Original model catalog P1 / 07-014 Historical Event History Models. **CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT**. This is an authentic historical country-year cohort-split predictive evaluation, not a real-time forecast, not a causal explanation of democratic breakdown, and not a reproduction of the source authors' statistical analyses.

## Actual original source and attribution

Pérez-Liñán and Mainwaring (2025), Democratic Trajectories in the Third Wave: Aligning Theory and Methods, original Harvard Dataverse [doi:10.7910/DVN/WFO1N1](https://doi.org/10.7910/DVN/WFO1N1), original dataset **version 1.1**, license **CC0 1.0**. The archive [source/](source/) permanently preserves three distinct original-source representations:

* Dataset original upload fetched through official format=original API: 265,851 bytes, source-registered MD5 **4343114d56124f88bce9d9cc3ce81523**, SHA256 ddca691b25a664ce13ef2471184e3d5ae3ed62cb72521e0593bff770efb0e4e6.
* Dataverse-converted official 1,731-row tabular dataset: 428,013 bytes, SHA256 ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba. Its MD5 differs from the original upload since Dataverse converted the data format; the two file hashes must never be incorrectly equated.
* Original author Stata replication script: 17,387 bytes, source MD5 2dd571e5f94bd1f79158dcd2b53b0b94, SHA256 664cf425684b97b8a7bf835ed748955e2e34426e8a14c0db8abbf98a4fb2e3ad. The author's Stata models were **not** run or reproduced.

The statistical event-history background is Cox (1972), [Regression Models and Life-Tables](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x), and Berry and Berry (1990), [State Lottery Adoptions as Policy Innovations: An Event History Analysis](https://doi.org/10.2307/1963526). The R172 hazard estimators are all project-authored simple Beta-smoothed conditional binary models; no Cox proportional hazard partial-likelihood estimates, policy diffusion estimates or causal effects are claimed.

## Source risk-set audit and exact inclusion

The actual converted dataset contains **1,731 years, 103 democratic transition episodes, 83 distinct country IDs and years 1975–2017**. The source description separately mentions 84 countries; the difference from 83 unique IDs in the actual verified data remains an explicitly unresolved descriptive discrepancy.

Outcome breakdown coding: 45 breakdown=1, 1,680 breakdown=0 and six missing outcomes. The **six missing outcomes all belong to Nigeria episode NGA2011 (2012–2017)**; the entire episode was excluded before fitting, rather than silently treating missing events as non-events. Valid source material is 1,725 rows across 102 labeled episodes.

The preregistered original source validator initially overasserted calendar year greater than transition year. [Initial failed CI 39545470112](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545470112) failed **before scores were computed**. The actual data contain **19** legitimate same-calendar-year transition observations with t=0, including Taiwan 1997, Argentina 1984, Chile 1990 and Greece 1975. We preserved original data and committed [a source-admissibility addendum](../../protocols/R172_SOURCE_SAME_YEAR_OBSERVATIONS_PRESCORE_ADDENDUM_01_2026-10-21.md), [commit a83088f](https://github.com/edwardsage419/Psychohistory-Research/commit/a83088fd20a64175c6d25a99b40f4cec6afc11c4), before any heldout scores were generated. Only the source-year validator changed to allow year==transition; **no model rule, split, smoothing weight, covariate cutoff, scoring rule or test outcome was selected post hoc**.

[Original frozen prescore protocol](../../protocols/R172_REAL_HISTORICAL_EPISODE_TEMPORAL_HOLDOUT_3_HAZARD_MODELS_PRESCORE_FREEZE_2026-10-21.md) [commit 099b7a5](https://github.com/edwardsage419/Psychohistory-Research/commit/099b7a50924c86fdaecb6254eca2748836ae0c64) defined: training of old transition cohorts up to 1998 using **only annual risk rows through 1999**, and temporally heldout *new transition episodes* starting 1999 or later, with observed years **2000–2017**. Old cohorts' later outcomes are withheld, neither trained nor scored.

| Partition | Years at risk | Episodes | Recorded breakdown events |
|---|---:|---:|---:|
| Training, old cohorts through 1999 | **581** | **67** | **12** |
| Heldout, new cohorts 2000–2017 | **319** | **35** | **18** |
| Older cohort followup after 1999, excluded from both training and evaluation | **825** | Existing older episodes | **15** |
| Nigeria NGA2011 episode, excluded for missing outcome | **6** | **1** | Unknown |

Training has 63 country codes and test has 32. **Some countries can appear in both train and test under different democratic episodes**, so this is an **episode-disjoint** but *not independent country-level* test. Eighteen heldout episodes end in a recorded breakdown; 17 are right-censored and must not be treated as never experiencing an event. The source episode sequences have no observed years after coded breakdown; all retained episode years are contiguous.

## Three prescored hazard models

All probability parameters are exact Python Fraction values, fitted exclusively from source training risk years. Year-level event log loss and Brier score were preregistered before looking at heldout outcomes.

* **M0 fixed annual null hazard**: p0=(E_train+1)/(N_train+2)=**13/583**.
* **M1 duration strata**: elapsed years t grouped as 0–2, 3–7, 8–15, and 16 or greater, with p_b=(E_b+20*p0)/(N_b+20).
* **M2 duration + first observed year's original source baseline liberal-democracy index**: low if libdem0 < 50 and high if libdem0 >= 50, with p_b,s=(E_b,s+20*p_b)/(N_b,s+20). **At t=0, or if this original index is missing, M2 equals M1**. This avoids using the first-observed-year covariate before it becomes observable; this conditional provenance assumption has not been independently validated against historical realtime data releases.

The category boundary 50 and smoothing weight 20 were frozen, not tuned on test scores. No contemporaneous GDP, later breakdowns or full-period regional exposures feed into predictors. None of these model strata establish a social, moral or political tipping point.

## All 319 actual heldout yearly scores — no posthoc selection

| Model | Heldout annual log loss | Heldout annual Brier | Annual log-loss difference versus M0 |
|---|---:|---:|---:|
| M0 constant | **0.235881126652** | 0.054407113235 | reference |
| M1 elapsed-time | **0.245235328446** | 0.054667027894 | **+0.009354201794** (worse) |
| M2 elapsed-time and baseline index | **0.234530415157** | **0.054105271593** | **−0.001350711495** (small improvement) |

All three models are evaluated on exactly the same 319 observed country-years, from 35 unseen transition episodes including 18 actually labeled breakdown events.

The mean **total** episode log loss, averaged over the 35 variable-length heldout episodes, is M0 2.149887982917; M1 2.235144850695; M2 2.137577212435. This episode-total score is a separate estimand from average yearly log loss.

Fixed uncertainty exercise: 512 bootstrap resamples of **whole heldout episodes**, pseudorandom seed 20261021, linearly interpolated empirical 2.5% and 97.5% quantiles.

| Model−M0 difference; lower is better | Point estimate | Episode-bootstrap 2.5–97.5 percentile interval |
|---|---:|---:|
| M1 annual log loss | +0.00935420 | **[−0.00135251, +0.02177499]** |
| M2 annual log loss | −0.00135071 | **[−0.01642915, +0.01778504]** |
| M1 annual Brier | +0.00025991 | **[−0.00011587, +0.00068103]** |
| M2 annual Brier | −0.00030184 | **[−0.00092673, +0.00027750]** |

**All four intervals include zero**, and training contains only 12 events. A stable M2 predictive gain is therefore **not established**. The 35 episodes can contain repeat country IDs: the episode bootstrap does not provide correctly country-clustered uncertainty, a defensible causal interval, or full model specification uncertainty. The performance limitations and worse M1 result are retained rather than discarded.

Full [319-row original heldout predictions CSV](R172_REAL_HELDOUT_PREDICTIONS.csv) records original episode/country/year/elapsed years/observed event and **all three exact rational probabilities per row**. No hidden scoring subset is used. The complete [result JSON](R172_EXACT_RESULTS.json) records original hashes, cohort IDs, all fit counts and exact fitted stratum probabilities, loss/Brier and percentile uncertainty, missing-data exclusion, duplicate-country disclosure, source-year addendum and evidence limits.

## Real CI and permanent reproducibility

First correct full dual-version [CI run 39545672065](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545672065): **success**, Python 3.11 and 3.12 each executed **92 genuinely different** test methods and gave identical source/result hashes. Final locked [CI run 39545815533](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545815533): **success**, both versions independently reran 92, and independent archival job **119043669106** reran 92 tests and recreated the exact full original file/data/results ZIP, checking all five SHA256. Original prediction CSV, JSON, source, source test and ZIP are in GitHub main at [archive commit e88784b](https://github.com/edwardsage419/Psychohistory-Research/commit/e88784bc28b5fbd45f85c9c7cf0ced8e7e503c14).

Total verified **5 × 92 = 460 actual method executions**, zero failures in the successful runs. The earlier rejected validator CI is not included in these successes. Repeated software executions are reproducibility, *not independent empirical studies*.

Artifact SHA256:
* program 633a4b65b9e9ffe31442f814f878bc6347444c435c830c9394e2780478150cd6
* tests e88020b3f87a1c3f538aab9aea84c87f0fde883f224e6df4647b87e1d134eadb
* full JSON 0cb8adfbe92cf32b27731f47068bd94cad9346e8545444a684a0c63040a10857
* all heldout CSV e7f81816d5d7ffc4c50e864dfd534db00477fd8bec81e04d306dbf479e5eee1d
* complete original dataset/code/test/predictions [ZIP](R172_Real_Historical_Holdout_3_Hazards_92_Tests.zip): 3d352c1014fc36db74a8c14587be7503ad7758bc7cbbf76d7066a1910db293bf

Reproduce from this folder with standard-library-only Python: python r172_real_historical_retrospective_hazards.py and python -m unittest -q test_r172_real_historical_retrospective_hazards.py. No paid API, additional provider or software packages required.

## Acceptance and limits

**CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT** on genuinely observed source historical country-year events, with explicitly frozen temporal prediction conditions and repeated exact replication. Stronger evidence than only artificial mathematical universes, but **not independent prospective historical event E3**, and distinct from the R073 repeated-human-game E2 criterion. No new independently issued E2 predictions or genuinely external E3 forecasts. R073 and PESEN v0.1 remain frozen.

Future real event model experiments should address source-dependent coding, same-country multi-episode dependence, proper country-level grouping, outcome timing robustness, competing events, covariate availability and independent replication. Preserve original project sequence: first complete all original R models, then unified taxonomy, and lastly fusion.

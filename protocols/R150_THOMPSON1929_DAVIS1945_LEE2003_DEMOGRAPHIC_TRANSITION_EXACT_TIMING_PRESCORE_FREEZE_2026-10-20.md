# R150 Prescore freeze — Thompson 1929 / Davis 1945 / Lee 2003 demographic transition timing and aggregate-identification limits
Date: 2026-10-20 Asia/Taipei. Fixed prior catalogue **P1 / 06-008 Demographic Transition Models**. MUST commit before creating R150 code, test results, or post hoc numerical findings; do not modify frozen math to fit observed outcomes. R151 age-structured models remain a separate future item.

## First-hand source authority actually checked
1. Warren S. Thompson (1929), "Population", American Journal of Sociology 34(6), 959–975. https://doi.org/10.1086/214874. University of Chicago original journal publisher article + author abstract read. Specifically Thompson categorized country populations into A (low mortality and increasingly controlled births), B (deaths falling more rapidly than births), and C (both vital rates little voluntarily controlled); his original classification is not the project's modern stages with fixed rate fractions. No full print PDF read; no page-specific source-equation claims.
2. Kingsley Davis (1945), "The World Demographic Transition", Annals of American Academy Political Social Science 237(1):1–11 DOI 10.1177/000271624523700102. SAGE publisher original article bibliographic page verified; original full-text restricted, not read.
3. Ronald Lee (2003), "The Demographic Transition: Three Centuries of Fundamental Change", J Econ Perspectives 17(4):167–190 DOI 10.1257/089533003772034943. AEA publisher ORIGINAL abstract directly verified, alongside academic hosted original-article excerpt reading, summarizing first declining mortality, then fertility, with temporarily accelerating and later declining population growth. Full print original PDF not verified as page-by-page visual first-hand read. Any 1800/2100 quantities in historical article are contemporary-to-2003 forecasts; never treat them as validated 2026 outcomes.

This is a CONCEPTUAL author-original-source comparison, plus PROJECT-CREATED finite mathematical E1. There is **no original author numerical model or actual census series reproduced**. No E2 humans, E3 history forecasts or observed country-level life tables.

## Frozen exact synthetic aggregate accounting model
One closed synthetic undifferentiated population (not births per woman or TFR). Real-valued expected population P0=1000; no integer rounding, no generations, no age or sex structure (R151). For each calendar step t=0..11, chosen year thresholds death-reduction td∈{0..8} and birth-reduction tb∈{0..8}. Instantaneous annual **crude per-capita rates** b_t=1/5 for t<tb else 1/20; d_t=1/5 for t<td else 1/20. t=0 threshold means already low from start. The stock is P(t+1)=P(t)+births_t−deaths_t+net_immigration_t. birth_t=P(t)*b_t, death_t=P(t)*(d_t+shock_death_t). No infant mortality or cohort migration modeled separately.
Three mechanically predeclared shock regimes (NOT estimated from historical data):
- NONE: every year extra death=0, migration=0.
- PANDEMIC_YEAR4: additional population death probability 1/10 at t=4 only, no extra death other times; 1/5+1/10=3/10≤1, births unchanged. `pandemic` is solely an arbitrary transient mortality perturbation, not an actual pandemic.
- INMIGRATION_YEAR4: net immigrants =P(t)/10 at t=4 only, other years0; fractional inflow synthetic expected people count, immigration enters additive stock, not births and not deaths.
This is a stated exact accounting scheme; total factor 1+b_t−d_t−death_shock_t+migration_rate_t always >= 0. Rate schedules 9×9×3=**243 exact scenarios**, 12 annual updates each. Give full history of P, births, deaths, net immigration (all rational serializations), annual rate and independent endpoint product. Separate birth/death accounting from stock-only observations.
All 9 equal thresholds b/d identical every year and in NONE remain P=1000 exactly; 36 schedules td<tb cause 3/20 net natural increase for tb−td years, 36 td>tb cause −3/20 during td−tb years. For NONE endpoints must satisfy:
- td<tb: P12=1000*(23/20)^(tb−td)
- td>tb: P12=1000*(17/20)^(td−tb)
- td=tb: P12=1000.
In all scenarios last three post-threshold years have b=d=1/20, so stock stops changing after both switches except 4th-year transient shock (all td/tb≤8 and shock year4), and SAME final vital rates do not imply same population size. Note crude rates equal after transition does NOT mean actual demographic momentum, which cannot be tested without age structure.

## Frozen causal and identification counterexamples
1. Two synthetic annual populations P(t) may be observationally identical (e.g. b=d=1/5 vs b=d=1/20 over 12 years) yet gross numbers of births/deaths differ by factor four; population STOCK ONLY cannot identify separate vital rates.
2. Same positive net growth 3/20 possible via (b=1/5,d=1/20) and (b=1/4,d=1/10), but gross births/deaths differ; rates chosen as mathematical controls, NOT as another Thompson stage or a plausible calibrated history.
3. Compare td=2,tb=6 to td=6,tb=2 with the same final rates, reversed order; expect divergent final P despite both ending low/low.
4. Shock in year4 is assigned by construction; closed P base cases and one-step shock effects exact, but not causal effects inferred from real pandemics or immigration.

## Independent verification and CI
- Forward book-keeping based solely on separate births, deaths, immigration per step, and independent closed-product recomputation of P12 using year-specific multiplication; exact Fraction and all 13 stock points (t0..12), verify accounting identities for **every** year and 243 schedules.
- Reverse accumulation alternate version using Fraction multiplication **from end** not reusing the forward stock process, an additional independent cross-check.
- Test invalid booleans, floats, negative, non-integral time, unknown shocks, impossible boundary regimes, rates >1, negative stock handling; source paper stage names always author-source qualifiers.
- ≥45 real unittest cases, at least 30 unique schedule parameter cases, full canonical JSON with all 243 histories and source-status disclosure.
- ZIP Python program + tests + canonical results; hash SHA256 ZIP and members, synchronize exact ZIP and docs to GitHub; independent Python3.11 and3.12 Actions each verify four SHA256s, all genuine unittests, full JSON byte-exact replay and exact numerical assertions before CLOSED_BOUNDED. If remote fails, status remains pending.
- New real human E2=0, external historical prediction E3=0; freeze R073/PESEN v0.1; finish prior R series, afterwards taxonomize then fuse. Next original catalogue item 06-009 Age Structured Population Models (R151), distinct mathematical scope.

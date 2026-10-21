# R167 scientific report: exact within-group and between-group cultural frequency decomposition

Date 2026-10-21. Original catalog **P2 / 07-009 Cultural Group Selection**. Precode [protocol was frozen](../../protocols/R167_CULTURAL_GROUP_SELECTION_72_TWO_GROUP_PRICE_COVARIANCE_PRESCORE_FREEZE_2026-10-21.md) on main in [commit a7ba75f](https://github.com/edwardsage419/Psychohistory-Research/commit/a7ba75f430f59217d9518a680fdebb70beb32d4). **CLOSED_BOUNDED_E1** for original project-authored two-group Fraction mathematics only. The two groups and variant A are purely fictional, with no actual group memberships, fitness, social payoff, cooperation measures, biological history or political labels.

## First-hand sources and scientific claim limits

* Robert Boyd and Peter J. Richerson (2002), [*Group beneficial norms can spread rapidly in a structured population*](https://doi.org/10.1006/jtbi.2001.2515), *Journal of Theoretical Biology* 215(3):287–296, [PubMed PMID12054837](https://pubmed.ncbi.nlm.nih.gov/12054837). Original Elsevier abstract directly checked. Their actual structured-population social imitation model and predictions are substantially more detailed than our aggregate two-group recurrence; author equations, simulations and any observed cultural data have not been reconstructed.
* Joseph Henrich (2004), [*Cultural group selection, coevolutionary processes and large-scale cooperation*](https://doi.org/10.1016/S0167-2681%2803%2900094-5), *Journal of Economic Behavior & Organization* 53(1):3–35, original Elsevier abstract checked. The author's argument concerns complex social learning, multiple behavioral equilibria, interactions between cultural and genetic transmission and large-scale cooperation. No genetic, institutional or interpersonal data from that study is used here.
* George R. Price (1970), [*Selection and covariance*](https://doi.org/10.1038/227520a0), *Nature* 227:520–521; original Nature issue listing and PubMed bibliographic record confirmed. R167 uses a separately verified elementary two-group covariance *identity* inspired by decomposition reasoning, **without reconstructing the full general Price equation derivation or identifying causes in observed populations**.

Group-level statistical reweighting does not itself identify a natural, cultural or institutional causal selection mechanism. Empirical designs must measure who learns from whom, the group-level reproduction/retention processes, within-group transitions, and competing explanations. The toy label "advantage" only means a positive coefficient assigned by this experiment.

## Frozen 72 artificial worlds

Two groups are indexed by lower/higher *artificial A frequency*. Four initial (p_low,p_high) pairs:
(1/4,3/4), (1/3,2/3), (1/5,4/5), (1/2,1/2). Initial high-frequency group weight h∈{1/2,3/4}, with other group weight 1−h. The within-group change coefficient δ∈{−1/4,0,+1/4}. Positive δ suppresses local A frequency and negative δ increases it:
\[
p'_g=p_g-\delta p_g(1-p_g).
\]
Artificial group-size/representation reweighting uses the **previous** group A frequency:
\[
R_g=1+\kappa p_g,\qquad w'_g=\frac{w_gR_g}{\sum_iw_iR_i},\qquad
P'=\sum_gw'_gp'_g,
\]
where κ∈{0,1,2}. **4 pairs ×2 initial group weights ×3 local changes ×3 group-weight strengths=72 frozen worlds**, each with snapshots t=0,1,2,3. The full 72×4 states, exact (p_low,p_high,w_low,w_high), aggregate P and changes are saved in [original complete 114,014-byte JSON](R167_EXACT_RESULTS.json).

Independent exact routes:
1. Direct fractional within update followed by normalization of both group weights and recomputation of P.
2. Independent two-group factorized covariance decomposition for group-weight changes:
\[
W=\sum_i w_i(p'_i-p_i),\qquad
B=\frac{w_0w_1(R_1-R_0)(p'_1-p'_0)}
          {w_0R_0+w_1R_1},\qquad
P'-P=W+B.
\]
The second route calculates group masses and the factorized covariance expression separately without calling the first route's step. **All 72×4 complete paths and all per-step W/B/total values agree exactly as Python Fraction objects**. This is mathematical self-consistency, not independent experimental replication of original authors or human groups.

## Frozen within-between reversal

For two initially equally weighted groups with p_low=1/4 and p_high=3/4, choose δ=+1/4 and κ=2. The initial aggregate A frequency is 1/2. Both *within-group* frequencies decrease:
\[
p'_0=13/64=0.203125,\qquad p'_1=45/64=0.703125.
\]
Under the exact frozen two-group weights, the decomposition is
\[
W=-3/64,\qquad B=+1/16=+4/64,\qquad
P'-P=+1/64.
\]
Consequently **the aggregate A fraction increases from 1/2 to 33/64≈0.515625 even while A loses within each group**. This is an explicit aggregation/Simpson-style reversal. It depends on group weights being allowed to shift toward the higher-A group; it cannot on its own establish group selection in actual societies or imply anything about whether the chosen behavior is socially good or adaptive.

Other independently tested limits:
* κ=0 gives unchanging group weights and B=0. All overall changes then arise from local within-group changes.
* δ=0 leaves each group's A frequency constant. The aggregate may still shift with κ>0 when the two group frequencies differ.
* If both groups have exactly equal A frequency, R is equal and B=0, even with κ>0. The relative group weights remain unchanged.
* Positive κ and increasing group A frequencies create a nonnegative B for the frozen ordered groups, but this **does not guarantee** the net overall A fraction increases whenever the within contribution is negative.
* Distinct initial group compositions and weights can produce different aggregate effects. Aggregated trajectories cannot identify historical pressure, social learning, causal group reproduction or group welfare without individual/group-level measurements.

## Reproduction, CI and immutable archive

Original [source code](r167_cultural_group_covariance_exact.py), [103 genuine distinct unittest methods](test_r167_cultural_group_covariance_exact.py): 72 uniquely named full-world paths and 31 independent mathematical identity, reversal, input rejection, group-weight, and exact JSON replay tests.

* [Initial GitHub Actions run39534151899](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39534151899): both Python3.11 and Python3.12 independently ran 103 authentic tests successfully; all four SHA256 artifact identities matched across versions.
* [Final pinned archive run39534227555](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39534227555): both Python versions ran 103 tests successfully; independent archive publisher job119007060855 reran 103, regenerated full [JSON](R167_EXACT_RESULTS.json) and original [source/test/JSON ZIP](R167_Cultural_Group_72_Worlds_103_Tests.zip), verified four SHA256 hashes and permanently committed these original files to GitHub main in [commit1925c01](https://github.com/edwardsage419/Psychohistory-Research/commit/1925c0144381562189d440a7794787112aa396cd).
* **515 actual unittest method executions across five runs, 103 different tests, zero failures.** These repetitions are computational verification, not multiple original human study observations.

Four fixed SHA256:
* source `bf005a409c97045c0beb2ca88ee652ca08978ac01d32a8e004b22805cfad8ae6`
* tests `88394c087e33ebd816b39077814b39ec78f403a2f7004ec45fca3e3a0e902561`
* full original results JSON `118d8f8d37832777e265205af3f4d05811bf543656c46f2e24873c9ae93a839a`
* original ZIP `71209080b55f1fbcb9e4d0365635d6ec5af2c2ceb2633097ef4e6ab7ce5116f6`.

Reproduce in `research/R167` with `python r167_cultural_group_covariance_exact.py > R167_EXACT_RESULTS.json` and `python -m unittest -q test_r167_cultural_group_covariance_exact.py`. Python standard library only.

**Final grade: CLOSED_BOUNDED_E1** for 72 frozen mathematical two-group dynamic cases. No authentic group conflict, cooperation, group selection, demographic trends or cross-cultural external forecast data were acquired. New independent E2=0 and E3=0. Keep R073/PESEN v0.1 frozen. Next original R-series candidate **R168 P1/07-010 Cumulative Cultural Evolution**, requiring new primary source review and separate preregistration. Finish all R-series first, then taxonomy/classification, then model fusion.

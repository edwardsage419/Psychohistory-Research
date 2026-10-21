# R166 Scientific report: cultural selection versus biased transformation in a finite binary population

**Date:** 2026-10-21. **Original catalog:** P1 / 07-008 Cultural Selection Models. **Outcome:** CLOSED_BOUNDED_E1 for one original 48-world exact mathematical identification experiment. **No human empirical data, original author simulation reproduction, or historical out-of-sample forecasting.**

## 1. Mandatory catalog provenance erratum and direct source audit

The existing source catalog labels the first-hand reference for 07-008 as `R19`. That link is **incorrect**. A new [read-only GitHub Actions run 39532579568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39532579568) inspected the actual 12,946-byte archived original R019 ZIP `archives/library-originals/心理史学_R019_正式研究包_2026-10-14.zip`. Its exact SHA256 is `080a786f4bd064494f8c57a7ec0cc32f183d2020e3eb643a0ea69881a721d797`; it has nine source/manifest/test members. The authentic R019 topic is the **two-network private belief versus public statement** theoretical model, with an original novelty audit of Anufriev, Borissov and Pakhnin (2023/2026), not cultural selection models. No R019 mathematical result is reused in R166. Original R019 ZIP remains unchanged. [Source dependency audit](R166_SOURCE_DEPENDENCY_TRIAGE_2026-10-21.md) records the correction; source-ID cleanup must not overwrite original catalog research history.

Verified direct literature:
* Mesoudi, Alex (2021), [*Cultural selection and biased transformation: two dynamics of cultural evolution*](https://doi.org/10.1098/rstb.2020.0053), *Philosophical Transactions of the Royal Society B* 376:20200053, [full original open-access paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8126458/). Distinguishes between preferential copying of variants and individual-level directional transformation, showing similar macro patterns can arise from different micro causes.
* The [original Mesoudi author repository](https://github.com/amesoudi/culturalselection_biasedtransformation) was inspected. Its actual [model1.R](https://github.com/amesoudi/culturalselection_biasedtransformation/blob/master/model1.R) blob identity SHA1 `1d2c4fa8db1d52ecfb3a233a7e6a216867e5c42c`. The original `philtrans_model1` runs real-valued agent traits, with selective copying of the highest-value demonstrator at probability s versus random copying, then an exponentially modified Gaussian `remg` transformation and 0–100 clipping. **The original R code was read but not executed, and none of its original continuous-state parameters or result figures was reconstructed.**
* Claidière, Scott-Phillips and Sperber (2014), [*How Darwinian is cultural evolution?*](https://doi.org/10.1098/rstb.2013.0368), *Philosophical Transactions B* 369:20130368, open original article discusses cultural attraction and limits of a pure selectional reduction.
* Boyd and Richerson (1985), [*Culture and the Evolutionary Process*, original publisher chapter contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html), separates direct biased transmission, natural selection of cultural variations, and guided variation.

## 2. Frozen project-authored 48 cases

Before code, [the exact protocol](../../protocols/R166_CULTURAL_SELECTION_VS_TRANSFORMATION_48_FINITE_WORLDS_PRESCORE_FREEZE_2026-10-21.md) was frozen in [commit 1a55a14](https://github.com/edwardsage419/Psychohistory-Research/commit/1a55a14a67cc3b1386f73c83fd3beb03017d07a5). There are only abstract binary tokens A and B in two artificial finite cohort sizes N∈{4,8}. Four initial counts for each size: N4 k={0,1,2,4}, N8 k={0,2,4,8}. Three predetermined directional regimes: neutral; artificial bias towards A; artificial bias towards B. Each regime is represented by two separate rules:

1. **Selection rule:** weight already-existing A and B exemplars by fixed positive weights wA,wB. Copying A probability at current fraction p=k/N is
\[
q_{SEL}(p)=\frac{w_Ap}{w_Ap+w_B(1-p)}.
\]
2. **Directed transformation rule:** independently copy a random demonstrator and transform the copied B into A at rate a or A into B at rate b:
\[
q_{TRF}(p)=p(1-b)+(1-p)a.
\]
Neutral settings are wA:wB=1:1 and a=b=0. A-favoring settings wA:wB=2:1 and (a,b)=(1/3,0). B-favoring settings wA:wB=1:2 and (a,b)=(0,1/3).

For either mechanism, the new A count is an independently sampled artificial binomial \(K_{t+1}\mid K_t=k\sim Binomial(N,q)\). Exactly **2 cohort sizes ×4 initial counts ×3 regimes ×2 mechanisms=48 frozen worlds**, each recording every full count distribution from t=0 through t=4. The [complete 116,861-byte JSON](R166_EXACT_RESULTS.json) records **12 complete exact transition matrices**, 48×5 full count distributions and all means.

Two independent algorithms were tested:
* Direct rational q, factorial/binomial combinatorics, and row-vector matrix update.
* Independent A versus B weighted-ticket arithmetic for SEL, independent retained/transformed-copy branch aggregation for TRF, followed by an explicit enumeration of all 2^N new individual indicator strings and independent nested-loop Markov propagation.

All **12 full kernels and all 48×5 count distributions agree exactly as Python Fraction**. The two algorithms are arithmetic replications of the same *project-defined hypotheses*, not separate evidence on original human cultural mechanisms.

## 3. Prespecified mathematical identification results

For p=1/2, the A-favoring selection and transformation mechanisms both produce exactly q=2/3. The full distribution for the next generation is identical for both models at **both N=4 and N=8**. The B-favoring pair analogously matches at q=1/3. Thus observing one such count transition cannot distinguish the mechanisms under these frozen assumptions.

For p=1/4, the A-favoring selection mechanism instead gives q=2/5, while transformation produces q=1/2. The two choices induce different binomial count distributions. At p=0, selection with no novel A stays fixed at zero, while directed B→A transformation produces q=1/3. These are testable **model discriminators**, not empirical results.

The more demanding fixed-start counterexample N=4, k0=2, A-favoring models is:
* At t=1, both models yield **identical full distributions** of A counts across all five possible count states.
* At t=2, their entire distributions differ. Exact total variation distance is
\[
TV_2=\tfrac12\sum_{j=0}^4\left|P_{SEL}(K_2=j)-P_{TRF}(K_2=j)\right|
=\frac{41284561}{1093955625}\approx0.03773878945.
\]
The corresponding second-generation expected A fractions are **2192/2835≈0.773192240** for selection and **7/9≈0.777777778** for transformation.

The one-step equality followed by an exact second-step separation is why the number of time points and initial frequencies matter. It also demonstrates a concrete problem of aggregation: even if one observed transition is perfectly measured, distinct mechanisms can predict it identically. Different starts or repeated transitions can break this equivalence in the artificial environment. Identifying actual mental transmission mechanisms needs observed demonstrator choices, transformations and field or laboratory variation, which this study did not perform.

With neutral parameters both models exactly reduce to the earlier **R165 μ=0 finite cultural drift kernel**, checked directly against the original R165 Python implementation. Selection always preserves the absent types at k=0 or k=N; one-directional transformation changes the formerly absorbing opposing boundary. This adds a distinct comparative identification mechanism relative to R164 deterministic content bias and R165 neutral drift, without treating the reused neutral kernel as new scientific evidence.

## 4. Real CI and reproducible provenance

Original [source](r166_cultural_selection_transformation_exact.py), [84 different unit tests](test_r166_cultural_selection_transformation_exact.py): 48 individually registered full worlds and 36 mathematical, identification, boundary, reflection, cross-stage R165 and input-validity tests.

* First [GitHub Actions run39533161253](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39533161253) succeeded: 84 real tests each on Python3.11 and 3.12 with independently identical original SHA256.
* Second [pinned archive run39533242415](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39533242415) succeeded: Python3.11 and 3.12 each reran 84 real tests; archive job119003894749 independently reran 84, regenerated all JSON and source/test ZIP and matched all four SHA256. Results were permanently committed to main in [archive commit01234cb](https://github.com/edwardsage419/Psychohistory-Research/commit/01234cbdbf6cc38fd5285289d4b73aed299c6377).
* **420 actual unittest executions, 84 different methods, zero failures** across both CI runs. Repetitions validate code and data provenance only.

Four SHA256:
* source `37874e66c0b68c96d3e97f7dfb1e907dc7b9596c963b1471000668517b5148f3`
* tests `1744b160f6af1583ea086da2f8c982bad5a304d03c709dfaa6cbafb7dca0008d`
* full JSON `ff50f5555841bac54db308c517543158ed3efc004cf4be42de4c6f3a3299e3a8`
* full original ZIP `831a2bac01b992ac1943e4e213db3ebdca2d4bec067ad317ee53ef92e32dea30`.

Independent replay: in `research/R166`, run `python r166_cultural_selection_transformation_exact.py > R166_EXACT_RESULTS.json`, then `python -m unittest -q test_r166_cultural_selection_transformation_exact.py`. Needs the adjacent original `research/R165` code for one cross-stage regression test; both are already in the repository. Python standard library only.

**Final scientific acceptance: CLOSED_BOUNDED_E1**, with a newly verified catalog-provenance correction and exact binary mechanism-identification counterexample. No Mesoudi-original model output, observed human choice, causal cultural transmission or held-out historical test was produced: E2=0, E3=0. Preserve frozen R073 and PESEN v0.1. Next original catalog item **R167 P2/07-009 Cultural Group Selection**. Maintain original sequence: complete all R, then classify and finally fuse.

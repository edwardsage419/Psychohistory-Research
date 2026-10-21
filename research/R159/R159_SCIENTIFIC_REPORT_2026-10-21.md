# R159 Scientific report: 48 exact cultural majority transmission worlds and source limitations

Date 2026-10-21. Original catalog **P1/07-001 Dual Inheritance Theory**. Precode protocol [frozen first at ddb4d36](https://github.com/edwardsage419/Psychohistory-Research/commit/ddb4d36216df0c71fe19caf0db988b8cae555900). **CLOSED_BOUNDED_E1 only for a single-trait cultural imitation submodel**, and absolutely no claim of a complete quantitative genetic-cultural two-inheritance system, no individual experimental observation, and no reconstructed original author's equations.

## Original primary sources reviewed and gaps
* L. L. Cavalli-Sforza and M. W. Feldman (1981), *Cultural Transmission and Evolution: A Quantitative Approach*, Princeton University Press, [original publisher/JSTOR description](https://www.jstor.org/stable/j.ctvx5wbt8). The book systematically analyzes vertical/oblique/horizontal cultural transmission in a broad population-genetic framework; original complete book mathematical chapters and empirical examples not reproduced here.
* R. Boyd and P. J. Richerson (1985), *Culture and the Evolutionary Process*, University of Chicago Press, [original publisher book and table of contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html). Contents directly verified: cultural inheritance, biased transmission and guided variation. The full book and model equations were not re-derived.
* J. Henrich and R. Boyd (1998), *The Evolution of Conformist Transmission and the Emergence of Between-Group Differences*, *Evolution and Human Behavior* 19(4):215–241, DOI [10.1016/S1090-5138(98)00018-X](https://doi.org/10.1016/S1090-5138(98)00018-X), [original Elsevier publisher abstract](https://www.sciencedirect.com/science/article/pii/S109051389800018X) and [Harvard author record](https://henrich.fas.harvard.edu/publications/evolution-conformist-transmission-and-emergence-between-group-differences). The original article investigates selection on imitation and conformity in varying environments and between-group differentiation; this R stage does NOT reproduce the evolutionary-selection mechanisms or source observations.

The project deliberately isolates the simple *mechanical effect of a three-demonstrator majority copying function*. It does **not** include genotype states, genetic selection, cultural-group identity, payoff choice, family inheritance, spatial networks, real human sample or changing environments. The labels are purely neutral artificial trait A/B frequencies, not actual religion, ethnicity, political belief, race or identifiable human group membership.

## Frozen 48 hypothetical transmission trajectories
Binary artificial cultural frequency \(p_t\in[0,1]\). Three independent exemplar draws yield a majority A with probability
\[
C(p)=p^3+3p^2(1-p)=3p^2-2p^3.
\]
A purely project-chosen mixture h between neutral copying and the majority rule plus symmetric artificial innovation/reset rate u yields
\[
p_{t+1}=(1-u)\{(1-h)p_t+hC(p_t)\}+u/2.
\]
This is a **purpose-built one-frequency recurrence**, not an equation taken verbatim from the named authors.

Frozen initial p0∈{1/4,2/5,3/5,3/4}, h∈{0,1/4,1/2,1}, u∈{0,1/10,1/4}. Exactly **48 distinct worlds, 7 time observations t=0,...,6**. All frequency values and majority probabilities are saved as full exact Fraction strings in [344545-byte complete results JSON](R159_EXACT_RESULTS.json). All 48×7 frequency values were strictly identical between separate independent computational routes:
1. Exact Fraction algebraic polynomial C(p)=3p²−2p³ with iterative updates.
2. Independent **enumeration of all eight triple demonstration configurations**, summing each majority-A configuration's exact Bernoulli probability before applying the same defined mixture. Second route does not call the first route's polynomial or stored frequency results.

These are distinct exact implementations checking consistency of the frozen mathematical definition, rather than independent source replicates.

## Mathematical results and counterexamples
* For initial p=1/4, majority-of-three probability is exactly \(5/32<1/4\); for p=3/4 it is \(27/32>3/4\). General identity \(C(p)-p=p(1-p)(2p-1)\) proves majority copying lowers a minority trait's prevalence and raises a majority trait's prevalence for all 0<p<1, p≠1/2, within the iid synthetic demonstration sampling assumption.
* With u=0, h>0 and p0<1/2, each frozen generational frequency strictly decreases; for p0>1/2, each strictly increases. With h=0 and u=0, every frequency stays static.
* With h=0 and u>0, \(p_t=1/2+(1-u)^t(p_0-1/2)\) exactly; this is a separate externally reset neutral dynamic, not natural selection.
* For initial p=1/2, **all possible h,u yield p_t=1/2 for the entire path**. Even a complete perfectly measured equilibrium path cannot identify either parameter in this particular case; a non-equilibrium experimental design is necessary.
* The pairs (p,1-p) are exactly mirror trajectories under common h,u. At boundaries p0=0,1, u=0 produces absorbing states, but u>0 breaks absorption. Positive u moves the **first** generation frequency toward 1/2 compared to u=0 at fixed p0,h. No globally dominant effect over repeated generations is claimed under joint conformity and reset.
* This pure frequency mechanism says nothing on its own about whether conformist learning is adaptive, whether institutions persist or how genetic and cultural inheritance coevolve.

## CI, identity and evidence claims
[Source code](r159_cultural_transmission_exact.py), [73 discoverable tests](test_r159_cultural_transmission_exact.py): 48 individually named complete worlds and 25 independent exact fraction/majority/negative-type/identification tests. [First GitHub Actions run39523466288](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39523466288) executed 73 tests under each of Python3.11/3.12, success. [Pinned run39523555967](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39523555967) repeated each environment's 73 tests, and independent archive publisher job118972908769 again executed 73 tests, verified four SHA256 and permanently committed the complete [JSON](R159_EXACT_RESULTS.json) and [ZIP](R159_Cultural_Majority_48_Worlds_73_Tests.zip) to GitHub main at [archive commit df5dcfc](https://github.com/edwardsage419/Psychohistory-Research/commit/df5dcfc7a0f86b0ce46eeb7068ab94688bb2f384). **365 genuine test executions but 73 distinct methods**, all success; no original human data.

Pinned SHA256:
* source `06e79227a73b802806fbd7a0bb3bd6dc33e3f994a8403c14fd8a06c58fdc8aeb`
* tests `e3c9318dc0194d0e2c7f96a8f8e34c7c116797885ca0c6a9371b72873b5d6216`
* complete JSON `618d975c379eefcc0929efbf20218a78832684abd5772ac5decf2e61415fdb7e`
* complete ZIP `504ac3f978fee5b93f17af3fbacf0e0360d54dd6bb2518303794529295934363`.

Reproduce from `research/R159`: `python r159_cultural_transmission_exact.py > R159_EXACT_RESULTS.json`; `python -m unittest -q test_r159_cultural_transmission_exact.py`. No third-party packages, full standard-library ZIP_LZMA artifact.

**CLOSED_BOUNDED_E1** for these 48 frozen exact cultural-frequency models and specified primary-source conceptual boundaries; no full gene-culture causal transfer, real-world behavior prediction E2 or historical cross-study prediction E3. Prior R073/PESEN v0.1 remain frozen. Next original candidate **R160 P2/07-002 Gene Culture Coevolution**, then continue all remaining R before classification/fusion.

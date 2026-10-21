# R163 scientific report: two success-biased copying rules and payoff signal reliability counterexamples

Date: 2026-10-21. Original catalog **P1 / 07-005 Success Biased Transmission**. The computation was preregistered in [the protocol](../../protocols/R163_BALDINI_SUCCESS_BIAS_72_PAYOFF_WORLDS_PRESCORE_FREEZE_2026-10-21.md) on main at commit [a7cc84b](https://github.com/edwardsage419/Psychohistory-Research/commit/a7cc84b1bb1025f7af3e182e4957d6556cb063b2), before implementing research code. **Scientific status: CLOSED_BOUNDED_E1**, exact project-generated single-round payoff-table arithmetic only.

## Author sources and replication boundaries

1. Ryan Baldini (2013), [*Two success-biased social learning strategies*](https://doi.org/10.1016/j.tpb.2013.03.005), *Theoretical Population Biology* 86:43–49. The [original Elsevier publisher article and extended abstract](https://www.sciencedirect.com/science/article/pii/S0040580913000336) and [PubMed record PMID23587700](https://pubmed.ncbi.nlm.nih.gov/23587700/) were inspected. The source explicitly distinguishes **Imitate the Best**, selecting the demonstrator with highest payoff, and **Compare Means**, selecting a cultural variant whose demonstrators have highest sample mean payoff. Baldini notes these strategies have different failures under stochastic payoffs, frequency differences and varying environments. We neither recreated the author's full stochastic payoff distribution, cultural recurrence, selection model, nor any original simulation or genetic-culture coevolution dynamics. Our 72 payoff tables and tie rules are wholly new project constructions.
2. Ryan Baldini (2012), [*Success-biased social learning: Cultural and evolutionary dynamics*](https://doi.org/10.1016/j.tpb.2012.06.005), *Theoretical Population Biology* 82(3):222–228. Original publisher abstract and [PubMed PMID22743216](https://pubmed.ncbi.nlm.nih.gov/22743216/) reviewed. The original reports conditions in which success-biased selection can be less adaptive than random copying. The original population dynamics and selection analysis were not reproduced.
3. Alex Mesoudi (2011), [*An experimental comparison of human social learning strategies: payoff-biased social learning is adaptive but underused*](https://doi.org/10.1016/j.evolhumbehav.2010.12.001), *Evolution and Human Behavior* 32(5):334–342, [author publication entry and original PDF](https://www.alexmesoudi.com/publication/mesoudi-experimental-2011/). The [Elsevier original abstract and visible article sections](https://www.sciencedirect.com/science/article/pii/S1090513810001443) report an empirical virtual-arrowhead learning setting with individual learning, payoff-biased choice, conformism, and random copying. The author's human trial-level data, author regressions, exact per-trial model choices and objective payoff landscapes were not acquired or independently scored. The reported empirical findings **must not be attributed to this E1 computation**.
4. Kendal et al. (2018), [*Social Learning Strategies: Bridge-Building between Fields*](https://doi.org/10.1016/j.tics.2018.04.003), *Trends in Cognitive Sciences* 22(7):651–665, [original publisher abstract](https://www.sciencedirect.com/science/article/pii/S1364661318300949). The review cautions that social learning strategies vary within people and contexts, making individual mechanism identification important.

## Freeze: 72 completely artificial single-observation worlds

Three fictional agents each display exactly one binary cultural symbol A=1 or B=0 and receive a *made-up reported score* in the 0–12 interval. There are six predetermined action/payoff profiles:
* A outlier: symbols (1,1,0), scores (12,0,8).
* B outlier: symbols (1,0,0), scores (8,12,0).
* A agreement: symbols (1,1,0), scores (10,9,2).
* B agreement: symbols (1,0,0), scores (2,10,9).
* Best-person payoff tie: symbols (1,0,0), scores (8,8,2).
* Within-variant mean tie: symbols (1,1,0), scores (8,0,4).

For each, three fixed *score-display transforms*: raw, reverse (12−score), and flat (all displayed scores equal to 6); two choice rules: Compare Means or Imitate the Best; and two *externally assigned* artificial "correct" tokens, A or B. Thus **6×3×2×2=72 frozen cases**, 72 total choice comparisons. The full [47,799-byte result ledger](R163_EXACT_RESULTS.json) stores each profile, strategy, displayed score, correct token, action A probability, unbiased person-copy baseline, artificial expected correct fraction and their difference.

**Exact tie conventions matter:**
* Imitate the Best randomly selects one of the individual demonstrators tied for the highest displayed payoff.
* Compare Means calculates average displayed payoff within each of the two cultural symbols. If the means tie, randomly selects one of the two **symbols**. It does not randomly select one of the three people.
* Random-copy comparator independently samples one person uniformly: P(A)=number of A models/3. This is different from the two-variant mean tie rule.

These definitions, the score inversion, and the externally assigned truth value are deliberate *mathematical probe choices*. They are not parameters fitted to human judgments. No one-round demonstration establishes the underlying psychological rule or long-term human cultural evolution.

## Independent exact Fraction computation

Direct route (A): exact max-payoff and within-symbol arithmetic means with Fraction, plus exact expected correctness and baseline differences.

Independent route (B): explicitly enumerate all highest-score demonstrator indices for Imitate the Best, and for Compare Means compare the cross products of payoff sums with opposite action counts instead of using route A's means. Resolve equal group means by enumerating two represented symbols. Recompute both correct-action frequencies separately. Both route results match **strictly exactly as Python Fraction** for all 72 cases. The full JSON encodes the five result quantities as exact rational strings.

## Prespecified contrasts and measurement limits

| Fixed raw table | Imitate the Best P(A) | Compare Means P(A) | Random-person baseline P(A) |
|---|---:|---:|---:|
| A outlier (1,1,0); (12,0,8) | 1 | 0 | 2/3 |
| B outlier (1,0,0); (8,12,0) | 0 | 1 | 1/3 |
| Best-person tie (1,0,0); (8,8,2) | 1/2 | 1 | 1/3 |
| Within-variant mean tie (1,1,0); (8,0,4) | 1 | 1/2 | 2/3 |

The original same artificial observations therefore **identify different decisions according to the selected computational rule**; observing only one action outcome does not establish which psychological rule generated it.

**Observed success versus true success:** In the raw A-outlier case, the Best strategy chooses A with certainty. If the assigned true correct token is A, expected correct choice improves from baseline 2/3 to 1, a gain **+1/3**. If truth is B instead, correct choice falls from baseline 1/3 to 0, a loss **−1/3**. The demonstrator payoff table is *unchanged* in this contrast; externally determined correctness is reversed. In real social learning, observed payoff reliability has to be measured or modeled, which this research has not done.

**Tie and ranking ambiguity:** Under flat scores on the A-outlier action pattern, the Best rule copies A with probability 2/3 (uniform over people) and the Means rule copies A with probability 1/2 (uniform over represented variants). No true payoff ranking exists in this artificial flat condition; tie conventions alone create this difference. An increasing affine score transformation preserves rank and group mean order, whereas reversing score signs can change which strategy selects which symbol. Confidence about "success bias" without specifying observation and tie rules is unwarranted.

**Competing explanations:** A learner selecting an apparently high-payoff demonstrator may be using an observed score heuristic, a prestige cue, majority-frequency learning, or individual exploration. Comparing the exact one-round toy scores does not distinguish such alternatives in real humans. The research does **not** claim Baldini's evolutionary model has been replicated, that either strategy is generally adaptive, or that human accuracy improvements have been estimated.

## CI, archive and transparent evidence level

Original program [r163_success_bias_payoff_exact.py](r163_success_bias_payoff_exact.py), [102 actual distinct unittest methods](test_r163_success_bias_payoff_exact.py), with 72 uniquely named frozen world tests and 30 independent mathematical, validity and data-replay tests.
* [First run39528469903](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528469903) succeeded for Python 3.11 and 3.12 with 102 tests per version.
* [SHA256 checked run39528566826](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528566826) succeeded for Python 3.11 and 3.12, 102 tests per version, validating four immutable SHA256 byte hashes.
* [Archive run39528599475](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528599475) succeeded for Python 3.11 and 3.12, 102 tests each. Third publication job118989052734 reran all 102 tests, recreated deterministic ZIP and JSON, validated SHA256 and permanently committed full files to GitHub main at [commit310acad](https://github.com/edwardsage419/Psychohistory-Research/commit/310acadf9b16124b0df5a386620aa6aa851db964).
* In all **seven 102-method executions = 714 executed unit tests** across three CI runs, zero failures. They cover 102 distinct methods; repeated executions do not create independent original subject datasets.
* SHA256 source `c680c53cbbcbc52200ffdd3c7b40b37a32ea6736c0011a64a9c21107271e7262`; tests `c2349e512b8c1fc1c23dd905109f1416e58940b56eee41ac45f5bc8aaa5f611c`; complete JSON `23979510af73c9b92e9cadb85ee86a9223401c4d13a00240f832938f046dde22`; ZIP `a3313a85ab0d5aa4865f28747ec05a7c3bcdc36716a12fddf6fa54d286e279cf`.
* Reproduce in `research/R163`: `python r163_success_bias_payoff_exact.py > R163_EXACT_RESULTS.json` then `python -m unittest -q test_r163_success_bias_payoff_exact.py`; standard library only. The complete original source/tests/data bundle is [R163_Success_Bias_72_Worlds_102_Tests.zip](R163_Success_Bias_72_Worlds_102_Tests.zip).

**Acceptance: R163 CLOSED_BOUNDED_E1** for frozen artificial signal-dependent one-round copying choice computations and source concept audit. Original human experiment replay E2=0, external historical forecast E3=0. Keep R073 and PESEN v0.1 FROZEN. Next original catalogue entry verified: **R164 P1 / 07-006 Content Biased Transmission**, followed by the remainder of the original R series, then unified model classification and fusion.

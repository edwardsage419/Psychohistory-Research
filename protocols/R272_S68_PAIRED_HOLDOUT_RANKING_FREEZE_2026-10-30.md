# R272 S68: paired two-test-bit holdout ranking uncertainty, design freeze

UTC date: 2026-10-29. Baseline main HEAD: 3d5349f5505679492ee324f8b47d028476b1fc7b.
Dedup key: (r,R272,original-R272-freeze-52f84dbf,S68 paired finite holdout model ranking).
This is a new, bounded complementary analysis. Existing R272 acceptance remains unchanged.

## Frozen question and source

Under the original R272 three Bernoulli worlds p in {1/4,1/2,3/4}, four training bits and two strictly held-out future bits, how often does the observed **paired two-bit test Brier score** prefer the model whose **population expected independent test Brier** is worse? Both compared models must use identical training and test bits. Source probability remains p^(six successes)*(1-p)^(six failures), with 64 six-bit configurations per p.

The three prespecified ordered model comparisons are (TRAIN_MLE,LAPLACE_BETA11), (TRAIN_MLE,CONSTANT_HALF), and (LAPLACE_BETA11,CONSTANT_HALF). All three original R272 predictor formulas and the Brier rule are frozen. For each p and pair compute exact probabilities P(D<0), P(D=0), P(D>0), exact E[D], E[D²], Var(D), where D is the **two-test-bit average Brier of the first model minus that of the second**. A positive D means first model worse on this test. Also compute the probability that the strict sign of observed D disagrees with the strict sign of E[D]. Ties are a separate outcome, never allocated to either winner. The 9 comparisons reuse the same 64 primitive six-bit outcomes per p; 576 comparison-labelled rows do not mean 576 independent experiments.

## Two independent computation routes

Route R directly enumerates each ordered six-bit source and evaluates both forecasts on the same two held-out labels, using exact fractions. Route B independently sums over K~Binomial(4,p) and J~Binomial(2,p) and computes paired D from q_A(K), q_B(K) and J. Route B must not call the route R enumeration function. Both must agree for all 9 comparisons on all 7 frozen statistics.

## Negative controls and acceptance limits

Require that identical forecasts yield D=0 for every source, that each p/pair has total mass one, and that a deliberately reversed D sign changes at least one directional probability or mean; reject missing, duplicated, and noncanonical comparison identities. Persist a full exact CSV, exact JSON, runnable standard-library Python, independent audit results and scientific report. If full source cannot be fetched, mark the gate OPEN. Use no paid service and no GitHub Actions without verified zero cost. This is E1 finite artificial evidence, internal nonblind reanalysis of an already read R272 source. Prior R272 report and population risks were read before this protocol; this is a prospective *new-computation* freeze only, not a blind external preregistration. R073/PESEN v0.1 remain frozen; no E2/E3 inference. Any unexpected result is retained as negative evidence.

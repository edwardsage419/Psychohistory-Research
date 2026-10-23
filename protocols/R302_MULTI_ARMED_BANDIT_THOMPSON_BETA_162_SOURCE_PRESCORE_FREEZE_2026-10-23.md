# R302 prescore freeze: two-armed Beta–Bernoulli bandit, Thompson selection probabilities vs posterior-mean greedy

Date 2026-10-23 Asia/Taipei. Original 239 P1 item **02-016 Multi Armed Bandits**. Freeze before R302 code/results. Scientific scope **E1 exact artificial posterior action selection, not sampled regret/time-series**, new human/animal E2=0 and historical E3=0. R073 and PESEN v0.1 unchanged. All R first, then taxonomy, finally model fusion.

## First-party source and limited object

W. R. Thompson (1933), "On the likelihood that one unknown probability exceeds another in view of the evidence of two samples", *Biometrika* 25(3–4):285–294, primary publisher DOI https://doi.org/10.1093/biomet/25.3-4.285. Motivation: select one of two uncertain success probabilities with posterior uncertainty; **this work computes exact two-arm posterior superiority probabilities only**. Auer, Cesa-Bianchi & Fischer (2002), "Finite-time Analysis of the Multiarmed Bandit Problem", *Machine Learning* 47:235–256, https://doi.org/10.1023/A:1013689704352, original manuscript https://people.eecs.berkeley.edu/~russell/classes/cs294/s11/readings/Auer%2Bal%3A2002.pdf. Their UCB1 and regret guarantees are **not implemented/reproduced** in R302. R297 Q-learning state-action control in a three-state MDP and R299 fixed-policy TD prediction differ from bandit posterior sampling; no earlier real study may be silently counted as new bandit E2.

## Fully specified artificial evidence universe

Two exchangeable binary reward arms A,B, each with independent Beta(1,1) prior on its unknown fixed Bernoulli success probability theta_A/theta_B. For each arm, set artificial observed success count s∈{0,1,2} and observed failure count f∈{0,1,2}; complete cross A_s,A_f,B_s,B_f results in **3^4=81 distinct count worlds**, each with **two fully labeled original arm-level sources**, **162 complete original source rows**. These source rows are count configurations, **not randomized actions, observed trial tapes, distinct persons, or bandit trajectories**. Because counts alone are sufficient statistics, outcomes ordering is not reconstructed nor used for time-order regret.

Posterior for arm i is Beta(a_i=1+s_i,b_i=1+f_i); exact mean mu_i=a_i/(a_i+b_i) and exact variance a_i*b_i/((a_i+b_i)^2*(a_i+b_i+1)).

Greedy policy chooses A if mu_A>=mu_B, else B, exact tie A. Thompson sampling at a single next **hypothetical** action draws independent theta_A,theta_B from the two posteriors and chooses larger; since continuous, ties have probability0. Analytically integrate exact TS choice probability P(A chosen)=P(theta_A>theta_B), B probability 1-P(A chosen). All probabilities rational Fractions. The actual random draw and realized outcome is **never** simulated.

Fixed exact original main implementation:
For integer a,b,c,d from Beta posteriors for A,B, integrate A density × CDF of B. Using beta function B(x,y)=(x−1)!(y−1)!/(x+y−1)! and beta-binomial polynomial CDF of B:
P(theta_A>theta_B) = Σ_{j=c}^{c+d−1} comb(c+d−1,j) * B(a+j,b+c+d−1−j) / B(a,b).
Independent no-import source audit must **not reuse this expansion**, and instead use alternate integral from expanding (1-t)^(d−1):
P(theta_A>theta_B) =
Σ_{k=0}^{d−1} (−1)^k comb(d−1,k) * B(a+c+k,b) / ((c+k)*B(a,b)*B(c,d)).
Verify independent rational equivalence for all 81 worlds and each of 162 individual action source rows.

## Frozen test claims

1. All count worlds have 81 unique full count vectors and exactly two action source rows with coherent posterior shapes, posterior mean/variance, greedy action, and TS single-action probabilities summing to1.
2. All-zero evidence case A0/0,B0/0: posterior mean each1/2; posterior variance each1/12; greedy action A by strict tie rule; Thompson selection A1/2,B1/2 (randomization despite greedy tie).
3. A successes1 failures0, B unobserved: A posterior Beta(2,1), mean2/3; B Beta(1,1), mean1/2; greedy A, TS probability(A)=2/3, B=1/3.
4. A successes2 failures0, B successes0 failures2: Beta(3,1) vs Beta(1,3), TS probability A=19/20, B=1/20, greedy A; probability of exploring worse-posterior-mean arm remains positive in this **chosen count state**.
5. Label swap complement exactly: for any A evidence count vector and B evidence count vector, swapping entire arms gives P_new(A)=1-P_old(A). Equal posterior shapes imply TS selection A=1/2 (regardless of certainty), while greedy action A by tie.
6. Posterior Beta(3,3) after A2 successes and A2 failures has mean1/2 and variance1/28 vs unobserved Beta(1,1) mean1/2 var1/12, even though both means are equal and TS choice is still1/2 against a uniform B. This separates posterior concentration from probability of superiority without claiming general exploration ranking.
7. All posteriors and probabilities exact bounded values; do not compute or assert true latent arm superiority, best actual arm, cumulative regret, reward trajectory, UCB1/logarithmic regret or real subject behavior, since actual generating arm rates are unspecified.

## Evidence and archival acceptance

Require Python3.11/3.12 executable --test/--emit; all 162 original arm-level synthetic source rows CSV; 81 world-wise exact posterior/greedy/TS JSON; SHA256; third-party independent alternate integral for exact 162 source checks plus adversarial source tamper and missing/duplicate checks; three observed successful GitHub Actions jobs with both Python interpreters and third independent permanent archive; formal bounded machine E1 acceptance. Only **after** these gates can original 239 crosswalk be advanced v1.6 by changing **only 02-016** and reducing pending47→46. No unseen original study falsely claimed. R073 and PESEN v0.1 stay frozen.

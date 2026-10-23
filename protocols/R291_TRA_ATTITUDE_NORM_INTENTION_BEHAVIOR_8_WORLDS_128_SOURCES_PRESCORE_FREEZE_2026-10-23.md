# R291 prospective prescore freeze: Theory of Reasoned Action (TRA), 8 bounded synthetic worlds

Date 2026-10-23 Asia/Taipei. Original 239-candidate catalogue 01-013 (P1). The completed adjacent primary research R290 is 01-011. This protocol must be committed before any R291 executable or results. Scientific level under study: **E1 exact artificial mathematical mechanics only**. Human behavioral observations E2=0 and historical E3=0. R073 and PESEN v0.1 remain frozen; complete all original R items before classification and fusion.

## First-party source and interpretation boundary

Fishbein, M. & Ajzen, I. (1975), *Belief, Attitude, Intention, and Behavior*, Addison-Wesley, original author-access page https://people.umass.edu/aizen/f%26a1975.html (chapter 7 formation of intentions, chapter 8 prediction of behavior). Ajzen, I. & Fishbein, M. (1980), *Understanding Attitudes and Predicting Social Behavior*, original author's bibliographic list https://people.umass.edu/aizen/pubstxt.html . In canonical TRA, behavioral attitude and subjective norm precede behavioral intention; intention is the proximal antecedent of volitional behavior. This freeze builds a **new synthetic binary probability skeleton** for examining that architecture, and does not attribute its numerical coefficients, probability distributions, linear functional form or direct-path violation to the source authors. 01-014 Theory of Planned Behavior (TPB) and perceived behavioral control remain separate, with no TPB candidate counted here.

## Complete deterministic synthetic design

Attitude A, subjective norm N each take -1 or +1 independently with probability 1/2 each. Intention I and actual behavior B each take 0 or 1. Four weights (a,n) are fixed:

* BALANCED: (1,1)
* ATTITUDE_HEAVY: (2,1)
* NORM_HEAVY: (1,2)
* NORM_NULL: (2,0)

Each profile is crossed with two behavior-generation mechanisms:

* MEDIATED: true conditional P(I=1|A,N)=1/2+(a*A+n*N)/8. True P(B=1|I,N,A)=1/4+I/2. Complete mediation B ⟂ (A,N) | I is built into this artificial generator.
* DIRECT_NORM_STRESS: same intention generator; true P(B=1|I,N,A)=1/4+I/2+N/8. This bounded violation of TRA's complete-intention-mediation skeleton creates a visible residual direct normative route; it is a negative-control DGP, and not a proposed TRA theoretical amendment or claim about real people.

All conditional probabilities are between 1/8 and 7/8 inclusive. For each world, the 16 tuples (A,N,I,B) in lexicographic product order have exact joint source probabilities (1/4)*P(I|A,N)*P(B|I,N,A); all 16 source cells must be present, including both intention and behavior outcomes. Eight worlds generate 128 fully labeled original source cells. No random generation, fitted parameters, human subjects or postresult coefficient tuning.

## Predictors, risks, and fixed primary claims

For predicting B from A,N before observing I, the exact full forecast is P(B=1|A,N)=1/2+[a*A+(n+2*d)*N]/16 where d=0 for MEDIATED and 1 for DIRECT_NORM_STRESS.

Compare four *population-optimal, fixed* Brier forecasters at this same pre-intention information point:
1. FULL_AN, exact P(B=1|A,N);
2. ATTITUDE_ONLY, exact P(B=1|A) marginalizing the independent N;
3. NORM_ONLY, exact P(B=1|N) marginalizing A;
4. CONSTANT, exact unconditional P(B=1)=1/2.

The Brier score for binary action B is (B-q)^2. Risks are weighted by the 16 original cell masses; baselines have no access to unobserved I or future B. FULL_AN is observationally optimal under its own artificial DGP, which *cannot* establish superiority on real samples.

For all 8 worlds, the independent closed-form exact *risk differences* must be:
R(ATTITUDE_ONLY)-R(FULL_AN)=(n+2d)^2/256;
R(NORM_ONLY)-R(FULL_AN)=a^2/256;
R(CONSTANT)-R(FULL_AN)=(a^2+(n+2d)^2)/256;
R(FULL_AN)=1/4-(a^2+(n+2d)^2)/256.
Use Fraction rational comparison, no float acceptance tolerance.

For the mediated four worlds, Pr(B=1|I,A,N) equals Pr(B=1|I) for every A,N,I; in direct-norm stress worlds it differs by N/8, and the conditional contrast between N=+1 and N=-1 at fixed I,A is exactly 1/4. The NORM_NULL+MEDIATED world must have R(ATTITUDE_ONLY)=R(FULL_AN). NORM_NULL+DIRECT_NORM_STRESS must have strictly positive normative omission gap 1/64; this is an explicit mechanism separation, not causality inferred from uncontrolled human data. Norm and attitude weights exchange their incremental predictive contributions across ATTITUDE_HEAVY and NORM_HEAVY mediated worlds.

An independent audit **must not import the main implementation**. It will read all emitted source cells, reconstruct the joint masses and conditional probabilities from frozen constants, recompute all four forecasts and Brier scores, confirm absence/presence of residual norm effects, source mass=1, and exact CSV/JSON SHA256. Independent "oracle" or intention after-outcome leakage is forbidden. Include adversarial negative checks for source modifications and formula violations if practical.

## Files and gates

Before CLOSED_BOUNDED_E1, require a Python >=3.11 standalone executable with --test/--emit, 128-row original labeled CSV, eight-world results JSON, source+results SHA256 receipt, independent code-only audit, scientific report, machine-readable acceptance with CI identifiers, and a successful observed three-job GitHub Actions matrix (Python 3.11/3.12 tests and independent auditor). Then independently audit only original catalogue 01-013 change from v0.4 to v0.5; preserve 239 unique candidates and 01-014 pending without adding TPB features. Versioned results in main, and explicit metadata and scientific acceptance separation. No scientific E2/E3 upgrades, and no prediction or generalization claim beyond this synthetic DGP.

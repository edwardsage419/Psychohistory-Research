# R291 S87 prospective freeze: intention measurement error and apparent residual norm prediction

Date: 2026-10-30 UTC. Parent R291 frozen synthetic Theory of Reasoned Action study: original protocol commit 161d40a01451f1e89be045910f95ec536768754c. This S87 protocol must be committed before any S87 calculation or scoring. Existing R291 acceptance is unchanged. E1 artificial mechanism only; E2 human=0; E3 historical=0. R073 and PESEN v0.1 remain frozen.

## Distinct research question
When intention I is measured through a noisy proxy J, can subjective norm N improve prediction of B even when the original synthetic mechanism satisfies B independent of N and A conditional on the *true* I? Quantify the exact out-of-sample Brier advantage of observing N in addition to A and J. This is a measurement error stress test, not a causal identification claim, a human measurement validation, or a reanalysis of the 1975/1980 authors' empirical studies.

## Fixed source generator and observation point
Use the eight original R291 worlds and fixed coefficients from its 2026-10-23 prescore freeze, without any refit or parameter changes: four profiles BALANCED(a=1,n=1), ATTITUDE_HEAVY(2,1), NORM_HEAVY(1,2), NORM_NULL(2,0), crossed with MEDIATED(d=0) and DIRECT_NORM_STRESS(d=1).
A,N independently equiprobable in {-1,+1}; I,B,J binary. Original P(I=1|A,N)=1/2+(a*A+n*N)/8 and P(B=1|I,A,N)=1/4+I/2+d*N/8. J is an independent symmetric misclassification of I with P(J != I|I,A,N,B)=e, e in {0,1/4,1/2}. The 32 ordered (A,N,I,B,J) source cells per world and error level, including zero-probability cells, must be preserved. Total 8*3*32=768 labeled cells. Source mass is (1/4)*P(I|A,N)*P(B|I,A,N)*P(J|I). No observed future B or true I may enter a forecast.

For each world and e, form four population-optimal exact conditional probabilities of future B=1 using only the stated observed features:
FULL_ANJ=P(B=1|A,N,J), AJ=P(B=1|A,J), AN=P(B=1|A,N), A=P(B=1|A). Each conditional is computed by summing full source masses over the hidden variables, without importing the R291 model implementation. For zero-mass conditioning events, do not divide by zero; their forecasts are undefined and contribute zero risk. Expected Brier risk is sum over all 32 cells of mass*(B-q)^2. The primary estimand is R(AJ)-R(FULL_ANJ). Additional comparisons: R(AN)-R(FULL_ANJ), R(A)-R(FULL_ANJ). All exact Fraction, no float tolerances.

## Prespecified validation and scope
1. Every world/e source has exactly 32 unique labeled cells, probabilities in [0,1], mass exactly 1, zero cells retained. Every conditional forecast used on a positive-mass cell is in [0,1].
2. All three omission penalties are nonnegative, by population conditional expectation.
3. For all MEDIATED worlds at e=0, R(AJ)-R(FULL_ANJ)=0 because J=I.
4. For all MEDIATED worlds at e=1/2, the primary omission penalty equals n^2/256, matching the original R291 pre-intention omission risk. For all DIRECT_NORM_STRESS worlds at e=1/2 it equals (n+2)^2/256.
5. For NORM_NULL MEDIATED, the primary penalty is zero for all e. For NORM_NULL DIRECT_NORM_STRESS, the primary penalty is 1/64 for all e.
6. For at least BALANCED MEDIATED at e=1/4, the primary penalty is strictly positive. No other numerical e=1/4 result or ordering is frozen.
7. Independent B verification must use a mathematically different approach (for example exact conditional variance decomposition or conditional cell aggregation), not import the R implementation, check all 24 worlds and at least one deliberate malformed-source rejection. The audit is internal nonblind and cannot be labeled external independent replication.
8. Negative evidence and any failed prespecified assertion remain visible. Retain original R291 and R073/PESEN artifacts unchanged. Do not modify original239 crosswalk or pending queue. Any real-data A subflow source must be separately licensed and screened, with no restricted data access.

Success for this S87 bounded increment: original protocol commit predates results, runnable source and all 768 cells, 24-world exact results, independent mathematical check, scientific report, and GitHub commit verification. CI only if no cost risk can be confirmed; otherwise NOT_RUN. This does not itself upgrade R291 formal acceptance or constitute human/historical validation.

# R188 cluster deletion third method: precomputation freeze

Date 2026-10-26. Baseline main HEAD 293c16fc6035e4eecc6518a3f38f3db377106f5d. R188 original acceptance remains unchanged.

Input: R188 frozen 180 artificial worlds, 6 groups of 8 observations, source y=a+b*x+c*xbar_g+epsilon, designs BALANCED (4,4,4,4,4,4), WEAK_BETWEEN (2,2,4,4,6,6), STRONG_BETWEEN (2,2,2,6,6,6), a in {0,1}, b in {1/4,1/2}, c in {-4,-2,0,2,4}, e in {0,1/4,1/2}. Compare against original R188 exact results.

Predeclared question: how does deleting one entire group affect the pooled and quasi demeaned slopes? For each world, omit each of six groups, keep the other 40 rows, and calculate four fixed theta values 0, 1/2, 3/4, 1. There must be exactly 180*6*4=4320 exact rational results, plus 720 full sample identities. No post hoc selection.

R primary route: regenerate all individual x,y values with the original within-cell symmetric epsilon signs, then perform centered OLS on transformed individual observations; theta=1 is within group OLS. B independent route: use group exposure shares and analytic Vwithin/Vbetween decomposition beta=b+c*(1-theta)^2*Vbetween/(Vwithin+(1-theta)^2*Vbetween). Both routes must agree exactly for all 4320 cases, with a separate identity check against original archived 720 full sample slopes.

Prespecified checks: BALANCED unchanged at b for all deletions; theta=1 always b; all denominators positive; quantify sign reversals relative to full sample; report fixed STRONG_BETWEEN,a=0,b=1/4,c=-4,e=1/4; run a mutation test adding a group-specific intercept, checking within-group slope invariance and potential pooled sensitivity. Record counterexamples and null results without filtering.

Evidence level E1 artificial algebra only. This does not estimate random effects, give uncertainty intervals, demonstrate out of sample prediction, identify contextual causality, or constitute external replication. R073 and PESEN v0.1 stay frozen; E2 and E3 increments zero. Commit scripts, exact receipts, scientific report and separate B audit under nonoverlapping paths, without modifying original files or shared crosswalk. Check main before writing, avoid overwrites. Do not run paid CI or incur new costs.

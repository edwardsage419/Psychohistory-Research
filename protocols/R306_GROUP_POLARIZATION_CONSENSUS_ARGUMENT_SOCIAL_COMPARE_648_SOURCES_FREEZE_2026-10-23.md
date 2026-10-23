# R306 protocol frozen before model: group polarization vs averaging and persuasive/counterarguments

Date 2026-10-23 Asia/Taipei. Original239 **03-012 Group Polarization Models** P1. Scope strictly **E1 artificial finite 3-person group mean change**, not empirical reproduction, social network or historical E3. Pre-commit this protocol before source files, scores/results. R073/PESEN v0.1 frozen. Finish R-series before taxonomy or fusion.

## Original empirical research and mechanism boundary

Moscovici & Zavalloni (1969), *The group as a polarizer of attitudes*, *Journal of Personality and Social Psychology* 12(2):125–135, DOI https://doi.org/10.1037/h0027568. The original article reported shifts of discussion-based judgments toward extremes among real human groups. Myers & Lamm (1976), *The group polarization phenomenon*, *Psychological Bulletin* 83(4):602–627, DOI https://doi.org/10.1037/0033-2909.83.4.602, reviews differentiation of interpersonal comparison and informational influence. Burnstein & Vinokur (1977), *Persuasive argumentation and social comparison as determinants of attitude polarization*, DOI https://doi.org/10.1016/0022-1031(77)90002-6; Sieber & Ziegler (2019), *Group Polarization Revisited: A Processing Effort Account*, DOI https://doi.org/10.1177/0146167219833389, describes modern competing social comparison and argument processing mechanisms.

**All quantitative formalization below is INVENTED IN THIS PROJECT**. These sources motivated separating a social-comparison mechanism from supportive/counterarg processing and a neutral averaging control; no participant trial-level values, original causal treatments, data, actual effect sizes, or quantitative author-specific model are reproduced. R305 SCT category fit, R304 social identity resource allocation, R072 reputation signal are separate subjects.

## Complete artificial finite source universe and equations

Three fictional opinion holders with prediscussion opinions x_i∈{-1/2,0,1/2}; enumerate all **3^3=27 ordered group triplets** including symmetric and all-neutral. Group prediscussion mean m=(x0+x1+x2)/3. Define direction sign q=sign(m), with q=0 if m=0. Social comparative target c = max(x_i) if m>0, min(x_i) if m<0, and 0 if m=0. This implements (only in project toy) using strongest currently observed same-direction opinion as group-norm comparator. Argument target a= q for SUPPORT_PRE_DISCUSSSION_DIRECTION and -q for COUNTER_PRE_DISCUSSION_DIRECTION. With m=0 both zero, **no arbitrary directional polarization is invented**.

Independently enumerate the project-fixed influence mechanism weights:
- CONSENSUS_AVERAGING α=0, β=0
- SOCIAL_COMPARISON_ONLY α=1/2, β=0
- PERSUASIVE_ARGUMENT_ONLY α=0, β=1/2
- COMBINED_SOCIAL_AND_ARGUMENT α=1/2, β=1/2.

Use **invented** single discussion step group consensus:
m_post = m + α(c−m) + β(a−m).
All three fictional members then report that exact consensus value m_post; no new opinion rows after a second round, no hidden stochastic likelihood, no social influence parameter fit. Because α,β≥0 and α+β≤1, m_post is a convex combination of m,c,a and remains within [-1,1]. Under CONSENSUS_AVERAGING, m_post=m independent of argument direction; individual variation may vanish but group mean does NOT shift, so mere averaging is not evidence of group polarization.

With q≠0, direction-preserving strict polarization when sign(m_post)=q and |m_post|>|m|; direction-preserving strict depolarization when same sign and |m_post|<|m|; direction flip when m_post*q<0; crossing zero or neutral initial states must receive appropriate ZERO_OR_NEUTRAL/AT_ZERO status and cannot count as strict polarization. The metric group mean shift and individual post opinions is **separate** from within-group consensus convergence; zero individual variance after consensus cannot be called increased or decreased group extremity by itself.

Two argument contexts support/counter × four alpha/beta mechanism policies × 27 original ordered opinion triples = **216 artificial worlds**, each containing all three before/after person records = **648 complete original artificial source rows**. Each CSV row contains frozen triplet, person slot/index, pre-opinion, premean, sign, social target, argument target, direction, α,β, individual post-consensus, post mean, signed change, abs-extremity change, polarization status and a flag of whether the individual changed. All Fraction exact. These are not 648 subjects or independent actual discussions.

## Frozen examples and counterexamples

For pre-opinion (1/2,1/2,1/2), m=1/2 and social target c=1/2. Social comparison only leaves m unchanged (no stronger observed member); supportive argument β=1/2 moves m_post=3/4 and counts polarization; counter argument β=1/2 targets -1 and moves m_post=-1/4, a direction FLIP, **not** polarization. Consensus-averaging keeps mean1/2 and suppresses individual variance trivially.

For heterogeneous pre-opinion (0,0,1/2), m=1/6 and social target c=1/2. SOCIAL_COMPARISON_ONLY moves consensus to 1/3, strict direction-consistent polarization; supportive PERSUASIVE_ARGUMENT_ONLY moves m_post=7/12, strict polarization; COMBINED supportive shifts m_post=3/4, strict polarization. For argument COUNTER, a=-1 and the same β=1/2 induces m_post=-5/12, direction flip (not polarization). All-neutral (0,0,0) remains mean0 under ALL mechanisms/directions, so absence of prediscussion direction cannot be treated as emergent positive/negative radicalization. All-negatives must be the exact sign-reversed mirror of positives if argument context sign is held relative to prediscussion direction.

The frozen **negative control** alpha=beta=0 must have no aggregate mean shift across all 27×2 input worlds. In a homogeneous all-positive world, social comparison alone has no group-mean change while supportive arguments can shift; mechanisms are mathematically nonidentical. No claim argument availability or observed strongest opinion reflects human social-psychological variables. No real efficacy/risk/political attitudes, no online platform forecasts.

## Release gates

Main Python 3.11/3.12 native --test/--emit; all 648 original source rows and 216-world JSON, SHA256; independent no-import exact source reconstruction with own implementation and 16+ tamper tests; three successful GitHub Actions jobs, independent third source permanent main archive, formal bounded scientific report/acceptance. Original catalogue crosswalk v2.1 then updates **only 03-012** (primary194→195, pending42→41); v2.0 existing-R072 source reattribution, R305 SCT, R304 social identity all unchanged. Real E2/E3 new0, R073/PESEN frozen; all R-series before taxonomy/fusion.

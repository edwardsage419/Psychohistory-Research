# R328 predictive error correction finite E1: prescore frozen protocol
Date 2026-10-24. Original239 02-010 Predictive Processing (P2). State at this commit: PROTOCOL_ONLY.

## Scope and existing R reuse
Checked R300 HMM forward-filter report, R112 Bayes updating report, R326 hierarchical Bayes report and R327 one-sense POMDP report. Their documented finite mechanisms involve discrete probability updating or planning; none of these checked reports demonstrates the present precision-weighted residual error gradient with separate top-down prior and sensory mismatch. Strict reuse of their scientific status is denied. Earlier ZIP itemwise audit is still OPEN.

English original source: Rao & Ballard (1999), Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects, Nature Neuroscience 2:79-87, DOI 10.1038/4580. The original hierarchical visual cortical model and natural-image findings are far richer than this project-created scalar analogue. Secondary mechanistic background: Friston (2005), A theory of cortical responses, Philosophical Transactions of the Royal Society B 360:815-836, DOI 10.1098/rstb.2005.1622.

## Frozen artificial model and exact source universe
Scalar prior prediction m in {0,1}; artificial sensory target y in {0,1,2}; prior precision r in {1,2}; sensory precision p in {1,2}. Exactly 24 complete parameter worlds. The scalar objective is E(x)=(r/2)(x-m)^2+(p/2)(y-x)^2. Initial estimate x_0=m. For t=0,1,2,3 use exact rational gradient update x_(t+1)=x_t+(1/4)[p(y-x_t)-r(x_t-m)]. Retain x_t and E(x_t) for all t=0,1,2,3,4: exactly 120 fully labelled artificial source rows. The analytic minimizer x_star=(r*m+p*y)/(r+p). All values exact Fractions; no neural measurements or human observations.

## Prospective falsifiers
1. All 120 CSV rows and 24-world JSON must byte-replay from the frozen Python program, with fixed order m, y, r, p, t.
2. Independent no-import auditor must derive x_t by closed-form recurrence solution x_t=x_star+(m-x_star)*(1-(r+p)/4)^t, independently compute energy, match every CSV row and all 24 JSON worlds.
3. For every world, E(x_(t+1)) <= E(x_t) for t=0..3. For y=m, all x_t=m and prediction errors vanish.
4. Fixed witness m=0,y=2,r=1,p=2 yields x_star=4/3 and x_4=85/64; changing to r=2,p=1 yields x_star=2/3 and x_4=85/128. Independent auditor must reject a deliberate tampered source row.
5. CI must complete 3 successful jobs, Python3.11, Python3.12 and independent no-import audit, before any E1 formal acceptance.

## Scientific bounds
Passing only proves exact finite scalar precision-weighted residual error dynamics in this constructed system. It does not reproduce Rao-Ballard 1999 visual cortex simulation, image statistics, receptive fields, predictive processing theory in general, brain neural prediction-error signals, real human E2, historical E3 or external forecasting. R073 and PESEN v0.1 frozen; original239 catalogue identity preserved. Taxonomy, model fusion and personal decision system deferred.

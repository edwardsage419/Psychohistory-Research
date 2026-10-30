# R293 S89 prescore freeze: endogenous respondent style and centered-score invariance

Date: 2026-10-30 UTC. Track R primary. Base main HEAD: 32e7de6128c82c5c82c7275c203ed91964673dca. This protocol is committed before S89 output computation. Original R293 protocol, 2112 original rows, bounded E1 acceptance and all earlier receipts remain unchanged.

## Objective and fixed source universe

Study whether a shared additive response-style factor correlated with a latent value can reverse observed raw association while within-person centering remains pathwise invariant. This is a finite artificial E1 sensitivity experiment only, not ESS PVQ21 human data or a Schwartz circumplex validation.

Reuse original R293 latent worlds without alteration: INDEPENDENT has 10 independent fair bits b0..b9, 1024 profiles; OPPOSED_PAIRS has five independent fair bits b0..b4 and ten values (b0..b4,1-b0..1-b4), 32 profiles. New response-style mechanisms:
* ANCHOR_PLUS: shared shift S=2*b0.
* ANCHOR_MINUS: shared shift S=2*(1-b0).

Each latent profile has equal mass 1/1024 or 1/32. Each new world enumerates every latent profile exactly once, hence 1024+32=1056 new sources per style and 2112 new labeled rows total. No independent random style draw in these new worlds. Original independent-style baseline remains separately archived in R293 and is not regenerated as a new original finding.

Observed raw slot X_i=V_i+S. Centered C_i=X_i-(sum_j X_j)/10. Preserve all 10 latent, raw and centered slots and exact rational source mass. Enumerate source labels, include zero-probability cells only if the fixed source universe contains any (none here).

## Precommitted comparisons

For each of four new worlds compute exact 10 means and 10x10 covariance matrices for raw and centered scores; total 800 covariance entries. Independently check that every centered score and centered covariance entry equals the original R293 corresponding latent-world baseline, and every pairwise score difference is preserved. The raw association of opposed pair slots (0,5) is predicted to be +1 despite latent correlation -1 under both anchored mechanisms; the original independent-style raw correlation was +3/5. For INDEPENDENT, the anchored raw correlation of slots (0,5) is 2/sqrt(5) under either mechanism, interpreted via exact squared-correlation 4/5. Check full source masses and uniqueness.

Negative controls: original independent-style source matrices, latent covariance signs, zero-shift algebra and pathwise centered shift invariance. No parameter tuning, model fitting, or post-result choice of slot pairs. Report any deviations as FAIL; no silent revisions to this protocol.

## Independent B audit and acceptance

B must reconstruct the covariance matrices using a mathematically separate linear-transform covariance method, not import the R enumerator; verify the persisted full source rows, exact source probabilities, pairwise differences, original R293 parity and selected exact correlations. Add mutation controls for duplicate/missing rows, wrong style, changed raw score, changed centered score, changed source probability, changed matrix. The audit is internal nonblind unless an external team actually reproduces it. Exact program execution is separate from formal scientific acceptance.

Keep original239 crosswalk v7.8 and pending154 unchanged; keep R073 and PESEN v0.1 frozen. E1 synthetic only; E2=0, E3=0. No GitHub Actions before verifying zero-cost eligibility. No billed services. New work belongs only in research/validation, research/evidence_audit and research/coordination/r, with A scout in research/data_scout if time permits.
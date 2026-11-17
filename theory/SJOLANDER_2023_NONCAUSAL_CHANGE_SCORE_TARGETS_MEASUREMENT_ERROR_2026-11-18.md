# Sjölander et al. (2023): noncausal change-score targets and measurement-error boundaries

track: theory
date: 2026-11-18 Asia/Singapore
source: Arvid Sjölander, Erin E. Gabriel, Iuliana Ciocănea-Teodorescu (2023), European Journal of Epidemiology 38:501–509
doi: https://doi.org/10.1007/s10654-023-00996-4
open original: https://pmc.ncbi.nlm.nih.gov/articles/PMC10164006/
license: CC BY 4.0; paraphrase and independently derived examples only
target_key: (theory,doi:10.1007/s10654-023-00996-4,version-of-record-2023-04-12,noncausal-targets-and-measurement-error)
status: PARTIAL (bounded original full-text sections and selected equations, no full typeset PDF formula audit)
ci: NOT_RUN
billing: no paid resources invoked; account billing NOT_RUN

## Original reading and new question

Read the open publisher-version HTML: Abstract, Introduction, Motivating example, A model for the change-score, Possible target parameters, A model for measurement errors, Estimation and bias (opening equations), and Discussion. Original printed pages 501–509; precise page-to-paragraph mapping and remaining bias expressions/Appendix are not fully verified against the typeset PDF.

The paper explicitly studies noncausal prediction/association, which is a separate target from the causal estimands debated by Tennant and Glymour. Let P be a covariate, U0 and U1 true baseline and follow-up, and Delta U = U1-U0. In its equal residual-variance Gaussian linear model, U0=a0+b0 P+eps0, U1=a1+b1 P+eps1, Corr(eps0,eps1)=r. The unadjusted predictive coefficient is betaP=b1-b0. Conditioning on the true baseline yields betaP*=b1-b0*r. Both are meaningful for different information sets. Their difference is b0(1-r), and either coefficient may be zero while the other is nonzero.

For example, b0=b1=2 and r=0.5 give betaP=0 and betaP*=1. This is a constructed algebraic example, not human or historical evidence. It demonstrates a conditional association can exist even if the marginal change association vanishes; it does not imply a causal effect of P.

The original measurement model is T0=c0+d0 U0+e0, T1=c1+d1 U1+e1, with measurement-error variance sigma^2 and error correlation rho. The original reports observed unadjusted gammaP=b1*d1-b0*d0, and baseline-adjusted gammaP*=b1*d1-b0*d0*(sigma^2*rho+d0*d1*s^2*r)/(sigma^2+d0^2*s^2). The observed marginal association can therefore differ from the true target betaP when measurement scaling differs across time.

Independent constructed check of the special case b0=b1=b, d0=d1=1, r=1, rho=0: gammaP=0, gammaP*=b*sigma^2/(sigma^2+s^2). With b=2, sigma^2=1, s^2=3, observed baseline-adjusted coefficient is 0.5 although the true marginal and conditional coefficients are both zero. This is a population-model algebra check, not a simulation or empirical verification. The source identifies this as a restrictive special case of prior measurement-error critiques, and extends to true change and systematic errors.

## Competing interpretation and limits

The article argues there is no universal rule favoring baseline adjustment or its omission in noncausal change-score studies. Prediction available with baseline information and prediction without it are distinct tasks. The paper recommends sensitivity analysis across plausible error parameters when systematic errors are possible. This does not settle Tennant/Glymour causal-effect disputes; those require a causal graph and target intervention.

Assumptions requiring scrutiny: linear conditional means, Gaussian equal-variance residuals, fixed error covariance structure, measurement calibration, and whether the future deployment actually observes baseline. Without validation or repeated measurements, latent measurement-error parameters can be unidentified. A strong conditional association can be a measurement artifact.

C candidate only: record observed P, T0, T1, measurement timing and calibration; predeclare whether baseline is available at prediction time, distinguish predictive target from causal intervention target, and specify reliability/error sensitivity bounds. A falsifiable empirical comparison would prospectively test calibrated predictive error in a held-out population for models with and without baseline. No personal data or product work, no C acceptance claim.

D W47: no new independent historical data or D acceptance claim. R scientific gates closed: 0. TH number created: 0. No R reruns.

## Unread / outstanding

Audit typeset original pages 505–509 and full Appendix bias expressions, compare competing measurement-error assumptions, and verify whether any previously archived related theory provides stronger conditions. The historical theory index is dated Nov 3 and is not exhaustive of newer files. No new human experiment, no independent historical replication, no CI. Frozen R073/PESEN v0.1 unchanged.

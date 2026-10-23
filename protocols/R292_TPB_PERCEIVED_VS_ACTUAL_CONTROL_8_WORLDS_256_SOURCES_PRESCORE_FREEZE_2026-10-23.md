# R292 preregistered finite artificial Theory of Planned Behavior (TPB) source freeze

Date 2026-10-23 Asia/Taipei. Original 239 catalogue ID **01-014**, P1. Scientific scope explicitly **bounded E1 artificial mechanisms, not human TPB validation**. Precedes all executable, output CSV and results commits. No human E2/historical E3, R073 and PESEN v0.1 frozen. Finish all R learning before taxonomy, then only later fusion.

## Original first-party anchor and distinction from R291 TRA

Ajzen, I. (1991), "The Theory of Planned Behavior," *Organizational Behavior and Human Decision Processes* 50(2):179–211, DOI https://doi.org/10.1016/0749-5978(91)90020-T; author's own publication page https://people.umass.edu/aizen/obhdp.html . Original 1991 paper and abstract frame attitude, subjective norm, and **perceived behavioral control** as antecedents of intention, with perceived control and intention predicting action depending on actual constraints. R291 01-013 concerns TRA and must not be retrospectively promoted to this distinct 01-014 candidate. Numerical coefficients, binary source distributions, feasibility gate and calibration regimes below are **our synthetic stress tests**, not from Ajzen's empirical sample. Perceived control C and actual feasibility F must remain separate variables, and observational prediction must not automatically be called identified causal influence or physical ability.

## Frozen full source generation: 8 worlds and 256 joint source cells

A (attitude), N (subjective norm), C (perceived control) are each in {-1,+1}, jointly independent fair binary. Intent I∈{0,1}; actual feasibility F∈{0,1}; observed action B=I*F deterministically. Four frozen intention-weight profiles (a,n,c):

* BALANCED = (1,1,1)
* CONTROL_HEAVY = (1,1,2)
* CONTROL_NULL = (1,1,0)
* NORM_HEAVY = (1,2,1)

Each profile crossed with control-calibration kappa∈{0,1}: UNINFORMATIVE (0), INFORMATIVE (1). Conditional probabilities are:
P(I=1|A,N,C)=1/2+(aA+nN+cC)/16;
P(F=1|C)=1/2+kappa*C/4;
I and F independent conditional A,N,C. F remains a distinct **unobserved actual opportunity/feasibility variable**, never conflated with C. For kappa=1, perceived C is a calibrated probabilistic proxy for F (P(F=1|C=-1)=1/4, P(F=1|C=1)=3/4), and for kappa=0 C contains no feasibility information. No coefficient or probability may be retrospectively tuned.

8 independent x 2^5 joint tuples (A,N,C,I,F) yield precisely **256 positive probability original source rows**, each recording B=I F, exact probability (1/8)*P(I|A,N,C)*P(F|C), true conditionals, four forecasts and labels. Every row has positive mass, complete world joint mass=1. All arithmetic Fraction, no random seeds, real persons or unbounded numerical sampling.

## Forecast information, control-omission counterexamples

All forecasts target B before observing I or F. The true full predictor:
Q_full(A,N,C)=P(I=1|A,N,C)*P(F=1|C).
Restricted TRA_AN predictor marginalizes C exactly:
Q_TRA(A,N)=1/4+(aA+nN)/32+c*kappa/64.
CONTROL_ONLY predictor marginalizes A,N:
Q_C(C)=(1/2+c*C/16)*(1/2+kappa*C/4).
CONSTANT forecast mu=1/4+c*kappa/64.

All expected Brier risks sum over 32 source rows per world. Define V_AN=(a²+n²)/1024, V_C=(4*kappa+c)²/1024, CROSS=kappa²*(a²+n²)/4096 and MU=mu(1−mu). Freeze analytic formula independent of enumeration:
R_constant=MU;
R_TRA=MU−V_AN;
R_control=MU−V_C;
R_full=MU−V_AN−V_C−CROSS.
Thus omitting C from an A,N-only model incurs exactly R_TRA−R_full=V_C+CROSS.

Negative control: CONTROL_NULL+UNINFORMATIVE has c=kappa=0 and omitting C incurs zero exact Brier loss. CONTROL_NULL+INFORMATIVE has c=0,kappa=1 and omission loss 1/64+(a²+n²)/4096>0, even though perceived control never enters intention. For fixed I=1, P(B=1|I=1,C=1)−P(B=1|I=1,C=-1)=kappa/2; fixed I=0, action B=0 always. This separates a synthetic control-as-intention input from a synthetic control-as-informative-proxy-for-opportunity. It does **not** prove the observed PBC score is actual ability, no instrument exists here, and kappa=1 is assigned by model.

Independent third auditor must parse exported original 256-cell CSV, reconstruct 32 tuples per world and probability factors without importing model; check strict B=I F, all per-world masses, exact forecasts, risk formulas, source/result SHA256 and adversarial tampering. No comparisons to R291 outcomes as though human predictive validation, and do not claim TPB real-world calibration.

## Scope/acceptance gates

Deliver executable >=Python3.11 --test/--emit, 256 original source CSV, eight full result world records, source/result SHA256, independent source audit, scientific report, machine acceptance only after observed successful GitHub Actions 3 jobs (Python3.11/3.12 and independent auditor). Then make one-row 239 original-catalogue v0.5→v0.6 evidence amendment (01-014 only); next queue reduces from 57 to 56, retaining older scoped evidence intact. Original 239 itself unchanged. E2=E3=0, overall original 239 scientific completion still NOT_ESTABLISHED. R073/PESEN v0.1 remain frozen.

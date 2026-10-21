# R157 Precode Freeze | Structural demographic pressure factorization and bounded lag responses

Date: 2026-10-21. Original catalog P2 / 06-015 Structural Demographic Theory. Parent main HEAD d026bab1b0a5d0fa3d118e62c083f59e131de490. R156 CLOSED_BOUNDED_E1.

## Primary source boundary, scientific interpretation
Peter Turchin (2013), "Modeling Social Pressures Toward Political Instability", *Cliodynamics* 4(2):241–280. DOI 10.21237/C7clio4221333, [original 40-page university-hosted article PDF](https://escholarship.org/content/qt6qp8x28p/qt6qp8x28p_noSplash_c3d0ac79e973d3c6029f872002050fcd.pdf); printed pp.241–247 directly read, especially printed p.246 multiplicative Political Stress Indicator Psi = MMP * EMP * SFD and population/elite/state separation. Author notes sources of structural pressure are not direct timings of unpredictable triggering events. Goldstone (1991) *Revolution and Rebellion in the Early Modern World*, University of California Press [author's bibliography](https://jackgoldstone.schar.gmu.edu/books/) and publisher bibliographic entry [University of California Press on Google Books](https://books.google.com/books?id=z8CXngEACAAJ) checked, but book full text NOT read. Turchin (2003) *Historical Dynamics: Why States Rise and Fall*, Princeton University Press [original book page](https://peterturchin.com/books/historical-dynamics/) and [Princeton/Oxford contents](https://academic.oup.com/princeton-scholarship-online/book/18842), chapter 7 "The Demographic-Structural Theory"; book full text not read.

Full Turchin (2013) original author empirical US case-study dataset, historic source tables, code and calibrated equations not reconstructed. The three-state dynamic below is **project-authored**, expressly NOT Turchin/Goldstone's original causal dynamic equation. Its component labels correspond only schematically to population stress (M), elite stress (E), fiscal stress (F); units are arbitrary artificial fractions in [0,1]. The product Psi=M*E*F parallels the source's conceptual index arithmetic but uses NONE of the published historical proxy definitions, scales, regressions, or observed political violence. This stage is E1 only. Never claim real event probabilities, actual political instability, ethnic/racial/political group traits, prediction or validation.

## Before execution: 72 scenario factorial and full ledger
Time t=0...12 (13 observations). Initial artificial pressures M_0=E_0=F_0=0. Exogenous permanent synthetic mass-pressure target H in {1/4, 1/2, 1}. Three lag coefficients a,b,c independently in {1/4,1/2}. Artificial fiscal buffering factor r in {0,1/2,1}. Exactly 3*2*2*2*3=72 distinct worlds.

Synthetic direct simultaneous recurrences:
M[t+1]=(1-a)M[t]+a H;
E[t+1]=(1-b)E[t]+b M[t];
F[t+1]=(1-c)F[t]+c (1-r) E[t].

All coefficients and states are nonnegative fractions; no exogenous instability-event variable. Record M,E,F, author's *schematic* multiplicative PSI=M*E*F, and **alternative diagnostic** additive mean Q=(M+E+F)/3 at every point. Explicitly distinguish Q from published PSI. At these artificial units, PSI is bounded by 1, and the product zero when any artificial factor zero. Holding all other inputs fixed, increasing fiscal buffering r cannot increase F or Psi, while M and E remain unchanged. This is a property of the imposed recurrence only.

## Independent exact path reconstruction
For each scenario, do not call direct recurrence from the checker. Use an independently coded affine matrix-power expansion:
x[t] = sum_{k=0}^{t-1} A^k b, with x=(M,E,F)^T,
A=[[1-a,0,0],[b,1-b,0],[0,c*(1-r),1-c]] and b=[a*H,0,0].
Compute with pure Fraction matrix-vector and matrix-matrix products, including t=0 identity and explicit powers. Must match all three state entries and PSI/Q in all 72*13 timestamps by strict Fraction equality; at least 72 uniquely named full-path unittest methods.

## Predeclared negative/interpretation controls
1. Exact sequential onset with H>0 and a,b,c>0, r<1: t=1 M>0 E=F=0; t=2 E>0 F=0; t=3 F>0. Thus "no initial PSI" is a product behavior, not a claim of absence of any societal strain.
2. r=1 forces F=0 and PSI=0 for the entire path despite growing M,E. A zero product cannot be treated as literal certainty of political peace.
3. Compare H=1,a=1/4 and H=1/2,a=1/2 with equal b=1/4,c=1/4,r=0: same complete t=1 measured vector (1/4,0,0) but distinct M2 (7/16 vs 3/8), so one-time observation does not identify forcing and adaptation speed.
4. Aggregation ranking reversal with constructed vectors A=(1,1,0) and B=(1/2,1/2,1/2): Q(A)=2/3 > Q(B)=1/2, Psi(A)=0 < Psi(B)=1/8. Product and mean are distinct research questions; do not select retrospectively on real outcomes.
5. Artificial steady asymptotes for H>0 are M*=H,E*=H,F*=(1-r)H. No finite-t equality to these limits required. In all 72 paths, 0<=M,E,F<=1 and PSI<=1.
6. Counterfactual buffering r=0 versus r=1/2 versus r=1 with other settings held fixed: M,E histories exactly unchanged, F/Psi nonincreasing with r at all times.
7. Validate source PSI algebra and monotonicity in each nonnegative factor, reject negative weights, inputs outside [0,1], booleans and non-Fraction/non-integer coercions, wrong dimension, negative t.

## Acceptance
Original precode freeze must be committed to GitHub main first. Program and separate authentic unittest source must be committed; all 72 full 13-point histories as UTF-8 deterministic JSON, with full schema and explicit E1 caveat. Run CI under Python 3.11 and Python 3.12, compare all four SHA256 of source, tests, full JSON and canonical deterministic ZIP; permanently submit JSON/ZIP to main and check commit/contents. Report math proof, source access, numerical/identity tests, and identify unavoidable validity gaps. Success is CLOSED_BOUNDED_E1 only: original author historical data or future-event prediction not supported. R073 and PESEN v0.1 remain FROZEN. Next original catalog is R158 P2 / 06-016 Conflict Event Process Models, if and only if R157 closure gate passes.

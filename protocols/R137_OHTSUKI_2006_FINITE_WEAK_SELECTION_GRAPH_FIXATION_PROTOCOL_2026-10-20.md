# R137 network reciprocity finite-size calculation protocol, frozen before GitHub CI
Date: 2026-10-20. Catalogue P1 05-013 Network Reciprocity.

## Scientific sources and separation
Primary: Ohtsuki, Hauert, Lieberman & Nowak (2006), Nature 441:502-505, DOI 10.1038/nature04605. Secondary primary theory: Chen et al. (2016), *Fixation Probabilities for Any Configuration of Two Strategies on Regular Graphs*, Sci Rep 6:39181, DOI 10.1038/srep39181, specifically its finite-N formula attributed to Taylor, Day and Wild (2007): b/c > k(N-2)/(N-2k) on bi-transitive regular graphs for death-birth weak selection. Different from R119-R125 diffusion/consensus/random network topology; these studies do not compute evolutionary fixation from donation games.

Scope of present independent implementation: fixed undirected unweighted and simple graph, N fixed with no mutation, one cooperator at uniformly random vertex, cooperation cost c per neighbour and benefit b per cooperator neighbour, payoff(C at i)= b*(number of C neighbours)-c*(degree), payoff(D at i)=b*(number of C neighbours). Fitness=1+w*payoff; exact selection gradient d rho_C(w)/dw at w=0, comparing rho_C(w) to neutrality 1/N. Three update rules precisely defined:
DB: random death then neighbour selected proportional to pre-event fitness;
BD: global parent proportional to fitness then replaces random neighbour;
IM: uniformly random focal samples itself or a neighbour proportional to fitness and copies its strategy.
Keep fitness evaluation at pre-event state. Do not use reproductive weight after deleting the target.
Graphs frozen for exact enumeration: simple cycles C5,C6,C7,C8,C9 (k=2), and complete graph K4 (k=3).
Main end points: neutral fixation 1/N, exact w=0 derivative, b/c threshold when derivative slope >0, exact finite-strength w=1/10000 counterchecks, full automorphism state-orbit reduction (not approximate). For cycles compare DB threshold exactly to 2(N-2)/(N-4); source 2006 b/c>k applies to large N with weak selection and cannot be applied to C5 as exact threshold. This protocol codifies completed exploratory code before remote CI and before any final acceptance; it must not be mislabeled frozen before all exploratory programming.

Specific results of preliminary code to be challenged in remote replay: DB cycles (N,threshold)=(5,6),(6,4),(7,10/3),(8,3),(9,14/5); IM cycles N7 threshold22,N8 threshold13,N9 threshold10; no positive weak selection benefit slope for BD over selected examples. Treat IM numbers as exact finite toy outcomes with explicit mechanism and no claim they derive from 2006 large N direct rule. Exact finite probability test where C6 b=3 / b=5 have opposite relation to 1/6 for w=1/10000.

For all selected examples: p0 transition stochastic, sum(dp/dw)=0, orbit reduction check, no floats in analytical math, cross-check finite w by independent explicit positive fitness transition solver. Inputs disconnected/nonregular invalid for fixation-gradient contract.
Unpublished author simulation not rerun. No real human E2, no historical E3. Never infer observed real-world social cooperation. R073 and PESEN v0.1 frozen. Complete all scheduled R first, then unified classification and fusion.

Acceptance: Python stdlib source+tests in immutable SHA256 ZIP; actual passing GitHub Actions jobs (3.11,3.12) with separate source file checks and declared numerical checks required before CLOSED_BOUNDED.
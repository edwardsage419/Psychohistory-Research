# R169 prescore protocol freeze | small adaptive culture-network Markov process

Date: 2026-10-21 (Asia/Taipei). Original candidate P2/07-011 Coevolving Networks. Predecessor: R168 CLOSED_BOUNDED_E1; E2 real trial-level source access remains blocked. This protocol must be committed to main **before** creating any R169 program or test file.

## Primary sources and author-model boundary

* Holme and Newman (2006), *Nonequilibrium phase transition in the coevolution of networks and opinions*, Phys. Rev. E 74, 056108, DOI https://doi.org/10.1103/PhysRevE.74.056108; original APS abstract and author manuscript arXiv:physics/0603023. Combines network rewiring toward same-opinion nodes with contact-mediated opinion change. Its original update rule selects a node and neighbor, not necessarily an active discordant edge; parameterization differs from our specification.
* Vázquez, Eguíluz and San Miguel (2008), *Generic absorbing transition in coevolution dynamics*, Phys. Rev. Lett. 100, 108702, DOI https://doi.org/10.1103/PhysRevLett.100.108702; original APS abstract and author arXiv:0710.4910: an edge joining opposite-state nodes is rewired with probability p, otherwise an endpoint changes state. Reports mean-field critical p_c=(mu-2)/(mu-1), NOT universally valid for small finite graphs.
* Gross and Blasius (2008), *Adaptive coevolutionary networks: a review*, J. R. Soc. Interface 5:259-271, DOI https://doi.org/10.1098/rsif.2007.1229; original open access PMC2405905.

R169 is a **new project-authored finite exactly enumerated n=4 labeled-graph experiment** grounded in the above conceptual distinction. It is **not** a direct recreation of either author's exact network topology distribution, original stochastic selection timing, infinite-network critical exponent or real human interactions. No source human network data or original author simulation output are used. Evidence level E1 exclusively.

## Frozen design

N=4 labeled persons {0,1,2,3}, undirected loop-free graph with no parallel edges, binary abstract A/B opinion per person.

Four source graph templates:
* path: edges [(0,1),(1,2),(2,3)]
* star: edges [(0,1),(0,2),(0,3)]
* cycle: edges [(0,1),(1,2),(2,3),(0,3)]
* chord: edges [(0,1),(1,2),(2,3),(0,2)]

Three frozen initial opinion vectors:
* block (0,0,1,1)
* alternate (0,1,0,1)
* singleton (0,0,0,1)

Three rewiring probabilities alpha={0,1/2,1}, two rewiring eligible-target rules target_mode={'same','any'}. Total **4×3×3×2=72 factorial worlds**, each a *full distribution over labeled (adjacency, node-state) pairs* for t=0,1,2,3 (three Markov transitions). No Monte Carlo sampling or floating-point calculation.

## Event clock and no-op semantics (all preregistered)

At one time step:
1. If the current graph has zero **discordant edges** (endpoints with different opinions), no event occurs; it is absorbing for the current rule.
2. Otherwise choose one discordant undirected edge uniformly.
3. Choose its **oriented anchor endpoint i uniformly** from the two choices and other end j.
4. With probability (1−alpha), anchor **adopts j's opinion**. Only one node-state changes, graph unchanged.
5. With probability alpha, sever the undirected (i,j) edge and choose a new node k uniformly among vertices k≠i that are not already neighbors of i **in the original graph**, with k≠j also required. The eligible set is filtered to opinion(k)=opinion(i) for target_mode='same' or unfiltered for 'any'. If set is nonempty add (i,k); otherwise it is a **true no-op** (preserves graph and opinions; the rewiring branch probability is not reassigned to adoption).
6. Each successful rewiring preserves edge count, with no new loops/multiedges. 'same' successful rewiring always removes exactly one discordant edge and adds an agreeing edge, whereas 'any' may replace with a discordant or agreeing link.

This active-edge-selected event clock is a bounded project variant and must not be silently described as the exact Holme-Newman timing convention.

## Two independent exact rational approaches

Oracle A: direct enumeration of discordant edges, uniformly selected orientation, and conditional alpha adoption/rewire branches, collecting exact Fraction probabilities into canonical state-key map. Recursively propagate through three steps.

Oracle B: independently enumerate the **oriented active-edge** sample space of length 2d, then enumerate an explicit categorical branch for (adoption, rewiring), and after any eligible rewiring enumerate all uniformly sampled target nodes. Do not call oracle A or import its event generator. Independently aggregate and propagate into the same canonical labeled state IDs. Strict Fraction equality required for all 72×4 **complete state distributions**, not just metrics. Verify probabilities sum to one exactly; check every supported successor valid and edge-count preserving for rewiring, and every path state within original graph edge-count bound.

## Frozen controls and inferences to test

1. alpha=0: **all** graph topologies are unchanged along every sampled branch; only opinions can change. target_mode cannot affect the entire path.
2. alpha=1: **all** opinion vectors are unchanged along every sampled branch; only graph topology can change. For the full two-mode data, identify any worlds showing different distributions under 'same' versus 'any'.
3. If no discordant edge, the whole state is absorbing for all alpha and modes.
4. If anchor has no eligible nonneighbor, chosen rewiring branch is a no-op; there is no rejected-edge redraw or implicit adoption.
5. In homophilic successful rewiring, number of discordant edges decreases by exactly 1; otherwise it remains when no-op. Thus at alpha=1 and mode='same', discordant-edge count on *every realized path* is nonincreasing.
6. Edge count stays invariant under all controls, including state adoption. All new edge endpoints canonical and valid.
7. A-count stays fixed at alpha=1; for alpha=0 at least one frozen world permits a different future A-count.
8. Different opinion-network graphs may have the same aggregate A-count and edge count but distinct discordance, component count, and future transition law. Prove using at least one counterexample drawn from the 72 frozen worlds.
9. For a fixed initial world, p=0 versus p=1 should change whether opinions can update versus edges can rewire. Demonstrate both branch types with positive probabilities on at least one initial configuration.
10. No measured personal attitudes, causal polarisation, psychological homophily, thermodynamic phase transition or parameter estimation. E2/E3=0, and R073/PESEN v0.1 frozen.

## Acceptance

>=72 uniquely named world tests, >=25 distinct deterministic negative/control/identity tests, full original exact JSON, deterministic source/test/JSON ZIP with four pinned SHA256. Execute both Python 3.11 and 3.12 CI and independent archive replay; archive full JSON and ZIP permanently to main, verify Git blob and acceptance report. Scientific closure only CLOSED_BOUNDED_E1. Next original catalog R170 must be verified, not guessed. Continue original R list, then classify, then fuse.

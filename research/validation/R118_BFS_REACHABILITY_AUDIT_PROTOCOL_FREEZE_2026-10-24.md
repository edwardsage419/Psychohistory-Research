# R118 independent reachable-state audit: prospective protocol freeze

Date: 2026-10-24. Repository main observed at `f496b393a24afd6c6b6e3db7ad4868d8a45eb67e`.
Catalogue: original239 03-019 Threshold Participation. Existing R118 is reusable and must remain unchanged.
Original primary source: Mark Granovetter (1978), *Threshold Models of Collective Behavior*, AJS 83(6), 1420-1443, DOI 10.1086/226707. Original source interpretation and original R118 limitations remain controlling.
Original R118 source blob SHA1 `438288bef99455ba9087988baf10eec09139ffe1`; original test blob SHA1 `c81b8fd6dfbb7802d7f1652c838ce4a9eb21a552`.
Existing R118 CI reference: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39248405444.

## Predeclared falsifiable tests

1. Independently enumerate all possible participant subsets as bit masks and all admissible one-person transitions. An inactive actor i can join a state S only when threshold_i <= |S|. Breadth-first search begins from the empty set. The independent audit must never call R118's sorted, synchronous, or CDF solvers to construct its own reachable-state result.
2. For every ordered integer threshold vector of n=1,2,3,4, the number of vectors must be (n+1)^n = 2,9,64,625; total 700. The maximal reachable participant count must match the existing R118 synchronous result for all 700 vectors. The independently reachable-state graph must contain the empty state, never remove a participant, and have no reachable transition after its maximal fixed point. The audit must fail closed on disagreement.
3. The two 100-person frozen examples must give (100,1) for original threshold chain versus one-person alteration, and (100,1) with exact equal threshold sums 4950 for the separately constructed two-person compensated alteration. These 100-person checks may use the original solver only as a comparison, since exhaustive subset search is limited to n<=4.
4. Negative controls: (1,1) must have no reachable nonempty subset from zero even though all-active is a static self-consistent configuration; (0,2,2) must have exactly one participant reachable. The audit must explicitly distinguish zero-seed reachable closure from arbitrary initial states and equilibria.
5. Mutation rejection: independently perturb the expected outcome of a (0,1,2) chain, and perturb the input threshold of a (0,1,2) chain into (0,2,2). Both must be detected as changed predictions. Verify SHA1 of original source and tests via Git blob identity, and SHA256 in the executing environment. Re-run existing 44 unit tests.
6. Produce a deterministic JSON audit receipt and a scoped scientific report. Run under Python 3.11 and 3.12 on standard public ubuntu-latest GitHub runners if the public-repository free-runner rule and workflow contents are confirmed. An independent audit job must execute the BFS script. Any failure keeps original239 link PENDING.

## Scientific limitations and grading

Max acceptance: `PASS_BOUNDED_INTERNAL_INDEPENDENT_REACHABILITY_E1`. The 700 vectors are mathematical enumerations, not independent humans. This internal method audit is distinct from an external researcher replication. No human E2 sample-out prediction, calibration, empirical confidence interval, causal estimate, or historical E3 is created. The algorithm assumes a complete global crowd, irreversible binary action, deterministic fixed thresholds, and zero initial seeds. These assumptions exclude neighborhood-specific diffusion, strategic exit, endogenous threshold learning and multiple initial-state equilibria. R073 and PESEN v0.1 are frozen. No taxonomy, model fusion, product work, paid services or Chinese-language sources.

## Evidence gates

A new audit file and workflow must be created at previously absent paths; original R118 and prior audit artifacts must remain untouched. After CI success, only then may the catalogue 03-019 link be upgraded. Check the actual main HEAD and path identities immediately before each write; reject any concurrent-path conflict. Do not represent directory acceptance as new empirical validity.

# R315 finite exact Watts Strogatz model: scientific report

Date 2026-10-24 Asia/Taipei. Original239 catalogue **04-017 Watts Strogatz Small World**, original P1. Scope **bounded mathematical E1 on synthetic graph states** only.

## Primary paper and frozen protocol

Watts, Duncan J., and Steven H. Strogatz (1998), *Collective dynamics of ‘small-world’ networks*, *Nature* 393:440–442, DOI https://doi.org/10.1038/30918 . Paper's regular ring rewiring is tested via a deliberately tiny, strictly specified early-edge variant. Protocol [R315 prescore freeze](../../protocols/R315_WATTS_STROGATZ_TWO_CLOCKWISE_EDGES_210_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed **before calculating** any results at `7cbbc7785a411d7d535536c028c3c051edf71e28`.

For N=8 and 10, start an undirected regular ring with neighbors at clockwise offsets 1 and 2, average degree four. Rewire just two initial clockwise *nearest-neighbor* edges in order, (0,1) then (1,2), at p∈{0,1/2,1}. A rewired edge picks a uniformly random node currently not connected to its active endpoint, excludes the old target and self, keeps active degree and E constant, and changes the old and new destination degrees by −1,+1. This finite convention is explicit; full original network sweeping and other endpoint reselection conventions are out of scope.

## Complete finite event enumeration and testable observations

The conditional first-stage branches number 4 (N8) and 6 (N10). Second stage has 4/5 or 6/7 choices respectively, depending on whether the prior edge was rewired. Full source census: **210 potential edge event atoms** and **180 ordered two-event paths** (19 per p when N=8, 41 per p when N=10). Every conditional branch mass and each (N,p) two-event path distribution equals 1, computed exactly with `Fraction`. Zero-probability counterfactual event rows remain archived to preserve complete frozen support.

Baseline N=8 network: C=1/2, average shortest path L=10/7. Baseline N=10: C=1/2, L=5/3. Each baseline has one connected component. The clustering coefficient averages neighbor-induced triangle density, while L averages shortest path over *all unordered node pairs* only when connected; if disconnected the metric is `null`, with component count reported. This prevents overstating connectivity or quietly averaging reachable nodes alone.

Under p=0, only the retain/retain path has positive probability and the final graph equals the baseline. Under p=1, paths containing a keep event have probability zero. Rewiring preserves undirected simple edge count, may redistribute degrees, and cannot support universal single-edge monotonicity of either C or L. The data enumerate two early edge decisions in small networks and should **never** be described as a full Watts–Strogatz randomized network ensemble, evidence for a realistic small world at intermediate p, a social network forecast, or empirical replication of the Nature paper's N=1000 findings.

## Reproducibility and limits

* Full [210-source CSV](R315_ALL_210_ORIGINAL_REWIRING_ATOMS.csv) records N,p,event stage,prefix event, source edge, rewire destination, exact selection chance and pre/post-edge graph.
* [180 graph-path JSON](R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json) records source choices, exact joint probability, complete final edge graph and computed C,L,components.
* [Main exact implementation](r315_exact_small_world.py) contains 34 unit tests run under Python 3.11 and 3.12; [independent no-import auditor](../catalogue_audit/independent_r315_source_audit.py) independently reconstructs all 210 atoms and 180 paths, plus C,L via Floyd Warshall instead of primary BFS.
* [GitHub live scientific CI 39995420565](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39995420565) verified **3/3 jobs completed success**: Python 3.11 34 tests, Python 3.12 34 tests, independent graph replay and full archive.
* Formal bounded E1 acceptance is written only after this verified run. New true human E2=0, historical E3=0; R073 and PESEN v0.1 remain frozen. Original239 catalogue linking should change **only 04-017**, next candidate 04-019 SBM after index verification.

# R310 Voter Model — exact stochastic neighbor copying and topology-sensitive martingales

Original239 P1 item **04-008**. Foundational Clifford & Sudbury(1973) https://doi.org/10.1093/biomet/60.3.581; Holley & Liggett(1975) https://doi.org/10.1214/aop/1176996306; heterogeneous graphs Sood et al.(2008) https://doi.org/10.1103/PhysRevE.77.041121. R310 examines a **frozen project-specified four-node one-step copying toy**, not real elections.

Path4, Cycle4, Complete4 undirected networks and all16 binary configurations produce **48 artificial worlds and 416 fully labeled directed update source rows**. Asynchronous voter update selects target uniformly among4, neighbor uniformly at target, copies neighbor's opinion. Complete source probabilities are Fraction exact. **Degree-weighted binary density is one-step expectation-conserved on all three undirected graphs**, but plain fraction need not be conserved on irregular PATH4. For state(1,0,0,0), PATH4 expected next plain=7/32 instead of initial1/4; degree weighted remains1/6; regular graphs retain plain1/4. This is about fictitious states, not human opinions.

* [Original frozen protocol 782990a1](https://github.com/edwardsage419/Psychohistory-Research/commit/782990a1cae101a3c0fd5ba37f89dc8ed9c2078c) / [full protocol](../../protocols/R310_VOTER_MODEL_THREE_GRAPH_416_DIRECTIONAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md)
* [Exact model code and1262 actual tests](r310_exact_four_node_voter_model.py)
* [All416 complete original source CSV](R310_ALL_416_ORIGINAL_VOTER_DIRECTED_UPDATE_SOURCES.csv)
* [All48 full worlds and exact source results](R310_EXACT_NETWORK_VOTER_MODEL_RESULTS.json)
* [SHA256 source/results receipt](R310_MACHINE_RECEIPT.json)
* [No-import full independent directed graph auditor and17 adversarial tests](../catalogue_audit/independent_r310_source_audit.py)
* [Full scientific report including failed first auditor and corrected CI](R310_SCIENTIFIC_REPORT_2026-10-23.md)
* [Machine-scoped acceptance](R310_FINAL_ACCEPTANCE_STATUS.json)

First [run39955723523](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955723523) failed on independent audit of CYCLE4 edge **serialization order**, corrected at [commit17a14103](https://github.com/edwardsage419/Psychohistory-Research/commit/17a14103c9f01f1b774883de77df831f759c7792) without altering protocol or math. Fresh [run39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344) **all three jobs success**. Full original sources archived main [commit2dc71bae](https://github.com/edwardsage419/Psychohistory-Research/commit/2dc71bae2a70dd3affc892e33712d0541822525b).

E1-only: no real citizens, ballots, human E2, historical E3, long-term consensus estimates, calibrated voter network or social forecast. Prior R309 SIR distinct. R073/PESEN v0.1 still frozen.

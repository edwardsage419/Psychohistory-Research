# R312 Deffuant–Weisbuch Model — exact asynchronous pairwise compromise E1

Original239 candidate **04-013**, P1. First-party Deffuant, Neau, Amblard, Weisbuch (2000), *Mixing beliefs among interacting agents*, https://doi.org/10.1142/S0219525900000078. Related Lorenz (2007) bounded confidence survey https://doi.org/10.1142/S0129183107011789.

**One selected unordered dyad per artificial step, NOT HK synchronized all-neighbor averaging, nor full Deffuant long-term stochastic dynamics.** Eight explicit four-agent opinion profiles ×3 thresholds {0,1/2,1} ×2 compromise strengths {1/4,1/2} = **48 artificial worlds**, each six equiprobable unordered encounters, **288 original pair events and 1152 complete fictional person-source rows**.

Conditional pair update xi←xi+μ(xj−xi), xj←xj+μ(xi−xj), permitted iff |xi−xj|≤epsilon. Each event preserves total group mean, while choice order matters over successive pairs. On profile F=(0,1/2,1,1), epsilon1/mu1/2: encounters (0,1)→(1,2) produce (1/4,5/8,5/8,1) but reversed order produces (3/8,3/8,3/4,1). On profile C, distance1 blocks (0,3) at epsilon1/2, while distance1/2 permits (1,2). No real persons or opinion survey sampled.

* [Prospective frozen protocol, commit2c8c9bfd](https://github.com/edwardsage419/Psychohistory-Research/commit/2c8c9bfd15a27574f0fffb02517eb5893aedfee9)
* [Full protocol](../../protocols/R312_DEFFUANT_RANDOM_DYAD_ONE_STEP_1152_PERSON_SOURCES_PRESCORE_FREEZE_2026-10-23.md)
* [Full source mathematical model and 3469 real tests](r312_exact_deffuant_dyadic_update.py)
* [All original 1152 artificial person-source rows](R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv)
* [All 48 worlds and 288 pair events with all four agents](R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json)
* [Source/result SHA256](R312_MACHINE_RECEIPT.json)
* [Independent no-import midpoint/shrink audit, 15 tamper tests](../catalogue_audit/independent_r312_source_audit.py)
* [Complete scoped scientific report](R312_SCIENTIFIC_REPORT_2026-10-23.md)
* [Final machine-scoped E1 acceptance](R312_FINAL_ACCEPTANCE_STATUS.json)

GitHub Actions [run39957585074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957585074) 3/3 success, original CSV+JSON+SHA permanently archived main [commit53052edb](https://github.com/edwardsage419/Psychohistory-Research/commit/53052edbe7a1f87a476f7c9297db5a961095667d).

Related previous [R311 confidence relation geometry](../R311/R311_SCIENTIFIC_REPORT_2026-10-23.md) and [R066 HK dynamics/conditional human village E2](../R066/R066_FINAL_ACCEPTANCE_STATUS.json) stay independent. No new real human E2, animal E2 or historical E3. R073/PESEN v0.1 remain frozen.

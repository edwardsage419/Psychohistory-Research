# R332 scientific report: finite task resource allocation and artificial recoding

Date 2026-10-24. Original239 02-015 Cognitive Resource Constraints. Formal grade **PASS_BOUNDED_E1_CONSTRUCTED_THREE_TASK_RESOURCE_ALLOCATION_ONLY**.

## English primary reference and strict reuse check
Miller (1956), *The Magical Number Seven, Plus or Minus Two*, *Psychological Review* 63:81-97, https://doi.org/10.1037/h0043158, primary full text https://www.yorku.ca/pclassic/Miller/, discusses capacity limits and recoding. This project uses invented task units and makes no universal seven-slot capacity claim. R260 hard-budget robustness constrains shock uncertainty rather than task processing; R259 multiobjective costs have no processing-capacity variable; R330 cue-recency retrieval and R295 habit acquisition also lack the frozen task-subset mechanism. No strict source-level equivalent verified. Early ZIP itemwise audit remains open.

## Protocol, source universe and exact solver
The falsifiable protocol was frozen in [5dde3f2d](https://github.com/edwardsage419/Psychohistory-Research/commit/5dde3f2dab6bf09d51542de57e58fc962d02fd56) before executable source and data commit [7a164a94](https://github.com/edwardsage419/Psychohistory-Research/commit/7a164a941b9fda3c529be37a5fa0bf80a8661f7d). All 112 original artificial source records enumerate eight binary subsets of three tasks at each of seven capacities and two recoding settings. Tasks A,B,C have fixed artificial costs 1,2,3 and utilities 1,3,4. Recoding reduces B cost from 2 to 1 and changes no other parameter. Each capacity c from 0 to 6 admits subsets with total cost <=c. Among feasible subsets choose maximum utility and lexicographically smallest bitstring in a tie. Fourteen world summaries store all winner and tie counts.

## Frozen exact results
Without recoding, optimal utilities at capacities 0..6 are (0,1,3,4,5,7,8). With recoding they are (0,3,4,4,7,8,8). Gains are (0,2,1,0,2,1,0). At capacity 4 the selected subset changes from 101 (A+C, utility5) to 011 (B+C, utility7). At capacity 3 the chosen subset is 001 (C, utility4) in both settings, because lexicographic tie breaking selects it over 110 (A+B) when recoded. Recoding does not reduce the constructed optimum in any capacity world. The numbers follow entirely from assigned task costs and utility; no human cognitive measurement or learned strategy is inferred.

## Reproducibility, audit and CI
Python standard-library code generates and byte-replays all CSV and JSON artifacts. Seven unit tests cover counts, both utility sequences, recoding gains, frozen counterexamples, feasible maxima and capacity monotonicity, and byte replay. Independent no-import auditor re-enumerates all 112 source rows and 14 summaries, including tie counts, and rejects deliberate CSV tampering. [GitHub Actions run 40041585075](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40041585075) completed success, with Python 3.11, Python 3.12 and independent audit jobs all successful.

## Scientific limits
E1 is a bounded mathematical resource allocation exercise. Resource costs, recoding effect and utility are project-defined. No human working-memory span, attention interference, learning of chunks, Miller experiment reproduction, human E2, historical E3, causal inference or external prediction is established. The catalogue link is provenance only. R073 and PESEN v0.1 remain frozen. Complete the R series before classification and fusion; personal decision system remains deferred.

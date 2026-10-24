# R344 scientific report: finite two-type A-B-A meta-path similarity

Date: 2026-10-24. Original239 **04-024 Heterogeneous Network Models**. Grade **PASS_BOUNDED_E1_CONSTRUCTED_TWO_TYPE_METAPATH_SIMILARITY_ONLY**.

## Sources and strict reuse
Sun et al. (2011), *PathSim: Meta Path-Based Top-K Similarity Search in Heterogeneous Information Networks*, *Proceedings of the VLDB Endowment* 4(11):992–1003, DOI 10.14778/3402707.3402736. Sun and Han (2013), *Mining Heterogeneous Information Networks*, *SIGKDD Explorations* 14(2):20–28, DOI 10.1145/2481244.2481248. [Preaudit](../../docs/ORIGINAL_239_04-024_HETEROGENEOUS_NETWORK_REUSE_PREAUDIT_2026-10-24.md) checks R316 fixed-block SBM, R343 multiplex projection and R341 ERGM. Early ZIP member-level strict reuse remains OPEN.

## Frozen protocol and exact results
[Prescore protocol](../../protocols/R344_HETEROGENEOUS_METAPATH_64_ARTIFICIAL_PAIR_ATOMS_PRESCORE_FREEZE_2026-10-24.md) committed at [000b7043](https://github.com/edwardsage419/Psychohistory-Research/commit/000b70435a2e1f65a1826af3fe604862be1f0c60), before [source commit 0eb0967f](https://github.com/edwardsage419/Psychohistory-Research/commit/0eb0967f693a17c6bb29154f78042220692e5c5b).

Two type-A and two type-B nodes, four binary bipartite incidence positions. Exhaustive 16 artificial networks, 64 ordered A-to-A source atoms. The A-B-A path count N_ij is the number of shared B-neighbors. PathSim-style score is 2*N_ij/(N_ii+N_jj), with zero for a zero denominator.

| Frozen falsifier | Exact result | Status |
|---|---:|---|
| F1: networks and source atoms | 16 / 64 | PASS |
| F2: path count and PathSim symmetry | 16 / 16 | PASS |
| F3: strictly positive off-diagonal similarity | 7 / 16 | PASS |
| F4: PathSim within [0,1] and correct diagonal | 16 / 16 | PASS |
| F5: swapping B labels leaves similarity unchanged | 16 / 16 | PASS |
| F6: 1010 and 0101 distinct networks, same A-B-A path counts | PASS | PASS |
| F7: independent byte replay, two tamper rejections | PASS | PASS |
| F8: Python 3.11, 3.12, independent CI | 3 success | PASS |
| F9: protocol before source, R073/PESEN unchanged | PASS | PASS |

The collision witness proves that this specific meta-path projection cannot identify B-node labels. It does not establish human similarity judgments, network embeddings or original PathSim empirical ranking performance.

## CI and provenance
[GitHub Actions run 40063860148](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40063860148) concluded success. Jobs python311, python312 and independent all success. Eight unit tests per interpreter. The independent enumerator reconstructs exact CSV and JSON bytes without importing production and rejects two deliberate tampering controls.

Protocol blob 311508f8c83a54459b6030f990ac94cd72588e78. Source blob d119907b968606da49308bf85c0cb4ac83dfff4d. Results blob 557e5251b7b56101bf2976fd34ed8130277bbf0b. Production blob b2457224923b2e68d14c79b0c36a7d82b0cdfb93. Independent blob c95121dbdd49536515d78cce7447c5e400027147.

## Scientific limits
Human E2: NOT_ESTABLISHED. Historical E3: NOT_ESTABLISHED. Original-author empirical replication: NOT_ESTABLISHED. No causal inference or large-scale heterogeneous network model validation. Catalogue association tracks provenance only. Early ZIP strict reuse OPEN. R073 and PESEN v0.1 frozen. Remaining 173 provisional links require itemwise audit before any classification or fusion. Personal decision system deferred.

# R340 scientific report: finite exact two-node SIS generator

Date: 2026-10-24. Original239 **04-007 SIS Epidemic Model**. Formal scientific grade **PASS_BOUNDED_E1_CONSTRUCTED_TWO_NODE_SIS_GENERATOR_ONLY**.

## Sources and reuse
Pastor-Satorras and Vespignani (2001), *Epidemic Spreading in Scale-Free Networks*, *Physical Review Letters* 86, 3200–3203, DOI 10.1103/PhysRevLett.86.3200. Van Mieghem (2011), *The N-intertwined SIS epidemic network model*, *Computing* 93, 147–169, DOI 10.1007/s00607-011-0155-y. Both are original non-Chinese sources. [Preaudit](../../docs/ORIGINAL_239_04-007_SIS_EPIDEMIC_REUSE_PREAUDIT_2026-10-24.md) checked R314, R316, R317 and indexed source search. Earlier binary ZIP itemwise reuse remains OPEN.

## Frozen protocol and artificial source
[Prescore revision 2](../../protocols/R340_SIS_TWO_NODE_48_ARTIFICIAL_GENERATOR_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed at [86c0d5fc](https://github.com/edwardsage419/Psychohistory-Research/commit/86c0d5fc0a371ecd804f4ee92d6d83f665f0755d) before the first R340 source commit [bf4547ee](https://github.com/edwardsage419/Psychohistory-Research/commit/bf4547eeb7a070a0b04fc14e1f25d114c12c17d8).

Two undirected adjacent nodes; states 00, 01, 10, 11. Recovery gamma=1, infection beta per infected neighbor, beta=1/2,1,2. The generator Q contains 48 complete artificial rate atoms across three exact matrices.

| Frozen falsifier | Exact result | Status |
|---|---|---|
| F1: worlds, states, source atoms | 3, 4, 48 | PASS |
| F2: all-healthy 00 absorbing | 3 of 3 | PASS |
| F3: single-infected and doubly-infected transitions | 6 and 3 checks | PASS |
| F4: zero-sum rows, nonnegative off-diagonal entries | 12 and 36 | PASS |
| F5: infection next-event probability from 01 | 1/3, 1/2, 2/3 | PASS |
| F5: recovery next-event probability from 01 | 2/3, 1/2, 1/3 | PASS |
| F6: frozen checks dictionary | exact | PASS |
| F7: independent no-import byte replay and two tamper controls | PASS | PASS |
| F8: Python 3.11, Python 3.12, independent audit | 3 successful jobs | PASS |
| F9: source follows prescore protocol; R073/PESEN unchanged | PASS | PASS |

The state 00 is absorbing because the construction contains no spontaneous infection. This small finite generator has no nonzero stationary endemic state. The first-event probabilities follow directly from competing exponential rates.

## Reproduction and provenance
Run `python research/R340/r340_sis_generator.py --test --audit` and `python research/catalogue_audit/independent_r340_sis_audit.py`. The independent program does not import production code and reconstructs exact CSV and JSON bytes.

[GitHub Actions run 40063363405](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40063363405) concluded success. Jobs python311, python312, independent each concluded success. Production has seven unit tests per interpreter. Independent auditor checks two deliberate tampering controls.

Protocol blob 334f0ebcf5cad782538f4cc705d82ff81f7c8249. CSV blob 36ae0a9a11d2f27dacd8948f9617122eade0c40c. JSON blob e5615c6d99bd79acac5501bda60976b3f7d3cad2. Production blob 7bd287300825266be1a13fc12229b8c48b01e7a7. Independent audit blob 7e780d30cdc6bb7fc3f1d4aabb6fb6b47fa98dca.

## Scientific limitations
These are investigator-constructed transition rates. No fitted infection data, human E2, historical E3, author empirical replication, large-scale scale-free epidemic threshold, persistence, or endemic prevalence is established. Directory association only tracks provenance. Early R001–R064 ZIP full content audit remains open. R073 and PESEN v0.1 frozen. Complete R-series evidence audit before classification and model fusion. Personal decision system deferred.

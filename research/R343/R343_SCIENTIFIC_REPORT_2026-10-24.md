# R343 scientific report: finite two-layer multiplex projection

Date: 2026-10-24. Original239 **04-023 Multiplex Networks**. Grade **PASS_BOUNDED_E1_CONSTRUCTED_TWO_LAYER_PROJECTION_ONLY**.

## Sources and strict reuse
Kivelä et al. (2014), *Multilayer networks*, *Journal of Complex Networks* 2:203–271, DOI 10.1093/comnet/cnu016. Boccaletti et al. (2014), *The structure and dynamics of multilayer networks*, *Physics Reports* 544:1–122, DOI 10.1016/j.physrep.2014.07.001. [Preaudit](../../docs/ORIGINAL_239_04-023_MULTIPLEX_REUSE_PREAUDIT_2026-10-24.md) checks R316, R317, R341 and R342 for strict two-layer identity reuse. Early ZIP member-level reuse remains OPEN.

## Frozen protocol and exact results
[Prescore protocol](../../protocols/R343_MULTIPLEX_TWO_LAYER_192_ARTIFICIAL_EDGE_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed at [85d72f14](https://github.com/edwardsage419/Psychohistory-Research/commit/85d72f14c9b386aa7ba5331d4497e6673f714773), before [source commit e9f696c0](https://github.com/edwardsage419/Psychohistory-Research/commit/e9f696c084e22c5c715d8d46d3734b97e5485856).

Two labeled undirected layers on the same three nodes, three edge positions per layer. Exhaustive 8 by 8 layer-pair universe, 64 artificial configurations, 192 complete edge atoms. Union and intersection are computed exactly edge by edge.

| Frozen falsifier | Exact result | Status |
|---|---:|---|
| F1: worlds and source atoms | 64 / 192 | PASS |
| F2: exact OR and AND bit rules | 192 / 192 | PASS |
| F3: unique union graphs | 8 | PASS |
| F3: complete union preimages | 27 | PASS |
| F3: empty union preimages | 1 | PASS |
| F4: complete union and empty intersection preimages | 8 | PASS |
| F5: layer swap preserves both projections | 64 / 64 | PASS |
| F6: frozen output format and checks | exact | PASS |
| F7: independent byte replay, two tamper rejections | PASS | PASS |
| F8: Python 3.11, 3.12, independent jobs | 3 success | PASS |
| F9: protocol before source, frozen assets unchanged | PASS | PASS |

Twenty-seven different layer-pair assignments share the same complete aggregate union graph. Eight of those have no overlapping edges. This is exact information loss under the investigator-defined projection, with no claim about actual multiplex network behavior.

## CI and provenance
[GitHub Actions run 40063743843](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40063743843) concluded success, with python311, python312 and independent all success. Six unit tests per production interpreter. The independent no-import bitmask enumerator reconstructs exact CSV and JSON bytes and rejects two deliberate tampering cases.

Protocol blob 5d83af607dc078ed661432f6c9c0ecdcab4461f5. Source blob 69270f49c0f2cefa1d65e41b5f4e6307ee91306d. Results blob 88f823d68c4b83e364b7ba39d842248756b1f800. Production blob 95cf64699ec624a22c3ba95fde27d0c8c45c79f7. Independent auditor blob 9260dc97c273a8fb9604f09f1ca458da8b1d3f04.

## Scientific boundaries
No observed multilayer social network, dynamical spreading, behavioral inference, human E2, historical E3 or original-author empirical replication. Catalogue association is provenance only. Early ZIP strict reuse OPEN. R073 and PESEN v0.1 frozen. Finish R series and itemwise evidence audits before classification and fusion. Personal decision system deferred.

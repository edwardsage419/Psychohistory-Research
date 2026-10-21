# R171 PRE-SCORE FREEZE: real Austronesian Phlorest tree integrity and exact language distances

Date: 2026-10-21. Original catalog P2 / 07-013 Cultural Phylogenetics. This freeze precedes any R171 analysis code. This study analyzes a **precomputed original-derived historical linguistic tree**, not synthetic human-like leaves.

## Primary archival dataset and scientific attribution

Russell D. Gray, Alexei J. Drummond and Simon J. Greenhill (2009), *Language phylogenies reveal expansion pulses and pauses in Pacific settlement*, Science 323(5913):479–483, DOI https://doi.org/10.1126/science.1166858 (PubMed PMID 19164742). Source-specific machine-readable derived dataset in [Phlorest gray_et_al2009](https://github.com/phlorest/gray_et_al2009), licensed CC-BY-4.0; cite original paper AND derivative dataset/commit. Data are already inferred from published 2009 linguistic observations and calibrations; no historical hypothesis should be falsely considered independent.

**Immutable source input at original Git commit** `a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5`:
* `cldf/summary.trees`, Git blob SHA1 `89139751991c9f5753d249baeb9230061db93a4d`, 10954 original bytes (a valid NEXUS text header was seen); graph branch unit `millennia` according to CLDF TreeTable. The original tree has a single `tree summary = [&R] (...);` statement, but `Tree_Is_Rooted` in `trees.csv` is empty; record this metadata inconsistency and do not assume an alternative root.
* `cldf/languages.csv`, Git blob SHA1 `3e48ef314a10d9684af6a47279e7a8df54b45f5a`, 23461 original bytes by Git API; ID is the tree-label join key. The UTF-8 decoded string length is **not** the raw-byte size; verify raw byte count after download.
* `cldf/trees.csv`, Git blob SHA1 `b4626d14b127b8197fb68c569016f53d033969e3`, 65932 original bytes; only the `summary` row is relevant. Read its Tree_Branch_Length_Unit and rooted field, preserve exact source in the archive.
* `cldf/Generic-metadata.json`, Git blob SHA1 `4be59bc5d99841796c04ba20bc98538d9c8e06f4`, 15415 original bytes, provides CLDF crosswalk. Archive exact bytes and schema.
All source requests must use URLs pinned to the immutable commit and allowlisted raw.githubusercontent.com host; check each actual `git hash-object` blob ID before parsing; fail, don't silently fallback to branch main. Store original source bytes separately under `research/R171/source/` with an attribution note. The published Phlorest README requests citing the DOI of the particular dataset release; no versioned Zenodo DOI is inferred from the above commit.

## Real-tree structural tests

Implement two **independent** Newick/NEXUS parsers:
- A: recursive descent on punctuation/newick tokens.
- B: character-scanned iterative stack reduction, independently recovering topology, terminal strings, Decimal edge lengths, polytomies and root.
Compare a canonical root-aware nested tuple representation including every original leaf name and branch length for exact equality; do **not** resolve polytomies or reroot the tree automatically. Reject malformed punctuation, duplicate terminal labels, illegal/negative/non-finite lengths, extra unrecognized statements and root-mode issues; log zero-length edge count instead of treating zero as an error.
- Extract exactly one tree and parse explicit `[&R]` marker. Record blank `Tree_Is_Rooted` as an unfilled CSV metadata cell even if NEXUS marker is rooted.
- Reconcile all tip IDs against CLDF `languages.csv` ID column; compute unique tip count, source language row count, shared count, tree-only IDs, language-only IDs, and provenance of any mismatches. Root and language-table membership is **not** historical correctness evidence.
- Structural summary: leaf/internal counts, total branch count, root degree, number and maximum degree of polytomies, root-to-tip branch-length minimum/maximum/median (Decimal exact), total branch length, zero/positive edge counts, and proof connectivity/no cycles.

## Two independently calculated distance routes

For the complete original tree calculate exact Decimal pairwise patristic distances among all distinct original tip IDs (allow zero-length edges). Route 1 uses parent pointers and rooted lowest-common-ancestor ancestor walks; route 2 makes an undirected weighted tree and runs independent depth-first path enumeration from each tip, never using route 1. Compare all ordered pairs for exact Decimal equality, symmetry, zero diagonal and triangle inequality for frozen distinct triples (not an empirical truth claim). Export **complete all-pair distances** in sorted-tip rows to `R171_ALL_PAIR_PATRISTIC_DISTANCES.csv`, preserve this CSV in the deterministic source/tests/results ZIP and include its exact SHA256 in full results JSON. Recompute a hash of canonical CSV in CI. O(n²) comparisons acceptable for ~400 published tips.

Preselected source-tip pairs for human-readable exact direct distances, without choosing after observing scores:
* SquliqAtayal / CiuliAtayal
* SquliqAtayal / Sediq
* Saisiat / Pazeh
* Pazeh / Thao
* Bali / Sasak
* MalayBahasaIndonesia / Melayu
* Kanakanabu / Saaroa
* Rukai / Tsou
* OldChinese / Buyang

If a pair is absent, record it **as absence**, not substitute a better-fitting pair. The pairwise distances are descriptive numbers on an **already fitted original tree**. Do not interpret time-calibrated patristic distances directly as independently measured divergence dates, and do not claim the geographic settlement conclusions or independent model likelihood reproduced.

## Admission/acceptance gates

1. Source bytes must match all four fixed Git blobs from the original commit; original input hashes recorded, original tree and language table permanently archived.
2. Both parsers agree exactly on all labeled topology and Decimal lengths; tree complete and valid; taxon join reconciliation and root/cell mismatch documented.
3. Both complete pairwise distance implementations match without tolerance; full pairwise matrix CSV and JSON summary reproducible across Python3.11 and 3.12.
4. A minimum of 60+ individually meaningful unittest methods: source hashes/schema, all source example pairs and tree edge/topology checks, independent parse/geometry tests, malformed input rejection, local source-to-join audits, and all-pair matrix recomputation equality. Tests may reuse actual verified source, not create fake human outcomes.
5. Deterministic original source/code/tests/JSON/CSV ZIP, all permanent archive files and SHA256 pinned in final dual-Python CI and independent archive job, GitHub main readback.
6. Research closure **CLOSED_BOUNDED_E1_SOURCE_DESCRIPTIVE_REAL_TREE** only; historical language tree already estimated by original authors. New independently held-out human-data E2=0; new independent external historical E3=0. R073 and PESEN v0.1 remain FROZEN.

R172 candidate must be checked against original catalog only once R171 acceptance finalized. Original R-series completion, then classification, then fusion.

# R171 scientific report: real published 400-tip Austronesian-language phylogeny provenance and exact full-distance audit

**Date:** 2026-10-21. **Original R catalog:** P2 / 07-013 Cultural Phylogenetics. **Outcome: CLOSED_BOUNDED_E1_SOURCE_DESCRIPTIVE_REAL_TREE.** Unlike prior R169–R170 artificial worlds, R171 reads and verifies **genuine already-inferred published source language-tree files**. It does not independently infer the language tree, recover actual historical language ancestry, score held-out modern linguistic traits, test population migration scenarios or replicate the original 2009 Bayesian phylogenetic fit. E2=0, E3=0.

## 1. Verifiable primary sources and exact original version

Original publication: Russell D. Gray, Alexei J. Drummond and Simon J. Greenhill (2009), [*Language phylogenies reveal expansion pulses and pauses in Pacific settlement*](https://doi.org/10.1126/science.1166858), *Science* 323(5913):479–483, [PubMed PMID19164742](https://pubmed.ncbi.nlm.nih.gov/19164742). The paper used lexical data on 400 languages and Bayesian phylogenetic methods to examine historical Pacific settlement. Its specific calibrated origin date, settlement phases and sensitivity checks are **not** reconstructed by R171.

Real published derivative dataset: [Phlorest `gray_et_al2009`](https://github.com/phlorest/gray_et_al2009) under **CC-BY-4.0**; [Phlorest overall Zenodo DOI](https://doi.org/10.5281/zenodo.8250067). Source is pinned to an immutable Git commit **`a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5`**. The Phlorest README requires citation of the original paper and the specific release DOI for the dataset version; the exact versioned release DOI is **not confirmed**, so the archive identifies the commit precisely and does not invent a dataset-version citation.

Full original files were **actually downloaded byte-for-byte and archived on main** through GitHub Actions. Their SHA1 values are original Git blob identities independently recalculated on the retrieved bytes; all four full raw files have matching expected sizes:
* `source/summary.trees`: **10,954 bytes**, SHA1 `89139751991c9f5753d249baeb9230061db93a4d`, SHA256 `d25f5f72e62ec480f196b84b7c17b838f4e253287a9cfbc588a8a27605f078e2`.
* `source/languages.csv`: **23,461 bytes**, SHA1 `3e48ef314a10d9684af6a47279e7a8df54b45f5a`, SHA256 `8736b406918f3d4fcac2077e73c0da0096e1983cba20ec2aa26c8cdea69a4db7`.
* `source/trees.csv`: **65,932 bytes**, SHA1 `b4626d14b127b8197fb68c569016f53d033969e3`, SHA256 `840b28101a915dfae4483e3738dc9a07cac365914ad91938ebad1d84306175cf`.
* `source/Generic-metadata.json`: **15,415 bytes**, SHA1 `4be59bc5d99841796c04ba20bc98538d9c8e06f4`, SHA256 `53f11dbaff8cb16b45c6010f21c30a8e3e138de5d96aa8a1718ab8a8b9886f76`.

Source download uses only `raw.githubusercontent.com` URLs explicitly pinned to that commit and rejects mismatching bytes. The files are included as literal original bytes in the [full reproducibility ZIP](R171_Real_Austronesian_Full_Tree_103_Tests.zip), alongside their separate archive paths.

## 2. Pre-registered source-tree structure audit

The [protocol was committed before any R171 implementation](../../protocols/R171_REAL_PHYLOREST_AUSTRONESIAN_TREE_FULL_DISTANCES_PRESCORE_FREEZE_2026-10-21.md), [commit ecdfbd7](https://github.com/edwardsage419/Psychohistory-Research/commit/ecdfbd7b5530b20b92fd2ce7b31c4d0ea2844da8).

The actual original NEXUS tree begins with `#NEXUS`, its single tree is named `summary`, and it has an explicit `[&R]` rooted marker. The companion CLDF `trees.csv` **leaves the `Tree_Is_Rooted` cell blank**; the source metadata thus omits an explicit CSV truth value even though the NEXUS itself includes an annotated rooted tree. We preserve rather than fabricate a replacement CLDF value. The companion tree row reports **branch-length unit 'millennia'**. The tree is an *already dated posterior summary*, with calibration and uncertain original fitting assumptions outside this analysis.

Two independently programmed NEXUS/Newick parsers, one recursive-token-based and one character-scanned stack-based, produced identical nested labeled topology and **every Decimal edge length exactly**, with no automatic rerooting or binary resolution of polytomies. Verified original structure:

| Quantity | Exact source-tree result |
|---|---:|
| Distinct tree tips / language-table rows | **400 / 400** |
| Exact tip-to-CLDF-ID matches | **400** |
| Tree-only / table-only labels | **0 / 0** |
| Total tree nodes | **756** |
| Nonroot branches | **755** |
| Internal nodes | **356** |
| Polytomous nodes, degree greater than 2 | **26** |
| Maximum number of children of one node | **8** |
| Zero-length edges | **52** |
| Sum of all source-tree branch lengths | **525.658981 millennia** |
| Minimum / median / maximum root-to-tip distance | **1.733214 / 4.633214 / 4.633215 millennia** |

The 400 labels are original source language entries, some of which are *outgroup taxa* or historically attested language varieties, not 400 independent contemporary interviews. Zero-length edges can place distinct names at zero tree patristic distance, without showing the languages are identical. The unequal root-to-tip depths are documented; forcing uniform terminal dates or binary branchings would modify the original source. **The summed branch lengths and root-tip distances are properties of an inferred dated tree, not independently measured chronological language separation dates.** The 2009 original abstract's migration-related timeline is not recalibrated here.

## 3. Every one of 79,800 real-source pair distances independently recomputed

For n=400 source tree tips there are exactly n(n−1)/2 = **79,800 unordered different-tip pairs**. Every distance is the sum of nonnegative original source branch lengths along the unique connecting tree path.

* Route A: direct index of rooted parent pointers and exact least common ancestor (LCA), computing `dist(root,a)+dist(root,b)−2*dist(root,LCA(a,b))`.
* Route B: independently creates an undirected weighted adjacency list and traverses the unique tree path from each original tip to every other tip, without calling the LCA algorithm.

All 79,800 distances **agree exactly as decimal arithmetic**; the exported [complete 2,292,699-byte original CSV](R171_ALL_PAIR_PATRISTIC_DISTANCES.csv) contains every actual original tip-name pair and its exact branch-length path distance in millennia. CSV SHA256: **`66ab2bb5645fcf86dfc91287c0886d2987470e2d65e457ce570106c02edf21ee`**.

Original-tree pair distance range: minimum **0.000000**, maximum **9.266429** (one most distant pair is ArakiSouthwestSanto and Buyang), mean **7.4006352335087719...** in millennia of summed tree edges. The positive numbers are patristic distances, **not** evidence that those real languages are separated by those exact amounts of calendar time; in rooted trees a pair's path includes both descendant branches and is not its node age.

Nine pair comparisons were explicitly frozen before analysis, all nine source names existed and were independently checked by both algorithms:

| Original linguistic tip names | Exact source-tree patristic distance (millennia) |
|---|---:|
| SquliqAtayal – CiuliAtayal | 2.644574 |
| SquliqAtayal – Sediq | 5.947138 |
| Saisiat – Pazeh | 5.992084 |
| Pazeh – Thao | 5.992084 |
| Bali – Sasak | 3.795798 |
| MalayBahasaIndonesia – Melayu | 0.344650 |
| Kanakanabu – Saaroa | 0.010696 |
| Rukai – Tsou | 3.471426 |
| OldChinese – Buyang | 6.345432 |

These are not language similarity tests against external observations. Any statement that a historical migration scenario was verified from these distance comparisons would re-use the *authors' fitted historical tree as its own ground truth* and would be circular. Original scholarly debate about Bayesian priors, contact/borrowing, rootedness and calibration is a separate scientific question.

## 4. Full original CI and source-archive provenance

[Original Python source](r171_real_phylogeny_exact.py), [103 different actual unittest methods](test_r171_real_phylogeny_exact.py). Tests include independent parser/graph calculations, original CLDF source hash/metadata validation, taxon crosswalk, every frozen pair, 33 original language-tip existence checks, exact complete matrix reproduction and dozens of corrupted tree/branch-length/CSV inputs.

* Initial dual-environment [GitHub Actions run39542653422](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39542653422): **success**. Python 3.11 and 3.12 independently downloaded and authenticated the four original sources, compared all 79,800 pairs, executed 103 actual tests each, 0 failed; original source/test/JSON/CSV/ZIP hashes identical.
* Pinned [GitHub Actions run39542768099](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39542768099): **success**. Both environments again executed 103 tests and verified five identical SHA256; the third independent archival job119034091747 independently downloaded all four original source files, recomputed full CSV/JSON, reran 103 tests, rebuilt the deterministic ZIP, checked every hash, then **permanently committed the exact original 4 CLDF files, matrix, JSON and ZIP** to main at [commit c181afd](https://github.com/edwardsage419/Psychohistory-Research/commit/c181afddf9863da320ed0ef7ec348234ca9a7b2d).
* Combined five real executions of 103 tests = **515 total unittest executions, 103 distinct methods, zero failures**. The final archive run logged a nonfatal Python ResourceWarning for one test's file iterator not being explicitly closed; this is a test-harness cleanup item, **not** a mathematical discrepancy or a failed test. All computed source identities and results are unchanged.

Five deterministic project-generated file SHA256:
* source code `04c204fb99e3ecd6a2a920fb1938a760c53c199111255bcfc44c3746f30a0183`
* tests `4b6b36c5bb561a6be198399e93f735d0380ff411e61366a8095525595445eadb`
* complete results JSON `65c18ba18eb50d4a977fbfdd02b29ba6b81e72f0b4578374f3cbb61899052f11`
* all-pair CSV `66ab2bb5645fcf86dfc91287c0886d2987470e2d65e457ce570106c02edf21ee`
* [complete source/tests/data archive ZIP](R171_Real_Austronesian_Full_Tree_103_Tests.zip) `f96399cd16915d7a6e90cefcb995692bd0c91beaa6b7cfb7b0250db0cd8a4765`.

An independent audit with Git clone and the permanently archived `research/R171/source` files needs only Python standard library:
`cd research/R171 && python r171_real_phylogeny_exact.py > R171_EXACT_RESULTS.json && python -m unittest -q test_r171_real_phylogeny_exact.py`. The all-pair CSV is deterministically regenerated. To explicitly fetch from the original unmodified commit before testing, `python r171_real_phylogeny_exact.py --fetch-sources`; this downloads original bytes only from the pinned original commit.

## Evidence grading and next stage

**Formal acceptance: CLOSED_BOUNDED_E1_SOURCE_DESCRIPTIVE_REAL_TREE.** This is a verified original-language-data **source integrity and mathematical transform result**, not E2 real independent behavioral prediction, not E3 genuinely held-out historical prediction, and not exact original author Bayesian posterior replication. New E2=0 and E3=0; R073 and PESEN v0.1 remain frozen.

Next original catalog **R172 P1 / 07-014 Historical Event History Models**. A valid R172 should involve event or adoption dates and competing survival/event-history models with explicit censoring and risk sets, ideally original real historical observations. An artificial curve should not be treated as a new historical event prediction. Finish original R series before unified categorization and subsequent fusion.

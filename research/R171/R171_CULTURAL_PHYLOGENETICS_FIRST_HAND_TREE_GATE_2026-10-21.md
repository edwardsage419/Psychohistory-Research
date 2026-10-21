# R171 first-hand data gate | Cultural Phylogenetics

Date 2026-10-21. Original frozen catalog **P2 / 07-013 Cultural Phylogenetics（文化亲缘与系统发育比较）**. R170 is CLOSED_BOUNDED_E1 and includes **no real language history evidence**. This document begins real original archival-tree discovery, but **R171 status remains SOURCE_AUDIT_ONLY**, not a prescored experiment or scientific closure.

## Primary literature and incompatible phylogenetic tasks

1. Gray and Atkinson (2003), [*Language-tree divergence times support the Anatolian theory of Indo-European origin*](https://doi.org/10.1038/nature02029), *Nature* 426:435–439. Original Nature article and PubMed PMID14647380 inspected. This original infers historical divergence under model-specific time calibrations; its stated hypothesis is contested, and it is not equivalent to a generic tree-distance computation.
2. Gray, Drummond and Greenhill (2009), [*Language phylogenies reveal expansion pulses and pauses in Pacific settlement*](https://doi.org/10.1126/science.1166858), *Science* 323(5913):479–483. The associated **original-source-derived Phlorest Austronesian phylogeny** is openly published by the Phlorest curators with a full documented CLDF representation; we separately verified the public [GitHub repository](https://github.com/phlorest/gray_et_al2009).
3. Pagel, Atkinson and Meade (2007), [*Frequency of word-use predicts rates of lexical evolution throughout Indo-European history*](https://doi.org/10.1038/nature06176), *Nature* 449:717–720. Original Nature source abstract inspected. Its data and model concern word-specific rate effects, not simply the existence of a reconstructed language tree.
4. Modern [D-PLACE source documentation](https://d-place.org/source) explicitly distinguishes **Glottolog taxonomic classification trees with no temporal branch-length meaning** from separately computed, often dated linguistic phylogenies, and notes that borrowing and language shift can break the equivalence of genealogy and cultural ancestry.

## Actual first-hand historical tree artifact available and verified by GitHub tools

Phlorest original derived data source: `phlorest/gray_et_al2009`, [data repository](https://github.com/phlorest/gray_et_al2009) (main branch), GitHub license **CC-BY-4.0**. The dataset README requires citation of both original Gray et al. 2009 Science paper and the **particular Phlorest release DOI/version**. The repository README currently references overall [Zenodo record DOI10.5281/zenodo.8250067](https://doi.org/10.5281/zenodo.8250067); it is a dataset-level source ID, **not yet a pinned version**.

GitHub recursive object tree confirms the original CLDF complete data files, without inventing any raw contents:
* `cldf/summary.trees`: actual readable #NEXUS tree, **10,954 original bytes**, Git blob SHA1 `89139751991c9f5753d249baeb9230061db93a4d`. The first 3 lines were read directly from the source main branch and include rooted `tree summary = [&R] (...)` and observed tip labels such as SquliqAtayal, CiuliAtayal, Sediq, Saisiat, etc., with decimal branch lengths. This is *a real tree artifact*, unlike arbitrary toy tip labels.
* `cldf/languages.csv`: 23,461 bytes, Git blob `3e48ef314a10d9684af6a47279e7a8df54b45f5a`.
* `cldf/trees.csv`: 65,932 bytes, Git blob `b4626d14b127b8197fb68c569016f53d033969e3`.
* `cldf/data.nex`: 13,793,308 bytes, Git blob `a2a188b7f778ebe5cb7b724e44ca43f0f3354b22`.
* `cldf/posterior.trees.zip`: 4,074,535 bytes, Git blob `8fcf11ce490deefad9b3700bdc3e048721a544ad`.

This is clear **source access to a published historical linguistic tree**, but **not yet** an independent E3 prediction or reproduction of the primary Bayesian inference. The complete posterior and character data are different files with independent provenance, and the language tree is *already fitted to language data*. Treating agreement with the same tree as independent evidence would be circular.

## Additional evolving aggregation and license caution

* [D-PLACE/dplace-data](https://github.com/D-PLACE/dplace-data) continues to publish source datasets with its **CC-BY-4.0** license.
* [D-PLACE/dplace-cldf](https://github.com/D-PLACE/dplace-cldf) is the current aggregator of cultural data and curated phylogenies. Its own README identifies a **CC-BY-NC-4.0 license** for the aggregated CLDF dataset, which is **not interchangeable with the CC-BY-4.0 licensed Phlorest source repo**. Preserve source-specific terms and the original author's citation; do not silently pool licensing.

## Exact next scientific audit gate before program design

1. Pin an immutable released **Phlorest gray_et_al2009 version/tag/commit**, inspect the root NEXUS syntax and CLDF mapping (tree IDs, taxa, branch length interpretation) and cite all source DOI/version identifiers.
2. Parse real summary tree with an independently checked NEXUS/Newick parser, validate no duplicate tip names, rooted/nonrooted consistency, branch length nonnegativity, hierarchy and taxon coverage against the CLDF languages table. Stop if original metadata names appear conflicting.
3. For a reproducible baseline, compute real-tree topological distances and branch-length patristic distances, exact tree/root sensitivity and language-label randomization contrasts, with a genuinely distinct independent implementation for tests. These would be **E1/E_source-descriptive calculations using real historical tree data**, not independent inference of the tree's correctness or causal reconstruction of migrations.
4. If later undertaking E3 historical external prediction, freeze an *independent* target/source dataset or later dated linguistic evidence not used to fit the tree; identify leakage and reticulate borrowing, and compare models. A train/test split of existing descendant tips against their published inferred source tree is not independent discovery.
5. Continue original R series with explicit acceptance, file identities and GitHub archive. R073/PESEN v0.1 remain frozen. Only after all R studies → uniform classification → model fusion.

**R171 has not formally concluded**: a real original tree's accessible Git blob is now verified, but no R171 data parsing or model scoring was run in this stage.

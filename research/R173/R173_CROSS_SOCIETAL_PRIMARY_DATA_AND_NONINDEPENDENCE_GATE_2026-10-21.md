# R173 original first-hand cross-societal comparison source and nonindependence gate

Date 2026-10-21. Original frozen catalog **P1 / 07-015 Cross Societal Comparison Models (跨社会比较模型)**, research purpose: differences in institutions and culture between societies. Prior R172 CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT.

This is **SOURCE_AUDIT_ONLY**. No correlation, causal model, heldout prediction, original anthropological conclusion or country/society inference is accepted for R173 yet.

## Primary publications and Galton's problem

* Murdock and White (1969), [*Standard Cross-Cultural Sample*](https://doi.org/10.2307/3772907), *Ethnology* 8(4):329 onward, original article defines a **186-society** designed sample intended to improve historical and diffusion independence versus uncontrolled ethnographic sampling. Its selection objective does **not guarantee independence**, and inclusion may bias estimates. The original SCCS source is not the same as a current D-PLACE dataset.
* Kathryn R. Kirby et al. (2016), [*D-PLACE: A Global Database of Cultural, Linguistic and Environmental Diversity*](https://doi.org/10.1371/journal.pone.0158391), *PLOS ONE* 11(7):e0158391, primary publisher open article. D-PLACE combines sources on 1400+ societies, spatial and phylogenetic links. The original article explicitly discusses shared cultural ancestry, spatial proximity and Galton's problem; observational correlations cannot be read as effects of a single institution or cultural tradition.
* Murdock's original Ethnographic Atlas variables were compiled over 1962–1971 and reworked in later coded releases; cultural focal observations are heterogeneous in date, source author, coding completeness and ethnolinguistic identity. Do not compare cultures as if all observed concurrently.

## Real first-hand source repository verified, permanently referencable commit

Original D-PLACE **dataset source** repo [D-PLACE/dplace-data](https://github.com/D-PLACE/dplace-data), default branch master, independently verified exact HEAD **9bfed2c8c206be00f55f71516f262bbca2234e5a**, repository license **CC-BY-4.0**. Citation instructions in its original README: cite Kirby et al. 2016 AND the underlying dataset original article(s), the precise D-PLACE version, and download date. Commit pins source content even if a release tag is not used.

Original **Ethnographic Atlas** files in the exact tree:
* datasets/EA/data.csv Git SHA1 **ca16bd039a0b0bc0b430e257b0f47cec53c05e8c**, 11,274,445 actual bytes (not yet downloaded in our run).
* datasets/EA/variables.csv Git SHA1 **badeb7299525b51190f740e1ce0bcbeba6c20856**, 29,887 bytes, read directly.
* datasets/EA/codes.csv Git SHA1 **0ac9eb7863f90f8e3c0ed33ea506ca491cd212d1**, 76,781 bytes, read directly.
* datasets/EA/societies.csv Git SHA1 **9a7e3ff625c7c9e2fb879cd914747c98cfc75888**, 162,348 bytes.
* datasets/EA/societies_mapping.csv Git SHA1 **31d34ee88fae59789a3cff6bf9625d09daef9555**, 22,352 bytes. Original README describes 1,291 EA societies (may differ from number of original coded rows, which remains to be checked).

Original **Standard Cross-Cultural Sample (SCCS)** derivative:
* datasets/SCCS/README.md Git SHA1 **74f52d4b30df53699750f338c26d4f1074efb161**, confirms selected **186 societies** and warns cultural variables were compiled across multiple independent articles.
* datasets/SCCS/societies_mapping.csv Git SHA1 **21281b89a015911c9d1dd1198b6618b82cc6bc8c**, 7,725 bytes, mapping source identifiers back to EA. Separate EA societies_mapping.csv has exactly 186 strings referencing an SCCS record; this is an **observed mapping text count**, not yet verified as a clean one-to-one matched statistical sample.
* SCCS/data.csv Git SHA1 **f12d284ca410a17e9a4789b2a8c6a8dc76fa70a7**, 25,983,817 bytes; full file is not yet downloaded.
* datasets/SCCS/variables.csv Git SHA1 **92743fcbd1c0acedc2f04af0c5175883b68a690e**, 536,633 bytes. SCCS and EA variable IDs need not be equivalent; no code may implicitly merge similarly numbered columns.

A different repository [D-PLACE/dplace-cldf](https://github.com/D-PLACE/dplace-cldf), default master HEAD d82fbb6e955d3b33317b80ddc49455fe8a8b1b68, states **CC-BY-NC-4.0** in its original README. This differs from CC-BY-4.0 on dplace-data. Do not silently substitute aggregated CLDF data under different terms.

## Real source variable definitions checked, no effect reported

The EA variable CSV directly lists:
* EA003 fishing dependence (ordinal coded 0–9, 'NA' explicit missing).
* EA005 agriculture dependence (ordinal coded 0–9, 'NA' explicit missing).
* EA006 predominant marriage transaction category (categorical, original codes 1–7 with explicit source labels, 'NA' missing), including bride-wealth, bride-service, token bride-wealth, gift exchange, other exchange, little/no consideration and dowry.

EA003 and EA005 share a subsistence-composition denominator, so **negative associations could arise mechanically**; they should not be the headline independent cross-cultural prediction. A possible distinct comparison is EA005 versus EA006, but this is **not preregistered here**, because actual coverage and matching have not yet been audited. The EA geographic/focal-year fields and glottocode IDs from societies.csv must be carried through and missing/ambiguous entries cannot be imputed without a protocol.

## Next strict scientific gate

1. Retrieve complete original D-PLACE EA data.csv, variables.csv, codes.csv, societies.csv and both EA/SCCS mapping files via **the immutable source commit only**; verify every raw byte's original SHA1 Git blob hash. Confirm source data.csv header, actual row grain (society, variable, code, possible source year) and absence of duplicated society-variable conflicts.
2. Build a semantically explicit EA–SCCS mapping table, document any one-to-many/fuzzy matches and do not force exact 186 coverage where source identifiers disagree.
3. Before computing any association, freeze the two cultural variable IDs, eligible source codes, temporal sampling window if possible, exclusion thresholds, missingness accounting, exact primary statistic, society-level permutation/bootstrap unit, and a stratified/family-spatial sensitivity design. Avoid posthoc favorable variable pair selection.
4. Distinguish unadjusted descriptive association, design/sample-composition sensitivity, language family/geospatial shared ancestry and causal conclusions. The SCCS selection was designed to improve independence; it is not a random experimental treatment.
5. Source descriptive arithmetic on real ethnographic data is not E2 independent real-human repeated-game prediction, nor genuinely external historical E3. R073 and PESEN v0.1 remain frozen. Finish original R series, then uniform classification, lastly fuse.

**R173 status: SOURCE_AUDIT_ONLY** pending authenticated raw source and prescoring freeze.

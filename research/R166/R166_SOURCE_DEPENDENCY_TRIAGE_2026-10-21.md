# R166 source dependency triage | original P1/07-008 Cultural Selection Models

Date: 2026-10-21. This is an **early source audit checkpoint only**, research status **SOURCE_TRIAGE_NOT_STARTED**, no prescored mathematical model and no closure claim.

Original candidate catalog `docs/MODEL_CANDIDATE_CATALOG_v0.1.json` says:
* id 07-008; name Cultural Selection Models (文化选择模型); priority P1.
* earlier first-hand source ID R19.
* review state: representative literature and abstract previously located, without full original-author replication.

A recursive scan of GitHub main at `7617fe61031bf42588932030ccf718690f7249ba` confirms **one archived earlier research artifact actually exists** at:
`archives/library-originals/心理史学_R019_正式研究包_2026-10-14.zip`.

**The R019 ZIP contents were not opened or audited in the current turn.** Its presence proves repository archival existence only, not primary-source accuracy or model validation. Avoid reusing a prior R19 result as new R166 evidence without verifying the source and baseline.

R166 entry gate before selecting further computation:
1. Read the R019 archived package's manifest, primary-source identifiers and original proposed models, then audit its true E1/E2/E3 level and whether its experiments were previously executed.
2. Check the cited original publications or independently verifiable author implementations and raw datasets. Document accessible texts versus abstracts and unavailable code.
3. Explicitly compare R019 with already completed R159 (single trait cultural conformity), R161 (finite social copying), R164 (content salience) and R165 (neutral drift) to avoid recycling the same equations under a new title.
4. Freeze one distinctly testable cultural selection mechanism or empirical contrast before writing any R166 model, choose independent exact or data-based replication checks, and define a source-linked acceptance gate.
5. Keep the pre-agreed sequence: finish remaining original R models, then comprehensive classification, and only then fusion. Preserve R073 and PESEN v0.1 frozen.

**R166 has not yet passed an acceptance gate.** The next verified work target is R019 archive retrieval/inspection and original literature audit. This file records a dependency, not new research evidence.


## R019 package actually audited in GitHub Actions

2026-10-21 read-only CI run [39532579568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39532579568) successfully opened `archives/library-originals/心理史学_R019_正式研究包_2026-10-14.zip`. Archived ZIP SHA256 `080a786f4bd064494f8c57a7ec0cc32f183d2020e3eb643a0ea69881a721d797`, 12,946 bytes, 9 members. The actual package directory is `心理史学_R019_双网络先行理论审查_v0.1`. Its README, MANIFEST, NOVELTY_GATE, Python source and 17 test log prove it is about audience-pressure/information-influence dual networks and private-belief/public-statement gaps, based on Anufriev, Borissov and Pakhnin (2023/2026). It is **NOT a cultural-selection model**. Catalog 07-008's `first_hand_source_id=R19` is a **demonstrable incorrect source linkage**. Do not reinterpret R019 as culture-selection evidence or alter its original archived record. Preserve this erratum as separate provenance.

## Reassigned direct primary source and original code verification

Alex Mesoudi (2021), "Cultural selection and biased transformation: two dynamics of cultural evolution", *Philosophical Transactions of the Royal Society B*, 376:20200053, DOI [10.1098/rstb.2020.0053](https://doi.org/10.1098/rstb.2020.0053), the original open research review in [PMC8126458](https://pmc.ncbi.nlm.nih.gov/articles/PMC8126458/), provides conceptual distinction and discusses empirical non-identification when selection and transformation generate similar cultural patterns. Crucially the original **author published R code** exists at [amesoudi/culturalselection_biasedtransformation](https://github.com/amesoudi/culturalselection_biasedtransformation), and the `model1.R` source was read directly: its `philtrans_model1` function uses real-valued agent traits, probability `s` of copying the highest-value demonstrator rather than random copying, followed by exponentially modified Gaussian transformation `remg` and clipping to 0..100. The source code takes `Beta`, `Sigma`, `n`, `t_max`, and `r_max`, and is associated with the 2021 manuscript. We did not run original R scripts or reproduce their figures, which require R packages (`emg`, `ggplot2`, `viridis`) and stochastic seeds. Our future R166 model is a **new exact binary-state identification experiment**, distinctly separate from this original continuous model.

Supporting source: Claidière, Scott-Phillips and Sperber (2014), [How Darwinian is cultural evolution?](https://doi.org/10.1098/rstb.2013.0368), *Philosophical Transactions B* 369:20130368, original open research paper, warns that cultural attraction and transformation need not be reducible to a strict replicator-selection picture. Boyd and Richerson (1985), [original publisher contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html), explicitly separates direct bias, natural selection of cultural variants and guided variation.

Status: **R019 archived bytes inspected and catalog source-ID error confirmed**. This is a provenance finding, not E2/E3 new empirical evidence and not a scientific closure of R166.

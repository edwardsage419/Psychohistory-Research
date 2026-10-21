# R168 scientific report: finite cultural ratchet, sampling extrema, and an unresolved human group-size controversy

**Date:** 2026-10-21. **Original catalog:** P1 / 07-010 Cumulative Cultural Evolution. **Scientific completion:** CLOSED_BOUNDED_E1 only for the explicitly frozen, project-authored **64 synthetic three-skill-level Markov worlds**. Original Derex (2013) Figure 1–3 data access is blocked; **zero independent empirical human outcome rows were analyzed, E2=0 and E3=0**. Cumulative culture in real humans and the group-size causal interpretation remain contested and untested by this program.

## 1. Primary research and contested estimates

Derex, Beugin, Godelle and Raymond (2013), [original Nature Letter](https://doi.org/10.1038/nature12774), used a 15-trial dual-task computer game involving 2, 4, 8 and 16-person human groups, contrasting a comparatively simple arrowhead and complex fishing-net task. Its publisher page lists downloadable Figure 1/2/3 XLS source data and supplemental methods. This research does **not** possess the original Figure XLS files, participant choices, individual trial records, author analysis code, or task score data. The distinction between an available advertised link and actual possession of source bytes is part of the scientific record.

The article stimulated a substantive methodological disagreement:
* Andersson and Read (2014), [*Group size and cultural complexity*](https://doi.org/10.1038/nature13411), Nature 511:E1, [university-hosted author copy](https://escholarship.org/uc/item/55b8w391), argued that an increased probability of observing *at least one* complex technique in a larger group can arise from its greater number of independent opportunities, even if individual rates are not improved. Their reanalysis questions a direct interpretation that group size improves complexity.
* Derex et al. (2014), [*Derex et al. reply*](https://doi.org/10.1038/nature13412), Nature 511:E2, defended evidence on skill retention, performance and diversity while differentiating group-level and individual-level targets. In the publicly available response, reported individual complex-task-use tests include χ²(1)=2.53, P=0.11 for linear size and χ²(1)=2.15, P=0.14 for a quadratic effect; those specific individual-level tests are not significant at the 0.05 convention. Neither side can be declared to have definitively won all issues based on this project's access-limited materials.

The five-page Social Sciences Replication Project [Ho and Wu replication plan](https://doczz.net/doc/8923791/replication-report---social-sciences-replication-project) lists a planned 65-group first sample and extension to 155 groups if necessary, focusing on the group-level diversity statistic; **the viewed report's Results sections still say "[To be added when replication experiments have been completed.]"**. It is protocol evidence, not proof that replication ran or succeeded.

A distinct data lead, Derex, Feron, Godelle and Raymond (2015), [original open paper](https://doi.org/10.1098/rspb.2015.0719) and [Dryad dataset](https://doi.org/10.5061/dryad.1425c), was verified using the official public metadata API. The Dryad version 3512 reports a CC0 licensed original 687,002-byte XLSX, MD5 `9514d3a33e933466dcec92079e5ea897`, and README DOCX. **The actual 2015 XLSX bytes were not acquired**: file stream 403, API individual download 401, dataset ZIP 401. This is a different experiment from the Nature 2013 group-size trial and is never conflated with it.

The complete evidence/access/provenance record, including a corrected JSON encoding error in the first Nature retrieval workflow, is [R168_EMPIRICAL_ACCESS_AND_2014_DISPUTE_AUDIT_2026-10-21.md](R168_EMPIRICAL_ACCESS_AND_2014_DISPUTE_AUDIT_2026-10-21.md). The successful [Nature 2013 retrieval audit run39538185600](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39538185600) identified a 3,038-byte publisher anti-automation challenge HTML and **zero resolved original XLS links**. A green access-audit CI run does not imply human source data were downloaded.

## 2. Precomputation frozen 64 synthetic skill-frontier worlds

All mathematics and case identities were fixed before code in [prescore protocol](../../protocols/R168_CUMULATIVE_CULTURE_64_THREE_LEVEL_SAMPLING_WORLDS_PRESCORE_FREEZE_2026-10-21.md), Git commit [b949ff7](https://github.com/edwardsage419/Psychohistory-Research/commit/b949ff711ccb4a8ccbc43b6788461ebb011845b2).

Abstract population sizes N={2,4,8,16}, independent *individual copying fidelity* f={1/2,3/4}, innovation u={0,1/8}, two access channels `full_pool` and `single_channel`, and starting artificial group best skill L0={0,2}. Exactly **4×2×2×2×2=64** fully specified worlds, each storing the entire 3-state distribution over t=0,1,2,3,4. The fictional group skill frontier is L∈{0,1,2}, which is the **highest** of m independent hypothetical individual outcomes, with m=N for fully shared access, m=1 for one effective channel. This **does not model a population-average skill**, subjective knowledge, use frequency, realistic social networks, actual technical tasks, measured human fidelity, or any original author's exact equations.

The individual child-level distribution for current group level k is:
* k=0: Pr(level0,1,2)=(1−u,u,0).
* k=1: ((1−u)(1−f),(1−u)f,u).
* k=2: (0,1−f,f).

The next group maximum's exact transition CDF follows `Pr(max≤j)=[Σ_(r≤j)Pr(child=r)]^m`. A second independent oracle instead enumerates m consecutive independent opportunities using a dynamic programming recursion for the maximum, never calling the powered CDF formula, and then propagates its own 3×3 Markov matrix. The **32 complete transition matrices and all 64×5 full probability vectors agree exactly** as rational Fractions. All state distributions normalize to one and all stationary claims use separately checked exact equations. Full original [107,255-byte JSON](R168_EXACT_RESULTS.json) stores entire data, not a sample of summary findings.

## 3. Prespecified exact identification findings

1. **Group retention can rise with N without improvement in any individual's f.** At shared frontier level2, each opportunity retains level2 with probability f, while fully pooled group retention is `1−(1−f)^N`. For f=1/2, retention goes from **3/4** in an N=2 fully pooled group to **65535/65536 ≈ 0.999984741** for N=16. **The individual probability remained exactly 1/2 in both scenarios**. A group-level success headline therefore does not uniquely imply better individual learning.
2. **Different individual fidelities can produce indistinguishable group one-period observations.** A two-person full pool with f=1/2 and a single effective observation channel with f=3/4 (regardless of nominal population) both have group skill2 retention **3/4**. The effective sample size must be observed or controlled, or a group indicator alone cannot separately identify actual individual fidelity.
3. **Sampling more opportunities slows loss yet need not create a permanent cultural ratchet.** With zero innovation u=0 and 0<f<1, 0 is absorbing. In the frozen 3-state chain, eventual group loss of all skill is certain; exact mean generations until hitting frontier0 from level2 are \(2/(1−f)^m\). At f=1/2: **8 generations for m=2** versus **131072 generations for m=16**. A very persistent group maximum is still transient in this restrictive stochastic process.
4. **The cumulative innovation route has a strict multistep requirement.** From shared level0, positive artificial u permits reaching level1 after one transition, while level2 is impossible until at least the second generation. These artificially coded transitions may be viewed as a necessary synthetic stage of an incremental ratchet, without implying real humans follow such discrete innovation probabilities.
5. **Innovation changes the long-run type.** For u=1/8 and 0<f<1, all three states are communicating and the 3×3 finite chain has a unique positive stationary law. All 16 such fixed (N,f,mode) combinations are solved using independent exact Fraction Gaussian elimination; every balance residual equals exactly zero. With u=0, a unique strictly positive stationary law must not be asserted.
6. In `single_channel` mode, the entire conditional Markov kernel and five-generation outcome are independent of nominal N, proving that number of people and the number of usable cultural observations are distinct mathematical quantities.

All six points are properties of **our defined three-state model**. They do not vindicate any particular side of the Nature 2013/2014 debate and do not verify real cultural ratchets, knowledge quality, cooperation or long-term historical trajectories.

## 4. Real GitHub Actions, source identities and evidence gate

[Project-original source](r168_cumulative_cultural_frontier_exact.py), [109 actual distinct unittest methods](test_r168_cumulative_cultural_frontier_exact.py) comprising 64 uniquely named worlds and 45 mechanism, mean extinction, stationarity, input, original-source-exclusion and JSON reproducibility checks.

* First remote [GitHub Actions run39539043139](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39539043139) **success** for Python3.11 and Python3.12, each executing 109 actual tests, and producing identical SHA256 source, test, JSON and ZIP.
* [Pinned independent archive run39539126007](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39539126007) **success**: both Python versions again ran 109 tests, fixed SHA256 matched, and publisher job119022621002 independently reran 109, rebuilt the complete deterministic JSON/ZIP, checked four hashes and permanently committed both original files to main in [commit1c4f1a7](https://github.com/edwardsage419/Psychohistory-Research/commit/1c4f1a777e79c9afc67c8750dd39295644a8e3a8).
* **545 genuine test method executions across two workflows, 109 unique methods, zero failures.** Repeated methods are computational repeatability, not new original human observations.
* SHA256 program `f203de0c441fc9d2111899ff8517170697dad3e940ba84b5b99f5a58705efe80`
* SHA256 tests `8411ed9df0e0d8a5c6e9f5a70aa9dd352314129898c7fdaf5abac4cd0ee4c215`
* SHA256 complete JSON `ce460cd0c591b399d86b61671548a75daf68b86b1827f0d8b3274cb376302019`
* SHA256 complete [source and results ZIP](R168_Cumulative_Culture_64_Worlds_109_Tests.zip) `4da18ba2bd77320d3802a0eb2be38a414efdd3030f1459a375cd4fd0ed9cd7d6`.

From `research/R168`, reproduce with `python r168_cumulative_cultural_frontier_exact.py > R168_EXACT_RESULTS.json` and `python -m unittest -q test_r168_cumulative_cultural_frontier_exact.py` (Python standard library only).

**Scientific disposition: CLOSED_BOUNDED_E1** for 64 synthetic model worlds and author-paper identification audit. The originally prioritized human empirical E2 stage is **BLOCKED_SOURCE_ACCESS**, neither refuted nor validated. New independent E2 real human predictions =0; E3 actual historical forecasts=0. Keep R073 and PESEN v0.1 FROZEN. Next original catalog is **R169 P2/07-011 Coevolving Networks**, requiring a separate primary source and prescore gate. Consistent roadmap: finish R series, classify only then, fuse only after classification.

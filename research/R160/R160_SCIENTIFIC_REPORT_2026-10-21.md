# R160 Gene culture coevolution: artificial joint genetic cultural frequencies, association and independent exact oracles

Date 2026-10-21. Original catalog **P2 / 07-002 Gene Culture Coevolution**. Frozen before implementation in [protocol](../../protocols/R160_GENE_CULTURE_JOINT_SELECTION_LEARNING_60_FRACTION_WORLDS_PRESCORE_FREEZE_2026-10-21.md), commit [f9557ed](https://github.com/edwardsage419/Psychohistory-Research/commit/f9557ed2596ba343047766854e8684b4f894417a). **CLOSED_BOUNDED_E1 for exactly 60 synthetic two-trait mathematical cases only.** Genetic labels G0/G1 and cultural labels C0/C1 are fictitious, unconnected to any population or social group.

## Original source audit and scientific access boundary

* Feldman and Laland (1996), *Gene-culture coevolutionary theory*, *Trends in Ecology & Evolution* 11(11):453–457, DOI [10.1016/0169-5347(96)10052-5](https://www.sciencedirect.com/science/article/pii/0169534796100525). Directly verified the Elsevier publisher abstract and [PubMed bibliographic record](https://pubmed.ncbi.nlm.nih.gov/21237920/). Source defines gene/culture transmission as interacting across generations. The full paper equations have not been reimplemented.
* Feldman and Zhivotovsky (1992), *Gene-culture coevolution: toward a general theory of vertical transmission*, *PNAS* 89(24):11935–11938, DOI [10.1073/pnas.89.24.11935](https://pmc.ncbi.nlm.nih.gov/articles/PMC50672/). Original open-access abstract and article record inspected. The original analyzes vertical cultural transmission and potentially multiple genetic loci. **Original detailed model parameterization, mating system and evolutionary cases are outside this experiment**.
* Laland, Odling-Smee and Myles (2010), *How culture shaped the human genome: bringing genetics and the human sciences together*, *Nature Reviews Genetics* 11:137–148, DOI [10.1038/nrg2734](https://www.nature.com/articles/nrg2734). Nature publisher research-review key points examined: genetically selected variants can respond to culturally created environments, and gene/culture coevolution is more complex than a single-trait static association. **No original observed allele frequencies, human data, model calibration or author statistical evidence was reconstructed here**.

The original research concerns real biological transmission and socially learned practices, frequently including Mendelian inheritance, learning and environment-dependent fitness. Here **all transition equations are independent project-authored toy assumptions**, with artificial clonal gene-tag inheritance, no sexual reproduction, mutation, mating, genomic loci, cultural-group identity, learned payoffs, or long-term fitness measure. The model is an E1 stress test about aggregate identification. It cannot be used to rank real genetic or cultural groups or claim actual genomic selection.

## Frozen 60 joint-state toy models

Let \(p_{gc}\) represent four artificial joint frequencies for \(g,c\in\{0,1\}\), indexed (00,01,10,11), summing to one. Five initial distributions: independent uniform \((1/4,1/4,1/4,1/4)\), positively associated \((3/8,1/8,1/8,3/8)\), negatively associated \((1/8,3/8,3/8,1/8)\), all C0 \((1/2,0,1/2,0)\), all C1 \((0,1/2,0,1/2)\). Parameters: synthetic G1/C1 interaction weight \(s\in\{0,1/2\}\), cultural three-demonstrator conformity \(h\in\{0,1/2,1\}\), and horizontal copying share \(u\in\{0,1/4\}\). Exactly **5×2×3×2=60 prespecified models** with t=0,1,2,3,4.

Project selection rule \(w_{gc}=1+s g c\), giving \(a_{gc}=w_{gc}p_{gc}/Z\), where \(Z=1+s p_{11}\). Let \(v=a_{01}+a_{11}\), the postselection cultural C1 marginal, and \(M(v)=3v^2-2v^3\). Cultural copying target \(q=(1-h)v+hM(v)\). The output joint table is
\[
p'_{g1}=(1-u)a_{g1}+u(a_{g0}+a_{g1})q,\qquad
p'_{g0}=(1-u)a_{g0}+u(a_{g0}+a_{g1})(1-q).
\]
Both the gene and culture marginals \(G=P(G1),C=P(C1)\), and their association \(D=p_{11}-GC\), are stored for all five times per world. Results comprise 60×5×4=1200 exact joint cell frequencies and 900 separately derived gene/culture/association diagnostics in the [complete 123,259-byte JSON](R160_EXACT_RESULTS.json).

Two independently written exact computations were tested: (1) rational selection normalization and direct majority polynomial recurrence; (2) explicit four-class selection-weight enumeration plus eight independently enumerated majority-of-three demonstration configurations, then add retained and replacement mass for each \((g,c)\). **All 60×5 joint tables agree entry-by-entry as exact Python Fraction numbers**, including every marginal and association. Both obey exact unit total and nonnegative cells. The second route does not call the first route's core update.

## Preregistered association counterexample

Take two initial worlds with same marginals \(G=C=1/2\):
* Positive association: \((3/8,1/8,1/8,3/8)\), \(D=+1/8\).
* Negative association: \((1/8,3/8,3/8,1/8)\), \(D=-1/8\).

With s=1/2 and horizontal update u=0, the first subsequent G1 gene frequencies are exactly **11/19≈0.578947** and **9/17≈0.529412**. The original gene/culture marginal frequencies alone therefore **do not determine the new marginal under the project-specific interaction selection law**; their joint association also matters. This is a mathematical observation about the toy transition equation, not an empirical inference about inherited human traits or culture affecting human genes.

## Other prespecified checks and limits

* When s=0, every stage's G1 frequency is strictly conserved, including when cultural copying changes frequencies or destroys gene/culture association. When u=0, the full joint process is independent of h; in such experiments conformity h cannot be recovered from frequency histories. When s=u=0, all distributions are static.
* In the two associated worlds with s=0, initial G=C=1/2 and u=1/4, regardless of h, both marginals stay at 1/2 while association contracts exactly from ±1/8 to **±3/32** after one time unit. The joint distribution changes even when both separate marginal trajectories are constant. This demonstrates a second observation-design ambiguity.
* For the initial culture C0-only world, no C1 ever appears; likewise C1-only remains all C1. This project includes no mutation/innovation mechanism. No appearance of a missing cultural variant can be predicted without adding and validating such a mechanism.
* Artificial positive selection s=1/2 with positive G1,C1 mass raises the G1 fraction after the selection stage. Subsequent cultural copying preserves that gene marginal for the same step. The claim is conditional on the fabricated weights and generational timing.
* Algebraic mass conservation, nonnegativity, input type rejection, exact association symmetry checks and full JSON replay were included among 90 actual Python unittest methods.

## Real CI and archival evidence

* Program [r160_joint_gene_culture_exact.py](r160_joint_gene_culture_exact.py); [90 distinct genuine tests](test_r160_joint_gene_culture_exact.py), including 60 different named full 5-step models and 30 separate boundary and input controls.
* First [CI run39524857411](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39524857411): Python 3.11 and 3.12 ran 90 tests each, success. Both computed all 60 full worlds independently and produced identical four SHA256 file identities.
* Pinned [CI run39524960129](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39524960129): Python 3.11 and 3.12 independently reran 90 tests each with four SHA256 validation; archive publisher job118977378163 repeated all 90 tests and hashes, then permanently pushed the [full 123259-byte JSON](R160_EXACT_RESULTS.json) and [complete original-source ZIP](R160_Gene_Culture_60_Worlds_90_Tests.zip) at [archive commit7eab756](https://github.com/edwardsage419/Psychohistory-Research/commit/7eab7567e16fd1fdd89edfcb241eb40e9a3d6053).
* **450 actual test executions across the two CI runs**, containing 90 distinct methods, zero failures. These are computational replays, not independent population observations.
* Four immutable SHA256 hashes: source `a267dccfab5801533a48dc50e0f0ea89af02ff2792a7f9494425a1b0f1a4c59e`; tests `b0a976cf9516569214139c676312c9034e57ac16569c51114cb1724008975673`; JSON `7073cfd2aa3cad37955065c619d9ad9da16ba5b63ad768c0ae226597e64536bc`; source ZIP `aa68cc231970b2957bc7967d4e0538b8903a654b995ec9e635fc5c3afd8e07c1`.
* Reproduce from `research/R160` using `python r160_joint_gene_culture_exact.py > R160_EXACT_RESULTS.json` and `python -m unittest -q test_r160_joint_gene_culture_exact.py`; Python standard library and ZIP_LZMA only.

**Bounded E1 closure** is supported only for the frozen toy mathematics and source concept audit. New E2=0 and E3=0; no gene-culture field data or causal genetics result. Keep R073 and PESEN v0.1 frozen. Next original catalog **R161 P1/07-003 Conformist Transmission**; classification and eventual model fusion remain deferred until the original R series is complete.

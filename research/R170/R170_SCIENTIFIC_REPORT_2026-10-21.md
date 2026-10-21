# R170 scientific report: exact limited two-word naming game and feedback identifiability

Date 2026-10-21. Original catalog **P2 / 07-012 Language Evolution Models**. Scientific status **CLOSED_BOUNDED_E1** for project-authored finite word-inventory calculations. This is an artificially restricted two-word four-agent naming process and cannot be interpreted as modeling full grammar acquisition, language vitality, human semantics, real-time conversation or historically attested speech change.

## Verified first-hand foundations and attribution limits

* Baronchelli, Felici, Caglioti, Loreto and Steels (2006), [*Sharp transition towards shared vocabularies in multi-agent systems*](https://doi.org/10.1088/1742-5468/2006/06/P06014), *Journal of Statistical Mechanics* P06014, [author manuscript](https://arxiv.org/abs/physics/0509075), [City University original institutional archive](https://openaccess.city.ac.uk/id/eprint/2672/). The original agents use memory inventories, ordered local language-game interactions and successful versus unsuccessful feedback, with population-size transitions and emergent word statistics. The original includes unbounded-new-word invention/large-population effects, none reproduced by the present two-word capped process.
* Baronchelli, Dall'Asta, Barrat and Loreto (2006), [*Topology-induced coarsening in language games*](https://doi.org/10.1103/PhysRevE.73.015102), *Physical Review E* 73, 015102(R), [original APS abstract](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.73.015102). The paper shows network contact geometry matters for naming games; the original large-network scaling and coarsening constants are not established here.
* Nowak, Komarova and Niyogi (2001), [*Evolution of universal grammar*](https://doi.org/10.1126/science.291.5501.114), *Science* 291:114–118, [PubMed PMID11141560](https://pubmed.ncbi.nlm.nih.gov/11141560). The original addresses grammar-learning coherence and the evolution of universal grammar: a different empirical/theoretical target from bounded synonymous labels.
* Abrams and Strogatz (2003), [*Modelling the dynamics of language death*](https://doi.org/10.1038/424900a), *Nature* 424:900, [original publisher page](https://www.nature.com/articles/424900a). The original model was fitted to historical language-frequency series, none of which were downloaded or fitted in R170. No original population-level hazard, real endangered-language parameter, or historical prediction is claimed.

The prior literature has multiple incomparable research targets (linguistic form, word-learning, conventionalization, grammatical coherence, and language-community survival). This stage explicitly studies only **a fixed finite single-object two-variant communication negotiation** and does not merge their evidential claims.

## Frozen 72 world conditions and exact rules

Original [protocol](../../protocols/R170_TWO_WORD_NAMING_GAME_72_INVENTORY_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md) froze all initial conditions, message events, feedback and negative controls *before code* at [commit1853b17](https://github.com/edwardsage419/Psychohistory-Research/commit/1853b17f26dfd90298fe1543215d4b809ba777fb).

Four artificial speaker nodes indexed 0–3, fixed contact graphs:
1. path, 3 undirected links;
2. star, 3 links;
3. cycle, 4 links;
4. complete, 6 links.

Three artificial initial word inventories:
* split A,A,B,B => (1,1,2,2) with bit masks {A}=1, {B}=2, {A,B}=3;
* alternate A,B,A,B => (1,2,1,2);
* bilingual A,AB,B,AB => (1,3,2,3).

Three message-flip parameters ν∈{0,1/4,1/2}; two independent project-specified feedback rules `both_confirm` and `listener_only`. Total **4×3×3×2=72 frozen worlds**, each storing the complete exact probability distribution over all four individual inventories at t=0,1,2,3 (3 communications).

At each event choose a graph edge uniformly, then orient it uniformly as speaker→hearer. Speaker utters a uniformly chosen A or B if bilingual, otherwise its singleton. With artificial probability ν, the *delivered* token flips to the other word. If hearer already knows the delivered token, the message is recognized: `both_confirm` reduces both parties' inventories to the delivered word, whereas `listener_only` reduces only hearer. If hearer does not know the delivered token, only hearer adds that word to their inventory and both existing words may coexist. **The channel flip is newly authored here and is not one of the original 2006 naming-game rules; it can deliver a token not originally uttered or known by the speaker.** No vocabulary invention beyond {A,B}, cultural fitness, conversational intent, language grammar, human cognition or actual observed utterance was measured.

## Two independent Fraction Markov oracles and bounded findings

Oracle A enumerates every undirected interaction edge, speaker/hearer orientation, speaker-word choice and separate channel-flip branches, then applies the listener recognition rule. Oracle B independently enumerates all directed contact pairs and computes the marginal probability of the *delivered token* via conditional mixture of speaker inventory and noisy channel, then independently applies recognition rules. Neither oracle calls the other's event-updater. Both propagate full four-agent inventory-state probability distributions.

All **72×4 complete state distributions** match exactly as Python Fraction. The [full 1,062,174-byte original JSON](R170_EXACT_RESULTS.json) stores every four-agent inventory and its rational probability, expected inventory memory items, expected bilingual persons, and probability of single-word unanimous states. Every stage distribution sums exactly to 1.

**Frozen experimental controls:**

1. With zero noise, all-A and all-B monolingual unanimity are absorbing for both feedback schemes. Nonzero noise makes those states *nonabsorbing*, even though all original speaker/hearer inventories agree.
2. Under a message channel flip of ν, with four speakers originally all A, the chance the group remains all-A after **one** event is **1−ν**, tested as 1 when ν=0, 3/4 when ν=1/4, and 1/2 when ν=1/2 on a path graph under both-confirm policy. This is a project-specific noisy channel phenomenon, not a measured real-language mutation rate.
3. At ν=1/2, the chance of receiving A from a randomly uttering speaker is exactly 1/2 whether its current inventory is A, B, or AB. The *eventual updated state distribution* may still depend on speaker/hearer inventories and feedback; the fair channel does not erase all memory-dependent effects.
4. When everyone is initially monolingual and ν=0, both feedback rules have identical **one-step** distributions. A monolingual speaker already holds their chosen word, so reducing their inventory on recognition makes no difference. When initial speakers may be bilingual, feedback affects their inventories on successful exchange and full distributions separate immediately.
5. **Exact one-step mechanism separation:** start with artificial initial inventories (A,AB,B,AB) and ν=0. The total variation distance of the complete t=1 inventory distributions between both-confirm and listener-only is:
   * path: **1/4**
   * star: **1/6**
   * cycle: **1/4**
   * complete: **1/6**.
   These were separately computed in the final archival GitHub CI, in addition to the frozen equality and distinctness assertions. This demonstrates that exact feedback inference can depend on which pairs can speak to one another; it does not establish a corresponding human learning effect.
6. A failed communication adds a previously unknown word to the hearer (temporary inventory expansion), while recognized communication can collapse a bilingual inventory to a singleton. This two-direction memory mechanism differs from R169's single rigid binary opinion per node, yielding a distinct research contribution.

R170 does not check long-run natural-language convergence, real multilingual transmission, true speaker-listener beliefs, grammar acquisition, language death, original 2006 word-frequency Zipf law or phase transition. These require external human data and differently specified models.

## CI validation, complete data and reproducibility

[Project source](r170_two_word_naming_game_exact.py), [111 genuine unittest methods](test_r170_two_word_naming_game_exact.py): 72 separately named full-world cases and 39 independent channel, feedback, graph, source, boundary and negative tests.

* Initial [GitHub Actions run39541240078](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39541240078) **success**, Python3.11 and Python3.12 each actually ran 111 tests, zero failures, identical four original SHA256 hashes.
* Locked and archived [run39541318811](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39541318811) **success**: both Python environments independently ran 111 tests and checked all four SHA256; third publisher job119029519760 separately reran 111 and regenerated deterministic JSON and ZIP, checked hashes, and printed exact one-step divergence and noisy unanimity probabilities. Permanent source/test/complete JSON ZIP + JSON published by [archive commit17bead4](https://github.com/edwardsage419/Psychohistory-Research/commit/17bead42dc93481e4358928dc30ba742e63c3b07).
* **555 actual unittest executions across five jobs, 111 unique methods, zero failures.** Multiple runs are program replicability, not five independent natural-language studies.

Original artifact SHA256:
* source `6587ad073fbc34adc5029c81521ed73f05da319b2c46c1f86361f0a4d31d67ac`
* tests `54fc5b8322fd54432c3a619355e54942e4d4fc780dc431c56f28204e492acd97`
* full JSON `2e63390bfbb6e0ddbf1622767e94d59b2b1db1a286c8f79caac1d333d61277ce`
* [deterministic source/tests/JSON ZIP](R170_Naming_Game_72_Worlds_111_Tests.zip) `1b8cf39c0afec2a90fd5aed661b04ac13dbfd9215910abd27fb7dd2d40f7c0f1`.

Replay in `research/R170`: `python r170_two_word_naming_game_exact.py > R170_EXACT_RESULTS.json` and `python -m unittest -q test_r170_two_word_naming_game_exact.py` using only the Python standard library.

**Formal science acceptance: CLOSED_BOUNDED_E1** for project-authored exact vocabulary memory and controlled message transmission. New E2 real independent human utterance predictions=0, E3 historical external forecasts=0. R073 and PESEN v0.1 stay frozen. Next original catalog **R171 P2 / 07-013 Cultural Phylogenetics**, pending separate source/data audit. Finish original R-series, then classify, then fuse.

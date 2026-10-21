# R169 source triage: Coevolving Networks (P2 / 07-011)

Date: 2026-10-21. Original `docs/MODEL_CANDIDATE_CATALOG_v0.1.json` item **07-011**, priority **P2**, exact title **Coevolving Networks** (共演化网络), original first-hand source ID is **null**. This is **SOURCE_TRIAGE_ONLY**, neither model code nor preregistered cases nor scientific acceptance for R169. Previous R168 is formally closed **E1-only** with Nature/Dryad original empirical access blocked.

## Direct verifiable primary sources

* Holme, Petter, and M. E. J. Newman (2006), [*Nonequilibrium phase transition in the coevolution of networks and opinions*](https://doi.org/10.1103/PhysRevE.74.056108), *Physical Review E* 74, 056108. Original [American Physical Society article](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.056108), [arXiv original author manuscript](https://arxiv.org/abs/physics/0603023), [PubMed PMID17279969](https://pubmed.ncbi.nlm.nih.gov/17279969). Publisher abstract directly checked: social opinions can change through contacts, while contacts can themselves be rewired in response to opinions; a parameter controls the mix, and the original model exhibits a large-system continuous transition in opinion diversity.
* Vázquez, Federico, Víctor M. Eguíluz and Maxi San Miguel (2008), [*Generic Absorbing Transition in Coevolution Dynamics*](https://doi.org/10.1103/PhysRevLett.100.108702), *Physical Review Letters* 100, 108702, original [American Physical Society page](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.100.108702) and [author preprint](https://arxiv.org/abs/0710.4910), PubMed PMID18352241. Original abstract reports a model where a discordant link is rewired with probability p or one endpoint copies its neighbor's state with 1−p, including a mean-field absorbing transition formula \(p_c=(\mu-2)/(\mu-1)\) involving mean graph degree \(\mu\). That critical value is **source-model/mean-field dependent and not established in any new project model**.
* Gross, Thilo, and Bernd Blasius (2008), [*Adaptive coevolutionary networks: a review*](https://doi.org/10.1098/rsif.2007.1229), *Journal of the Royal Society Interface* 5:259–271, [original PMC open review](https://pmc.ncbi.nlm.nih.gov/articles/PMC2405905/), PubMed PMID17971320. Highlights network topology and node-state dynamics coevolving under local rules; serves as conceptual audit rather than validation of any specific numerical model.

## Nonduplication and scientific mechanism gate

R166 addressed copying-vs-directed transformation using a **fixed complete mixing population** and R167 addressed externally assigned **two group weights**. R169 should introduce a genuinely changing **explicit adjacency graph**, rather than relabeling the same aggregate mixing equations. Do not conflate:
1. changes in binary node opinions along a fixed graph,
2. rewiring edges while leaving all individual opinions unchanged,
3. joint coevolution in which rewiring changes future opportunities for information transfer.

A candidate *new project-defined* small-network experiment would freeze four-node undirected simple graphs, two binary opinion patterns, three rewiring probabilities and two rewiring target rules (homophilic versus unconditional), and calculate the full exact one-step and two-step distributions over labeled graph/opinion states using independent rational event enumeration. The homophilic target must be an eligible same-opinion nonneighbor and a graph with no eligible target must specify a no-op rather than silently resampling. A neutral control must preserve the number of undirected links under rewiring, while imitation preserves graph topology. Tests must separate changes in edge discordance, opinion frequencies and connected-component fragmentation and avoid inferring causal social polarization from a finite algebraic example.

## Gates before implementing R169

1. Inspect original author methodology enough to confirm orientation, rewiring eligibility, target selection and event clock: distinct papers may employ different conventions. Do not call a project-defined four-node implementation an exact original Holme–Newman or Vázquez replication unless parameterization truly matches.
2. Freeze all graph templates, opinion patterns, rewiring rates, tie/no-target handling, observation windows, full probability target and independent oracle protocol before model code.
3. Audit whether the original authors provide downloadable code or ground-truth data and record fixed SHA, if available. Avoid fabricated real-network or opinion observations.
4. Under exact finite n=4 math, do **not** claim a thermodynamic phase transition or the mean-field critical \(p_c\) has been replicated. Large-size effects and actual population evidence require entirely distinct studies.
5. Keep R073 and PESEN v0.1 FROZEN. Original full R-series → unified classification → fusion.

**R169 presently unclosed.** The original first-hand sources have been linked and the nonduplicative experiment target is defined conceptually, but no R169 E1/E2/E3 evidence is accepted here.

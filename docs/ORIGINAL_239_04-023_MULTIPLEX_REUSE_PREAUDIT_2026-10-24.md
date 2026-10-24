# Original239 04-023 Multiplex Networks: source and strict reuse preaudit

Date: 2026-10-24. State: OPEN_STRICT_REUSE_SCOPE. Next pending item after 04-021 SAOM. This is a research preaudit, with no E1 acceptance.

## Original non-Chinese literature
Kivelä et al. (2014), *Multilayer networks*, *Journal of Complex Networks* 2(3):203–271, DOI 10.1093/comnet/cnu016, https://doi.org/10.1093/comnet/cnu016 . Boccaletti et al. (2014), *The structure and dynamics of multilayer networks*, *Physics Reports* 544:1–122, DOI 10.1016/j.physrep.2014.07.001, https://doi.org/10.1016/j.physrep.2014.07.001 . Both describe distinct interaction layers and structural/dynamical consequences of preserving layer identities.

## Existing research strict reuse
R316 known-block SBM and R341 edge-triangle ERGM use one undirected edge type. R317 temporal contact events add time ordering, with no independently checked two-layer simultaneous relation identity. R342 SAOM changes one directed tie, without layer identity. This preaudit has not verified a full multiplex model in existing R. Early R001–R064 ZIP member-level reuse audit remains OPEN; absence from checked READMEs does not prove historical novelty.

## Proposed R343 bounded scope
Two labeled undirected relation layers on the same three nodes, three edge positions each. Exhaustively enumerate 64 layer-pair configurations. Compare union and intersection aggregate graphs, show information loss from union-only projection, and verify invariance under layer swapping. No real multiplex network, diffusion dynamics, human E2 or historical E3. R073 and PESEN v0.1 remain frozen. R-series evidence audit before taxonomy and fusion.

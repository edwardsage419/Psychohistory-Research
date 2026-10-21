# R170 prescore freeze | finite two-word naming-game internal inventories

Date 2026-10-21. Original catalog P2/07-012 Language Evolution Models. Primary source audit in `research/R170/R170_LANGUAGE_MODELS_PRIMARY_SOURCE_GATE_2026-10-21.md`. R169 CLOSED_BOUNDED_E1 complete, but its fixed binary opinion is not a linguistic inventory mechanism. Protocol must be committed **before all R170 model code and data**.

## Primary model concept and historical boundary

Baronchelli et al. (2006), *Sharp transition towards shared vocabularies in multi-agent systems*, DOI https://doi.org/10.1088/1742-5468/2006/06/P06014; original university repository https://openaccess.city.ac.uk/id/eprint/2672/ and author preprint https://arxiv.org/abs/physics/0509075. Related contact-topology naming game Baronchelli et al. (2006), DOI https://doi.org/10.1103/PhysRevE.73.015102. These ground the ideas of word inventories, repeated random speaker-hearer communication, feedback and convention adoption. The following is a **project-authored exact finite variant**, not the original unbounded vocabulary/lattice model or its population scaling. It does not model grammatical inference, language extinction, real spoken language, measured human communication or original author code.

## Freeze 72 exact finite inventory worlds

Four artificial labeled speakers/hearers 0,1,2,3 linked by one of four **fixed** undirected contact networks:
* chain: [(0,1),(1,2),(2,3)]
* star: [(0,1),(0,2),(0,3)]
* cycle: [(0,1),(1,2),(2,3),(0,3)]
* complete: all six undirected edges.

Each speaker has an internal nonempty **two-word lexical inventory** selected from exactly {A}, {B}, {A,B}, internally represented by bit masks 1,2,3. Three initial patterns:
* split: (A,A,B,B) => (1,1,2,2).
* alternate: (A,B,A,B) => (1,2,1,2).
* bilingual: (A,AB,B,AB) => (1,3,2,3).

Three message mutation/flipping probabilities nu∈{0,1/4,1/2}. Two listener-feedback rules `both_confirm` and `listener_only`. Total 4 networks×3 initial inventories×3 message-noise rates×2 update modes=**72 frozen worlds**, each retaining a complete exact distribution over all 4 inventory masks at t=0,1,2,3 (three contact events). Graphs are fixed in R170 to distinguish this from R169 rewiring.

## Exact event specification

At each time step:
1. Select uniformly an undirected graph edge, then uniformly its orientation, assigning the anchor **speaker s** and the other endpoint **hearer h**.
2. Speaker picks one of the currently held word variants A/B uniformly from its inventory. If it knows two words, it selects each with probability 1/2.
3. **Project-specific channel model**: the sent token is independently flipped A↔B with probability nu. Thus a hearer can receive a token speaker did not previously hold; this is an *artificial symbol-channel mutation*, not a model of acoustic mistakes or a rule of the original naming-game authors. Both parties receive feedback about the **delivered** token, not the speaker's originally selected word.
4. If hearer currently knows delivered token, communication is classed as recognized:
   - `both_confirm`: speaker and hearer **each reduce** their inventories to the delivered singleton token (speaker may learn a newly mutated delivered token).
   - `listener_only`: hearer reduces their inventory to delivered singleton, while speaker inventory does not change.
5. If hearer does **not** know delivered token, hearer **adds** it to their inventory; speaker inventory does not change regardless of feedback rule.
6. All probabilities exact Fraction. Agents always have one or two words. No new third vocabulary variant and no empty inventory. No code may quietly repair/noiselessly redraw messages.

## Independent exact Markov routes and controls

Route A: enumerate edges × orientations × speaker-word choices × channel-flip branch × listener recognition response, then merge identical 4-inventory vectors exactly; independent complete distribution propagation.

Route B: independently enumerate all **directed contact edges** and derive the probability that each delivered word A/B reaches a hearer from the speaker inventory with channel mutation. Recompute recognition and update without calling A; independently propagate. All 72×4 full distributions, mean lexical memory size, probability of unanimous A-singleton/B-singleton conventions, and probability of bilingual retention must strictly match. Save every exact Fraction result in canonical deterministic JSON, no float.

Prespecified boundary controls:
1. With nu=0, unanimous A-singleton and B-singleton states are absorbing under either feedback rule on any contact graph.
2. With nu>0, unanimous A-singleton can be perturbed by a mutated delivered B, so **message noise destroys unanimity absorption** in this artificial channel.
3. With all agents initially monolingual and no mutation, feedback policy `both_confirm` versus `listener_only` cannot differ on the *first* event when recognition happens, because speaker already has the singleton uttered; failure never changes speaker. However later interactions may generate bilingual speakers and then differentiate rules.
4. A bilingual speaker paired with a hearer recognizing their utterance can shrink the speaker's inventory under `both_confirm`, while `listener_only` preserves it. The bilingual initial pattern must show a positive-probability full distribution difference at t=1 when nu=0.
5. When nu=1/2, the delivered token is exactly a fair Bernoulli A/B regardless of whether speaker holds singleton A, singleton B, or both. This applies to the *delivered-token distribution*, not all post-feedback state transitions.
6. Non-connected graphs may preserve independent conventions, but all four frozen networks are connected; do not infer real-language convergence from finite time t≤3.
7. All edge topology remains fixed; only inventories change. Individual memory sizes can temporarily increase on failure and decrease on successful acknowledgment. No claim of Zipf law or large-population phase transition.
8. Exact probability normalization, invalid type/float/boolean controls, dynamic bilingual-memory count and no-new-symbol invariants. Cases with zero contact edges are invalid for the frozen design.

## Acceptance

72 individually named worlds plus at least 25 distinct mechanism/negative tests, two independent exact full-state oracles, preserved complete canonical JSON and source/test/JSON ZIP, four SHA256 locked and Python3.11/3.12 CI, independent archival replay on main with post-readback and machine/scientific report. Close **CLOSED_BOUNDED_E1 only** if all gates pass. New E2 and E3 must remain 0. Keep R073/PESEN v0.1 frozen. Determine next original R171 title from frozen catalog; finish all R, only afterward classify and fuse.

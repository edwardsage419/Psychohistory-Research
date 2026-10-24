# R333 prospective finite triadic feedback protocol

Date: 2026-10-24. Original239 item: 03-002 Social Cognitive Theory. Scientific grade target: bounded artificial E1 only.
Predecessor main HEAD at pre-registration: 70e966d9321706d98c9efa204a8cdfaf2b3d1f50. This protocol must be committed BEFORE source code, synthetic state records, and scoring results.

## Source and reuse decision
Bandura (1989), Human agency in social cognitive theory, American Psychologist 44(9):1175–1184, DOI 10.1037/0003-066X.44.9.1175. Bandura (2001), Social cognitive theory: an agentic perspective, Annual Review of Psychology 52:1–26, DOI 10.1146/annurev.psych.52.1.1.
Earlier R291 and R292 cover attitude, norms, intentions and perceived control without reciprocal environment feedback. R303 addresses observational acquisition versus expression, R305 social categorization, R308 collective efficacy. No inspected artifact strictly establishes the three-direction finite transition required here. Early ZIP-wide itemwise audit remains open. No transfer of their E1 or E2 grade to R333.

## Artificial, deliberately noncanonical mechanisms
Three binary variables P personal state, B expressed behavior, E environment. All updates are synchronous and use old time-t state. All eight initial P,B,E triples and both do(B_1) values 0 and 1 are enumerated for each mechanism. Four updates t=0 to t=4. After computing the first transition, overwrite B_1 with the assigned intervention, then continue updates. There are 2 mechanisms x 8 initial states x 2 interventions = 32 worlds and 160 time-indexed complete source records.
Cyclic reciprocal toy: P'=P XOR E; B'=P XOR B; E'=B XOR E.
Feedforward comparator: P'=P XOR E; B'=P XOR B; E'=E.
These equations are researcher-invented truth tables, not Bandura equations or estimates. Both contain E to P and P to B, but only the cyclic rule contains B to E. The intervention is imposed in code, not a randomized human intervention.

## Frozen falsifiers and expected exact contrasts
F1: Every one of 16 paired initial/intervention worlds must have the same behavior B_1 across mechanisms. Any mismatch rejects this protocol's one-step observational equivalence.
F2: Exactly 8 of 16 paired worlds must differ in P_2, and exactly 8 of 16 must differ in B_3. A different count rejects the proposed finite mechanism claim.
F3: For each of the eight initial states, comparing do(B_1=0) with do(B_1=1), E_2 must change in all eight cyclic worlds and zero feedforward worlds. A different count rejects the feedback intervention contrast.
F4: Exactly 160 records, ordered mechanism cyclic then feedforward, lexicographic initial P,B,E, intervention 0 then 1, time 0..4. Each record must include initial state, intervention, t, P,B,E. Byte-level reproducibility required.
F5: Independent auditor must re-enumerate the transition using separately implemented bit logic, reject at least one changed state cell and at least one altered world result. Production module imports prohibited in independent audit.

## Scope and acceptance
E1 is conditional exact arithmetic over constructed Boolean dynamics. Behavior-only one-step equality cannot identify the feedback mechanism. This toy provides no empirical estimate of Bandura's theory, no observational causal identification, no human E2, no historical E3, no general stochastic feedback or long-run result.
A successful CI requires Python 3.11 and 3.12 production replay/tests plus a separate independent no-import audit. Formal acceptance must follow verified success of all three jobs and include source identity, machine receipt and explicit scientific limitations. Update original239 crosswalk only after formal acceptance. Preserve R073 and PESEN v0.1 frozen; complete R series before taxonomy or fusion.

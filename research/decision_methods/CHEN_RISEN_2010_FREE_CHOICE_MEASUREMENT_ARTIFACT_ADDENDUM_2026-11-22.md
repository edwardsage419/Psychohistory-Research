# Chen and Risen (2010): postchoice rating change does not identify preference change

Actual research date: 2026-11-22. Theory track. Methodological addendum to SHAROT_ET_AL_2012_CHOICE_INDUCED_PREFERENCE_VERSION_BOUNDARY_2026-11-21.md. No personal records.

## Decision capability and gap
A decision assistant may record option ratings before and after choosing. An observed increase in the chosen option's rating cannot alone establish that the choice caused the user's underlying preference to change. The distinction matters when reviewing life decisions or proposing automatic updates to future value weights.

## Primary publications and inspected scope
1. Chen, M. Keith, and Jane L. Risen (2010), “How Choice Affects and Reflects Preferences: Revisiting the Free-Choice Paradigm,” Journal of Personality and Social Psychology 99(4):573–594, DOI 10.1037/a0020217. Inspected the author abstract preserved in PubMed (PMID 20658837), including the theorem claim and experimental summary; did not audit full proof or data. https://pubmed.ncbi.nlm.nih.gov/20658837/
2. Alós-Ferrer, Carlos, and Fei Shi (2015), “Choice-induced preference change and the free-choice paradigm: A clarification,” Judgment and Decision Making 10(1):34–49. Inspected the openly available abstract and explanatory mathematical discussion, including the counterexample to the universal positive-spreading claim. https://dlab.sauder.ubc.ca/sjdm/journal/12/12710/h2.html
3. Brehm, Jack W. (1956), “Postdecision Changes in the Desirability of Alternatives,” Journal of Abnormal and Social Psychology 52(3):384–389, DOI 10.1037/h0041006. Verified primary publication metadata and publicly exposed opening text, without reviewing the full experiment. https://pubmed.ncbi.nlm.nih.gov/13318848/

## Evidence and competing explanations
Chen and Risen show that choosing among alternatives supplies information about latent preferences that noisy initial ratings may miss. Their experimental summary reports apparent postchoice spreading in a condition where the choice occurs after both ratings, making the observed difference impossible to attribute to a preceding choice. This challenges causal interpretation of a simple before/after rating difference.

Alós-Ferrer and Shi demonstrate that Chen and Risen's asserted *universal strictly positive* spreading theorem does not hold under all stated assumptions. Their counterexample can generate zero or negative spreading with stable preferences. They nonetheless agree the traditional free-choice design has an identification problem. Therefore the defensible conclusion is **non-identification from ordinary before/after choice ratings**, not that the artifact always creates positive spreading and not that real preference change never occurs.

Other explanations include newly learned attributes, actual experience of the selected option, memory and measurement noise, deliberation, and genuine change in priorities. The existing Sharot 2012 record examines long-term self-choice versus computer-choice comparisons, with small delayed samples. This addendum only addresses the inference boundary of a single user's rating history; it does not repeat Sharot's empirical review.

## Candidate operational rule
When a user revises the rating of an already chosen option, retain the timestamped original ratings and choice, display the new rating as a separate observation, and ask at most one question *only if* the explanation would change a consequential recommendation: “这次评价变化，主要来自新的经历或信息，还是你现在看法不同了？” “不确定” is valid.

Never infer a causal preference update from rating change alone. Do not overwrite original weights. Any new weight used for future comparisons requires explicit user confirmation. Where there is no need to revise a recommendation, record the change without interrupting the conversation.

## Six synthetic acceptance cases (design only; not executed)
1. Prechoice A=7, B=7; chooses A; later A=9. Show rating change, causal attribution UNKNOWN.
2. A chosen after an unrecorded decisive feature is considered; later A rises. Preserve the possibility that choice revealed existing preference.
3. Ratings change before the actual choice in a rate-rate-choose sequence. Must not label this a postchoice causal effect.
4. A decreases after choice. Do not force a positive-spreading prediction from Chen and Risen's general theorem.
5. New factual evidence improves A; distinguish information update from value-weight update.
6. User explicitly confirms a new value weight; new analysis uses new version while archived original comparison remains reproducible.

## Validation and handoff
Evidence classification: published methodological arguments and author abstracts, plus a reviewed open methodological counterexample. No original numerical reproduction, full-text proof audit of Chen and Risen, independent experiment, software test, or personal scientific validation. This is a candidate interpretation rule.

Model track: consider an optional, single-question rating revision explanation with immutable snapshots. Data track: separate rating time, choice time, new evidence time and consented weight revision. Independent acceptance track: keep the six synthetic cases as proposed holdouts, compare against a simple no-causal-attribution baseline, and verify no retrospective overwrite. Do not treat these as executed tests.

Zero additional cost. No CI, PR merge, development authorization, private data, R073 or PESEN v0.1 changes.

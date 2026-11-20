# Ellsberg (1961): ambiguity and the boundary of inferring probabilities from choices

Actual research date: 2026-11-21 (Asia/Singapore). Track: personal decision theory, unnumbered supplement. Status: primary-text scoped review COMPLETE; independent empirical validation NOT_RUN.

## Decision capability and deduplication
Capability: clarify whether a user's stated preference reveals a likelihood estimate, or instead a preference for better-known evidence. This is distinct from C028-C034 interval robustness calculations, Hertwig 2004 rare-event experience, and the recent information-value method cards. It supplies a questioning and interpretation rule, not a new probability estimator. Recent main directory names and open PRs were checked before writing. No R-series acceptance or frozen protocol is changed.

## Primary source and actually inspected scope
Daniel Ellsberg (1961), *Risk, Ambiguity, and the Savage Axioms*, Quarterly Journal of Economics 75(4), 643–669. DOI https://doi.org/10.2307/1884324 .
Author-hosted scan of the journal reprint: https://www.ellsberg.net/wp-content/uploads/2023/03/DE_Notes_Papers_Risk_Ambiguity__the_Savage_Axioms_reprinted_from_Quarterly_Journal_of_Economics_Vol_LXXV_November_1961.pdf .
Actually inspected source text: pages 643–654, especially pp. 646–647 (inference from preference and axioms), pp. 650–653 (two urns and choice-pattern contradiction), and pp. 653–654 (partial sampling and three-color example). Pages 655–669, full formal model, footnotes and subsequent literature remain outside this round's primary-text verification. The author-hosted file is read for analysis; its copyrighted full text is not redistributed.

## Source-grounded finding
Urn I contains 100 red and black balls in an unknown proportion; Urn II contains 50 red and 50 black balls. In the author's hypothetical elicitation, a person may prefer a bet on red from II over red from I, and also prefer a bet on black from II over black from I (pp. 650–651). With fixed stakes and a single additive subjective probability for each urn, both strict preferences cannot be interpreted solely as event-probability rankings: the first would require p(red in I)<0.5 and the second p(black in I)<0.5, contradicting p(red in I)+p(black in I)=1. The original text explicitly describes the informal observations as under nonexperimental conditions and frames the examples as hypothetical. Do not describe these as a randomized trial or attach invented sample sizes/effect sizes.

The contradiction depends on assuming the same prize utility, exhaustive complementary colors, stable information and a single additive probability representation. A preference for a known-risk option can instead reflect evidential confidence, ambiguity attitude, decision rule or elicitation context. It does not identify a numeric belief about either color.

## Candidate system question and explanation rule
When a user says “I prefer the option with more reliable information,” ask: “Is this because you think its outcome is more likely, because the evidence is better established, or because you would rather avoid uncertainty about the probabilities? You may select multiple reasons or say unknown.”

Store separately: (a) observed or stated event frequencies and provenance, (b) user-provided subjective probabilities if explicitly supplied, (c) confidence in the evidence/probability model, (d) ambiguity preference, and (e) final choice. No automatic conversion from option preference to a numeric event probability. If probability remains unknown, retain unknown and present a conditional or interval comparison only if its assumptions are authorized and sourced.

## Synthetic acceptance counterexample
For the two urns above, the user chooses Urn II both when paid for red and when paid for black. An implementation infers from the first choice p_I(red)=0.4 and from the second p_I(black)=0.4, then treats the remaining 0.2 as a third color. FAIL: only two colors exist. It also FAILS if it interprets these two choices as empirical evidence that both outcomes in Urn I have probability below 0.5. PASS: records the two stated preferences, flags probability identification as unavailable, asks about ambiguity versus likelihood, and retains the two-color exhaustive constraint.

Additional metamorphic check: changing the display order of red and black without changing their definitions must not create an inferred probability or silently revise user-stated probabilities.

## Competing explanations and limitations
Competing mechanisms: utility differences in actual stakes, distrust of the sampling mechanism, missing third outcome in the user's mental model, framing/order effects, and stable ambiguity preferences. The paper's stylized urns do not establish a universal personal ambiguity-aversion coefficient, nor predict that choosing the known-risk option improves life outcomes. Explicit user beliefs and externally validated event rates may support probabilities separately. An ambiguity-averse choice alone cannot.

## Evidence and handoff
Primary-source scope read: COMPLETE. Synthetic logical contradiction checked algebraically: COMPLETE. Archive creation and readback: to be verified after write. Original participant-level statistical replication: NOT_RUN. Software execution, external validation and scientific acceptance: NOT_RUN.

Independent acceptance track: reserve an unseen two-color choice-order reversal case and test that no probability is hallucinated. Model track: assess a distinct ambiguity-confidence clarification field and conditional explanation. Data track: verify provenance and sampling assumptions before any empirical base rate is displayed. No development authorization is implied. No paid API, CI, personal data or restricted raw data used.

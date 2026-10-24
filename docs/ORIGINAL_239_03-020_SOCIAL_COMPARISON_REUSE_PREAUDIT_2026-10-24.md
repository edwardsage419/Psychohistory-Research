# Original239 03-020 Social Comparison Theory: source and strict reuse preaudit

Date: 2026-10-24. Status: OPEN_STRICT_REUSE_SCOPE. Original priority P2, next after v5.6 original239 pending six-item queue.

English original: Festinger (1954), *A Theory of Social Comparison Processes*, *Human Relations* 7(2):117–140, DOI 10.1177/001872675400700202, publisher https://journals.sagepub.com/doi/10.1177/001872675400700202 . The original theory concerns evaluating opinions and abilities, particularly in the absence of objective standards, and comparison with other people. Review: Wood (1989), *Theory and Research Concerning Social Comparisons of Personal Attributes*, *Psychological Bulletin* 106(2):231–248, DOI 10.1037/0033-2909.106.2.231, emphasizing multiple comparison goals and social context. No original participant-level data acquired.

Checked R338 artificial reference-gap and desire/entitlement/feasibility/attribution model, R293 value centering, R303 observational acquisition/expression and R334 induced compliance. These contain related social-cognitive ingredients, but the inspected scopes do not establish a model of comparison-target selection under objective-feedback availability. GitHub code searches for 'social comparison', 'Festinger', 'comparison target', 'reference group' returned no indexed matches. Search absence is weak evidence and does not cover early binary ZIP archives.

Strict reuse status: NO_STRICT_TARGET_SELECTION_REUSE_VERIFIED_IN_CHECKED_R. Early R001–R064 ZIP member-level audit OPEN_BINARY_ACCESS_BLOCKER. R338's reference-gap comparison arithmetic is an existing reusable submechanism, but it does not establish the target-selection process.

Candidate R339 E1: investigator-created self score 2, candidate A/B scores in {0,1,2,3,4}, binary objective-standard availability. Compare similarity-based nearest target with high-score target; when objective standard available both use NONE and self score. Exhaustive 50 worlds and 100 artificial atoms. This is a limited finite selection contrast only; no measured human comparisons, original Festinger replication, E2 or E3. R073/PESEN v0.1 frozen. R series before classification and fusion.

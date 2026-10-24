# R114 independent symbolic odds audit, bounded report

Date: 2026-10-24. Catalogue 03-008. Research track: existing R114 reused without changing its source or original acceptance.

## Evidence provenance

Frozen protocol commit: `d7ad98e970cfb938ee5d224f57a3d3cb1b3ab871`. Independent committed script blob: `238be57de645f91dfe1c69094898fe5cbe6a450f`. Original source blob: `468d41849c360be061944c0dfafa6e5df866da67`, independently reconstructed local source SHA256 `8fbd5571974e435e52a0328e3d9c732877c08f9c5fb056d076edbdfd581e2a24`, matching the existing original R114 CI receipt. Committed script was reconstructed byte-identically in the local execution environment and checked against its Git blob SHA1. Local Python 3.13.5 execution completed 50 assertions with no failures.

Original sources: Bicchieri and Xiao 2009 DOI 10.1002/bdm.621 (publisher abstract); Bicchieri, Lindemans and Jiang 2014 DOI 10.3389/fpsyg.2014.01418 (open full text). Original 2009 subject-level data, fitted coefficients and experiment replication remain unavailable in this audit.

## Predeclared checks and results

Four constructed integer coefficient models and all 16 factorial cells were independently evaluated with exact integer log odds and 65-digit Decimal exponential probabilities. All 16 probabilities agreed with the existing R114 implementation within 1e-14. The four symbolic interaction contrasts equal the frozen fourth coefficients. Aligned empirical/normative belief conditions are observationally identical for the two single-belief models, while both discordant cells separate them with opposite ordering. Two completions of an unobserved fourth cell prove the interaction cannot be uniquely recovered from three cells. Deliberate perturbations of one probability and one interaction log odds were both detected.

Local receipt: `research/validation/R114_INDEPENDENT_SYMBOLIC_ODDS_LOCAL_EXECUTION_RECEIPT_2026-10-24.json`.

## Scope and validation gates

The local internal method audit passed: **50 checks, 16 constructed cells, 2 rejected tamper controls**. The original R114 historical 30-test GitHub Actions run `39236924459` had passed previously. New workflow `.github/workflows/r114_independent_symbolic_odds_audit.yml` is committed with only standard public Ubuntu runners, no artifacts and no chargeable resources. At this report's preparation, the GitHub Actions run listing had **no new run** for the new workflow. CI state is **NOT_RUN**, not success. New crosswalk acceptance and removal from the 168-item queue are deferred until the committed script has independently executed on GitHub Actions or an equivalent independently verified execution gate is accepted.

No held-out real prediction, calibration, cluster bootstrap, real subject-level experiment or causal identification was conducted. The 2009 published significance statement cannot be converted into a fitted coefficient from this synthetic design. This is internal procedural independence, not external researcher replication. Scientific evidence remains bounded synthetic E1; new E2=0 and E3=0. R073 and PESEN v0.1 remain frozen. The original239 directory link is not scientific validation.

Next: confirm workflow run and SHA-verified Python 3.11/3.12 replay. If no run appears, preserve CI blocker, retain original239 pending state, continue next priority without inventing acceptance.

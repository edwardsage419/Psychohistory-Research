# R077 exact scoring candidate implementation plan

> Native execution in this session; use executing-plans and one fresh review.

Goal: close the callable exact-Brier repair gap left explicitly open by PR18,
without changing frozen original code, protocols, data or historical results.
Base: main3221a84fba91731071b8931447837e07578210be.
Spec: user Codex B v2.0 B1; project workflow v2 and R077 Rev002 freeze.

Architecture: new score_exact_brier(fit,sessions) returns {scores, exact_Brier}.
Reuse original scorer for unchanged validation/log loss and PR18 summarize for
exact Brier aggregation/votes. Recover p0 from consistent complete integer source
tables, alpha20 and noise1/20. Preserve seven families, six pairs, session weights.
No author run()/data download/real scoring/production wiring. This candidate's
exact mathematical probabilities differ from intermediate binary float rounding;
adoption is subject to owner/ChatGPT review, not a protocol amendment here.

Files: candidate.py (specific numeric adapter), test_candidate.py (synthetic
behavior), replay.py (bounded command evidence), pins.json, REPORT/HANDOFF/evidence.
No new general runner or second full scoring oracle; reuse PR16/18 read-only.

Review focus: wrong float rounding masquerading as exact; inconsistent source
marginals; target label leakage; treatment/session weighting; loss of tiny genuine
directions through tolerance or float conversion. Test each in the candidate suite.

- [ ] Reproduce original 35/11 failure; first failing candidate tie regression.
- [ ] Implement minimum exact probability/Brier adapter with strict source counts.
- [ ] Check independent integer tie witness, Decimal oracle, complete score shape,
  independent permutations, near-zero nonzero effects and malformed sources.
- [ ] Replay ordinary/-O and existing second Python; preserve original FAIL and
  verify frozen inputs unchanged. Original R073/R077 suites; root unittest discover
  reported literally (repository has no global Python test configuration).
- [ ] One fresh-context read-only review; handle actionable findings once.
- [ ] Refresh main/PR scope, draft PR, remote readback; no merge/CI dispatch/cost.

Historical human impact UNKNOWN: archived aggregate means/votes do not identify
per-session exact margins. Rev002 freezes original model blob and scoring; do not
assume this candidate is approved for true-data adoption. Any revised human results
or protocol/source changes require a concrete owner/ChatGPT decision separately.

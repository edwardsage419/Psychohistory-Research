# B audit: R326 S122 exact independent factored recomputation

Date 2026-11-01. Track B. Target (b,R326,S122_f2e4798f,nonblind_full_atom_and_mutation_audit). Prior R326 S122 freeze commit f2e4798fc97697c642cc1fa20fd70cdd987b1c50. The B auditor was written separately from the JavaScript enumerator, using Python Fraction and per-group factored evidence and success-weighted evidence; no import of the R generator. It read the complete 768-row R CSV and 1,076-byte R JSON, compared all 20 fields for each atom, normalized each law/group probability to 1, and recomputed the six expected Brier risks and signed contrasts.

## Observed execution
Python 3.13.5 standard library, normal and -O modes both PASS. Independent expected Brier:
H: 2150517/9614080, 9/40, 1/4.
I: 16336700817/72211354880, 9/40, 1/4.
Eight injected mutations rejected: delete row, duplicate row, law change, joint mass, hierarchical prediction, weighted score, fabricated E2 evidence scope and aggregate loss. No input from a different human research team, no blinding, no real holdout sample. The local first attempt failed because original source identity flag had not yet been set; the exact original 3679-byte CSV was then independently reconstructed with Git blob 3d2481365160c33fabbba7f8be6c3a9ff78e5121, and the primary parent check was executed before final normal and optimized PASS. This failed gate remains recorded.

R persisted CSV Git blob 27f50f1bbb10bb78c43f41acf29af58268957708; JSON blob 30e88f65e1b15b5d6010f647750a9526898b88eb. B source local Git blob a55e4c78e0f257b78d56d7e1f15c21783d06ed7a. These are programmatic exact identities. CI for S122 NOT_RUN. R326 parent CI success is historical and does not apply to S122.

## Scientific audit scope
E1 synthetic mathematics, conditional on two specified generating laws. Independent H/I factorization makes the 768 atom equality a useful internal nonblind check. Posterior expected Brier under the true law has Bayes optimality by construction. No empirical calibration, no human E2, no historical E3, no genuinely independent external replication. Negative control for uniform history weights passed; model misspecification I produces a positive pooling penalty. Parent R326 acceptance unchanged.

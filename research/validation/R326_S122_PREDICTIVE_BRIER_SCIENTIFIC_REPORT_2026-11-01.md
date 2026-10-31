# R326 S122 scientific report: predictive Brier and misspecified pooling

Date 2026-11-01. Original239 02-007. Prospective extension protocol commit f2e4798fc97697c642cc1fa20fd70cdd987b1c50. Parent source Git blob 3d2481365160c33fabbba7f8be6c3a9ff78e5121, original frozen model unchanged.

## Question and methods
Under two exact artificial data-generating laws, assess predictive risk of the frozen R326 hierarchical posterior, independent-group posterior, and constant 1/2. Law H is the original three-group shared-regime hierarchy. Law I has three independent group theta values with marginal high probability 1/2. Both retain two observations per group and theta in {1/4,3/4}. All 64 six-bit histories, 3 target groups, 2 next outcomes and 2 laws give 768 exact rational joint probability atoms. Brier expected loss uses actual generative probabilities, averaged across three groups. Original 1/64 enumeration weight is coverage only.

## Exact results
| Law | Hierarchical Brier | Independent Brier | Constant Brier |
| --- | --- | --- | --- |
| H, shared regime | 2150517/9614080 (0.2236841175) | 9/40 (0.225) | 1/4 |
| I, independent groups | 16336700817/72211354880 (0.2262345146) | 9/40 (0.225) | 1/4 |

Under H, independent minus hierarchical Brier is **12651/9614080** (about 0.001315883). Under I, hierarchical minus independent Brier is **89145969/72211354880** (about 0.001234515). Thus borrowing helps under the shared-regime generative law and hurts under the independent-group law. Both laws share the same single-group marginal prior; independent-group risk equals 9/40 under each.

## Executed evidence and limits
The primary BigInt exact enumeration produced 768 records and matched all 192 parent posterior predictions in the original 64-row CSV. The original 3679-byte parent CSV was independently regenerated with matching Git blob 3d2481365160c33fabbba7f8be6c3a9ff78e5121. A separately factored Python Fraction computation compared all 768 rows and six expected risks and rejected eight mutations. Positive mass, six group-level normalization checks, complement symmetry and a negative control for incorrect uniform-history weighting passed. Local runtime: Node 22.16.0 and Python 3.13.5. Parent R326 prior CI evidence is separate. New S122 CI NOT_RUN, and no external independent-team replication.

This is E1 mathematical evidence under artificial known laws. Real-world model fit, E2 human prediction, E3 historical validation, empirical probability calibration and external independent replication are OPEN. Original R326 bounded E1 acceptance remains unchanged. R073 and PESEN v0.1 frozen.

# R307 S103 scientific report: heldout exact identifiability of minority influence gates
Date 2026-10-31 UTC. Track r. Prescore frozen at commit e3d70b11b9f5f4cb691cee44c1aa1a7d7fe16ad6. Original R307 acceptance CLOSED_BOUNDED_E1 remains unchanged. New S103 status PARTIAL. Evidence E1 artificial only.

## Original sources and scope
Original project model: research/R307/r307_exact_minority_consistency_private_public.py, blob 5c8e2f1192d7e43bc2d6d1e306094b7e268e9eaa, source freeze 4f74448e261ac61c65cd60926a056d6916a84e34. Original theoretical context: Moscovici, Lage and Naffrechoux 1969 DOI 10.2307/2786541; Wood et al. 1994 DOI 10.1037/0033-2909.115.3.323. The numerical likelihood and pressure factors were invented by this project. No original human response data or author-fitted parameters were used.

## Prescore disclosure
Before freezing S103, a pilot with prior 1/4 and t=3 was inspected. Pilot results cannot count as prospective evidence. The confirmatory grid has disjoint prior 1/2 and exposure t=1,2,3, all 27 (consistency,credibility,normative pressure) triples per t, totaling 81 artificial worlds. The protocol fixed six observation designs before confirmatory scoring.

## Exact confirmatory result
For EACH of t=1,2,3 the complete finite partition is identical in cardinality:

| Design | Distinct signatures | Class size histogram | Singleton worlds | Uniform prior optimal exact triple identification |
| --- | ---: | --- | ---: | ---: |
| D0 no exposure, private/public m=1 | 1 | {27:1} | 0 | 1/27 |
| D1 private m=1 | 4 | {3:2,6:1,15:1} | 0 | 4/27 |
| D2 public m=1 | 10 | {1:6,2:3,15:1} | 6 | 10/27 |
| D3 public m=1 and m=2 | 10 | {1:6,2:3,15:1} | 6 | 10/27 |
| D4 private/public m=1 | 10 | {1:6,2:3,15:1} | 6 | 10/27 |
| D5 private/public m=1 and m=2 | 10 | {1:6,2:3,15:1} | 6 | 10/27 |

Full 81 worlds, 18 partitions, all member identities and exact rational signatures are archived. In this restricted exact known-grid setting, D2, D3, D4 and D5 have the SAME partition, so adding a second minority size or a private channel has zero extra identifiability gain. Exposure t=1,2,3 changes probability magnitudes, but these three horizons do not change the partition.

## Mechanism
For fixed prior p=1/2 and positive exposure, private probability depends on the product c*k. Five (c,k) pairs yield zero product; their three n values form one 15-world indistinguishable class because both private and public equal the prior. Product 1/2 occurs for two (c,k) pairs, yielding three two-world classes indexed by n. Products 1/4 and 1 each occur for one (c,k) pair and each n, giving six singleton worlds. PRIVATE_ONLY cannot identify n and yields four classes. PUBLIC_ONLY at m=1 happens to distinguish the same ten classes as JOINT in this fixed discrete grid. That finite-grid coincidence does not establish generic parameter identification with continuous values, noisy observations, unknown prior or unknown exposure count.

Uniform-prior optimal classification accuracy counts classes / 27 for a stipulated known prior over the 27 artificial triples. This is not a real-world prediction accuracy or population prevalence. No sample-split learning or empirical calibration was performed.

## Independent B and acceptance
R generator was actually evaluated in a V8 JavaScript execution context, creating the 81-row CSV and 18-design JSON. A separate no-import algebraic audit evaluated all persisted GitHub CSV and JSON fields and rejected 8/8 final mutations. A separate Python Fraction oracle ran locally in Python 3.13.5 both ordinary and optimized mode, 8/8 mutations rejected; this is within-project nonblind checking. Original archived Node CLI execution and external-team replication NOT_RUN. The first B mutation harness had a no-op edit and falsely accepted its third attempted mutation; the harness was corrected before the final eight effective tests. Preserve this failed development observation.

A01 finite protocol PASS, A02 original project source identity PASS and author empirical source OPEN, A03 exact synthetic artifact generation and independent internal audit PASS with native CLI/CI OPEN, A04 controls and mutation tests PASS after correction, A05 bounded E1 scope PASS, A06 formal extension acceptance OPEN. Overall S103 PARTIAL. No new E2 human or E3 historical evidence. R073 and PESEN v0.1 frozen.

## Next
Any attempt to estimate real private/public belief differences needs actual paired observations, clear consent and licensing, cluster-aware evaluation, external holdout, uncertainty, and separately identified consistency/credibility manipulations. Keep original239 v7.8 and pending154 unchanged. No paid services or Actions initiated.

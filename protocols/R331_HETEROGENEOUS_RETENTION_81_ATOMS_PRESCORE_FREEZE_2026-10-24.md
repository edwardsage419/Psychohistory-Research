# R331 preregistered bounded E1 protocol: heterogeneous retention mixture
Date 2026-10-24. Catalogue 02-014 Memory Decay Models. This file must be committed before creating model code, CSV, derived results, or audits.

## Prior evidence and reuse decision
Read original239 v4.8 and pending14 queue, R330 retrieval source/report, R295 habit report, R302 Bayesian bandit report. R330 uses fixed cue and recency weights for action choice and does not test retention survival over delays; R295 models habit acquisition; R302 models Bayesian success beliefs. No exact source-level equivalent was verified. Repository-wide search for 'forgetting decay retention' and 'Ebbinghaus' returned no matches, but early ZIP exhaustive audit remains open. Reuse as contextual evidence only; no strict scientific reuse claim.

## English-language primary research
Ebbinghaus (1885; English 1913), Memory: A Contribution to Experimental Psychology, chapter 7, https://psychclassics.yorku.ca/Ebbinghaus/index.htm. Ebbinghaus measured savings in relearning; constructed retention values below are not his savings observations. Wixted and Ebbesen (1991), On the Form of Forgetting, Psychological Science 2(6):409-415, https://doi.org/10.1111/j.1467-9280.1991.tb00175.x. Authors compare power, exponential and other empirical forgetting functions; no original human data is used here.

## Frozen artificial design and falsifiers
Three ordered retention bases (a,b): (1/4,1/2), (1/4,3/4), (1/2,3/4). Three fast-component weights w: 1/4,1/2,3/4. Nine worlds, delays t=0..8 inclusive, exactly 81 full artificial source records.
Component contributions are w*a^t and (1-w)*b^t. Mixture S(t)=w*a^t+(1-w)*b^t. Single homogeneous exponential comparison Q(t)=[w*a+(1-w)*b]^t. All numbers exact rational. No fitting, noise, random seeds or human subjects.
Predeclared checks: S(0)=Q(0)=1 and S(1)=Q(1); S(2)-Q(2)=w(1-w)(b-a)^2 > 0 in every world; S(t)>=Q(t) for t=2..8; S(t) strictly decreases over t=0..8; all 81 component rows and 9 world summaries must byte-replay. For a=1/4,b=3/4,w=1/2, t2 S=5/16, Q=1/4, gap=1/16. A failure of any exact equality, ordering, row count, independent audit, or tamper rejection blocks acceptance.
Independent auditor must not import production code and must recompute each atom using Fraction. A deliberately altered source value must be rejected.

## Formal boundary
PASS_BOUNDED_E1_CONSTRUCTED_HETEROGENEOUS_RETENTION_ONLY is available only after actual independent audit and successful GitHub Actions on Python 3.11 and 3.12. The result demonstrates a finite mathematical aggregation effect; no proof of psychological trace mechanism, individual forgetting function, Ebbinghaus savings replication, original human E2, historical E3 or predictive performance. Catalogue link is provenance only. R073 and PESEN v0.1 remain frozen. Complete R series before classification and fusion; personal decision system deferred.

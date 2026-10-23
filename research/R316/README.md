# R316 | Exact known-block SBM | Original239 04-019

Exact finite E1: 4 synthetic nodes, fixed block vector (0,0,1,1), all 64 undirected edge graphs under 2 regimes (p_within,p_cross)=(3/4,1/4) and (1/4,3/4). 768 graph-dyad source atoms, 128 graph likelihoods, known-parameter total variation 203/256.

Pre-score freeze [commit8a973088](https://github.com/edwardsage419/Psychohistory-Research/commit/8a9730882203dffbf46e1ef843bb8f52b2b9674d), prior to model and source calculations.

```bash
python research/R316/r316_exact_sbm.py --test
python research/R316/r316_exact_sbm.py --audit
python research/catalogue_audit/independent_r316_sbm_source_audit.py --audit
```

See [research report](R316_SCIENTIFIC_REPORT_2026-10-24.md), [all original source factors](R316_ALL_768_ORIGINAL_GRAPH_DYAD_PROBABILITY_ATOMS.csv), and [all graph likelihoods](R316_EXACT_128_GRAPH_LIKELIHOODS.json).

Primary Holland, Laskey & Leinhardt 1983, https://doi.org/10.1016/0378-8733(83)90021-7 . No observed human ties, community detection, network dynamics, E2 or E3.

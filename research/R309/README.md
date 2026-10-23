# R309 SIR Epidemic Model — exact 5-agent discrete artificial Markov transitions

Original239 candidate **04-006** P1. Original classical SIR compartments: Kermack & McKendrick (1927), DOI https://doi.org/10.1098/rspa.1927.0118. **R309 uses a project-defined discrete chain-binomial contact/recovery update**, not authors' original continuous derivation, epidemic calibration, or human cultural contagion study.

Exactly five artificial agents, all 21 S/I/R compositions and all9 p,q∈{0,1/2,1} pairs, giving **189 artificial worlds, 1,134 fully labeled original transition source rows** (including impossible/zero-probability events). Each susceptible is infected if any of I originally infected independent p-contacts succeed; only the original infectives recover with independent q. All source weights exact Fraction, sum to1 in every world, conserving N5. Key example S3 I2 p=q=1/2: attack3/4, expected next counts3/4,13/4,1; chance1/256 for zero new infections and both old recover. At p=q=1 next (S,I,R)=(0,3,2), because newly infected do NOT recover instantly.

* [Prescore freeze commit aec096d7](https://github.com/edwardsage419/Psychohistory-Research/commit/aec096d72f66c44ac1b13dd5ed1ce9d169f21aac), [full protocol](../../protocols/R309_SIR_FINITE_FIVE_AGENT_EXACT_TRANSITIONS_1134_SOURCES_PRESCORE_FREEZE_2026-10-23.md)
* [Native exact probabilistic model, 3417 actual tests](r309_exact_five_agent_sir_transitions.py)
* [All 1134 original event source CSV](R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv)
* [Complete 189-world source and outcome JSON](R309_EXACT_FIVE_AGENT_SIR_RESULTS.json)
* [Original CSV and JSON SHA256 receipt](R309_MACHINE_RECEIPT.json)
* [Independent 11664 binary contact/recovery elementary assignments, 17 adversarial tests](../catalogue_audit/independent_r309_source_audit.py)
* [Full scientific report with boundary safeguards](R309_SCIENTIFIC_REPORT_2026-10-23.md)
* [Bounded E1 machine acceptance](R309_FINAL_ACCEPTANCE_STATUS.json)

[GitHub Actions science run39955168677](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955168677) three jobs success on Python3.11/3.12 plus independent third source archiver; full data permanently archived [commit54997770](https://github.com/edwardsage419/Psychohistory-Research/commit/549977708267ac455d0ac61ec3fee0d0330b43ce).

No real persons, pathogens, cultural or opinion diffusion E2; no multi-step observed trajectories or real epidemic parameter fitting; historical E3 zero, R073/PESEN v0.1 frozen.

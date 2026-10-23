# R324 Psychometric Paradigm of Risk Perception: finite constructed two-axis E1

Original239 **01-017**, P2. [Protocol frozen](https://github.com/edwardsage419/Psychohistory-Research/commit/854fc11f1be6e902de753a919b9594884241ee8d) before [source and data](https://github.com/edwardsage419/Psychohistory-Research/commit/ae9568f0d5c04f9973db6e2b7f9883d5ba8333f5). Four artificial worlds, 16 binary hazard descriptor states each, **64 original artificial rows**. D=dread1+dread2, U=unknown1+unknown2, score=aD+bU. Dread-only vs unknown-only ranking reverses across (3,1) and (1,3), ties under (1,1), and remains rank-equivalent under (2,2).

**PASS_BOUNDED_E1_CONSTRUCTED_RISK_COMPOSITE_ONLY**, after [corrected three-job green CI run 40021287400](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021287400). The [first CI run 40021221413](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021221413) failed due to a syntax typo in a unit test; [repair commit](https://github.com/edwardsage419/Psychohistory-Research/commit/6ebdfed14ef01a897533dfe09fcfd0853e0edd3d) corrected the test only. Python 3.11/3.12 each ran 26 tests, with independent no-import reconstruction.

[Scientific report](R324_SCIENTIFIC_REPORT_2026-10-24.md), [formal acceptance](R324_FINAL_ACCEPTANCE_STATUS.json), [machine receipt](R324_MACHINE_RECEIPT.json), [generator](r324_risk.py), [64 source rows](R324_ALL_64_ARTIFICIAL_RISK_STATES.csv), [exact results](R324_EXACT_FOUR_SCORING_WORLDS.json).

Replay: `python research/R324/r324_risk.py --test`, `python research/R324/r324_risk.py --audit`, and `python research/catalogue_audit/independent_r324_risk_audit.py`.

This is project-defined artificial E1. No fitted psychometric factors, 1978 participant replication, human E2 or historical E3. R073/PESEN v0.1 unchanged.

# B track: independent R319 S115 panel-joint mathematical receipt audit

Date: 2026-11-01 Asia/Singapore. Target key: (B,R319,S115_528872dd,full_240_joint_and_latent_persistence_identity).
Status: PASS_INTERNAL_NONBLIND_E1_ONLY. External blind replication NOT_RUN.

## Read scope and source identity
Read original R319 protocol, original R319 84-atom CSV (Git blob abbc6b79715535bcf0b5d35d7f8c8578c82a2ef6) and 15-world marginal JSON (Git blob 5ea1cde7f7f5bad3c0b12bbeee614ac7dda7a947). Independently reconstructed all 84 original source rows and their conditional probabilities, mixture masses, weighted contributions, original marginal vectors and unique keys: 84/84 exact PASS. Read S115 prescore protocol committed at 528872dd56d66255014419d1da383de430fc67e7 before S115 calculation. Read new 240-cell CSV and 15-world JSON. Nonblind status declared because original R319 results and S115 R outputs were visible.

## Independent audit method
R code is native Node BigInt rational pair construction. B code is standalone Python 3.13.5 Fraction enumeration, no import of R code. For REDRAW, B explicitly enumerates four ordered latent beta pairs; for PERSISTENT, it enumerates two fixed beta alternatives. Compared all 240 source rows, all 15 exact TV and Bayes accuracy values, all world keys, summary metadata and source row universe. Verified q(1-q) covariance identity in each ordered pair, all 10 q=0/1 boundary controls, and joint mass normalization via exact source agreement. Original R source 84 atoms were separately checked from GitHub contents, without using a private dataset.

Commands executed locally:
1. node r319_s115_panel_persistence.js --emit --out-dir /mnt/data
2. node r319_s115_panel_persistence.js --audit
3. python b_r319_s115_panel_fraction_audit.py --csv R319_S115_ALL_240_PANEL_JOINT_CELLS.csv --summary R319_S115_EXACT_PANEL_SUMMARY.json --selftest
4. python -O b_r319_s115_panel_fraction_audit.py with the same flags.
All commands returned exit 0, PASS. Eight targeted mutations were rejected in each Python mode: deleted cell, duplicate cell, probability tamper, mechanism swap, alternative index tamper, mixing mass tamper, TV summary tamper, false E2 evidence promotion. Source CSV SHA256 ac218326bf68d7bd4d6db385921d679ac0706d07ce09130e6458d925dc646531; JSON SHA256 7509fdbddc82102bbf524a2302c7e84cb83226fc916976c8fa423e83830902b5.

## Scientific and operational gates
No empirical data or labels are present. Leakage, sample-out evaluation, human probability calibration, cluster bootstrap and empirical confidence intervals are NOT_APPLICABLE to the exact enumerated E1 universe. No human predictive improvement or real mechanism recovery can be inferred. Original R319 bounded E1 acceptance remains unchanged. New S115 is PARTIAL_E1_EXTENSION pending any additional acceptance governance; code execution alone does not grant formal acceptance. E2=0; E3=0; external independent replication NOT_RUN. No Actions triggered because free billing status has not been independently verified. Remote commit SHA and CI status to be appended by R-track coordination after push.

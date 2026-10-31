# TH169 theory track handoff

track: theory
subflow: TH169
handoff_utc: 2026-10-31T02:18:40Z
baseline_head_before_work: f23038027379166a7456692a912d84a11a4f7f2f
head_before_handoff: 3d5742a1523bb97994ae3f239131c0972a8e4be6
target_key: (theory,MURALIDHARAN_NIEHAUS_SUKHTANKAR_SMARTCARDS,TH169-theory-v1,archive_inventory_independent_replication_and_adoption_selection)
status: COMPLETE_BOUNDED_NOTE
claim: NO
claim_expiry_utc: N/A
artifact_paths: theory/TH169_SMARTCARDS_REPLICATION_ARCHIVE_INDEPENDENT_REPLICATION_IDENTIFICATION_2026-10-31.md ; theory/th169_replication_selection_bounds_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261031T021840Z-th169-archive-independent-replication-handoff.md
commits: note=1d029849022b88e157bd574e7844b5c7043e8fc9 ; script=21f252464fffe40d63d495c2c743b11a48b81eb5 ; index=3d5742a1523bb97994ae3f239131c0972a8e4be6
source_blobs: note=96b13bb78912af5fd21c3b4f8e570568178fe637 ; script=bd7d943a85ed771e872dd01b8bbe169879ccb8d6 ; index=e86d89607e56c874d7749f13b2730d7fb97f95b8
source_read: openICPSR V1 root/20141346_data/analysis_code/data and LICENSE/README file metadata; Atanda 3ie Replication Paper 23 sections 2-6 and Appendix A1-A3 selected tables; original 2016 AER abstract, 2014 NBER metadata and Atanda 2019 journal abstract.
source_links: https://www.openicpsr.org/openicpsr/project/113012/version/V1/view ; https://www.3ieimpact.org/sites/default/files/2019-06/RPS23_Biometric_Smartcards_and_payment_disbursement_India_3.pdf ; https://doi.org/10.23846/RPS0023 ; https://doi.org/10.3886/E113012V1 ; https://doi.org/10.1080/19439342.2019.1646782
new_findings: 37 analysis scripts and 62 data files listed; independent same-data replication reports reproducibility, missing-to-zero recoding, small control conversion, and around 90 percent robustness comparisons; observational carded-status gap cannot serve as unconditional upper bound. Synthetic equal-group observed difference 2/5 compatible with ATE -3/10, 1/10, 7/10; conditional sharp interval [-3/10,7/10].
verification: GitHub note/script/index write commits returned and blob identities read. Equivalent synthetic Fraction calculations independently executed locally PASS. Remote script byte version was NOT_RUN because raw.githubusercontent.com DNS failed in local container. No CI requested.
evidence_boundary: nonblind existing published independent replication and synthetic arithmetic; no original data download or original mandal ID matching; no new R E1/E2/E3.
C_today: C008 completed, original blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87 unchanged by this track.
D_this_week: D002 completed, original blob b2556a008eca156222acd3f3b85caa50f85c5fac unchanged by this track.
coordination: checked 12 open codex/* PRs; #1 R257 S53 comparator counterexamples and #3 strict gate unmerged; #2 sync protocol unmerged; R304 S100 latest main handoff remains independent. No competing TH169 entry in main at baseline.
blockers: openICPSR LICENSE download redirected to login; README download 403; Dataverse JS verification; 2014 October revised NBER manuscript and mandal randomization identities not recovered. Do not circumvent access restrictions or pay.
cost: no new paid services, API, Actions dispatch or CI; billing status NOT_VERIFIED.
next: TH170 inspect 3ie tables and missing-to-zero selection sensitivity; retry original archive metadata legally if public access changes; do not infer 2014/2016 unit identity.

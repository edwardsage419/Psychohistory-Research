# TH184 theory handoff
track: theory
subflow: original-theory
run_date: 2026-11-01 Asia/Singapore
observed_head_at_start: 9d4fe722d6b4bb1f5e3c47ea638bbf946cc15b27
target_key: (theory,Paluck2016+ICPSR37070v2,method-theory-v1,school-block-randomization-missingness)
activity: completed theory and exact synthetic audit
status: COMPLETE for bounded theory note only
sources: DOI 10.1073/pnas.1514483113; 10.1073/pnas.1804429115; 10.3886/ICPSR37070.v2; arxiv 1803.02764
results_seen: ICPSR four-school blocks and V2 public-use metadata; 2018 correction adjusted 25% vs unadjusted 23%; artificial 6-school p=1/10 and blocked 8-school p=1/18; 23 local tests each in normal and optimized Python.
output_paths: theory/TH184_SCHOOL_CLUSTER_RANDOMIZATION_BLOCKS_PUBLIC_DATA_VERSION_2026-11-01.md; theory/th184_cluster_randomization_audit.py; theory/INDEX.md; research/coordination/theory/20261031T171120Z-th184-cluster-randomization-handoff.md
evidence_scope: nonblind original-text and metadata reading plus synthetic exact calculations; no real microdata, independent ATE, E1/E2/E3, or prospective historical prediction
commit_sha: same commit as this record; inspect GitHub history
PR: null
ci_status: NOT_RUN; no workflow intentionally triggered, actual billing unverified
billing_checked: false
blockers: original randomization block treatment counts and original 2016/2018 variance receipts not independently recovered; ICPSR data not downloaded
next_action: TH185 public ICPSR V2 dictionary, block variables and source code access, without overlap with R empirical replay

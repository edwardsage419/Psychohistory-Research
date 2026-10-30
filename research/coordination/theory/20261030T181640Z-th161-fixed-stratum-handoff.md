# TH161 theory track handoff
track: theory
subflow: main_theory
run_date: 2026-10-31 Asia/Singapore
run_start_utc: 2026-10-30T18:16:40.198Z
observed_head: 24ccf33c3eab052bb632b313c8fe06edc2a7bfd3
target_key: (theory,WOVO_KANG_IMBENS_ARONOW_SAMII_SAVJE,TH161-theory-v1,fixed_stratum_assignment_peer_exposure_positivity_identification)
activity: complete_bounded
status: COMPLETE
claim: NONE
claim_expiry: N/A
source_links: https://teresasmolina.github.io/mywebsite/WPO.pdf ; https://arxiv.org/abs/1609.04464 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8372033/ ; https://www.e-publications.org/ims/submission/AOAS/user/submissionFile/25166?confirm=053d6417
work_performed: directly reviewed original WOVO sections 2.3/4/tables 1-4, Kang-Imbens 2016 sections 2-4, Aronow-Samii 2017 sections 1-3, Savje-Aronow-Hudgens 2021 sections 3.2/5.2; Basse/Feller and Baird et al abstracts only; independently enumerated all N4 K2 assignments and three observationally equivalent worlds.
results_seen: 15 bounded propositions and 12 audits; fixed K gives peer saturation difference 1/(N-1), direct-effect nonpositivity for equal peer saturation; three synthetic worlds yield identical observed Y=.16+.01Z for all six assignments while own direct effects -0.01,0,+0.01; unknown real WOVO strata N/K and peer network.
evidence_scope: THEORY_NOTE_BOUNDED, nonblind original reading and synthetic exact checks; no worker microdata, independent causal estimates, future predictions, or new R E1/E2/E3; R073 blind FAIL preserved and PESEN v0.1 frozen.
output_paths: theory/TH161_FIXED_STRATUM_ASSIGNMENT_PEER_DIFFUSION_EXPOSURE_POSITIVITY_2026-10-31.md ; theory/INDEX.md ; research/coordination/theory/20261030T181640Z-th161-fixed-stratum-handoff.md
commit_sha: SAME_COMMIT_AS_THIS_HANDOFF (resolve via git log for this path)
PR: NONE
ci_status: NOT_RUN, commit message includes [skip ci]; account-wide Actions not independently verified
billing_checked: NO, no paid APIs/services or CI explicitly triggered
calendar: C008 COMPLETE 2026-10-31 blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87 unchanged; D002 COMPLETE 2026-W44 blob b2556a008eca156222acd3f3b85caa50f85c5fac unchanged
codex: 12 open PRs, #1 R257 S53 coverage gap and #3 proposed fix remain unmerged, #2 sync protocol unmerged; none treated as adopted.
blockers: original AEARCTR-0003311 immutable preregistration and full 2026 final supplement unavailable; original per-stratum N/K, peer network, SMS receipt history, worker microdata unavailable.
next_action: refresh main HEAD and codex PRs; TH162 exposure positivity and anonymized network misclassification; next C009 on next research day and D003 on 2026-W45.

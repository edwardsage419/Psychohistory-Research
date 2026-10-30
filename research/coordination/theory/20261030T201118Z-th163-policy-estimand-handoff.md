# TH163 theory track handoff

track: theory
subflow: TH163
run_date: 2026-10-31 Asia/Singapore
handoff_utc: 2026-10-30T20:11:18Z
baseline_main_HEAD: faf567396955510b13817435468cfed44e9a3ca1
target_key: (theory,SAVJE_AUERBACH_YU_NETWORK_POLICY,TH163-theory-v1,design_conditional_exposure_versus_policy_total_effect)
activity: completed
status: COMPLETE
claim: NO
claim_expiry_utc: N/A
read_scope: main HEAD and 12 latest commits; 12 open codex PR titles/abstracts; TH162, C008, D002, R298 S94, MKT158, project standards and owner sequence; Sävje 2023 arxiv pages 1-17, Auerbach 2024 full 4 sections, Yu 2022 sections1-3, Sävje rejoinder public extract. Nonblind.
source_links: https://arxiv.org/pdf/2103.06471 ; https://academic.oup.com/biomet/article/111/1/21/7606757 ; https://arxiv.org/pdf/2205.12803 ; https://academic.oup.com/biomet/article/111/1/25/7606747
work_performed: 14 bounded theoretical propositions and 12 exact synthetic audits; tested locally with Python standard library, no CI.
results_seen: two synthetic worlds with same design conditional exposure effect +1/10 but policy TTE +1/10 versus -1/2; one world's exposure effect changes 1/5 to 1/10 to 0 across Bernoulli probabilities; fixed K=1 three-person observed results identical while policy effects +1/10, +1/2, -1/10.
evidence_scope: THEORY_NOTE_BOUNDED, synthetic E1-type calculations only; no R scientific E1/E2/E3 increment; R073 blind FAIL, PESEN v0.1 frozen.
output_paths: theory/TH163_POLICY_EFFECT_EXPOSURE_MAPPING_DESIGN_DEPENDENCE_2026-10-31.md ; theory/th163_policy_exposure_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261030T201118Z-th163-policy-estimand-handoff.md
commit_sha: RESOLVE_FROM_GIT_HISTORY
PR: NONE
calendar: C008 2026-10-31 blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87 read-only; D002 2026-W44 blob b2556a008eca156222acd3f3b85c5fac read-only.
codex: 12 PRs open and unmerged at baseline; PR #1 S53 checker gap and PR #3 candidate fix pending; #2 workflow sync protocol unmerged.
ci_status: NOT_RUN; intended commit message [skip ci]; no dispatch.
billing_checked: NO
blockers: no WOVO true peer network, no real network validation, no Sävje rejoinder paywalled full text; full policy identification unsupported.
next_action: refresh main and PRs; TH164 partial identification under network threshold and policy dose; C009 next research day, D003 next week.

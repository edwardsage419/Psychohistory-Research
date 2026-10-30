# E121 R291 S87 prescore receipt binding mutation audit and daily governance

UTC 2026-10-30. Track operations. Target (operations,R291,S87-freeze-4f51f811,original-B-prescore-metadata-binding). Baseline main 94cc5194a3810dd9963a44e0112d605d58dc29f8. Status COMPLETE_BOUNDED_READONLY_NONBLIND_E1.

## Read scope and source identity

Read docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md, README, docs/NEXT_RESEARCH_GATES.md, original239 crosswalk v7.8 first lines (blob 36f24235901172642c46853298aebb421f1a3552), pending154 first lines (blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f), latest R291 S87 freeze, full 24-world JSON, complete 768-row CSV, R/B reports, prior E120, and 12 open codex PR titles/bodies. Checked theory TH156 and R track handoffs. Prior R290 S86 original B checker Git blob 5f1cf8e8299cfff0276b2bbee3d3af69ef0eb869 remains unchanged. No duplicate R290 optimization or oracle mutation study attempted.

R291 S87 freeze commit 4f51f8119ab5faba95fcf4b7b44b63eb6bb3621b is an ancestor of scored result commit 0f399655b2ffab19ee4e2125acc68c913dc1c4d8; compare status ahead=3, behind=0. R291 S87 B checker original blob 53148a6e4c15f7983ace3648bd896f5cfb401df4, original CSV blob d04ce3b99d37f4433e0251190324304de3df19c6, JSON blob ecd62fab3b63f5398abe2cda6e086c4819ce1a0a.

## New actual mutation evidence

The original archived B checker function was extracted without editing its body and executed in JavaScript V8 against the full remote persisted CSV and JSON. Baseline returned PASS, 24 worlds, 768 source rows, 128 zero-mass rows. Then six independent top-level JSON mutations were applied, preserving every CSV row and numerical result.

* Replace parent_R291_freeze with UNVERIFIED_FROZEN_PROTOCOL: incorrectly accepted PASS.
* Delete parent_R291_freeze: incorrectly accepted PASS.
* Replace S87_prescore_commit with NOT_FROZEN: incorrectly accepted PASS.
* Delete S87_prescore_commit: incorrectly accepted PASS.
* Change new_human_E2 from number 0 to string "0": correctly rejected.
* Change R073 from FROZEN to UNFROZEN: correctly rejected.

This is a new four-case receipt provenance coverage gap in the original B function. It is distinct from R290 S86's assert/-O and oracle universe gaps and from earlier R286 metadata findings. Actual freeze ancestry was separately checked through GitHub, so the current unmodified archived S87 freeze is valid as far as the inspected commit ordering establishes. The false accepts concern future tampering and claim verification, not a discovered mathematical error in the 24 exact Brier risks.

Reproduction source research/operations/e121_r291_s87_prescore_metadata_gate_20261030.js records expected Git blob IDs and runs the original B function in a Node vm against the persisted files. In this run the actual six mutation executions were V8, not native Node CLI; the newly archived reproduction script's native Node run remains NOT_RUN. No changes to R or B code or receipts. Scientific S87 status PARTIAL, internal nonblind artificial E1, external independent replication 0.

## Daily cross-track governance

R291 S87 R/B have 768 artificial sources and independent conditional variance check; archived original Node CLI and full scientific acceptance remain OPEN. A track UCDP GED 26.1 codebook/temporal precision reviewed, source ZIP raw bytes and license downstream use still need independent checking before E2/E3. TH156 bounded source audit archived; theory does not displace R series. Codex PR #1 R257 S53 original comparator blind failure and PR #3 strict validator candidate are OPEN_UNMERGED. All 12 codex PRs remain open; no PR accepted into main by this audit. R281 S77 frozen failure, R286 S82 22 false accepts, R284 S80 six gaps and R290 S86 -O/oracle/universe gaps remain prior open issues. No shared index or frozen protocol changed. No Actions invoked. Billing/quota NOT_CHECKED; no paid service used. New E2/E3 0.

Next E122: owner-track follow-up on S87 prescore field binding and R290 S86 issues; otherwise check latest R native execution. Do not promote any old PASS to full scientific acceptance.

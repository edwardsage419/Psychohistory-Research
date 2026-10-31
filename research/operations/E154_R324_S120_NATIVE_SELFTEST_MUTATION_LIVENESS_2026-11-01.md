# E154 R324 S120 original Node CLI and negative-control liveness audit
Date: 2026-11-01 (Asia/Singapore). Baseline main 3f5cef26ed8a20da14f2f9d30ff86c11af88508e.
Target key: (operations,R324,S120_dc2bc2ad,native-selftest-mutation-liveness).
Status: ENGINEERING_DEFECT_CONFIRMED; mathematics PARTIAL_E1_EXTENSION. Nonblind. Read original R324 S120 report, frozen commit, original code, 64-row source, persisted 64-row CSV, persisted JSON, B independent audit summary and R handoff. The B track previously checked the 64 atoms and nine mutations. This E task addresses the original native Node CLI gap and its own selftest.

## Exact input identities and actual execution
Original R324 script Git blob 3e2c099cb638277d55b2bb0aa20af044aa4628e2.
Original R324 source CSV Git blob 1b0062eeea020606a3d510d566da43db03ace8d9.
S120 persisted 64-atom CSV Git blob eeef39b66165e2ec0a918ccedb4f038b078cd05b.
S120 persisted JSON Git blob a95be44193a4a7890203049d5615b4f27c93453e.
The exact source script was reconstructed from the connector response and independently checked against its Git blob. Original and S120 input files were regenerated using that byte-identical source, then independently matched against the fixed remote Git blob identities. This is a hash-verified reconstruction of remote bytes, not a separate download of the four original files.
Runtime: local Node.js v22.16.0. Original --check on the persisted byte-identical files: PASS. Original --emit: generated CSV and JSON byte-identical to persisted blobs. Original --selftest: exit nonzero with 'Error: mutation accepted'. This failure was preserved.
Cause: the first negative-control expression replaces the literal substring ',0,0,0,0\\n' in a CSV that contains no such substring. The replacement is a no-op. The second negative-control modifies JSON atom_count and is live. Original selftest expects two rejections and therefore fails even when the generator is correct.
Independent audit script additionally injects a real change into the first CSV data row and confirms original --check rejects it. Audit script's own assertions pass, while original --selftest remains a recorded FAIL.
## Scientific and governance interpretation
The defect is in the original selftest fixture, not evidence that the archived R324 S120 mathematical output is incorrect. No protocol, original code, original CSV, receipt, or other track was edited. The B track's existing independent calculations and nine mutations retain their previously documented scope. Native --check and --emit are now evidenced; native --selftest gate is OPEN/FAIL. Do not label native CLI fully green. S120 stays PARTIAL_E1_EXTENSION, human E2=0, historical E3=0, external blind reproduction NOT_RUN.
Other tracks: R324 handoff and TH189 were read; R-series learning-first order unchanged. Codex PR #1 and #3 remain open/unmerged at audit time. Original239 and pending154 were not reaudited item by item. GitHub Actions not triggered. Billing balance not independently verified; no paid operations initiated.
Suggested next owner-approved engineering action: add a separate regression test with a guaranteed live CSV mutation, then rerun native selftest without altering frozen scientific results. Preserve original failing output and distinguish any repaired auxiliary checker from historical evidence.

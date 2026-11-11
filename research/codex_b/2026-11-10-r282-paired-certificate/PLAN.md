# R282 S78 same-source paired-count certificate

Base main b3b3b9a1af020130e7c0e1a9cc0b58021be08e8e; independent branch
codex-b/r282-s78-paired-certificate-20261110. Only this directory changes.

Reproduced: archived B strict gate returns exit0 for paired counts replaced by
zero, paired field removed, or schedule declaration reversed. Existing192-row
inverse transition checks and classification summaries remain correct. Root
original_R282_paired_counts and schedules are not read by that gate. No original
numeric error is asserted; report4counts correctly32/48, but persisted proof is
incomplete. R/B reports/addenda/E112 already audited other fields; no matching
paired-count fix found in21 openPRs. R280 temporal selection protection adequate;
R281 frozen-tie failure already documented, leave both untouched.

Independent method: compile frozen XOR transitions as 2x4 GF(2) coefficient rows,
compose twice over six primitive variables. For each sequential schedule vsSYNC
at t1/t2, difference is a2x6 binary linear map of rank r. Uniform64 sources have
kernel size2^(6-r), giving32/48 disagreements for r1/2 without source enumeration.
Bind all192 archived traces to symbolic forms, count actual same-index pairs and
require both routes equal all4 integer JSON leaves; bind schedule declarations.
Reuse pinned old B gate unchanged for full observational/inverse checks on same
immutable CSV/JSON byte snapshot. Strict JSON duplicate-key rejection and exact
paired field shape/types, not general external science/provenance certification.

Files: algebra.py,audit.py,test_certificate.py,replay.py,evidence,report/handoff.
TDD first. Actual native R Node CLI produces CSV/JSON byte-identical; old inverse
B and new supplement on archive/emitted. Normal/-O new12unittest methods;10 real
bad-input CLIs (8old false accepts,2existing correct rejects); record allcommands,
raw streams,sha/version/source pins and math certificate. One own-code mutation
tests independent rank protection. No human scores, changed frozen metrics,
models, splits or historical files. Independent algorithm is ours, not original.

- [x] RED/GREEN12 tests, exact GF2 proof and paired-field repair.
- [x] Native execution, archive identities, old/new bad cases, ordinary/-O.
- [x] One fresh-context review, fix issues with regression if needed.
- [x] Refresh main/PR scopes, draft independent PR [skip ci], attach and inspect
  all-events CI status; no automatic merge/paid operations/scientific closure.

# Codex B incremental handoff — 2026-11-10

target_key: (Codex-B,R074+R075,frozen-2026-10-17,synthetic-donor-multiplicity-tests)
baseline_main: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
scope: only this Codex B directory; no historical program/freeze/receipt changes
evidence: synthetic program verification and internal independent exact oracle

Duplicate-first-donor source mutants pass old R074 20/R075 24 tests because their
session fixtures are identical. New heterogeneous-fixture oracle rejects them,
including equal-row-count omission/repetition. Original trainers agree with the
oracle; no historical human computational error established. Final 103 positive
tests normal and -O pass; raw commands/hashes/logs are in evidence/final-*.
Independent engineering review's empty-input issue fixed and regression-proven.

Do not repeat existing R074/R075 macro-aggregate or R077 sign audits for this issue.
Review/optionally adopt this standalone synthetic acceptance package through its
incremental PR; production caller/CI adoption NOT_RUN. R272 and R333–R340 caller
work remains with existing tracks. Raw-data identity/partner/time extraction and
cross-session physical re-enrolment remain separate scientific/source questions;
no authorization to score new humans is inferred. E2/E3/external-team replication=0,
R073/PESEN frozen, formal queue net closure=0. No merge or CI dispatch requested.

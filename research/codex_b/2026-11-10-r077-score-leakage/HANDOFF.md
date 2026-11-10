# Codex B incremental handoff — R077 numeric acceptance

target_key: (Codex-B,R077,Rev002-2026-10-17,synthetic-score-information-flow)
baseline_main: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
branch: codex-b/r077-score-leakage-20261110
scope: only this directory; no dependency on draft PR #13

Actual current-label mixture and Brier-as-logloss source mutants both pass all
24 archived R077 guards. New independent Fraction/70-digit Decimal score oracle
rejects both and a row-weighting control. Original scorer matches the synthetic
oracle: 68 calls/10200 public output leaves per numerical contract. Normal/-O:
59 positive methods each; no historical human scores rerun. Claiming fit immutable
and target-training-count zero does not prove numeric predictions exclude labels.

Existing R077 archive/sign audit is a different completed task; do not repeat it
as this package's result. A's new #14 integration and #15 S53 authentication PRs
were read during prepublication refresh and are disjoint. R272/R333–R340 caller
work remains with current owners. No production/CI adoption is implied.

Scientific questions still open: raw participant identity/re-enrolment, partner
and time extraction, real-world independence/causality, historical-human numeric
acceptance and external-team replication. New E2/E3=0; R073/PESEN frozen; formal
queue net closure=0. No CI dispatch, paid resource/API, or automatic merge.

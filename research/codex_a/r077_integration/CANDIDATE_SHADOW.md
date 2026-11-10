# A2 continuation — opt-in PR28 synthetic shadow

track: Codex A engineering
subflow: A2 fixed-source callable-candidate integration preparation
run_date: 2026-11-10 UTC
observed_head: 3221a84fba91731071b8931447837e07578210be
status: COMPLETE synthetic engineering shadow; PARTIAL production integration
source_links: https://github.com/edwardsage419/Psychohistory-Research/pull/28 ; fixed head 02989a4944d0f100035927883762d83e4dba4925 ; B28 HANDOFF.md/candidate.py/test_candidate.py
output_paths: research/codex_a/r077_integration/
commit_sha: actual incremental delivery commit in PR29
ci_status: NOT_RUN
billing_checked: existing environment only, no paid API/resource/install/dispatch; CI quota NOT_VERIFIED
evidence_scope: artificial source/count fixtures, no human rescoring or scientific acceptance

## Newly available interface and scope change

After the initial preflight package was delivered, B published #28 with the
callable `candidate.score_exact_brier(fit, sessions)` interface. This continuation
uses that interface directly; it does not port, modify or duplicate B's formulas.
It extends the existing A entrypoint with **explicit `--candidate-shadow` opt-in**,
preserving default behavior and the mandatory artificial-preflight flag.

The existing 40-source snapshot is reused. The fixed B28 manifest's 14 input pins
are checked against the captured current checkout/live bytes; candidate.py,
test_candidate.py and pins.json are exported from the exact unmerged Git head.
Nine inputs overlap the baseline with identical blobs. No proposed file is
treated as main-adopted, read from an arbitrary live B worktree or fetched online.

Run only B's 12 candidate tests and its existing source/case/tiny-case helpers,
rather than repeating the unchanged 59-method baseline. The worker invokes the
actual new callable on the 35 existing artificial targets and the tiny nonzero
fixture. A's wrapper identity-joins by the typed positive-position key, binds
original outputs and the integer witness to the baseline diagnostic, checks tie
votes/exact deltas and preserves the tiny fixture's nonzero direction. This is
engineering contract validation of trusted pinned children, not independent
reimplementation of mathematical scoring.

## Actual results and acceptance recommendation

- Normal/-O: the default entry retains 40 authenticated sources, 35 artificial
  cases and 11 original failures; shadow is absent unless explicitly selected.
- Normal/-O shadow: candidate12 tests pass; 35/35 candidate orders are exact ties;
  the original scorer still has its 11 false-improvement cases. The tiny fixture
  remains two worse sessions with the exact positive delta supplied by B's test.
- All four native CLI invocations deliberately return **2**, top-level
  BLOCKED_ORIGINAL_R077_UNREPAIRED / production_ready false. Candidate shadow
  PASS is strictly artificial and does not override that veto.
- All 16 A methods pass per mode, including four new shadow methods. Initial
  permissive-shadow RED produced six assertion/subtest failures across four
  methods. Duplicate/missing cases, original-output mismatch, bool vote counts,
  wrong exact deltas and tiny-direction corruption reject.
- A fresh read-only review found no important issue; it independently reran 14
  non-mutating helper methods per mode, inspected dependency overlap and native
  evidence, and retained the explicit production/scientific scope. The complete
  16-method runs and native invocations are A's retained execution evidence.

#28 is eligible for owner engineering-merge review in this bounded scope. It
remains an unmerged draft; neither this recommendation nor #1–#20's old approval
authorizes its adoption. A did not rerun B's entire 71-method/other-runtime
campaign or claim an independent mathematical discovery.

## Reproduce and inspect

```sh
python3 -B -m unittest discover -s research/codex_a/r077_integration -v
python3 -O -B -m unittest discover -s research/codex_a/r077_integration -v
python3 -B research/codex_a/r077_integration/preflight.py . --artificial-preflight --candidate-shadow
python3 -O -B research/codex_a/r077_integration/preflight.py . --artificial-preflight --candidate-shadow
```

The last two commands intentionally exit 2. Fixed B18 and B28 Git objects must
already exist locally; the entrypoint does not fetch missing objects. Raw command
streams, candidate test stderr, source identities and RED/GREEN are in
`shadow_evidence.tar.gz`; all members were SHA256 verified and listed in
`shadow_evidence_members.json`. Current delivered hashes are in
`artifact_hashes.json`. The earlier evidence archive and initial commit8e50c7e2
remain intact. Source-sidecar data records 40 baseline entries and 17 candidate
entries, with overlap explicit rather than counting them as independent sources.

## Remaining blockers and next action

The original scorer is still unchanged and not repaired. The candidate implements
exact mathematical formulas, not bitwise old-float emulation; its source-count
consistency checks do not establish actual donor membership, timeline validity
or dataset qualification. Real-data invocation, revised votes, scientific
reacceptance and any frozen-protocol/source revision remain NOT_AUTHORIZED /
NOT_RUN. Historical human impact is UNKNOWN. R073/PESEN and old results remain
unchanged; new human/E2/E3/external-team evidence and formal closures=0.

blockers: specific merge authorization; ChatGPT/owner scientific and frozen-source
disposition before qualified human shadow/rescoring. No CI quota confirmation.
next_action: hand off this callable synthetic integration and retained original
failure to the scientific owners for disposition; only then wire qualified data
behind explicit source checks. Do not install an original-scoring hook or change
default scoring based solely on these synthetic results.

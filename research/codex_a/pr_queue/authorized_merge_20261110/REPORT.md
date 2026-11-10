# Authorized engineering adoption — pre-merge evidence

The user explicitly authorized merging all candidates in the delivered plan. This supersedes the earlier no-merge restriction for PRs #1–#20 only. PRs #21 and #22 are outside this plan and remain open. Scientific acceptance remains with ChatGPT; no paid CI, automatic dispatch, history deletion, force push or branch deletion is authorized.

## Actual validation

Base main: `81188642a7d32d94d8cc4773785a3d2b89349ebb`. The source change since the previous main is an added research coordination audit; it is preserved. A dedicated clone created real sequential local merge commits in this order:

`1, 3, 15, 7, 5, 8, 9, 17, 13, 16, 18, 19, 20, 4, 6, 10, 11, 12, 2, 14`.

All 1,234 paths added by these candidates are additions: no preexisting main path is overwritten. The combined tree is `25e588b455ed300cd92cb0b949cb65e1e92ddef2`. The pinned PR heads and each local merge commit are recorded in `candidate.json`. This evidence increment changes #14 documentation/evidence only after that snapshot; executable-source equality is checked separately before adoption.

`run_matrix.py` executes `python3 -B [-O] -m unittest discover -s <scope> -v` in the isolated merged tree. All 19 positive scopes passed both modes: 38 suites, 270 methods per mode, 540 executions total. Full commands, counts, exits and raw logs are in `evidence/matrix.json` and `evidence/tests/`. Tests left tracked candidate files unchanged. No whole-repository, Python 3.11, external scientific or production-caller acceptance is claimed.

The #1 comparator probe reproduced six false accepts and met seven probe expectations. Original R077 `legacy_regression.py` returned exit 1 with 11 failing subcases in each mode; this is a known original defect, not a passing suite or a fix to that original program. S53 remains blind FAIL / scientific PARTIAL; R170 witness ordering remains NOT_ESTABLISHED / scientific PARTIAL.

## CI and merge guards

Parsed all 560 current workflow event definitions: only push/path-filtered and manual dispatch triggers. None of the 1,234 paths matches a push trigger; no workflow is changed or added. Merge commits use `[skip ci]` as an additional guard. No workflow dispatch is requested. CI absence is not a pass.

Before each GitHub merge: require the expected main SHA and approved candidate head SHA, mark that candidate ready, merge using the exact head SHA with a merge commit, then verify its two parents and tree against the locally validated sequential tree. An unexpected main/head/tree change or permission/policy error stops the remaining merges. Branches and historical evidence are preserved.

This file records PRE-MERGE validation, not a claim that remote adoption is complete. GitHub PR merged status and the final delivery report establish actual remote adoption. The evidence-carrying #14 commit is merged last.

## Remaining work

Review #21/#22 independently. Address the original R077 defect only under a separate reviewed change; continue to preserve frozen protocols and original results. Production binding and formal scientific acceptance remain open.

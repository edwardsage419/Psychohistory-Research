# R077 mainline integration checklist — engineering veto retained

Recorded 2026-11-11 11:50 Asia/Shanghai. Base main:
`ce6ae2dbf96f5346cf5062de3773b72c0ab90446`.
Independent A branch; original preflight/scorer and B directories are untouched.

## Actual status

**COMPLETE**: new executable `mainline_checklist.py` verifies adopted Git/worktree
identity for B18's40 inputs, B28's14 inputs plus3 candidate/program files; verifies
all13 members of the fixed A29 archive; reuses existing `classify` and
`validate_shadow` to check retained diagnostics. No new scoring math, framework,
human data or mathematical subprocess is introduced. Only Git read commands run.

**BLOCKED**: production adoption. Success still exits2, `production_ready=false`,
11 original synthetic failures retained,35 synthetic corrected orders matched.
Historical human impact is UNKNOWN; no production scorer hook is installed.
No override/approval flag can turn this tool into production authorization.

**NOT_RUN**: new human scoring, new mathematical suites, scientific reacceptance,
actual CI, external replications, downloads and paid resources. Source-qualified
retained evidence is explicitly distinguished from a new mathematical run.

## Commands actually tested

```sh
python3 -B research/codex_a/r077_integration/mainline_checklist.py .
python3 -B -O research/codex_a/r077_integration/mainline_checklist.py .
python3 -B -m unittest discover -s research/codex_a/r077_integration -p test_mainline_checklist.py -v
python3 -B -O -m unittest discover -s research/codex_a/r077_integration -p test_mainline_checklist.py -v
```

Checklist: expected exit2 both modes. Three unit methods pass both modes: actual
identity+veto checks; forged success/erased original failure rejection; retained
input-identity mismatch rejection. Python3.12.14. Initial missing implementation
caused an import error; this was a RED scaffold, not a discovered R077 defect.
Existing R077 numerical failures remain unfixed in the original scorer.

If source bytes change, first review the change and update the explicitly pinned
versions; the checklist fails closed on unreviewed adapter identity. Only then
rerun existing artificial entrypoints as needed:

```sh
python3 -B research/codex_a/r077_integration/preflight.py . --artificial-preflight --candidate-shadow
python3 -B research/codex_a/r077_integration/preflight.py . --artificial-preflight
```

Both require exit2, not a production pass. Already unchanged/qualified synthetic
math suites were deliberately not repeated in this package. Rollback is to omit
`--candidate-shadow` or stop optional preflight/checklist; original scorer is not
replaced. No frozen model restoration, data rewrite or history deletion needed.

## Executable checks and mainline prerequisites

| Item | Status / exact boundary |
|---|---|
| B18 original and diagnostic source identity | COMPLETE40 objects, fixed Git+HEAD+live bytes |
| B28 candidate inputs/program adoption | COMPLETE14+3 objects, same three-way binding |
| A29 synthetic result receipt | COMPLETE fixed Git archive13 members/hash/length |
| Original failure and shadow result validation | COMPLETE retained11 failures/35 corrections, production veto |
| Candidate API | `score_exact_brier(fit,sessions)` returns `scores`, `exact_Brier`; optional artificial adapter only |
| Human source identity/license/complete risk set/timeline/donor qualification | NOT_ESTABLISHED by this tool |
| Frozen scoring adoption and scientific comparison authorization | BLOCKED_NOT_AUTHORIZED |
| Production caller hook / same qualified-data old-new comparison | NOT_INSTALLED / NOT_RUN |
| Historical human scientific impact | UNKNOWN_NOT_RECOMPUTED |
| Formal scientific reacceptance | NOT_RUN, owned by ChatGPT/R mainline |

Candidate count consistency is not source qualification, donor authentication or
timeline validation. The new tool independently closes the adoption gap: unlike
merely loading3 files from a fixed Git object, it also requires those files to be
actually adopted at current HEAD and unchanged in the live checkout. It accepts
only the two reviewed adapter hashes (main and PR30 literal-only update).
Current Git bytes are authoritative; stale historical UNMERGED text is not a
source/deployment test. Historical reports are preserved verbatim.

## PR28/29/30 and concurrent B31

* PR28 MERGED: head `02989a4944d0f100035927883762d83e4dba4925`, merge
  `8c41317582923885af4ecfacae985305c2c75bd0`.
* PR29 MERGED: head `714ec9a7e257fff98044f0f68391944d526ac1d1`, merge
  `c703f0dc6fc35b00d21c7dd7cd586a6ff9d9b71e`.
* PR30 OPEN draft, head `8005fcb75e9e20545adb245edd45d72dbc374632`,
  mergeable at read time, no checks. Independent engineering review confirmed
  only two preflight literal replacements (UNMERGED→PINNED and CLI help), metadata
  receipt and artifact manifest. All10 artifact identities verified. Its native
  `--help` exits0 with pinned wording. No scoring/input/math/production-veto edit.
  **ENGINEERING_ACCEPTABLE; separate merge authorization required. Not merged.**
  Its recorded normal/optimized outputs have unchanged numeric diagnostics and
  source identities. No irrelevant full mathematical suite was repeated.
* New PR31 OPEN draft, head `03cf49d8970f273bb58ef0bfd125252166482dce`:
  Codex B's scalar Brier/integer certificate and human-shadow readiness package.
  Read its current scope/PR handoff; not adopted or scientifically accepted here.
  It reports current complete human risk set not recovered and leaves human
  impact UNKNOWN. Future scientific source/double-run qualification should use
  B's plan after mainline review, rather than a second A mathematical algorithm.

PR30 and31 authorization is not inherited from prior PR1–29 merges. This package
changes none of their files and merges neither. Empty check lists are NOT_RUN,
not CI PASS. All live PR snapshots are archived with the observation context.

## Evidence, identities, independent review and next task

`checklist_evidence.tar.gz`/`checklist_evidence_members.json` preserve actual
commands/outputs, review, PR30 native metadata check and dated GitHub snapshots.
`checklist_artifact_hashes.json` identifies this new package. Existing manifests
and archives remain untouched to avoid conflict with PR30/historical evidence.

Original scorer blob `70889bd15c6fd943bdb07ab3ae1f60c943ebc538`, SHA256
`247e682681bd606db3967732aae3cbfc4af41766ffd31c45adcdc839016d593a`.
Candidate blob `b050fcf14c3507bdb044365047e939cca14cccac`, SHA256
`9be76dbf2441ecd842f8b51f613847299b80408cdef644ff9060ace6948f5f53`.
Retained A29 archive SHA256
`ea6324c5e8dc07c74a319858f3d758e624f74172735dd8dbdccb1f2533d6527a`.

Fresh read-only review found no Important issue, confirmed no math execution/
scientific promotion, and ran all3 lightweight methods. No files edited by review.

Next task: independent engineering review of B31 source/receipt interfaces and
its qualified double-run plan, keeping mathematical ownership with B and actual
human scoring/frozen scientific adoption blocked pending mainline decisions.
No arbitrary queue closure: R-series scientific acceptance remains separate.
Delivery is an independent draft PR; GitHub commit/PR and subsequent readback
identify the final version. No production merge is performed.

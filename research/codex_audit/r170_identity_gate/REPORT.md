# R170 evidence byte-identity supplement

Status: COMPLETE for this byte-identity gate. R170 full frozen extension acceptance: PARTIAL. Date: 2026-10-29 UTC. Observed main: `e2614fec5027247de328a5aeef295c4ed3bc9338`.

## Problem and bounded result

Draft PR #8 compared all 288 R170 state laws with exact arithmetic. Its runner records three historical identity comparisons as booleans; a future changed source/summary or receipt can yield `false` while the runner still writes `status: COMPLETE`. This is a static review finding about the prior runner, not a newly executed counterexample against its full model computation. The authentic prior receipt passes all three comparisons. No historical false result is alleged.

This separate gate hard rejects any changed byte in four pinned original files before trusting their summary. It then requires the full B receipt length and SHA256, and B Python source SHA256, to match that summary. It does not execute either model. Even a semantically equivalent reserialization is rejected because the target is exact historical byte identity. A new legitimate source version requires an explicitly reviewed new pin set; do not loosen these checks to accept it silently.

The authentic full B receipt from fixed draft PR #8 commit `fd0d2c65084d1ef99b6040ce0464b237c38431b5` has 23,004 bytes and SHA256 `8cdf817c0e32cd48ea1a70dd1f9d0c5fc55022c8d355981157d0181934ab2565`. All four original Git blob IDs still match current main. This supplement leaves PR #8 and original research files unchanged. It imports no code from PR #8; only its fixed receipt is an input. The receipt can alternatively be regenerated with the original B Python CLI, preserving raw stdout bytes.

## Reproduce

Use Python 3.12 standard library only. At a repository checkout containing these new files and the four pinned original inputs:

```sh
python -B research/evidence_audit/r170_b_edge_utterance_20261026.py > /tmp/r170-b-full.json
python -B research/codex_audit/r170_identity_gate/identity_gate.py . /tmp/r170-b-full.json --output /tmp/r170-identity.json
R170_FIXTURE="$PWD" R170_B_RECEIPT=/tmp/r170-b-full.json python -B -m unittest discover -s research/codex_audit/r170_identity_gate -v
```

The first command is an alternative regeneration step, NOT_RUN in this round. This round reused the previously archived fixed receipt and ran the gate against the local exact-source snapshot. `identity_result.json`, `execution.json` and the raw logs record actual paths, commands, versions, outputs and hashes. Use a distinct output path for each concurrent run. Outputs aliasing any input or the gate script are refused without altering those protected files. Ordinary result paths, including paths under the source root, are supported. Other failed runs remove a preexisting success output and return a nonzero exit with a PARTIAL message. Inputs must remain stable during a gate run; no locking or filesystem snapshot is supplied. This gate authenticates bytes read during the run.

Ten tests first failed against an intentionally empty stub (10 assertion failures, zero errors; `red.log`). After review identified a stale-success path-policy boundary, an eleventh targeted regression failed before the fix (`red_output_policy.log`). The final normal and optimized-mode runs each passed eleven tests. Cases cover authentic inputs, four changed source files, same-length receipt corruption, semantic-only equivalent receipt bytes, missing receipt, stale success invalidation, overwrite refusal, and stale success under the source root. Private temporary copies hold all mutations. Tests and gate do not alter historical sources.

## Limits and remaining work

Matching hashes authenticate correspondence to the pinned repository summary, not who ran it, when it ran, a signature, or external replication. All prior outputs were already seen: NONBLIND internal engineering evidence supporting artificial E1. No new model worlds, human E2, historical E3, or external-team replications. The first-witness sorting ambiguity described in PR #8 remains PARTIAL; byte identity cannot resolve it.

Full repository tests, original R170 111-test suite, original large result audit, model computation this round, and GitHub Actions: NOT_RUN. Native Git checkout/worktree is unavailable in this environment; delivery uses an isolated fixed-SHA API snapshot and only additive files. No paid API, cloud resource, dataset purchase, workflow dispatch, or new automation was used. GitHub account billing/free CI quota is NOT_VERIFIED; commits and PR include `[skip ci]`.

Next useful R task: after rereading fresh handoffs, close the R271 S67 archived native Node CLI/persisted-receipt gap, if still open. This task is separate from the source-identity supplement and needs its own input manifest and negative controls.

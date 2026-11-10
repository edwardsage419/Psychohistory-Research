> Historical scope at commit f804fe1f. Current A1 v2.0 coverage and PR dispositions are recorded in [A1_V2_REVIEW.md](A1_V2_REVIEW.md).

# Independent engineering review of PRs 21–23

Base main: `25bcd51dd58bf0c245ae84c563406e679a966b5a`.
This package adds Codex A CLI regressions and independent execution evidence.
It does not modify Codex B implementations, research files or frozen protocols.

| PR | Fixed reviewed head | Target | Engineering disposition |
|---|---|---|---|
| #21 | `4e2bfb58971db2b3a420fa0587f5a5d41f704424` | R279 / S75 native replay | Both modes reproduced; no implementation defect found in this scope |
| #22 | `c4aa392a39e6cddad9857febfed29f3b00e41dd9` | R282 / S78 GF(2) paired certificate | Both modes reproduced; independent identity/schema CLI checks pass |
| #23 | `30050722a94ad68640b9a12cbeeb2a0a7e3e014c` | R289 / S85 heldout contract | Both modes reproduced; independent identity/schema CLI checks pass |

The main `audit_queue.py` was reused without modification: three PR/main checks
and three PR pairs had no textual conflict or overlapping proposed paths.
A dedicated clone also performed real sequential local merges of all three.
All differences from main were new Codex B paths. These local merges were not
pushed and do not establish main adoption. Earlier #1–#20 adoption is unchanged.
The three targets are distinct and have no new cross-PR functional dependency.
Older #21/#22 bases preserve identical pinned research inputs on current main;
their age alone does not establish a source mismatch.

## Actual execution

Each proposed `replay.py --output NEW_DIRECTORY` ran in normal and optimized
Python 3.12.14 with Node v24.22.1, without dependency installation or network.
All six runs exited 0. Per mode: #21 invoked 84 original unittest methods;
#22 and #23 invoked 12 candidate methods each. That is 216 existing/candidate
method executions across both modes, separately from the new A tests below.
We rehashed all 192 captured stdout/stderr streams and all 39 recorded source
fingerprints per mode; every recorded hash matched. Tracked candidate files
remained unchanged.

- #21 regenerated all five core/S75 artifacts byte for byte, checked 36
  population fields, and reproduced all nine expected bad-input rejections
  per mode. Zero-mass rows remained present.
- #22 regenerated both original artifacts byte for byte. Its archived B gate
  still accepted eight bad paired declarations; the proposed supplement rejected
  all ten bad artifacts and detected its intentionally capped-rank mutant.
- #23 regenerated both original artifacts byte for byte. Its two deliberately
  corrupted source copies still emitted false-success artifacts; the proposed
  gate rejected them and four persisted controls. The single-route tie control
  was already rejected by the original program and was not miscounted as a new
  gate rejection.

The new `test_cli_contracts.py` independently invokes fixed #22/#23 real CLIs
from temporary exports of immutable Git objects. Both modes pass **10 methods,
35 real CLI calls each** (11 valid and 24 rejected artifacts per mode), with no
skips. Coverage includes independent per-schedule CSV rotation, independent
result-collection reordering, duplicate identities, duplicate keys at root and
nested depths, nonfinite JSON, bool/float identity confusion, source coverage,
missing/extra success-shaped fields and the mandatory original B executable pin.

One fresh read-only review found a P2 gap in the initial A tests: synchronized
reversal preserved alignment and could miss a positional join. In one fix pass,
independent permutations were added. Disposable positional-join mutants pass
the synchronized-only control but now produce five expected assertion failures.
A disposable default-JSON-parser mutant produces four expected duplicate-key
assertion failures. These are test-sensitivity controls in temporary copies,
not defects found in the unchanged proposed validators. No re-review was used
after the covering RED/GREEN verification. No other important finding remained.

## Reproduction and evidence

The fixed PR Git objects must already be available locally; missing objects
fail, rather than skip or silently download. No candidate checkout is needed
for the new A tests:

```sh
python3 -B research/codex_a/pr21_23_review/test_cli_contracts.py -v
python3 -O -B research/codex_a/pr21_23_review/test_cli_contracts.py -v
```

For the complete B replays, use a separate clone with the three fixed heads
locally integrated and run each module's `replay.py --output <new-directory>`
in both modes. Exact commands, versions, source hashes, Git blob identities,
raw output streams, candidate commits/tree, queue inventory, and A CLI case
records are in `evidence.tar.gz` (161 members). `evidence_members.json` lists
each member's SHA256; all members were re-read and verified after packaging.
`artifact_hashes.json` covers the delivered files with SHA256 and Git blob IDs.
The `cli/` proof scripts accept the current test-file path; the positional
proof's `--synchronized-only` flag reproduces the weaker control. RED proofs
intentionally exit 1; clean tests exit 0.

## Status and boundaries

Prepared on an independent Codex A branch for a new draft PR. #21/#22/#23
remain open drafts: the previous explicit merge authorization covered the
delivered #1–#20 plan. No merge, original PR branch update, CI dispatch,
fee-bearing resource, source rewrite or formal scientific acceptance occurs
in this package. Empty Actions/check lists are not CI PASS or free-quota proof.
Python 3.11, other platforms, whole-repository tests and production binding
remain NOT_RUN. No single repository-wide Python/Node test command was found.

The old R077 regression remains a separate known failure; this package neither
fixes nor reclassifies it. Human/E2/E3/external-team evidence and formal research
queue closures added: zero. R073 and PESEN v0.1 remain frozen. Engineering
acceptance of these bounded CLIs is not scientific reacceptance or proof that
arbitrary implementations preserve real chronological holdout.

Next: hand off the reviewed #21–#23 candidates for disposition, then continue
the source/receipt/production-binding queue under the same scientific limits.

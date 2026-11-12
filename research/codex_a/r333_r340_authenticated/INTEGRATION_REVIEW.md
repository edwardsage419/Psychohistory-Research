# Current PR integration and R127 predeployment acceptance

Observed main: `d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c`, 2026-11-12 UTC.
Read current workflow requirements, research-sync rules, formal154-item queue
(27P0/82P1/45P2), PR states and B handoffs. No frozen protocol or queue change.
This review updates present integration state; historical PR35 evidence stays intact.

## Fixed candidates and conclusions

| PR | Reviewed head | Engineering disposition |
|---|---|---|
|30|8005fcb75e9e20545adb245edd45d72dbc374632|APPROVE_CANDIDATE, metadata-only behavior preserved|
|31|b928dc8d97202005560e2e73129c13adfd374097|APPROVE_CANDIDATE / REQUIRES_PR30; B-owned pin correction now adopted|
|32|16778c53b2e7a2c590ff65c854b1f7034169050d|APPROVE_CANDIDATE, formal workflow activation unapproved|
|33|9d5041acdfc3f13a002e2cfbb6c33d4dfaed6af4|APPROVE_CANDIDATE, production veto retained|
|35|9ae4eb923b7d1cbc78fdc0c81cddee591efc68ef|APPROVE_CANDIDATE, evidence/handoff; old candidate-pin experiment is historical|
|36|211f90b2509a9e958b560780bc30d7a488a518b9|APPROVE_CANDIDATE, bounded R273 original/native replay|

All remain OPEN draft, not adopted on main. At snapshot all six merge with main
and all15 pairwise Git merge-tree checks have no conflict. Changed-path overlaps
are empty. Git text mergeability alone did not detect the old30/31 runtime pin
mismatch. Reused the existing audit_queue.py for Git analysis, not a new framework.

B corrected31 during this session: commit5030d6b3 plus its delivery docs now pin
PR30 adapter blob833512df7f3fde37f84a76df30bc176ffc58c6b7, bytes13835, SHA256
8e04095a1b984d47245563a363309f5a7e332326584e53f0a17545235cf8ef23.
The other33 old files remain byte-identical; the old manifest is separately kept.
Independent review verified both maintenance runs'9 commands/18 streams each,
22-source capture,20 unchanged fingerprints, retained failure controls and help.

**Do not apply A35's pin patch again.** Updated31 deliberately rejects current
main WITHOUT30; it must follow/combine with30. Original03cf49d8 evidence remains
historical, not overwritten. We only reviewed actual B commits; A never edited
B's files. The old A35 verify_combination.py intentionally simulated a candidate
pin refresh and must not be used as proof B adopted it.

PR36 review:18 pins,22 fingerprints per mode,32 commands/64 streams,5 artifact
identities and8 domain negatives per mode verified. Its new5 tests passed normally
and with -O;576 paired atoms link to1728 original model records and27 risks.
Original emitter remains NORMAL in both B parent modes; no optimized original
assert claim. Source qualification and scientific acceptance are separate. R077
actual source bytes/license/risk mapping and human impact remain unresolved.

New PR37, head a6f51d4b4805ce585f791ecb1cade7b6528bd594, is B's R277 native package.
Read its scope only to avoid concurrent work; NOT_REVIEWED/NOT_ADOPTED here. It
changes B's separate R277 directory and does not intersect this entry's56 inputs.
No R277 computation or implementation was performed by A.

## Actual six-PR combination after B adoption

A disposable latest-main clone received only the actual six fixed PR diffs.
No candidate B patch was applied. Source-only executions:

* B31 capture: normal/-O exit0,22 identities including the adopted adapter.
* A33 checklist: normal/-O expected exit2; production_ready=false;11 original
  synthetic failures and35 corrected synthetic permutations remain recorded.
  Existing retained validators are reused, not new scoring computation.
* PR32 prepare generated the SAME original R127 patch; it applied in the TEMP
  clone, gate.capture authenticated5 sources, then all3 target buffers restored
  byte-for-byte by reverse application. No R127 math/test campaign rerun.

Local combined fixture e72709b613d0c8b29c06488f413c0af3a70ff16b;
local R127 candidate fixture055356825603530ee9809a3dda65ddafd1e67bca.
These are NOT GitHub deliveries/runs. combined.bundle preserves the exact latter
fixture with public main d4740c2c prerequisite; bundle SHA256
57ac0012ebb4dc99b91b86a4a48522e52d3815fa7ad1d8b7e10fe6f65a5f6d08.
Six native command exits and12 streams independently reviewed; source-only means
no numerical R077/R127 campaign or human rescoring in this combination.

PR35's8 artifact entries and100 archive members were authenticated and reused.
Its local3.11 tests, R127 assert/log/E2/sidecar/no-op/conflict failure evidence and
rollback were NOT repeated. Fixed R127 patch SHA256 remains
ed2b03c7985d93db9c915abaa4e3bffeae665803dbd00db8364eba14a62cf44e.
Current original workflow blob4b22f653dc7516bb31ead23e45dcf7f62261d79d and all3
patch preimages still match the reviewed candidate manifest. Real workflow stays
unchanged and still requires the candidate repair before new formal acceptance.

## Exact R127 mainline deployment checklist

| Gate | Actual observation | Required authorized operation and success criterion | State |
|---|---|---|---|
|Owner review|PR32 has no GitHub comments/reviews; PR35's new B comment concerns pin adoption, not R127 deployment|R-mainline records approval of the exact patch/version and helper dependencies; re-read latest target blobs before applying|BLOCKED_OWNER_APPROVAL|
|Git archival and concurrency|Immutable A sidecar path and STOP-on-remote-advance rule are documented proposals|Approve new per-run sidecar archive location, unchanged historical receipt and no rebase/force; only that sidecar may enter result commit; identical retry no-op and conflicting update reject|PENDING_POLICY_ACCEPTANCE|
|Runtime|PR35 locally verified standalone CPython3.11.17; actual setup-python/ubuntu runner never tested|After cost/CI authorization, record actual interpreter/runner identity and obtain60 original tests/138 typed fields with required negative controls; local build is not proof of GitHub binary equivalence|LOCAL_COMPLETE_ACTIONS_NOT_RUN|
|External provenance|Local run/attempt/job keys are claims; numeric job ID and external attestation absent|After authorized run, independently read official run/attempt/jobs/logs and source/result commits; match tested checkout/workflow/source/log hashes, job completion and archived sidecar; keep tested vs result commits distinct|NOT_ESTABLISHED|
|Cost eligibility|Public repo is visible, but free quota/runner eligibility not confirmed|Owner confirms selected actual Actions resources incur zero new cost BEFORE dispatch; do not infer billing eligibility from public visibility or empty run lists|NOT_VERIFIED_NO_DISPATCH|
|Bot and branch writes|Current integration credential advertises push; Actions permissions/default-token/main-protection reads each returned HTTP403|Owner confirms actual bot contents:write and branch policy permits intended sidecar write; no secrets in logs; failure must stop and leave remote evidence intact; do not test main push before authorization|BLOCKED_PERMISSION_EVIDENCE|

No denied API was bypassed or repeatedly retried. Repo write permission for the
current credential does not prove Actions-token rights. No workflow, branch rule,
credential or billing setting was changed. Read failures are recorded with the
exact endpoints and prior tool-response provenance.

Precise future authorized steps: adopt helpers, R-mainline applies exact three-file
patch, confirm zero-charge runner and bot policy, authorize a controlled CI run,
then independently check official API run/attempt/job metadata and Git result
readback. Successful local tests or source identities alone satisfy none of the
missing deployment authorizations or external provenance gates. Existing historical
run39348775741 is not re-attested by a future candidate run.

Before deployment, reverse-patch check restores three reviewed targets in the
isolated clone. After deployment, any rollback must use a new authorized wiring
revert and preserve all historical/new receipts. Stop on remote advance/push
failure; do not reset/rebase/force public history. Scientific acceptance remains
a separate R-mainline decision and05-003 stays provisional.

## Integration order and remaining boundary

Technical candidates32/33/35/36 are independent and may be reviewed/adopted without
running the real R127 workflow. Adopt30 BEFORE updated31, or coordinate them as
a reviewed pair; verify B capture and A33 source/veto on their actual combined
checkout. No old pin fallback or second patch application. No merge is authorized
by this report: prior authorization covered1–29 only.

COMPLETE: six-candidate Git/runtime review, actual B-owned dependency resolution,
source-only combination, PR36 engineering acceptance and R127 deployment checklist.
PARTIAL: mainline/production integration. NOT_RUN: real CI, human scoring, formal
scientific reacceptance, new E2/E3. R073/R077/R127/PESEN/frozen history unchanged.
The real next deployment action needs owner approval; independent local P0 work
continues in the accompanying authenticated R333–R340 entry, without new math.

Final queue observation also found B PR38 (R275 S71 optimized guards), head
fbf71dcaee98508a0a861518bfcc6bb768da5a81. Like37 it is a separate, unreviewed B
package; this report does not award it acceptance or perform its computation.

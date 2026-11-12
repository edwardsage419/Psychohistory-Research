# B-owned PR30 dependency requalification (not a new mathematical validation)

Starting main d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c; old PR31head03cf49d8.
PR30head8005fcb7; A35patch at9ae4eb92 reviewed independently. Only PR31pins.json's
preflight entry changes: blob/bytes/SHA256. All33other original PR31files remain
byte-identical, including mathematical code, raw evidence and original reports.
The old entire pins manifest is preserved in evidence/pin-refresh-20261112/.
Historical snapshots still describe their original run; they are not overwritten
or automatically relabelled as executed against the new adapter.

Reviewed PR30 scope: preflight.py plus artifact_hashes.json and deployment
metadata only. Preflight has exactly two literal replacements (deployment status
and --help); reverse-normalized ASTs are identical. Formula/scoring/source/model/
data/freeze/production veto logic is unchanged. The approved A35patch equals the
independently derived pin-only manifest. Any other file/literal/source change
aborts this qualification instead of automatically accepting a hash refresh.

| preflight identity | Previous | Qualified PR30 candidate |
| --- | --- | --- |
| Git blob | 2a6d2e6a45e5bce1d2f676613a57ab7668f4ed39 | 833512df7f3fde37f84a76df30bc176ffc58c6b7 |
| Bytes | 13845 | 13835 |
| SHA256 | 101adc1271e7ccbcf10f02e62afc0916bccd96d80278e9258cc9bfae6f45baaf | 8e04095a1b984d47245563a363309f5a7e332326584e53f0a17545235cf8ef23 |

New pin manifest blob43e06956dc98d387c7eaf738f738cd170359d97f, SHA256
1bf54f4da4cbd02b137050dc5237262289ac350ec60fa91f2171f17cf2c85ac6.

Actual verification (repository root, new output directory):

```bash
python3 -B research/codex_b/2026-11-11-r077-scientific-readiness/maintenance/verify_pin_refresh.py --output research/codex_b/2026-11-11-r077-scientific-readiness/evidence/pin-refresh-20261112/run-final
```

The helper uses a disposable local shared clone of fixed latestmain+PR30+old31;
no real A-owned file is edited. Ordinary/-O source captures before refresh exit1
with the expected SOURCE_BLOB:preflight.py. After exactly A's reviewed patch,
both captures exit0/22fingerprints. Only preflight.py and the pins-manifest's own
fingerprint differ from the old receipt; all20other fingerprint records match.
The helper is nested under maintenance so the existing root *.py capture set
remains22. It does not create a second verifier or loosen the old capture code.

Finite regressions use retained A29 output, not new model calculations:
classify retains production_readyfalse/exit2/11old failures, validate_shadow
retains35corrected cases/tiny direction and returns PINNED_CANDIDATE metadata.
Corrupting the retained tiny direction is rejected. Native --help shows the new
wording. Changing an unrelated B candidate byte makes source capture exit1 in
both modes.9recorded commands/18stream hashes per complete helper run; no new
unittest-method or mathematical-score count is claimed. Initial run and final
scope-guard run are separately retained. No full7/71method campaign rerun.

Important integration requirement: this revised PR31depends on PR30's qualified
adapter version. Current main WITHOUT PR30 is expected to reject the new pin.
Do not interpret that as a mathematical failure or make the capture accept two
versions opportunistically. Codex A must combine the corresponding fixed heads
in the reviewed adoption order and update its fixed integration references.
No remote merge/rebase/force-push/CI/scoring activation is authorized here.

R077 human source/license/session mapping barriers remain unchanged; no network
probes, real data, human fit or human scoring. Historical vote impactUNKNOWN.
This closes only the known metadata-source dependency in the combined proposal.
New evidence in this subdirectory, old scientific evidence unchanged.

One fresh read-only review found no actionable issue and independently ran the
complete helper with source-only captures. Details/command/limits are in the
new independent-review note. PR31 is updated incrementally without rebase or
force; Codex A is notified with the new fixed head and manifest identity after
remote readback. Do not apply A35's old pin patch a second time after this change.

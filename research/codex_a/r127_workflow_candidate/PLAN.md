# R127 workflow candidate — implementation and acceptance plan

Base main ce6ae2dbf96f5346cf5062de3773b72c0ab90446. R127 protocol and
R-mainline handoff remain authoritative. All real changes stay under this Codex A
directory. Never edit/apply a patch to the real workflow during this task.

Reuse #26 gate.py as the sole log/source/stage-two validator. Prepare a precise
three-file patch: workflow wiring, its entry in gate pins, and the pin-manifest
hash constant. Original model/test/report/receipt bytes stay fixed. Recomputing
the workflow pin is explicit and reproducible, never a permissive fallback.

The frozen protocol requires Git archival; artifact-only publication cannot be
silently substituted. Candidate publication archives a new immutable sidecar in
the Codex directory, keeps the historical receipt intact, treats identical
already-committed bytes as a no-op and stops if remote main advanced. No automatic
rebase/force push. Only explicit main-ref publication is proposed in the YAML.
R-mainline approval and free-CI confirmation are required before activation.

Tasks:
1. Build/test immutable sidecar and claimed run/attempt/job-key metadata using
   gate26; do not claim externally authenticated CI IDs/time from local tests.
2. Build deterministic guarded patch/manifest; test baseline, stale/partial
   application and already-applied states in a disposable clone.
3. Apply patch only in temp clone, commit locally, run real60/138 normal/-O and
   invalid-log/E2/count/source controls. Historical receipt/freeze hashes stay fixed.
4. Test publication/no-op/concurrent remote/dirty tree/immutable conflict against
   local bare repos only. No network pushes or Actions runs from tests.
5. Produce R077 executable integration checklist and retain PR30 source-only
   independent review; source changes are required before repeating math suites.
6. Fresh read-only review, one fix pass if needed, independent draft PR and remote
   readback. All source IDs/raw outputs and remaining scientific boundaries saved.

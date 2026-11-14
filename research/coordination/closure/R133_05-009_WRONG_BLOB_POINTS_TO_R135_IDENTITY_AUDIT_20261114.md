# R133 05-009 provenance correction, 2026-11-14

Starting main: e05b386dbfdab84ba411a555729ebfa6135614f8.

The existing `research/coordination/closure/R133_05-009_ITEMWISE_BOUNDED_DISPOSITION_2026-11-13.md` cites Git blob `72e60d3e0fa8f131c6a4864d0d6cc89afbe350fc` as the R133 final acceptance identity. Direct retrieval of that Git blob returns JSON with `research_id=R135`, `catalogue_id=05-011`, `candidate=Indirect Reciprocity`, DOI `10.1016/j.jtbi.2004.06.005`, 4096 norms and 61440 invasion checks. The cited object belongs to a different model.

Direct retrieval of blob `70d36423e87eca9a14f7b6f9f18177e66c9116d5` returns `research_id=R133`, `catalogue_id=05-009`, `candidate=Evolutionarily Stable Strategy`, DOI `10.1038/246015a0`, and the original bounded R133 scientific status. This latter blob was previously observed for `research/R133/R133_FINAL_ACCEPTANCE_STATUS.json` on main and commit `5943286dbf41f41f405d13bdaa98e1e7ddaec9d8`.

Reproduce via GitHub's Git blob endpoint:
```
https://api.github.com/repos/edwardsage419/Psychohistory-Research/git/blobs/72e60d3e0fa8f131c6a4864d0d6cc89afbe350fc
https://api.github.com/repos/edwardsage419/Psychohistory-Research/git/blobs/70d36423e87eca9a14f7b6f9f18177e66c9116d5
```
Decode the REST JSON `content` base64 field when using a raw HTTP client. The connected GitHub reader returned decoded blob text.

**Finding:** confirmed historical audit citation misattribution, with potential false source identity if used for catalogue closure. No evidence that R133 scientific outputs changed or historical CI was compromised. Preserve R133 research-level bounded E1 and 05-009 catalogue ACTIVE/provisional status. New scientific closures 0; E2/E3 upgrades 0.

R mainline handoff: recheck target main HEAD and file blob, correct the old audit citation, and require exact path/blob plus `research_id`, `catalogue_id`, DOI agreement in future acceptance checks. Fail closed on mismatch. No R core code, frozen protocol, CI, crosswalk or scientific status changed. No new fees.

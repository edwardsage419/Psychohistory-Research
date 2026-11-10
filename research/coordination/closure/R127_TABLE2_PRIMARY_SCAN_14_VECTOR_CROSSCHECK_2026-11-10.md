# R127 Table 2 primary scan cross-check, 2026-11-10

Track: closure. Scope: original catalogue 05-003, R127, published treatment A Table 2 first and tenth period marginal counts. Starting main: `c2a419c33bc968b7d8109a6ed2f7212cd9f89834`.
Frozen source: `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md`, blob `4734ede5133701d622acfda76c4f9474bf660b21`.
Prior bounded derivation: `research/coordination/closure/R127_TABLE2_MARGINAL_TRANSITION_IDENTIFICATION_BOUNDS_2026-11-10.md`, blob `5a760d3055ba4ed40f37069b18e144498e0a371d`.

## First-hand source inspected

Van Huyck, Battalio & Beil (1990), *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, *American Economic Review* 80(1), Table 2, printed pp. 240–241. University-hosted reproduction: https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf . Visually inspected PDF pages 7 and 8 (zero-based PDF pages 6 and 7), including each of the seven effort-category rows at periods 1 and 10 for all seven experiments. Only these 14 vectors were checked in this audit; the intermediate periods and other tables were not re-transcribed.

## Direct visual transcription cross-check

Order of effort levels is [7,6,5,4,3,2,1]. Every vector below was independently read from the original page image and compared entry by entry to the frozen protocol.

| Experiment | n | Original Table 2 period 1 | Original Table 2 period 10 | Match frozen protocol |
| --- | ---: | --- | --- | --- |
| 1 | 16 | [8,3,2,1,1,1,0] | [1,0,0,0,1,1,13] | yes |
| 2 | 16 | [4,1,3,4,1,3,0] | [1,0,1,0,0,1,13] | yes |
| 3 | 14 | [4,2,5,3,0,0,0] | [2,0,0,1,0,2,9] | yes |
| 4 | 15 | [6,0,8,1,0,0,0] | [0,0,0,0,0,2,13] | yes |
| 5 | 16 | [2,1,9,3,1,0,0] | [0,0,0,1,1,3,11] | yes |
| 6 | 16 | [5,2,5,2,1,0,1] | [3,0,0,0,0,5,8] | yes |
| 7 | 14 | [4,1,2,4,1,1,1] | [1,0,0,0,0,3,10] | yes |

All fourteen seven-entry vectors agree with the archived frozen transcription (98 of 98 integer cells). Each period sums to its experiment n, and sum of n across experiments is 107. The first-period effort-1 count is 2 and last-period effort-1 count is 77. Independent standard-library arithmetic over the fourteen vectors reproduces the previously archived sharp bounds for changed effort [89,107] and new effort-1 entrants [75,77], conditional on fixed within-experiment membership. Experiment 4 has disjoint period-1 and period-10 supports, implying exactly 15 changed efforts.

## Acceptance boundary

Result: COMPLETE for this narrow **original Table 2 period 1/10 transcription check**. It removes the specific source-transcription caveat in the previous marginal-bound note. The mathematical bounds remain E1 partial identification on published real-human aggregates. They are not linked individual transitions, E2 out-of-sample prediction, or E3 cross-environment evidence. No machine receipt identity, original source-code execution, full original-paper reproduction, licence for republishing source pages, or catalogue itemwise closure has been newly verified. R127 remains CLOSED_BOUNDED and catalogue 05-003 remains provisional pending separate itemwise evidence acceptance. No frozen protocol or other track file changed.

Execution: local standard-library arithmetic on independently transcribed numbers; no new Actions or CI triggered. Cost: no additional paid service invoked. Next: compare R127 final machine receipt against its exact source/test/report blobs and required frozen acceptance criteria, then decide whether the catalogue item can be CLOSED_BOUNDED under the itemwise standard.

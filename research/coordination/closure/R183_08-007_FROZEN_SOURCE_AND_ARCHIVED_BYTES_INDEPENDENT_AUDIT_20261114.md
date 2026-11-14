# R183 / original 239 item 08-007: frozen source and archived byte identity audit

Date: 2026-11-14 UTC. Scope: read-only scientific closure evidence. Starting main: `da2912dd6519ffb7f8bb8dd21d3578e18c0332ec`.

## Independently executed checks

Read the exact files from the starting main commit via the GitHub repository connector. Recomputed SHA256 from UTF-8 file content using an independent JavaScript implementation of SHA256, with the known `abc` test vector `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` passing. The connector supplied the text content; this audit does not establish byte identity of any independently downloaded CI artifact or historical ZIP.

| File | Computed SHA256 | Frozen or acceptance expected SHA256 | Result |
| --- | --- | --- | --- |
| `research/R177/R177_EXACT_RESULTS.json` | `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535` | same | MATCH |
| `research/R183/R183_EXACT_RESULTS.json` | `40927bae4616a9d9fc91ed964257a9d436372d9196abd8fabceb40740189a000` | same | MATCH |
| `research/R183/R183_ALL_4125_TRAINING_COUNT_PAIRS.csv` | `1dcd2a85c2b241346e8fae8fe85727e2b8c0560fa2916c1e8ce01eb384acf285` | same | MATCH |

Git blob for frozen R177 generator `research/R177/r177_four_finite_count_families_exact.py`: `2d032513ce84141214b6b3f84df9c0ed9976a02b`, matching the R183 prescore protocol. Git blob for R183 native Python: `d3aba985f8f7c7de21ca12f318f73abaa7fb3b0d`. Frozen protocol blob: `e01003e1899739b42b2ed746f1837b8591e870b6`.

CSV structure independently inspected: 4125 data rows, 45 distinct (n, true p0, true p1, mechanism) worlds; 15 worlds each with 25, 81 and 169 count pairs. No duplicate six-field (n, p0, p1, mechanism, k0, k1) keys and no out-of-range k0/k1 values. This is a structure and archived identity check, not a new probability or native execution check.

## Scientific disposition

The R183 frozen input identity and the three current main archived textual file SHA256 claims match. Prior independent E1 rational and numerical audits cover 45 worlds, 4125 pairs, and logloss; this audit avoids repeating those computations. Research status remains `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC`; original catalogue item 08-007 remains `PROVISIONAL_PRIMARY_README_LINK` pending itemwise disposition. No E2/E3 evidence, no real-human test, no formal catalogue closure.

Still required: native Python execution of frozen R183 at an independently identified checkout; verification of its 60-digit Decimal.ln path and generated outputs against archived bytes; separate historical CI artifact and ZIP byte equivalence if required by acceptance standard; original paper coverage and directory-level acceptance decision. Historical CI success alone does not establish artifact byte identity.

No core code, protocol, PR, or CI changed. No paid resource invoked.

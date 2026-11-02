# Theory coordination: TH212 1912 Bombay annual species and sampling denominator

track: theory
subflow: coordination
run_date_utc: 2026-11-02T14:34:00Z
target_key: (theory,BombayPlagueCommission1908+1912,1908-published-scan+1912-published-scan,rat-species-sampling-denominator-and-temperature-chamber-table-identity)
observed_main_before_write: f8efb53c8fec78727f23519b68756ab1d8b172c7
source_scope: 1908 Journal of Hygiene p283 Table III actual NIH PMC scan; 1912 Journal of Hygiene pp221-226 actual NIH PMC scans; 1908 p284 Table IV PDF text
status: COMPLETE_BOUNDED_PRIMARY_IMAGE; PARTIAL_CAUSAL_IDENTIFICATION; NOT_RUN_REAL_DATA_REESTIMATION
work_performed: Table III verified 5/29 vs13/46 Bombay rats, 8/25 vs18/27 ship rats, 4/8 vs15/15 guinea pigs; cool room also dry. 1912 five annual tables transcribed, sampling suspension/correction p221 noted. 1909 to 1910 M.rattus infected counts +28.94% while all examined +30.50%, crude per-all-examined proxy slightly down; species-specific infection prevalence unidentified. Human deaths down29.69%.
tests: Python Fraction 13 assertions PASS, 0 FAIL; arithmetic only, no real historical causal verification
output_paths: theory/TH212_BOMBAY_1912_RAT_SPECIES_DENOMINATOR_TABLEIII_IMAGE_AUDIT_2026-11-02.md; theory/INDEX.md; research/coordination/theory/20261102T143400Z-th212-bombay-1912-denominator-handoff.md
C_D: C010 COMPLETE 2026-11-02; D003 COMPLETE 2026-W45 on 2026-11-02; read only
frozen: R073/PESEN v0.1 unchanged; R272 P0 OPEN; R E1/E2/E3 and MARKET unchanged; open Codex PRs unmerged
ci_status: NOT_RUN; no dispatch
billing_checked: NO_PAID_ACTION; ACCOUNT_BILLING_NOT_VERIFIED
next_action: change discipline; if returning to Bombay, require species-specific examined denominators and sampling correction before prevalence/causal claims
claim_window: optional two-hour advisory only, not an atomic lock

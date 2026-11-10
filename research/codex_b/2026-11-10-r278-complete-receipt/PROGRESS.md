# Plan: research/codex_b/2026-11-10-r278-complete-receipt/PLAN.md

Read latestmain e5f2baa7,18openPRs, recent R/B/operations handoffs, R278S74 freeze,
original JS, B receipt checker, persisted960-row CSV/JSON and reports. A focuses
queue integration and S53/R170 authentication; prior B work R073–R077 disjoint.
No overlapping committed/PR task observed; uncommitted chat activity unobservable.
Five actual old CLI mutations all PASS: conditional list deletion,cov999,delta999,
R073MODIFIED,E2False. Old checked risk/source fields remain protected.
Ruling: reuse archived B math/source checker and add only missing complete receipt
math/schema; keep all historical programs/results. User autonomy/continue permits
inline TDD implementation then one fresh-context reviewer without design pauses.

Task1 RED12 methods:9assertion failures/3errors. Initial implementation GREEN12.
Both native replay modes reproduced7false JSON accepts and rejected8cases with
new140-leaf gate; CSV68025/JSON4851 emitted bytes equal archives exactly.
Additional actual CSV schema probes showed old B and initial supplement both
accepted a duplicated source_probability column (first value999 hidden by valid
last column) and a surplus data cell. New regression CSV-shape RED13methods has
1failure, then strict13-field header/row-width precheck gives GREEN13/13.
This is input-wire validation, not a reimplementation of the existing B math.

Final normal/-O replays each13positive test methods,9old false accepts and1correct
old rejection, new10/10rejections. Five positive original/new CLI invocations per
mode (Node emit, B archive/emitted, new archive/emitted) all succeed. All8code/
source/protocol fingerprints unchanged before/after and match current bytes.
Original B emits ResourceWarning for its pre-existing unclosed CSV reader in
unittest context; warnings are captured, not hidden, and historical code is kept.

# R170 authenticated composition plan

User-authorized continuation; independent branch from main. Reuse PR8 runner and two adapters, and PR9 identity CLI, pinned by exact bytes. Authenticate four historical source/receipt files and the frozen protocol before staging. Execute PR8 against a temporary snapshot, then require PR9 on that newly generated B receipt before success. No existing PR edits, no mathematical reimplementation, no historical witness substitution.

- Read current main, all open PR heads, both source implementations and freeze.
- Write tests; observe absent composition fail.
- Implement authenticated staging and mandatory sequential original gates, stdout-only final result.
- Verify normal/optimized modes, input/code changes, child failure, wrong summary types, mismatched execution and identity receipts, original input stability.
- Record hashes, review, and deliver draft PR; no merge/CI.

Dependencies supplied explicitly: --pr8-dir containing run_audit.py/export_js_states.js/export_python_states.py from 1d8294ee81c7e23cb16bb8882ebc619089a35c65, and --identity-gate from 89a64ecd2975a7fa0409f000cef45b1b2792a8b4. No automatic download. No persistent success file; stdout is caller-managed. PARTIAL limits and unresolved lexical key ordering remain. Temporary snapshots authenticate individual bytes read, not historical time, author signatures or atomic filesystem capture.

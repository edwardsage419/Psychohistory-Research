# R333–R340 composite acceptance: isolated receipt-shape counterexample (2026-11-10)

track: R closure independent audit
subflow: P0 candidate acceptance gate review
run_date: 2026-11-10
observed_head: 89ddc17dd85432858dc185687237218188c69c1a
source_links:
  - research/evidence_audit/r333_r340_composite_acceptance_20261101.py (Git blob 104beae6d60e4df8e879841567ca08c4088438a4)
evidence_scope: Static source inspection plus independently reconstructed validator-only executable counterexample; no production subprocess run.
status: PARTIAL
ci_status: NOT_RUN
billing_checked: No paid service or new CI triggered; actual billing unverified.

## Finding

The current `validate_math` accepts any 40-character string for each `gate_blob`, without checking hexadecimal syntax or matching the blob against an independently expected value. It also accepts the reported `subprocess_checks=16` based on shape and equality only. A separately implemented copy of the exact validation predicates accepted a fabricated eight-model receipt whose `gate_blob` values were `"z" * 40`.

Executable isolated counterexample (Python standard library):

```python
MODELS = [f"R{x}" for x in range(333, 341)]
def require(condition, message):
    if not condition:
        raise ValueError(message)
def validate_math(value):
    require(value.get("status") == "PASS_ALL_EIGHT_BOUNDED_E1_RECEIPTS", "math status")
    require(value.get("evidence") == "E1_ARTIFICIAL_ONLY", "math evidence")
    require(type(value.get("subprocess_checks")) is int and value["subprocess_checks"] == 16, "math subprocess count")
    models = value.get("models")
    require(isinstance(models, list) and len(models) == 8, "math universe length")
    require([m.get("model") for m in models if isinstance(m, dict)] == MODELS, "math universe identity/order")
    require(all(m.get("result") == "PASS_BOUNDED_E1_RECEIPT"
                and isinstance(m.get("gate_blob"), str) and len(m["gate_blob"]) == 40
                for m in models), "math model results")
fake = {"status": "PASS_ALL_EIGHT_BOUNDED_E1_RECEIPTS",
        "evidence": "E1_ARTIFICIAL_ONLY", "subprocess_checks": 16,
        "models": [{"model": m, "result": "PASS_BOUNDED_E1_RECEIPT", "gate_blob": "z" * 40}
                   for m in MODELS]}
validate_math(fake)
print("SYNTHETIC_FORGED_MATH_RECEIPT_ACCEPTED_BY_VALIDATE_MATH = YES")
```

Observed output: `SYNTHETIC_FORGED_MATH_RECEIPT_ACCEPTED_BY_VALIDATE_MATH = YES`.

## Boundaries and scientific interpretation

This proves a validator-only format weakness. It **does not demonstrate a production acceptance bypass**: the composite runner pins the upstream source blobs, executes those pinned programs in normal and optimized Python modes, and compares their outputs. The upstream programs may enforce stronger invariants. No actual model result was forged in the repository, and no E1/E2/E3 evidence grade is changed. No claim is made that historical CI accepted a false result.

Recommended follow-up: inspect the pinned upstream mathematical gate's `gate_blob` generation and expected identity bindings. If its outputs are not already protected by independently checked identities, add a narrowly scoped negative test and exact identity/hex checks at the appropriate owner-controlled gate. Keep the eight workflow production-adoption issue separately open. Avoid cross-track code modifications without R owner coordination.

output_paths: this file only
blockers: full native end-to-end execution unavailable in current local environment (GitHub hostname resolution failure); pinned upstream program not yet independently executed in this run.
next_action: audit pinned upstream gate's identity verification and run real negative tests before any severity escalation.

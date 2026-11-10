# A2 — reversible R077 integration preflight

Base main: 3221a84fba91731071b8931447837e07578210be.
Spec: Codex A engineering v2.0 A2, B18 HANDOFF.md and existing exact_pair.py
limitations. Do not edit B mathematics, original scoring, historical results or
frozen protocols. Do not reconstruct exact model probabilities in Codex A.

The existing B18 replay correctly reports supplement PASS while retaining an
original regression failure, but returns exit 0 for that bounded replay. A
production caller must not mistake that successful diagnostic for readiness.

Create a small stdout-only preflight that reuses B18's exact DIAGNOSTICS code
unchanged. Authenticate the 40 source identities in B18's fixed Git receipt,
confirm current checkout bytes/tracked blobs, and export one temporary snapshot.
Run only the existing 35-case diagnostic, not the already-validated 59-method
baseline suite. Validate complete case identities and classification metadata.
Known original failures produce status BLOCKED_ORIGINAL_R077_UNREPAIRED, exit 2;
malformed evidence/source/runtime errors exit 1. No condition automatically
promotes these artificial diagnostics to human-production approval.

Tests first: reject forged success, duplicate identities, bool counts, missing
fields, false flags, and human-source promotion; accept the exact artificial
diagnostic as a completed preflight with production veto. Run real normal/-O
entrypoints and review source preservation. Deliver a separate draft PR after
read-only review. Next integration requires B-owned exact probability export,
source qualification and corresponding scientific/protocol authorization.

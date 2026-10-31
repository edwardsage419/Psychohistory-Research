#!/usr/bin/env python3
"""Synthetic audit of ActivityWatch pinned sync.rs destination ID lookup.

No network, real user data, or ActivityWatch native execution. The program
models only the documented raw-ID -> sanitized-ID -> legacy-scan priority.
"""
import re


def sanitize_hostname(value):
    s = re.sub(r"[^a-z0-9_-]+", "_", value.strip().lower()).strip("_")
    return s or "unknown"


def raw_destination(base, origin):
    return f"{base}-synced-from-{origin}"


def lookup(source, destinations):
    """Return destination and branch. Mirrors the two early lookup branches."""
    base, origin = source["base"], source["origin"]
    raw = raw_destination(base, origin)
    if raw in destinations:
        return raw, "raw"
    sanitized = raw_destination(base, sanitize_hostname(origin))
    if sanitize_hostname(source["hostname"]) == "unknown" or sanitized.endswith("-synced-from-unknown"):
        return None, "unknown_rejected"
    if sanitized != raw and sanitized in destinations:
        return sanitized, "sanitized"
    return None, "legacy_or_create"


def run():
    checks = 0
    def check(value):
        nonlocal checks
        assert value
        checks += 1

    base = "aw-watcher-window"
    a = {"base": base, "origin": "Office Laptop", "hostname": "Office Laptop", "device_id": "device_A"}
    b = {"base": base, "origin": "office_laptop", "hostname": "office_laptop", "device_id": "device_B"}
    dest = {raw_destination(base, "office_laptop"): {"device_id": "device_A", "origin": "Office Laptop"}}
    check(sanitize_hostname(a["origin"]) == sanitize_hostname(b["origin"]))
    check(a["device_id"] != b["device_id"])
    target, branch = lookup(b, dest)
    check(branch == "raw")
    check(target in dest)
    check(dest[target]["device_id"] != b["device_id"])
    # A's import would hit the same destination via the sanitized fallback.
    target_a, branch_a = lookup(a, dest)
    check(branch_a == "sanitized")
    check(target_a == target)
    # The proposed provenance-aware guard rejects both direct-lookup collisions.
    check(dest[target]["device_id"] == a["device_id"])
    check(dest[target]["device_id"] != b["device_id"])
    # Different base bucket names do not collide.
    different, branch_other = lookup({**b, "base": "aw-watcher-afk"}, dest)
    check(different is None)
    check(branch_other == "legacy_or_create")
    # Missing provenance in a legacy destination cannot establish device identity.
    legacy = {target: {"origin": "Office Laptop"}}
    check("device_id" not in legacy[target])
    check(lookup(b, legacy)[0] == target)
    # Unknown hostname is rejected when there is no exact raw destination.
    unknown = {**b, "origin": "???", "hostname": "???"}
    check(lookup(unknown, {})[1] == "unknown_rejected")
    # The pinned code's raw branch runs before the unknown guard: scope caveat.
    preexisting_unknown = {raw_destination(base, "???"): {"device_id": "device_A"}}
    check(lookup(unknown, preexisting_unknown)[1] == "raw")
    print(f"MKT164 synthetic checks={checks} PASS; cross-device raw/sanitized alias demonstrated")


if __name__ == "__main__":
    run()

"""Validate the v0.2 scientific guards in the actual interpreter mode."""
import json
import sys

from psychohistory.degroot import DeGroot
from psychohistory.prediction import protocol_spec, run_comparison, synthetic_rows, validate_split


def reject(callback):
    try:
        callback()
    except ValueError as error:
        return str(error)
    raise RuntimeError("Scientific guard unexpectedly accepted invalid input")


spec = protocol_spec(7)
changed = synthetic_rows(spec)
changed[-1]["available_at"] = spec["split"]["cutoff"] + 1
result = run_comparison(spec)
if result != run_comparison(spec):
    raise RuntimeError("Identical registered comparison changed")
math = DeGroot().verify_reference()
print(json.dumps({
    "optimization": sys.flags.optimize,
    "future_information_rejected": reject(lambda: validate_split(changed, spec)),
    "scope_change_rejected": reject(lambda: run_comparison({**spec, "scope": "EMPIRICAL"})),
    "metrics": result["metrics"],
    "mathematics": math,
}, sort_keys=True))

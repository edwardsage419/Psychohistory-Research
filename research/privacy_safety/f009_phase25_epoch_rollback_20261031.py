"""F009 phase25 synthetic deletion epoch and restore policy; no real user data."""
import itertools
import json

checks = 0

def require(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)

def loose(m, t, a, b, backup):
    return m == t == a == b == backup

def strict(m, t, a, b, backup, trusted):
    return loose(m, t, a, b, backup) and m >= trusted

accepted_loose = []
accepted_strict = []
for state in itertools.product((2, 3), repeat=5):
    m, t, a, b, backup = state
    x = loose(*state)
    y = strict(*state, trusted=3)
    require(not y or x, 'strict subset')
    require(not y or min(state) >= 3, 'no stale scope')
    if x:
        accepted_loose.append(state)
    if y:
        accepted_strict.append(state)
require(len(accepted_loose) == 2, 'loose count')
require(len(accepted_strict) == 1, 'strict count')
require((2, 2, 2, 2, 2) in accepted_loose, 'fully rolled back bundle')
require((2, 2, 2, 2, 2) not in accepted_strict, 'rollback rejected')
require((3, 3, 3, 3, 3) in accepted_strict, 'current bundle')
require(not strict(3, 3, 3, 3, 2, 3), 'old backup blocked')
require(not strict(3, 3, 2, 3, 3, 3), 'old device acknowledgement blocked')
print(json.dumps({'states': 32, 'assertions': checks,
                  'loose_accept': len(accepted_loose),
                  'anchored_accept': len(accepted_strict),
                  'scope': 'synthetic E1; no real signatures, deletion or devices'}))

#!/usr/bin/env python3
"""Synthetic fail-closed permission policy. NOT an Automerge or Keyhive runtime test."""
from dataclasses import dataclass
from itertools import product

ACCESS = {'none': 0, 'relay': 1, 'read': 2, 'edit': 3, 'admin': 4}

@dataclass(frozen=True)
class Request:
    protected: bool
    server_policy_enabled: bool
    adapter_wrapped: bool
    online: bool
    version_current: bool
    access: str
    operation: str


def allow(req: Request) -> bool:
    if not req.protected or not req.server_policy_enabled or not req.adapter_wrapped:
        return False
    if not req.online or not req.version_current:
        return False
    required = {'fetch': 1, 'read': 2, 'push': 3, 'grant': 4}[req.operation]
    return ACCESS[req.access] >= required


if __name__ == '__main__':
    total = 0
    permitted = 0
    for bits in product((False, True), repeat=5):
        for level, op in product(ACCESS, ('fetch', 'read', 'push', 'grant')):
            req = Request(*bits, level, op)
            actual = allow(req)
            total += 1
            permitted += int(actual)
            assert actual == (all(bits) and ACCESS[level] >= {'fetch': 1, 'read': 2, 'push': 3, 'grant': 4}[op])
            if not all(bits):
                assert not actual
    assert total == 640
    assert permitted == 10
    print(f'PASS: {total} synthetic policy states; allowed={permitted}, denied={total-permitted}')
    print('WARNING: no Keyhive installation, encryption, offline device or real authorization exercised')
